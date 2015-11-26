import bpy

def get_layer(gdata_owner, layer_name):

    grease_data = bpy.data.grease_pencil
    if gdata_owner not in grease_data:
        gp = grease_data.new(gdata_owner)
    else:
        gp = grease_data[gdata_owner]

    # get grease pencil layer
    if not (layer_name in gp.layers):
        layer = gp.layers.new(layer_name)
        layer.frames.new(1)
        layer.line_width = 1
    else:
        layer = gp.layers[layer_name]
        layer.frames[0].clear()

    return layer

def generate_gp3d_stroke(obj, layer):
    layer.show_points = True
    layer.color = (0.2, 0.90, .2)

    verts = obj.data.vertices
    for f in obj.data.polygons:

        s = layer.frames[0].strokes.new()
        s.draw_mode = '3DSPACE'  # or '2DSPACE'
        s.points.add(len(f.vertices))
        for i, v in enumerate(f.vertices):
            p = s.points[i]
            p.co = verts[v].co
            p.pressure = 1.0

def main():
    obj = bpy.context.active_object
    data_name, layer_name = 'stack_data', "stack layer"
    layer = get_layer(data_name, layer_name)
    generate_gp3d_stroke(obj, layer)
    bpy.context.scene.grease_pencil = bpy.data.grease_pencil[data_name]

main()
