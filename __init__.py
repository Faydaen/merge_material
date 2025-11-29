bl_info = {
    "name": "Merge material",
    "blender": (4, 0, 0),
    "category": "Object",
}

import bpy
import json


# --- Операторы ---
class OT_MaterialInfo(bpy.types.Operator):
    bl_idname = "object.first_button"
    bl_label = "Material info"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # Создаем или получаем текстовый блок
        text_name = "Material Info JSON"
        if text_name not in bpy.data.texts:
            text_block = bpy.data.texts.new(text_name)
        else:
            text_block = bpy.data.texts[text_name]
        
        # Записываем JSON в текстовый блок
        json_data = {"hello": "world"}
        text_block.clear()
        text_block.write(json.dumps(json_data, indent=2))
        
        # Переключаемся на текстовый редактор с этим блоком
        for area in context.screen.areas:
            if area.type == 'TEXT_EDITOR':
                area.spaces[0].text = text_block
                break
        
        self.report({'INFO'}, "JSON выведен в текстовую панель")
        return {'FINISHED'}


class OT_MergeMaterial(bpy.types.Operator):
    bl_idname = "object.second_button"
    bl_label = "Merge material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "Нажата вторая кнопка")
        print("Вторая кнопка нажата")
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


# --- Текстовая панель ---
class TEXT_PT_material_info(bpy.types.Panel):
    bl_label = "Material Info"
    bl_idname = "TEXT_PT_material_info"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Material Info"

    def draw(self, context):
        layout = self.layout
        text_name = "Material Info JSON"
        
        if text_name in bpy.data.texts:
            text_block = bpy.data.texts[text_name]
            layout.label(text=f"Текстовый блок: {text_name}")
            layout.label(text=f"Строк: {len(text_block.lines)}")
        else:
            layout.label(text="Нажмите 'Material info' для создания JSON")
        




# --- Регистрация ---
def register():
    bpy.utils.register_class(OT_MaterialInfo)
    bpy.utils.register_class(OT_MergeMaterial)
    bpy.utils.register_class(VIEW3D_PT_merge_material)
    bpy.utils.register_class(TEXT_PT_material_info)
    print("register")


def unregister():
    if hasattr(bpy.types.Scene, "merge_material_text"):
        del bpy.types.Scene.merge_material_text

    bpy.utils.unregister_class(TEXT_PT_material_info)
    bpy.utils.unregister_class(VIEW3D_PT_merge_material)
    bpy.utils.unregister_class(OT_MergeMaterial)
    bpy.utils.unregister_class(OT_MaterialInfo)


if __name__ == "__main__":
    register()