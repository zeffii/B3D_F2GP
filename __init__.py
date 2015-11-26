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
    triangulate(bm, faces=bm.faces[:], quad_method=0, ngon_method=0)
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


def generate_gp3d_stroke(bm, layer):
    layer.show_points = True
    layer.color = (0.2, 0.90, .2)

    verts = bm.verts
    verts.ensure_lookup_table()

    for f in bm.faces:
        s = layer.frames[0].strokes.new()
        s.draw_mode = '3DSPACE'  # or '2DSPACE'
        s.points.add(len(f.verts))
        for i, v in enumerate(f.verts):
            p = s.points[i]
            p.co = verts[v.index].co
            p.pressure = 1.0


class FGPDispatcher(bpy.types.Operator):

    bl_label = "Short Name"
    bl_idname = "wm.fgp_callback"

    fn_name = StringProperty(default='')
    data_name = StringProperty(default='stack_data')
    layer_name = StringProperty(default='stack_layer')

    def do_fgp(self, context):
        obj = context.active_object
        print('gets here')
        if not (obj and obj.type == 'FONT'):
            return

        print('should be here')
        GP = bpy.data.grease_pencil
        layer = get_layer(GP, self.data_name, self.layer_name)
        bm = get_mesh(obj)
        generate_gp3d_stroke(bm, layer)
        bm.clear()

        context.scene.grease_pencil = GP[self.data_name]

    def execute(self, context):
        print('wtf!', '||', self.fn_name, '||')
        if self.fn_name == 'set_gp_from_font':
            print('leaves execute')
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
