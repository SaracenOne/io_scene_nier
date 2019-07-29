import os
import struct

import bpy
from bpy.props import StringProperty, BoolProperty, FloatProperty, EnumProperty
from bpy_extras.io_utils import ImportHelper

bl_info = {
    'name': "Nier Model Importer",
    'author': 'Saracen',
    'blender': (2, 80, 0),
    'version': (0, 5, 0),
    'location': "File > Import > Nier Model (.mdv)",
    'description': 'Importer for Nier\'s MDV model format.',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Import-Export'
}

from .importer import Importer

class ImportNierModel(bpy.types.Operator, ImportHelper):
    """Load a Nier model file."""

    bl_idname = 'import_scene.nier'
    bl_label = 'Import Nier Model Format'

    filename_ext = '.mdv'
    filter_glob = StringProperty(
        default='*.mdv',
        options={'HIDDEN'},
    )

    def draw(self, context):
        layout = self.layout

    def execute(self, context):
        imp = Importer(self.filepath, self.as_keywords())
        imp.do_import()
        return {'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(ImportNierModel.bl_idname, text="Nier Model (.mdv)")


def register():
    if bpy.app.version >= (2, 80, 0):
        bpy.utils.register_class(ImportNierModel)
        bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    else:
        bpy.utils.register_module(__name__)
        bpy.types.INFO_MT_file_import.append(menu_func_import)


def unregister():
    if bpy.app.version >= (2, 80, 0):
        bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
        bpy.utils.unregister_class(ImportNierModel)
    else:
        bpy.utils.unregister_module(__name__)
        bpy.types.INFO_MT_file_import.remove(menu_func_import)


if __name__ == '__main__':
    register()
