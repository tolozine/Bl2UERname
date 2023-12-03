# 导入依赖库
import bpy
import os
import subprocess
import tempfile
import re

from bpy.props import (StringProperty,
                   CollectionProperty,
                   IntProperty,
                   )

from bpy.types import (Panel,
                   AddonPreferences,
                   Operator,
                   PropertyGroup,
                   )
                   
# 重命名方法
def rename_suffix(self, context):
    for obj in bpy.context.selected_objects:
        base_name = context.scene.object_custom_name
        if base_name == "":
            name_split = obj.name.split("_")
            if "low" in name_split:
                obj.name = obj.name.replace("_low", "")
            elif "high" in name_split:
                obj.name = obj.name.replace("_high", "")
            base_name = obj.name.split("_" + self.suffix)[0]
        obj.name = base_name + "_" + self.suffix
    return {'FINISHED'}


# 重命名添加后缀
class RenameObjectSuffix(bpy.types.Operator):
    bl_idname = "rename.suffix"
    bl_label = "Rename Objects"

    suffix: StringProperty()

    def execute(self, context):
        rename_suffix(self, context)

        return {'FINISHED'}


class RenameObjectPrefix(bpy.types.Operator):
    bl_idname = "rename.prefix"
    bl_label = "Rename Objects"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        # 获取自定义前缀
        prefix = bpy.context.scene.rename_prefix
        pattern = re.compile(r'\.\d+$')

        for i, obj in enumerate(selected_objects, start=0):
            base_name = obj.name                
            base_name = re.sub(pattern, '', base_name) 
            obj.name =  f"{prefix}_"+ base_name + f"_{i:02d}"

        return {'FINISHED'}


# 面板 - 重命名
class RenamePanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_rename_panel"
    bl_label = "Rename"
    bl_category = "Bl2UERename"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_order = 2

    def draw(self, context):
        layout = self.layout

        # 获取Blender的语言设置
        language = bpy.context.preferences.view.language
        # 根据语言设置按钮和文本框的标签
        if language == "zh_CN":
            batch_rename_text = "批量命名"
        else:
            batch_rename_text = "Batch Rename"


        # 添加自定义属性  
        row = layout.row(align=True)
        row.prop(context.scene, "rename_prefix",text="")#新的自定义属性
        row.operator("rename.prefix", text=batch_rename_text, icon="GPBRUSH_FILL")

            

#注册类
CLASSES = (
    RenameObjectSuffix,
    RenamePanel,
    RenameObjectPrefix
)

# 注册和反注册函数
def register():
    for klass in CLASSES:
        bpy.utils.register_class(klass)  # 注册每个类
    bpy.types.Scene.object_custom_name = StringProperty(name="Custom Name")
    bpy.types.Scene.rename_prefix = bpy.props.StringProperty(name="Prefix", default="NewName")


def unregister():
    for klass in CLASSES:
        bpy.utils.unregister_class(klass)  # 反注册每个类
    del bpy.types.Scene.object_custom_name
    del bpy.types.Scene.rename_prefix


# 如果是主文件，则注册
if __name__ == "__main__":
    register()
