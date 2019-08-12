import os.path
from .stream import Stream
from .float import Float
from .mdv import MDV

from mathutils import Vector
import math

class MDP:
    data_array = []

    class MDP_data:
        vert_array = []
        normal_array = []
        uv_array = []
        face_array = []
        used_id_array =[]
        weight_array = []

        def __init__(self):
            self.vert_array = []
            self.normal_array = []
            self.uv_array = []
            self.face_array = []
            self.used_id_array =[]
            self.weight_array = []

    def parse_mdp_file(self, f, mdv_struct):
        self.data_array = []
        total_verts = 0

        for i in range(len(mdv_struct.IXBF_array)):
            mdp_data = MDP.MDP_data()
            current_IXBF_info = mdv_struct.IXBF_array[i]
            f.seek(current_IXBF_info.far_offset)
            face_end = current_IXBF_info.far_offset + current_IXBF_info.far_size
            start_direction = -1
            f1 = Stream.Read16UIntegerBE(f)
            f2 = Stream.Read16UIntegerBE(f)
            face_direction = start_direction
            while(f.tell() <= face_end):
                f3 = Stream.Read16UIntegerBE(f)
                if f3 == 0xffff:
                    f1 = Stream.Read16UIntegerBE(f)
                    f2 = Stream.Read16UIntegerBE(f)
                    face_direction = start_direction
                else:
                    face_direction *= -1
                    if (f1 != f2) and (f2 != f3) and (f3 != f1):
                        if face_direction > 0:
                            mdp_data.face_array.append([f1,f2,f3])
                        else:
                            mdp_data.face_array.append([f1,f3,f2])
                    f1 = f2
                    f2 = f3

            current_VXBF_info = mdv_struct.VXBF_array[i]
            current_vsize = mdv_struct.vsize_array[i]

            f.seek(current_VXBF_info.far_offset)
            vert_count = int(current_VXBF_info.far_size / current_vsize)
            for j in range(vert_count):
                back = f.tell()
                
                xyz_data = Stream.Read32FloatBEArray(f, 3)
                mdp_data.vert_array.append(Vector([xyz_data[0], -xyz_data[2], xyz_data[1]]))
                if current_vsize in [24,28]:
                    f.seek(back + 20)
                    u = Float.ConvertHalf2Float(Stream.Read16UIntegerBE(f))
                    v = Float.ConvertHalf2Float(Stream.Read16UIntegerBE(f))
                    mdp_data.uv_array.append([u,1-v])
                if current_vsize in [32,36,40,44,48,52,56]:
                    f.seek(back + 24)
                    u = Float.ConvertHalf2Float(Stream.Read16UIntegerBE(f))
                    v = Float.ConvertHalf2Float(Stream.Read16UIntegerBE(f))
                    mdp_data.uv_array.append([u,1-v])
                f.seek(back + current_vsize) 

            if current_vsize not in [20]:
                self.data_array.append(mdp_data)
                total_verts += vert_count