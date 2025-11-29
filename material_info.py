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
        material_map[mesh.name] = get_material_textures(mesh)
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
