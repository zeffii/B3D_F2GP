import bpy
import bmesh

triangulate = bmesh.ops.triangulate


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
    print('cooolio2223333')
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
