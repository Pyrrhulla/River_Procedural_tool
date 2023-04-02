import hou

# This code is called when instances of this SOP cook.
node = hou.pwd()
geo = node.geometry()
Step_Multiplier = node.parm("Step_Multiplier").eval()

# Add code to modify the contents of geo.
# Connect the curve and the height of the heightmap
inputNode = node.inputs()
curve = inputNode[0].geometry()
volume = inputNode[1].geometry()
heightfield = volume.prim(0)

for prim in geo.prims():
    points = prim.points()
    for point in points:
        original_pos = point.position()
        sampled_height = heightfield.sample(original_pos)
        gradient_direction = heightfield.gradient(original_pos)
        gradient_offset = -gradient_direction * Step_Multiplier
        new_pos = [original_pos[0] + gradient_offset[0], sampled_height + gradient_offset[1], original_pos[2] + gradient_offset[2]]
        point.setPosition(new_pos)