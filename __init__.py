bl_info = {
    "name": "Merge material",
    "blender": (4, 0, 0),
    "category": "Object",
}

import bpy

class OT_Test(bpy.types.Operator):
    bl_idname = "object.test_operator"
    bl_label = "Test Operator"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "Работает!")
        print("Работает")

        return {'FINISHED'}

def register():
    print("Addon registered 1")
    bpy.utils.register_class(OT_Test)


def unregister():
    bpy.utils.unregister_class(OT_Test)

if __name__ == "__main__":
    register()

