import bpy
from math import pi
from mathutils import Vector, Matrix

    
class View3D_Pivot_Controls(bpy.types.Operator):
    """a pivoting navigation operator"""
    bl_idname = "view3d.pivot"
    bl_label = "Pivot Controls"
    
    cam = None
    cam_obj = None
    cam_mat = Matrix.Rotation(pi/2,3,'X')
    veiw_zoom = 0
    ini_mpos = Vector((0.0,0.0))
    rot_state= Vector((0.0,0.0))

    def execute(self, context):
        v3d = context.space_data
        rv3d = v3d.region_3d

        rv3d.view_location = self._initial_location + Vector(self.offset)
        
    def modal(self, context, event):
        
        rot_state=self.rot_state
        cam_mat=self.cam_mat
        mpos=Vector((event.mouse_x, event.mouse_y))
        mdist=mpos-self.ini_mpos
        
        speed_factor = 2/pow(1.41421 + self.view_zoom / 50,2) /1.11 # found magic numbers in blender source code
        
        if event.type in {'MIDDLEMOUSE'}:
            return {'FINISHED'}
        
        if event.type == 'MOUSEMOVE':
            rot_state+=mdist*speed_factor
            
            angle_x=Matrix.Rotation(rot_state[0]/72,3,'Y')
            angle_y=Matrix.Rotation(-rot_state[1]/72,3,'X')
            self.cam_obj.rotation_euler=(cam_mat @ angle_x @ angle_y).to_euler()
            self.ini_mpos = mpos
            return {'RUNNING_MODAL'}
        
        
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):

        if context.space_data.type == 'VIEW_3D':
            v3d = context.space_data
            rv3d = v3d.region_3d
            
            self.view_zoom = rv3d.view_camera_zoom


            if not "Pivot_cam" in bpy.data.cameras:
                self.cam=bpy.data.cameras.new("Pivot_cam")
                self.cam.angle=pi/8*7 
            else:
                self.cam=bpy.data.cameras['Pivot_cam']
            if not "Pivot_cam" in bpy.data.objects:
                self.cam_obj=bpy.data.objects.new("Pivot_cam",self.cam)
                self.cam_obj.rotation_euler=self.cam_mat.to_euler()
                #bpy.context.scene.collection.objects.link(self.cam_obj) # Not necessary
                bpy.context.scene.camera=self.cam_obj
            else:
                self.cam_obj=bpy.data.objects['Pivot_cam']
                    
            if rv3d.view_perspective != 'CAMERA':
                rv3d.view_perspective = 'CAMERA'
                
            cam_mat = Matrix.Rotation(pi/2,3,'X')

            self.ini_mpos = Vector((event.mouse_x, event.mouse_y))

            context.window_manager.modal_handler_add(self)
            
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}
        
    def cancel(self, context):
        destroy_custom_navigation()
        return {'FINISHED'}
    
        
def destroy_custom_navigation(self):
    if "Pivot_cam" in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects['Pivot_cam'])
        

def register():
    bpy.utils.register_class(View3D_Pivot_Controls)
    
def unregister():
    bpy.utils.unregister_class(View3D_Pivot_Controls)


if __name__ == "__main__":
    register()
