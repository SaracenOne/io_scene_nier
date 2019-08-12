import bpy
from .mdp import MDP

class ModelOutput:
    def create_model(self, mdv, mdp):
        for i in range(len(mdp.data_array)):
            data_array = mdp.data_array[i]
            name = mdv.mesh_name_array[i]

            mesh = bpy.data.meshes.new(name)
            mesh.from_pydata(data_array.vert_array, [], data_array.face_array)
            if(mesh.validate):
                ob = bpy.data.objects.new(name=name, object_data=mesh)

                ob.name = name
                ob.data = mesh

                scene = bpy.context.scene
                scene.collection.objects.link(ob)