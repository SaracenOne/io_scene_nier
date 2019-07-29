import os.path
from .stream import Stream
import math

class MDV:
    class MeshInfoDescriptor:
        name = ""
        unkId = 0
        unused = 0
        offset = 0
        size = 0
        far_offset = 0
        far_size = 0
        unk_flag = 0

        def __init__(self):
            self.name = ""
            self.unkId = 0
            self.unused = 0
            self.offset = 0
            self.size = 0
            self.far_offset = 0
            self.far_size = 0
            self.unk_flag = 0

    bonesdata = []
    IXBF_array = []
    VXBF_array = []
    VXST_array = []
    mesh_name_array = []
    vsize_array = []

    def parse_mdv_file(self, f):
        f.seek(0x10)

        bone_offset = 0
        bone_offset_raw = Stream.Read32SIntegerBE(f) + 0x80
        if bone_offset > 0:
            bone_offset += 0x80

        f.seek(0x110)

        NODT_off = Stream.Read32SIntegerBE(f) + 0x100
        heap_offset = Stream.Read32SIntegerBE(f) + 0x100

        f.seek(0x180)
        mesh_1 = Stream.ReadFixedString(f, 4)
        mesh_1_size = Stream.Read32SIntegerBE(f)
        mesh_1_off = f.tell() + mesh_1_size

        rem_0 = Stream.ReadFixedString(f, 4)
        rem_0_size = Stream.Read32SIntegerBE(f)
        rem_0_name = Stream.ReadFixedString(f, rem_0_size)

        strb = Stream.ReadFixedString(f, 4)
        strb_size = Stream.Read32SIntegerBE(f)
        strb_off = f.tell() + strb_size
        strb_count = Stream.Read32SIntegerBE(f)

        strl = Stream.ReadFixedString(f, 4)
        strl_size = Stream.Read32SIntegerBE(f)

        name2_array = []
        for m in range(strb_count):
            name2 = Stream.ReadCString(f)
            name2_array.append(name2)

        f.seek(strb_off)
        mat_id_array = []
        mat_slot_tex_id = []

        while(True):
            if f.tell() == mesh_1_off:
                break
            
            name_1 = Stream.ReadFixedString(f, 4)
            name_1_size = Stream.Read32SIntegerBE(f)
            relative_start = f.tell()
            if name_1 == "DSNA":
                f.seek(relative_start + name_1_size)
            elif name_1 == "TRSP":
                f.seek(relative_start + name_1_size)
            elif name_1 == "EFFE":
                f.seek(relative_start + 0x10)
            elif name_1 == "TPAS":
                f.seek(relative_start + name_1_size)
            elif name_1 == "CSTS":
                f.seek(relative_start + 0x04)
            elif name_1 == "CSTV":
                f.seek(relative_start + name_1_size)
            elif name_1 == "SAMP":
                mat_id = Stream.Read32SIntegerBE(f)
                mat_id_array.append(mat_id)
            elif name_1 == "SSTV":
                mat_slot = Stream.Read32SIntegerBE(f)
                tex_id = Stream.Read32SIntegerBE(f)
                mat_name_id = Stream.Read32SIntegerBE(f)
                if mat_slot == 29:
                    print ("The Diffuse Texture is " + name2_array[tex_id])
                if mat_slot == 32:
                    print ("The Normal Texture is " + name2_array[tex_id])
                if mat_slot == 35:
                    print ("The Specular Texture is " + name2_array[tex_id])
                if mat_slot == 44:
                    print ("The 2nd Normal Texture is " + name2_array[tex_id])
                #break
            elif name_1 == "MATE":
                mat_slot_id = Stream.Read32SIntegerBE(f)
                mat_slot_n1 = Stream.Read32SIntegerBE(f)
                mat_slot_n2 = Stream.Read32SIntegerBE(f)
                mat_slot_id2 = Stream.Read32SIntegerBE(f)
                mat_slot_tex_id1 = Stream.Read32SIntegerBE(f)
                mat_slot_n = Stream.Read32SIntegerBE(f)
                mat_slot_n = Stream.Read32SIntegerBE(f)
                mat_slot_tex_id2 = Stream.Read32SIntegerBE(f)
            elif name_1 == "VARI":
                f.seek(relative_start + 0x10) 
            elif name_1 == "PRIM":
                mesh_slot_id = Stream.Read32SIntegerBE(f)
                mesh_slot_id = Stream.Read32SIntegerBE(f)
                mesh_slot_id = Stream.Read32SIntegerBE(f)
                mesh_slot_id = Stream.Read32SIntegerBE(f)
                mesh_slot_id = Stream.Read32SIntegerBE(f)
                mesh_mat_id = Stream.Read32SIntegerBE(f)
                mesh_slot_id = Stream.Read32SIntegerBE(f)
                mat_slot_tex_id.append(mesh_mat_id)
            elif name_1 == "BONE":
                f.seek(relative_start + 0x04) 
            elif name_1 == "BOIF":
                f.seek(relative_start + name_1_size)
            elif name_1 == "IMTX":
                f.seek(relative_start + name_1_size)            
            else:
                break 

        # Bones
        self.bonesdata = []
        if bone_offset > 0:
            f.seek(bone_offset)
            CJF = Stream.ReadFixedString(f, 4)
            rig_name = Stream.ReadFixedString(f, 0x20)
            bone_count = Stream.Read32SIntegerBE(f)
            unknown_count = Stream.Read32SIntegerBE(f)
            bone_name_start = Stream.Read32SIntegerBE(f) + bone_offset
            unknown_name_start = Stream.Read32SIntegerBE(f) + bone_offset
            bone_parent_start = Stream.Read32SIntegerBE(f) + bone_offset
            bone_matrix_start = Stream.Read32SIntegerBE(f) + bone_offset
            bone_inv_matrix_start = Stream.Read32SIntegerBE(f) + bone_offset

            bone_name_array = []
            bone_parent_array = []

            f.seek(bone_name_start)
            for i in range(bone_count):
                unknown_01 = Stream.Read32SIntegerBE(f)
                bone_name = Stream.ReadFixedString(f, 0x20)
                bone_name_array.append(bone_name)
                self.bonesdata.append([bone_name])

            f.seek(bone_parent_start)
            for i in range(bone_count):
                bone_parent_id = Stream.Read16UIntegerBE(f)
                bone_parent_array.append(bone_parent_id)
                self.bonesdata[i].append(bone_parent_id)

            f.seek(bone_matrix_start)
            for i in range(bone_count):
                row1 = Stream.Read32FloatBEArray(f, 4)
                row2 = Stream.Read32FloatBEArray(f, 4)
                row3 = Stream.Read32FloatBEArray(f, 4)
                row4 = Stream.Read32FloatBEArray(f, 4)
                self.bonesdata[i].append([row1, row2, row3, row4])

        # Mesh
        f.seek(heap_offset)
        heap = Stream.ReadFixedString(f, 4)
        null1 = Stream.Read32SIntegerBE(f)
        sect_size = Stream.Read32SIntegerBE(f)
        heap_1_size = Stream.Read32SIntegerBE(f)
        count_1 = Stream.Read32SIntegerBE(f)
        name_size = Stream.Read32SIntegerBE(f)
        null2 = Stream.Read32SIntegerBE(f)
        heap_count = Stream.Read32SIntegerBE(f)
        myoff = f.tell()
        f.seek(heap_offset + heap_1_size)
        self.mesh_name_array = []

        while(True):
            if f.tell() >= (heap_offset + count_1):
                break
            mesh_name = Stream.ReadCString(f)
            if mesh_name != "":
                self.mesh_name_array.append(mesh_name)

        f.seek(myoff)

        self.IXBF_array = []
        self.VXBF_array = []
        self.VXST_array = []

        for i in range(heap_count):
            mesh_info_descripter = MDV.MeshInfoDescriptor()
            
            mesh_info_descripter.name = Stream.ReadFixedString(f, 4)
            mesh_info_descripter.unkId = Stream.Read32SIntegerBE(f)
            mesh_info_descripter.unused = Stream.Read32SIntegerBE(f)
            mesh_info_descripter.offset = Stream.Read32SIntegerBE(f)
            mesh_info_descripter.size = Stream.Read32SIntegerBE(f)
            mesh_info_descripter.far_offset = Stream.Read32SIntegerBE(f)
            mesh_info_descripter.far_size = Stream.Read32SIntegerBE(f)
            mesh_info_descripter.unk_flag = Stream.Read32SIntegerBE(f)
            heap_id = mesh_info_descripter.name

            if heap_id == "IXBF":
                 self.IXBF_array.append(mesh_info_descripter)
            elif heap_id == "VXBF":
                self.VXBF_array.append(mesh_info_descripter)
            elif heap_id == "VXST":
                self.VXST_array.append(mesh_info_descripter)
            elif heap_id == "VXAR":
                pass
            elif heap_id == "VXBO":
                pass
                
        print(Stream.ReadFixedString(f, name_size))
        modelName = Stream.ReadCString(f)
        print("Model name: " + modelName)

        Stream.SeekAlign(f, 0x10)
        near_offset = f.tell()
        self.vsize_array = []
        for i in range(len(self.VXST_array)):
            f.seek(near_offset + self.VXST_array[i].offset + 0x30, 0)
            vert_size = Stream.Read32SIntegerBE(f)
            print(vert_size)
            self.vsize_array.append(vert_size)