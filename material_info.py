import bpy


def get_material_textures(obj):
    """
    Возвращает словарь, где ключи - названия материалов,
    а значения - списки названий файлов текстур (изображений) в этих материалах.

    Args:
        obj (bpy.types.Object): Объект, материалы которого нужно проанализировать.

    Returns:
        dict: Словарь {material_name: [texture_name, ...]}
    """

    material_textures_map = {}

    # Проверяем, есть ли у объекта слоты материалов
    if not obj.data.materials:
        return material_textures_map  # Возвращаем пустой словарь, если материалов нет

    # Итерируемся по слотам материалов объекта
    for slot in obj.material_slots:
        material = slot.material

        # Проверяем, назначен ли материал на слот
        if material:
            material_name = material.name
            texture_list = []

            # Проверяем использование нод и наличие нодового дерева
            if material.use_nodes and material.node_tree:
                tree = material.node_tree

                # Итерируемся по всем нодам
                for node in tree.nodes:

                    # Ищем ноды типа 'TEX_IMAGE' (Изображение Текстуры)
                    if node.type == 'TEX_IMAGE':

                        # Проверяем, назначено ли изображение на ноду
                        if node.image:
                            # Добавляем название файла текстуры в список
                            texture_list.append(node.image.name)

            # Добавляем запись в итоговый словарь.
            # Даже если список текстур пуст, материал будет в словаре.
            material_textures_map[material_name] = texture_list

    return material_textures_map


def get_material_info():
    meshes = get_meshes()
    material_map = {}
    for mesh in meshes:


        # получаем список тестур для каждого материала
        material_textures = get_material_textures(mesh)

        # получаем "список списков" одинаковых материалов
        grouped_materials = group_identical_materials(material_textures)

        # пробегаемся по спискам одинаковых материалов
        # и отдельно записывам название первого материла
        # чтобы можно было переименовывать
        material_map[mesh.name] = []
        for grouped_material in grouped_materials:
            material_map[mesh.name].append({
                "list":grouped_material,
                "target": grouped_material[0]
            })


    return material_map


def get_meshes():
    """
    Получить все меши у выделенной арматуры (либо сиблинков меши)
    """

    obj = bpy.context.active_object

    if obj is None:
        print("Ошибка: нет активного объекта")
        return []

    # Если выделена арматура
    if obj.type == 'ARMATURE':
        armature = obj
        meshes = [child for child in armature.children if child.type == 'MESH']
        if meshes:
            return meshes
        else:
            return []
    # Если выделен объект, который является дочерним арматуры
    elif obj.parent and obj.parent.type == 'ARMATURE':
        armature = obj.parent
        meshes = [child for child in armature.children if child.type == 'MESH']
        if meshes:
            return meshes
        else:
            return []
    else:
        print("Ошибка: выделите арматуру или её дочерний объект")
        return []


def group_identical_materials(material_textures):
    """
    Группирует материалы, которые имеют одинаковый набор текстур,
    пустые массивы не считаются одинаковыми

    Args:
        material_textures (dict): Словарь вида 
          {'material_name': ['texture_name_1', 'texture_name_2'], ...}
          (Результат функции get_material_info).

    Returns:
        list: Список списков, где каждый внутренний список содержит названия 
              одинаковых материалов.
              Например: [['mat_a', 'mat_a2', 'mat_a3'], ['mat_b']]
    """

    # Словарь для группировки: ключ - уникальная комбинация текстур (кортеж),
    # значение - список материалов, использующих эту комбинацию.
    texture_to_materials = {}

    for material_name, texture_list in material_textures.items():


        if len(texture_list) == 0:
            continue

        # 1. Сортируем список текстур, чтобы порядок не имел значения.
        # 2. Преобразуем в кортеж, чтобы использовать его как неизменяемый ключ словаря.
        #    Если материал не имеет текстур, ключ будет пустым кортежем ().
        sorted_texture_key = tuple(sorted(texture_list))

        # Добавляем материал в соответствующую группу
        if sorted_texture_key in texture_to_materials:
            texture_to_materials[sorted_texture_key].append(material_name)
        else:
            # Создаем новую группу для этой комбинации текстур
            texture_to_materials[sorted_texture_key] = [material_name]

    # Возвращаем только значения словаря (списки материалов)
    return list(texture_to_materials.values())


# ------------------ сливание материалов -----------------

def merge_materials(material_data):
    for object_name, materials_list in material_data.items():
        # print(f"\nОбъект: {object_name}")

        # if object_name != "Genesis8Female.Shape":
        #     continue


        for material_info in materials_list:
            new_name = material_info["target"]
            list_materials = material_info["list"]

            print(f"\n\n ------------- {object_name}\\{new_name} ----------------")

            merge_duplicate_materials(object_name, list_materials, new_name)


def merge_duplicate_materials(obj_name: str, material_names: list, new_material_name: str):
    # объект
    obj = bpy.data.objects.get(obj_name)
    if obj is None:
        print(f"Object '{obj_name}' not found.")
        return

    # собрать материалы
    mats = [bpy.data.materials.get(name) for name in material_names]
    mats = [m for m in mats if m is not None]

    # основной материал (оставляем его)
    main = mats[0]

    if len(mats) == 1:
        print("Всего один материал")
        main.name = new_material_name
        return


    # Индексы материалов в объекте
    mat_indices = {slot.material: i for i, slot in enumerate(obj.material_slots)}

    print_mat_list(mat_indices)

    # Индекс основного
    main_index = mat_indices.get(main)

    if main_index is None:
        print("Main material not found in object's slots.")
        return

    # Все остальные материалы (которые нужно заменить)
    replace_materials = mats[1:]

    # Индексы заменяемых материалов
    replace_indices = {mat_indices[m] for m in replace_materials if m in mat_indices}

    print(f"{main_index} -> {replace_indices}")


    # Переназначаем **в полигонах**
    if obj.data.materials:
        for poly in obj.data.polygons:
            if poly.material_index in replace_indices:
                poly.material_index = main_index



    print("Материалы на удаление:")
    print_removable(replace_materials, obj)

    # Теперь убираем старые материалы из слотов
    # Удалять будем справа налево, чтобы индексы не сбивались
    for mat in replace_materials:
        try:
            idx = obj.material_slots.find(mat.name)
            if idx != -1:
                obj.active_material_index = idx
                bpy.ops.object.material_slot_remove()
        except:
            print("что-то пошло не так")

    # переименовывам только после того как удалили все другие матеиалы
    # чтобы не было конфликтов
    main.name = new_material_name

    print(f"Merged {material_names} into '{new_material_name}'.")



# --- для отладки ---
def print_mat_list(mat_indices):
    for mat, indices in mat_indices.items():
        print(f"\t- {mat.name}: {indices}")


def print_removable(replace_materials, obj):
    for mat in replace_materials:
        idx = obj.material_slots.find(mat.name)
        print(f"\t- {mat.name}: {idx}")