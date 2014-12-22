



#    Addon info
bl_info = {
    'name': 'High to Low poly bake list (H2LBakeList)',
    'author': 'Ni Zu',
    'location': 'scene panel',
    'category': 'Scene'
    }

import bpy 

###################################
########### PROPERTIES
###################################



class H2LBentry(bpy.types.PropertyGroup):
    LOobj = bpy.props.StringProperty(subtype='NONE' )
    HIobj = bpy.props.StringProperty(subtype='NONE' )
    dist =  bpy.props.FloatProperty()
    bias =  bpy.props.FloatProperty()
#    nmtexpath = bpy.props.StringProperty(subtype='FILE_PATH')


class H2LB(bpy.types.PropertyGroup):
 
    index = bpy.props.IntProperty()

    bakelist=bpy.props.CollectionProperty(type=H2LBentry)

    nmimg = bpy.props.StringProperty()
    aoimg = bpy.props.StringProperty()
    dispimg = bpy.props.StringProperty()
   



###################################
########### OPERATIONS
###################################

class OP_H2LB_slotadd (bpy.types.Operator):
    "add slot to bakelist"
    bl_idname = "scene.h2lbslotadd"
    bl_label = "add slot"
    
    
    def execute(self, context):

        listitem=bpy.context.scene.H2LB.bakelist.add()
        try:
            listitem.LOobj= bpy.context.scene.objects.active.name
        except:
            pass
        return {'FINISHED'}

class OP_H2LB_slotremove (bpy.types.Operator):
    "add slot to bakelist"
    bl_idname = "scene.h2lbslotremove"
    bl_label = "remove active slot"
    
    
    def execute(self, context):


        try:
           bpy.context.scene.H2LB.bakelist.remove(bpy.context.scene.H2LB.index)
        except:
           bpy.context.scene.H2LB.bakelist.remove(0)
           
        return {'FINISHED'}


    
class OP_H2LB_populate_lo (bpy.types.Operator):
    "populate list from selected objects (as lowpoly targets)"
    bl_idname = "scene.h2lbpopulatelo"
    bl_label = "use selected as LO chunks "
    
    
    def execute(self, context):
        
        for obj in bpy.context.selected_objects:
            listitem=bpy.context.scene.H2LB.bakelist.add()
            listitem.LOobj= obj.name
            

        pass    
        return {'FINISHED'}

class OP_H2LB_populate_hi (bpy.types.Operator):
    "populate list from selected objects (as lowpoly targets)"
    bl_idname = "scene.h2lbpopulatehi"
    bl_label = "create copies for hipoly "
    
    
    def execute(self, context):

        pass    
        return {'FINISHED'}


class OP_H2LB_bakeloop(bpy.types.Operator):
    "execute batch baking of ao,disp,nm for all hi to low chunks"
    bl_idname = "scene.h2lbake"
    bl_label = "RUN BAKE"
    
    
    def execute(self, context):
        H2LB = bpy.context.scene.H2LB
        bakelist = bpy.context.scene.H2LB.bakelist
        
        ###
        
        for baketype in ['nmimg','aoimg','dispimg']:
            
            
            ##set bake mode 
            
            if baketype == 'nmimg' :
                mode = 'NORMALS'
            elif baketype == 'aoimg' :
                mode = 'AO'
            elif baketype == 'dispimg' :
                mode = 'DISPLACEMENT'
                
            bpy.context.scene.render.bake_type = mode
            
            ## loop through lo/hi pairs and bake
            for i in bakelist :
                
                bpy.ops.object.select_pattern(pattern=(i.HIobj+'*'))
                bpy.ops.object.select_pattern(pattern=i.LOobj)
                bpy.context.scene.objects.active = bpy.data.objects[i.LOobj]
                
                if i.LOobj and i.HIobj != '':

                ##assign image
                
                    for uv_face in bpy.data.objects[i.LOobj].data.uv_textures.active.data:
                        uv_face.image = bpy.data.images[H2LB[baketype]]
                ### do it !
                
                bpy.ops.object.bake_image()           


            ##rebake with final padding ??
            pass 
            
            

        return {'FINISHED'}



###################################
########### USER INTERFACE
###################################

        
        

class SCENE_UL_H2LBList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        sce = bpy.context.scene
                
        #layout = self.layout
        row = layout.row()
        row.prop_search(item, "LOobj", context.scene, "objects",text="LO")
        row.prop_search(item, "HIobj",context.scene, "objects",text="HI")
        
        
class H2LBPanel(bpy.types.Panel):
    """"""
    bl_label = "H2L Bake List"
    bl_idname = "SCENE_PT_H2LB"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        sce = bpy.context.scene
        
        row = layout.row()
        row.prop_search(sce.H2LB,"nmimg",bpy.data,"images")               
        row = layout.row()
        row.prop_search(sce.H2LB,"aoimg",bpy.data,"images")
        row = layout.row()
        row.prop_search(sce.H2LB,"dispimg",bpy.data,"images")

        layout.template_list("SCENE_UL_H2LBList", "", sce.H2LB, "bakelist", sce.H2LB, "index")

        row = layout.row()
        row.operator("scene.h2lbslotadd")
        row.operator("scene.h2lbslotremove")
        
        row = layout.row()
        row.operator("scene.h2lbpopulatelo")
        row = layout.row()
        row.operator("scene.h2lbpopulatehi")
        
        row = layout.row()
        row = layout.row()
        row.operator("scene.h2lbake")
        
        
        
###################################
########### REGISTER
###################################


def register():

    bpy.utils.register_class(H2LBentry)
    bpy.utils.register_class(H2LB)    
   
    bpy.types.Scene.H2LB=bpy.props.PointerProperty(type=H2LB)

    bpy.utils.register_class(OP_H2LB_slotadd)
    bpy.utils.register_class(OP_H2LB_slotremove)


    bpy.utils.register_class(OP_H2LB_bakeloop)

    bpy.utils.register_class(OP_H2LB_populate_lo)
    bpy.utils.register_class(OP_H2LB_populate_hi)
    

    bpy.utils.register_class(H2LBPanel)
    bpy.utils.register_class(SCENE_UL_H2LBList)


def unregister():


    bpy.utils.unregister_class(H2LBentry)
    bpy.utils.unregister_class(H2LB)    
    
    bpy.utils.unregister_class(OP_H2LB_slotadd)
    bpy.utils.unregister_class(OP_H2LB_slotremove)

    bpy.utils.register_class(OP_H2LB_bakeloop)

    bpy.utils.unregister_class(OP_H2LB_populate_lo)
    bpy.utils.unregister_class(OP_H2LB_populate_hi)

    
    bpy.utils.unregister_class(H2LBPanel)
    bpy.utils.unregister_class(SCENE_UL_H2LBList)


 
if __name__ == "__main__":
    register()
        