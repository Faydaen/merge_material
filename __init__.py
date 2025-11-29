bl_info = {
    "name": "Merge material",
    "blender": (4, 0, 0),
    "category": "Object",
}

import bpy

# --- Операторы ---
class OT_MaterialInfo(bpy.types.Operator):
    bl_idname = "object.first_button"
    bl_label = "Material info"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "Нажата первая кнопка")
        print("Первая кнопка нажата")
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

        # Большое текстовое поле
        # layout.label(text="Текстовое поле:")
        # layout.prop(context.scene, "merge_material_text", text="")


# --- Регистрация ---
def register():

    bpy.utils.register_class(OT_MaterialInfo)
    bpy.utils.register_class(OT_MergeMaterial)
    bpy.utils.register_class(VIEW3D_PT_merge_material)
    print("register")
    # Добавляем свойство для текстового поля
    bpy.types.Scene.merge_material_text = bpy.props.StringProperty(
        name="Merge Material Text",
        description="Большое текстовое поле",
        default="",
        options={'MULTILINE'}  # делает поле многострочным
    )


def unregister():
    del bpy.types.Scene.merge_material_text

    bpy.utils.unregister_class(VIEW3D_PT_merge_material)
    bpy.utils.unregister_class(OT_MergeMaterial)
    bpy.utils.unregister_class(OT_MaterialInfo)


if __name__ == "__main__":
    register()