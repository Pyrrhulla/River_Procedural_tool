import hou
import math
from random import random 
# This code is called when instances of this SOP cook.
node = hou.pwd()
geo = node.geometry()

# Add code to modify the contents of geo.
Threshold = node.parm("Threshold").eval()
Slow_descent = node.parm("Slow_descent").eval()

height_trigger = node.parm("height_trigger").eval()
max_cascade_generate = node.parm("max_cascade_generate").eval()

color_attribute = geo.findPointAttrib("Cd")
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

    regions = []
    tmp_region = {}
    tmp_region['points'] = []
    tmp_region['previous_point'] = tmp_region['next_point'] = None
    tmp_region_firstP = None

    for i in range(1, len(points)):
        current_height = points[i].position()[1]
        previous_height = points[i-1].position()[1]
        height_diff = abs(current_height - previous_height)
        region_height_diff = 0
        if(tmp_region_firstP):
            region_height_diff = abs(current_height - tmp_region_firstP.position()[1])
        if((height_diff>height_trigger) and (region_height_diff <= max_cascade_generate)):
            #points[i].setAttribValue(color_attribute, hou.Vector3(0, height_diff, 0)) 
            tmp_region['points'].append(points[i])
            if(tmp_region_firstP == None):
                tmp_region_firstP = points[i]
        else:
            if( len(tmp_region['points']) > 1):
                tmp_region['previous_point'] = points[i-1]
                tmp_region['next_point'] = points[i+1]
                regions.append(tmp_region)

            tmp_region = {}
            tmp_region['points'] = []
            tmp_region['previous_point'] = tmp_region['next_point'] = None
            tmp_region_firstP = None
    
    for region in regions:
        random_color = hou.Vector3(random(), random(), random())
        half_region = math.trunc(len(region['points'])/2)
        half_region_position = region['points'][half_region-1].position()
        count = 0
        for point in region['points']:
            #point.setAttribValue(color_attribute, random_color)
            current_position = point.position()
            if(count < half_region):
                point.setAttribValue(color_attribute, hou.Vector3(0,1,0))
                point.setPosition((current_position[0],region['points'][0].position()[1], current_position[2]))
            else:
                point.setAttribValue(color_attribute, hou.Vector3(0,0,1))
                if(count == half_region):
                    point.setPosition((half_region_position[0],region['points'][len(region['points'])-1].position()[1], half_region_position[2]))
                    point.setAttribValue(color_attribute, hou.Vector3(1,0,0))
                else:
                    point.setPosition((current_position[0],region['points'][len(region['points'])-1].position()[1], current_position[2]))
            count +=1
