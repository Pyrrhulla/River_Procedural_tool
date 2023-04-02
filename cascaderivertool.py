import hou

# This code is called when instances of this SOP cook.
node = hou.pwd()
geo = node.geometry()

# Add code to modify the contents of geo.
Threshold = node.parm("Threshold").eval()
Slow_descent = node.parm("Slow_descent").eval()

for prim in geo.prims():
    points = prim.points()
    count = 0
    startPt = 0
    previous_height = points[startPt].position()[1]
    for point in points: 
        current_height = point.position()[1]
        diff = current_height - previous_height
        if diff > Threshold:
            current_height = previous_height
            point.setPosition((point.position()[0], current_height, point.position()[2]))
        weight = hou.hmath.fit(count, 0, len(points)-1, 0, 1)
        weight *= weight 
        point.setPosition((point.position()[0], point.position()[1] - (Slow_descent*weight), point.position()[2]))
        count+=1
        previous_height = current_height