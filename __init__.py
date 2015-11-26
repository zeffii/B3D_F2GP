import bpy
from mathutils import Vector, Matrix

# using: http://blender.stackexchange.com/questions/16107/
# is-there-a-low-level-alternative-for-bpy-ops-object-origin-set

context = bpy.context

def origin_to_base(obj):
    mw = obj.matrix_world
    me = obj.data

    start = Vector()
    for vec in obj.bound_box:
        start+= Vector(vec[:])

    lowest_z = min([v[:][2] for v in obj.bound_box])
    start *= (1/8)
    local_origin = mw * Vector((start.x, start.y, lowest_z))
    
    mat = Matrix.Translation(mw.translation - local_origin)
    
    if me.is_editmode:
        bm = bmesh.from_edit_mesh(me)
        bm.transform(mat)
        bmesh.update_edit_mesh(me, False, False)
    else:
        me.transform(mat)

    me.update()

    obj.matrix_world.translation = local_origin


objs = [mo for mo in context.selected_objects if mo.type == 'MESH']

for o in objs:
    origin_to_base(o)
