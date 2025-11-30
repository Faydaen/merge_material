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
        print(f"\nОбъект: {object_name}")
        for material_info in materials_list:
            new_name = material_info["target"]
            list_materials = material_info["list"]
            print(f"новое имя {new_name}")
            print(list_materials)

        # print(materials_info["list"])
        # new_name = material_data[obj_name][0]["target"]
        # materials_names = material_data[obj_name][0]["list"]









# def merge_duplicate_materials(obj_name: str, material_names: list, new_material_name: str):
#     # Получаем объект
#     obj = bpy.data.objects.get(obj_name)
#     if obj is None:
#         print(f"Object '{obj_name}' not found.")
#         return
#
#     # Фильтруем существующие материалы
#     existing_mats = [bpy.data.materials.get(name) for name in material_names]
#     existing_mats = [m for m in existing_mats if m is not None]
#
#     if not existing_mats:
#         print("No valid materials found.")
#         return
#
#     # Берём первый материал как основной
#     main_mat = existing_mats[0]
#     main_mat.name = new_material_name
#
#     # Карта старых материалов → новый
#     mat_map = {m.name: main_mat for m in existing_mats}
#
#     # Перебираем слоты материалов объекта
#     for slot in obj.material_slots:
#         if slot.material and slot.material.name in mat_map:
#             slot.material = main_mat
#
#     # Теперь удаляем старые материалы (кроме основного)
#     for mat in existing_mats[1:]:
#         # Удаление только если материал больше нигде не используется
#         try:
#             bpy.data.materials.remove(mat)
#         except RuntimeError:
#             # Если материал используется — просто пропускаем
#             print(f"Cannot remove material '{mat.name}', it is still used somewhere.")
#
#     print(f"Merged materials {material_names} into '{new_material_name}'.")


# def edit_mesh(object_name):
#     """перейти в режим редаткирования объетка, сбросив выдление со всех вертекстов"""
#     bpy.context.view_layer.objects.active = bpy.data.objects[object_name]
#     bpy.ops.object.mode_set(mode='EDIT')
#     bpy.ops.mesh.select_all(action='DESELECT')