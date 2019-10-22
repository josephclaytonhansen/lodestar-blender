##import, define the billingual dictionary, and prepare for intepretation.
import bpy
import os
import re

with open("/Volumes/SNOWFALL/Blender/lodestar_1_0_0_langref.txt") as f:
  d = dict(x.rstrip().split(None, 1) for x in f)
  f.close()
 
 
##now that the file has been read, the d dict is converted to a ShaderNode dict. Prefix can be changed. 
lr = {y:x for x,y in d.items()}
prefix = "ShaderNode"
s =""
for x in lr:
    seq = (prefix, lr[x])
    lr[x] = s.join(seq)
    
##Blender context and objects are defined, for the rest of the program to access. The node tree is cleared. 
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
space = bpy.context.view_layer.objects.active
space.select_set(state=True)
ntree = space.active_material
ntree.node_tree.nodes.clear()

##text to translate should be received through the UI, but for now: 
text = "rgba0..diff0-color/p1.rough//..glos0-color/p1.rough//=itex0.p1=diff0.mixs0-slot1=glos0.mixs0-slot2=p1.mixs0-fac=mixs0.p0=texc0-uv..mapv0..mute0..disp0..mato0-displace=ligp0-isshadowray-..mixs1-fac=tran0..mixs1-slot2=p0..mixs1-slot1=mixs1.mato0-surface="


##hold on to instances in z list and number them: all diff0 are combined into a single entry. diff1 would be a seperate entry. This way, each distinct node takes one slot in the z list. The lr dict turns z entries into nodes: lr[z[n][0:4]] gives the node type for lr translation. z[n] gives each individual node. 

z = []
for i in lr:
    highest = (re.finditer(str(i), text))
    highest = list(highest)
    count = -1
    for x in range(0, len(highest)):
        count = count + 1
        total =  re.finditer(str(i), text)
        for l in total:
            e = text[l.start():l.start()+5]
            if e[4] == str(count):
                if e not in z:
                    z.append(e[0:4]+str(count))

#The z list is now ready to use! oz list keeps unique instances, while z is now nodes. 
oz = z
up = 0
translation_index = [0,0]
for p in z:
    z[up] = z[up][0:4]
    z[up] = ntree.node_tree.nodes.new(lr[z[up]])
    
    ##In this non-written code, check location and move accordingly...
    
    z[up].location[0] = z[up].location[0] + translation_index[0]
    z[up].location[1] = z[up].location[1] + translation_index[1]
    print(z[up])
    up = up + 1
    
    ##In this non-written code, create links between z[n].inputs and z[n].outputs

    ##ntree.node_tree.links.new(OB.outputs[0], QB.inputs[0])