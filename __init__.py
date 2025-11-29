bl_info = {
    "name": "Merge material",
    "blender": (4, 0, 0),
    "category": "Object",
}

import bpy
import json
import importlib
from . import material_info


# --- Операторы ---
class OT_MaterialInfo(bpy.types.Operator):
    bl_idname = "object.material_info_button"
    bl_label = "Material info"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # Создаем или получаем текстовый блок
        text_name = "material_info"
        if text_name not in bpy.data.texts:
            text_block = bpy.data.texts.new(text_name)
        else:
            text_block = bpy.data.texts[text_name]
        
        # Записываем JSON в текстовый блок
        json_data = material_info.get_material_info()
        text_block.clear()
        text_block.write(json.dumps(json_data, indent=2))
        
        # Переключаемся на текстовый редактор с этим блоком
        for area in context.screen.areas:
            if area.type == 'TEXT_EDITOR':
                area.spaces[0].text = text_block
                break
        
        self.report({'INFO'}, "Информация о материалах выведена в текстовую панель")
        return {'FINISHED'}


class OT_MergeMaterial(bpy.types.Operator):
    bl_idname = "object.merge_material_button"
    bl_label = "Merge material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        text_name = "material_info"

        # Проверяем, что текстовый блок существует
        if text_name not in bpy.data.texts:
            self.report({'ERROR'}, "Текстовый блок material_info не найден")
            return {'CANCELLED'}

        text_block = bpy.data.texts[text_name]

        try:
            # Читаем весь текст и парсим JSON
            json_str = text_block.as_string()
            material_data = json.loads(json_str)

            # Теперь у тебя есть словарь с данными
            print("Прочитан JSON:", material_data)

            # Здесь можно реализовать логику объединения материалов
            # например, пройтись по material_data и что-то сделать
            self.report({'INFO'}, "JSON успешно прочитан из material_info")

        except Exception as e:
            self.report({'ERROR'}, f"Ошибка чтения JSON: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}


# --- Панель ---
class VIEW3D_PT_merge_material(bpy.types.Panel):
    bl_label = "Merge material"
    bl_idname = "VIEW3D_PT_merge_material"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Merge material"   # название вкладки в N-панели

    def draw(self, context):
        layout = self.layout

        # Кнопки
        layout.operator(OT_MaterialInfo.bl_idname)
        layout.operator(OT_MergeMaterial.bl_idname)





# --- Регистрация ---
def register():
    importlib.reload(material_info)
    bpy.utils.register_class(OT_MaterialInfo)
    bpy.utils.register_class(OT_MergeMaterial)
    bpy.utils.register_class(VIEW3D_PT_merge_material)
    print("register")


def unregister():
    if hasattr(bpy.types.Scene, "merge_material_text"):
        del bpy.types.Scene.merge_material_text

    bpy.utils.unregister_class(VIEW3D_PT_merge_material)
    bpy.utils.unregister_class(OT_MergeMaterial)
    bpy.utils.unregister_class(OT_MaterialInfo)


if __name__ == "__main__":
    register()