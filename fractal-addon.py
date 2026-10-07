bl_info = {
    'name': 'Fractal Addon',
    'author': 'Solrika',
    'version': (0, 0, 2),
    'blender': (4, 2, 0),
    'category': 'Add Mesh',
}

import bpy
import math
from math import *

class MESH_OT_addFractal(bpy.types.Operator):
    bl_idname = "mesh.create_fractal"
    bl_label = "Make your own fractal!"
    bl_options = {"REGISTER", "UNDO"}
        
    Turn: bpy.props.IntProperty(name = "Angle", default = 90, min = 0, max=120)
    Sizes: bpy.props.IntProperty(name = "Size", default = 1, min = 1, max = 500) 
    a: bpy.props.IntProperty(name = "Count", default = 0, min = 0, max = 5) 
    Fractal: bpy.props.IntProperty(name = "К,М,С,П,свой", default = 1, min = 1, max = 5)
    Axiom: bpy.props.StringProperty(name = "Rule", default="F") 
            
    def execute(self, context):
        a_count=self.a
        f_number=self.Fractal
        sizes = self.Sizes
        turns=math.radians(self.Turn)
        axiom=self.Axiom
        
        y = 0
        z = 0
        n = 0
        angle = 0 
        m = 0
        
        stack_y=[] 
        stack_z=[] 
        stack_angle=[]
        stack_n=[] 
        vertices=[]
        edges=[]
        
        if f_number==1:
            name = "A+A-A-A+A"
        if f_number==2:
            name = "A-A+A+AA-A-A+A"
        if f_number!=3  and f_number!=4 and f_number!=5:
            for i in range (a_count): 
                s_ln=len(axiom)
                for j in range (s_ln):
                    if axiom[j]=="F":
                        axiom = axiom.replace("F", name)
                for g in range (s_ln):
                    if axiom[g]=="A":
                        axiom = axiom.replace("A", "F")
        if f_number==3:
            name1="B-A-B"
            name2="A+B+A"
        if f_number==4:
            name1="AA"
            name2="A[B]B"
        if f_number!=1 and f_number!=2 and f_number!=5:
            s_ln=len(axiom)
            for i in range (a_count): 
                for j in range (s_ln):
                    if axiom[j] == "F" or axiom[j] == "G":
                        axiom = axiom.replace("F", name1)
                        axiom = axiom.replace("G", name2)
                for g in range (s_ln):
                   if axiom[g] == "A" or axiom[g] == "B":
                        axiom = axiom.replace("A", "F")
                        axiom = axiom.replace("B", "G")
            s_ln=len(axiom)
            for i in range (s_ln):
                if axiom[i]=="G":
                    axiom = axiom.replace("G", "F")
            
        vertices.append((0,y,z)) 
        n+=1
        ln=len(axiom)
        for i in range (ln):
            if axiom[i]=="F" and axiom[i-1] != "F" and axiom[i-1] != "]":
                vertices.append((0,y,z))
                edges.append((n-1,n))
                n+=1
            elif axiom[i]=="F" and axiom[i-1] == "]":
                vertices.append((0,y,z))
                edges.append((m,n))
                n+=1
            elif axiom[i]=="F" and axiom[i-1] == "F":
                y+=math.sin(angle)*sizes
                z+=math.cos(angle)*sizes
                vertices.append((0,y,z))
                edges.append((n-1,n))
                n+=1
            elif axiom[i]=="+": 
                angle+=turns
                y+=math.sin(angle)*sizes
                z+=math.cos(angle)*sizes
            elif axiom[i]=="-":
                angle-=turns
                y+=math.sin(angle)*sizes
                z+=math.cos(angle)*sizes
            elif axiom[i]=="[": 
                stack_y.append(y)
                stack_z.append(z)
                stack_angle.append(angle)
                stack_n.append(n-1)
                angle+=turns
                y+=math.sin(angle)*sizes
                z+=math.cos(angle)*sizes
            elif axiom[i]=="]":
                if stack_y and stack_z and stack_n and stack_angle:
                    y = stack_y.pop()
                    z = stack_z.pop()
                    m = stack_n.pop()
                    angle=stack_angle.pop()
                angle-=turns
                y+=math.sin(angle)*sizes
                z+=math.cos(angle)*sizes
                
        base=bpy.data.meshes.new("fractal")
        base.from_pydata(vertices,edges,[])
        base.update()
        obj = bpy.data.objects.new('fractal', base)
        view_layer=bpy.context.view_layer
        view_layer.active_layer_collection.collection.objects.link(obj)
        return {'FINISHED'}
    
def menu_func(self, context):
    self.layout.operator(MESH_OT_addFractal.bl_idname, text="Add Fractal", icon='FORCE_TURBULENCE')

def register():
    bpy.utils.register_class(MESH_OT_addFractal)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(MESH_OT_addFractal)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
