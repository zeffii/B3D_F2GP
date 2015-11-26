import bpy
import bmesh
from bpy.props import StringProperty

triangulate = bmesh.ops.triangulate


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


def get_mesh(obj):
    mesh_settings = (bpy.context.scene, False, 'PREVIEW')
    data = obj.to_mesh(*mesh_settings)
    bm = bmesh.new()
    bm.from_mesh(data)
    triangulate(bm, faces=[bm.faces], quad_method=1, ngon_method=1)
    return bm


def get_layer(GP, gdata_owner, layer_name):

    if gdata_owner not in GP:
        gp = GP.new(gdata_owner)
    else:
        gp = GP[gdata_owner]

    # create new or pick up named GP layer
    if not (layer_name in gp.layers):
        layer = gp.layers.new(layer_name)
        layer.frames.new(1)
        layer.line_width = 1
    else:
        layer = gp.layers[layer_name]
        layer.frames[0].clear()

    return layer


def generate_gp3d_stroke(mesh, layer):
    layer.show_points = True
    layer.color = (0.2, 0.90, .2)

    verts = mesh.verts
    for f in mesh.faces:
        s = layer.frames[0].strokes.new()
        s.draw_mode = '3DSPACE'  # or '2DSPACE'
        s.points.add(len(f.vertices))
        for i, v in enumerate(f.vertices):
            p = s.points[i]
            p.co = verts[v].co
            p.pressure = 1.0


class F2GPDispatcher(bpy.types.Operator):

    bl_label = "Short Name"
    bl_idname = "wm.f2gp_callback"

    fn_name = StringProperty(default='')
    data_name = StringProperty(default='stack_data')
    layer_name = StringProperty(default='stack_layer')

    def try_f2gp(self, context):
        obj = context.active_object

        if not(obj and obj.type == 'FONT'):
            return

        GP = bpy.data.grease_pencil
        layer = get_layer(self.data_name, self.layer_name)
        bm = get_mesh(obj)
        generate_gp3d_stroke(GP, bm, layer)
        bm.clear()

        bpy.context.scene.grease_pencil = GP[self.data_name]

    def execute(self, context):
        if self.fn_name == 'set_gp_from_font':
            self.try_f2gp(context)
        return {'FINISHED'}


class F2GPCommandPanel(bpy.types.Panel):

    bl_label = "Convert Font To GP"
    bl_idname = "OBJECT_PT_f2gp"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOL_PROPS'

    def draw(self, context):
        scn = context.scene
        layout = self.layout

        row = layout.row()
        row.prop(scn, 'f2gp_data_name')
        row.prop(scn, 'f2gp_layer_name')

        row = layout.row()
        maker = row.operator("wm.f2gp_callback", text='make gp')
        maker.data_name = scn.f2gp_data_name
        maker.layer_name = scn.f2gp_layer_name


def register():
    scn = bpy.types.Scene
    scn.f2gp_data_name = StringProperty(default='stack_data')
    scn.f2gp_layer_name = StringProperty(default='stack_layer')
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
    scn = bpy.types.Scene
    del scn.f2gp_data_name
    del scn.f2gp_layer_name
