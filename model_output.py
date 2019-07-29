import bpy
from .mdp import MDP

class ModelOutput:
    def create_model(self, mdp):
        for i in range(len(mdp.data_array)):
            data_array = mdp.data_array[i]
            name = "model-"+str(i)

            mesh = bpy.data.meshes.new(name)
            mesh.from_pydata(data_array.vert_array, [], data_array.face_array)
            """
            if(mesh.validate):
                scene = bpy.data.scenes.active
                obj = scene.objects.new(mesh, name)
                mesh.recalcNormals()
                mesh.update()
            """