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


