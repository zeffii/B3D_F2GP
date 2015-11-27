# GPL3 - Use, Diffuse, Amuse.

bl_info = {
    "name": "Font to GP",
    "author": "Dealga McArdle",
    "version": (0, 1),
    "blender": (2, 7, 6),
    "location": "",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"
}

import importlib

import bpy
from bpy.props import StringProperty

if 'resources' in globals():
    importlib.reload(resources)

from .resources import (get_mesh, get_layer, generate_gp3d_stroke)


class FGPDispatcher(bpy.types.Operator):

    bl_label = "Short Name"
    bl_idname = "wm.fgp_callback"

    fn_name = StringProperty(default='')
    data_name = StringProperty(default='stack_data')
    layer_name = StringProperty(default='stack_layer')

    def do_fgp(self, context):
        obj = context.active_object
        if not (obj and obj.type == 'FONT'):
            return

        GP = bpy.data.grease_pencil
        layer = get_layer(GP, self.data_name, self.layer_name)
        bm = get_mesh(obj)
        generate_gp3d_stroke(bm, layer)
        bm.clear()

        context.scene.grease_pencil = GP[self.data_name]

    def execute(self, context):
        if self.fn_name == 'set_gp_from_font':
            self.do_fgp(context)
        return {'FINISHED'}


class FGPCommandPanel(bpy.types.Panel):

    bl_label = "Convert Font To GP"
    bl_idname = "OBJECT_PT_fgp"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOL_PROPS'

    def draw(self, context):
        scn = context.scene
        layout = self.layout

        col = layout.column()
        col.prop(scn, 'fgp_data_name')
        col.prop(scn, 'fgp_layer_name')

        row = layout.row()
        maker = row.operator("wm.fgp_callback", text='make gp')
        maker.fn_name = 'set_gp_from_font'
        maker.data_name = scn.fgp_data_name
        maker.layer_name = scn.fgp_layer_name


def register():
    scn = bpy.types.Scene
    scn.fgp_data_name = StringProperty(default='stack_data')
    scn.fgp_layer_name = StringProperty(default='stack_layer')
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
    scn = bpy.types.Scene
    del scn.fgp_data_name
    del scn.fgp_layer_name
