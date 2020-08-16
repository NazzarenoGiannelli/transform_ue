#info that transforms a regular script into an installable addon
bl_info = {
    "name": "Transform to Unreal Engine",
    "author": "Nazzareno Giannelli <nazzareno@myd3sign.com>",
    "version": (1, 0),
    "blender": (2, 83, 0),
    "category": "Object",
    "location": "View 3D > Object",
    "description": "Copy location, rotation and scale of the selected objects to clipboard and easily paste them into Unreal Engine",
    "warning": "",
    "doc_url": "https://github.com/NazzarenoGiannelli/matslotcleaner",
    "tracker_url": "",
}

import bpy
from math import*
import subprocess
import sys
import os

python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')

# 'C:\\Program Files\\blender283\\2.83\\python\\bin\\python.exe'

#check the pip installation
subprocess.call([python_exe, "-m", "ensurepip"])
#subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

#install pyperclip
subprocess.call([python_exe, "-m", "pip", "install", "pyperclip", "--user"])

import pyperclip

#create the new Operator Class
class OBJECT_OT_transform_ue(bpy.types.Operator):
    """Copy location, rotation and scale of the selected objects to clipboard (then go to UE and Ctrl+V)"""
    bl_idname = "object.transform_ue"
    bl_label = "Transform to UE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        #variable for the selected objects
        selected = bpy.context.selected_objects

        #variable for counting the selected objects
        counter = 0

        #empty list to fill with UE actors data for the selected objects
        actorsList = []

        #transform values for every selected object
        for s in selected:

            #make the object active
            bpy.context.view_layer.objects.active = s

            #get object location in centimeters
            locX = str(s.location.x * 100)
            locY = str(s.location.y * 100)
            locZ = str(s.location.z * 100)

            #get object rotation in degrees
            rotX = str(degrees(s.rotation_euler.x))
            rotY = str(degrees(-s.rotation_euler.y))
            rotZ = str(degrees(-s.rotation_euler.z))

            #get object scale
            sclX = str(-s.scale.x)
            sclY = str(s.scale.y)
            sclZ = str(bpy.context.active_object.scale.z)
            
            #add numbering to the current object
            counter += 1

            actorsList.append("""
                Begin Actor Class=/Script/Engine.StaticMeshActor Name=Cube19_4 Archetype=/Script/Engine.StaticMeshActor'/Script/Engine.Default__StaticMeshActor'
                    Begin Object Class=/Script/Engine.StaticMeshComponent Name="StaticMeshComponent0" Archetype=StaticMeshComponent'/Script/Engine.Default__StaticMeshActor:StaticMeshComponent0'
                    End Object
                    Begin Object Name="StaticMeshComponent0"
                        StaticMesh=StaticMesh'"/Engine/BasicShapes/Cube.Cube"'
                        StaticMeshDerivedDataKey="STATICMESH_F9378A28F161444987BACE79B2590E57_228332BAE0224DD294E232B87D83948FQuadricMeshReduction_V1$2e0_26D666F86459324BE77D4F6A1939C6698000000000100000001000000000000000100000001000000010000000000000000000000000000004000000000000000020000000000803F0000803F0000803F0000004000000000050000004E6F6E650030000000803F0000803F000000000000004100000000000034420303030000000000000000LS0MNSzzzzzzzz0"
                        OverrideMaterials(0)=Material'"/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial"'
                        RelativeLocation=(X="""+ locX +',Y='+ locY +',Z='+ locZ +""")
                        RelativeRotation=(Pitch="""+ rotY +',Yaw='+ rotZ +',Roll='+ rotX +""")
                        RelativeScale3D=(X="""+ sclX +',Y='+ sclY +',Z='+ sclZ +''')
                    End Object
                    StaticMeshComponent="StaticMeshComponent0"
                    RootComponent="StaticMeshComponent0"
                    ActorLabel="Placeholder_'''+ str(counter) +'''"
                End Actor''')

        #join the actors text
        actorsText = " ".join(actorsList)

        #text snippet that goes at the beginning
        beginText = """Begin Map
            Begin Level"""

        #text snippet that goes at the end
        endText = """
            End Level
        Begin Surface
        End Surface
        End Map"""

        #use the pyperclip module in order to copy the C++ text to clipboard
        pyperclip.copy(beginText + actorsText + endText)

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_transform_ue.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_transform_ue)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_transform_ue)
    bpy.types.VIEW3D_MT_object.remove(menu_func)