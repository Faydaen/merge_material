import bpy

def get_material_info_json():
    """
    Возвращает JSON с информацией о материалах.
    """
    json_data = {"Hello": "world 2!"}

    # active_obj = bpy.context.view_layer.objects.active
    # json_data =  get_object_material_textures(active_obj)

    return json_data


def get_object_material_textures(obj):
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
