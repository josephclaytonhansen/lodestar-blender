"""Lodestar (translator), by Joseph Hansen. For Blender 2.8, currently. Hope you find this useful! Please respect the license; this is free to use, but don't steal without giving credit.

Consider donating (I'll love you forever) at ko-fi.com/josephclaytonhansen"""

#define the billingual dictionary, and prepare for intepretation.
import bpy
import os
import re

##Current memory draw: ~17.3 MB
##Current code size: 4.81 KB + 1.31 KB (6.12 KB)
##Current download size: 
##Current speed: instant

##functions!!!!
def moveNode(n,p=0,y=0,x=0,s=30):
#node, paths (each path is 1, so an output branching three times would be 3), y offset (should iterate, so 1,2,3...), node height offset (as a number from 0 to 100 as 1.0 to 2.0), and x offset.
    y=y*100
    x=x*100
    if p > 0:
        y = 200 - y
    if s > 0:
        y = y*(1+s/100)
    n.location[0] = n.location[0] + (x)
    n.location[1] = n.location[1] + y
    
def lastScan(count):
    ##find and return the node PREVIOUS to the current node
    lastni = scan[count-2]
    lastn = text[lastni:lastni+5]
    cn = oz.index(lastn)
    zcn = z[cn]
    return zcn

def currentScan(count):
    ##find and return the CURRENT node
    thisni= scan[count-1]
    thisn = text[thisni:thisni+5]
    nn = oz.index(thisn)
    znn = z[nn]
    return znn

def scrub(direction,count):
    ##encompass all, for ease
    if direction == 0:
        return currentScan(count)
    elif direction == -1:
        return lastScan(count)

##THIS NEEDS FIXED.BADLY.
    
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
text2 = "rgba0..diff0-color/p1.rough//..glos0-color/p1.rough//=itex0.p1=diff0.mixs0-slot1=glos0.mixs0-slot2=p1.mixs0-fac=mixs0.p0=texc0-uv..mapv0..mute0..disp0..mato0-displace=ligp0-isshadowray-..mixs1-fac=tran0..mixs1-slot2=p0..mixs1-slot1=mixs1.mato0-surface="

text = "rgba0..diff0-color/p1.rough//..glos0-color/p1.rough//=itex.p1=diff0.mixs0-slot1=glos0.mixs0-slot2=p1.mixs0-fac=mixs0.mato-surface="

text1 = "rgba0..diff0-color/p1.rough//rgba0..diff1-color/p1.rough//"

##hold on to instances in z list and number them: all diff0 are combined into a single entry. diff1 would be a seperate entry. This way, each distinct node takes one slot in the z list. The lr dict turns z entries into nodes: lr[z[n][0:4]] gives the node type for lr translation. z[n] gives each individual node. 

z = []
for i in lr: 
    ##I'm here to read text and find nodes. Also covfefe. 
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

oz = list(z) 
##An oz list keeps unique instances, while z is now nodes. 
up = 0
for p in z: 
    z[up] = z[up][0:4]
    z[up] = ntree.node_tree.nodes.new(lr[z[up]]) 
    ##Here the nodes are actually added.
    up = up + 1
    
##This is where we make links. 

##ntree.node_tree.links.new(zcn.outputs[(output_type)], znn.inputs[(input_type)])
##That is the magic line, that will be added later. 
scan = list()
count = 0
y_offset = 0 
for i in range(0, len(text)):
    if text[i:i+4] in lr:
        scan.append(i)
        ##each location in scan is the start of a node. 
        count = count + 1
        attr=""
        pth=1
        ##path, being a variable, varies.
        if i > 4: 
            ##direct connection
            if text[i-1] == ".":
                if text[i-2] == ".":
                    zcn = scrub(-1, count)
                    znn = scrub(0, count)
                    ntree.node_tree.links.new(zcn.outputs[0], znn.inputs[0])
                    moveNode(znn, pth, count+y_offset,count)            
                else: 
                    ##search for branches-pth also goes up
                    y_offset = y_offset + .5
            elif text[i-1] == "=": 
                ##end of path- pth also goes up
                y_offset = y_offset + 1
       
##This is debug- useful prints are scan/len, z/len, and oz/len.
