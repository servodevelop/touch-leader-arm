"""Render the extracted CAD BOM with Blender Cycles; no invented geometry.

Usage: blender --background --factory-startup --python scripts/render_bom.py --
       --mesh-dir /absolute/path/to/temporary-meshes
"""
import argparse
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector, Matrix
import math

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / 'hardware'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mesh-dir', required=True, type=Path)
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    manifest = json.loads((MODEL / 'bom.json').read_text())
    output = MODEL / 'images'
    output.mkdir(exist_ok=True)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    scene.cycles.seed = 0
    scene.cycles.use_denoising = True
    scene.render.resolution_x = scene.render.resolution_y = 1024
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.view_settings.view_transform = 'Standard'
    scene.world.use_nodes = True
    nodes, links = scene.world.node_tree.nodes, scene.world.node_tree.links
    nodes.clear()
    out = nodes.new('ShaderNodeOutputWorld')
    mix = nodes.new('ShaderNodeMixShader')
    ray = nodes.new('ShaderNodeLightPath')
    ambient = nodes.new('ShaderNodeBackground')
    ambient.inputs['Color'].default_value = (.8, .8, .8, 1)
    ambient.inputs['Strength'].default_value = .45
    background = nodes.new('ShaderNodeBackground')
    background.inputs['Color'].default_value = (1, 1, 1, 1)
    background.inputs['Strength'].default_value = 1
    links.new(ray.outputs['Is Camera Ray'], mix.inputs[0])
    links.new(ambient.outputs[0], mix.inputs[1])
    links.new(background.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], out.inputs[0])
    material = bpy.data.materials.new('Neutral CAD display material')
    material.use_nodes = True
    nodes, links = material.node_tree.nodes, material.node_tree.links
    nodes.clear()
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    out = nodes.new('ShaderNodeOutputMaterial')
    bsdf.inputs['Base Color'].default_value = (.50, .49, .46, 1)
    bsdf.inputs['Roughness'].default_value = .45
    bevel = nodes.new('ShaderNodeBevel')
    bevel.inputs['Radius'].default_value = .003
    bevel.samples = 4
    links.new(bevel.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    for position, power, size in [((2, -4, 6), 180, 4), ((-4, -1, 2), 80, 4), ((2, 4, 3), 150, 3)]:
        light = bpy.data.lights.new('Softbox', 'AREA')
        light.energy, light.shape, light.size = power, 'DISK', size
        obj = bpy.data.objects.new('Softbox', light)
        scene.collection.objects.link(obj)
        obj.location = position
        obj.rotation_euler = (-obj.location).to_track_quat('-Z', 'Y').to_euler()
    camera_data = bpy.data.cameras.new('Orthographic')
    camera = bpy.data.objects.new('Camera', camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    camera_data.type = 'ORTHO'
    identifiers = [row['id'] for row in manifest['items']] + ['touch-r1-assembly']
    for identifier in identifiers:
        data = json.loads((args.mesh_dir / f'{identifier}.json').read_text())
        mesh = bpy.data.meshes.new(identifier)
        mesh.from_pydata(data['vertices'], [], data['triangles'])
        mesh.update()
        obj = bpy.data.objects.new(identifier, mesh)
        scene.collection.objects.link(obj)
        obj.data.materials.append(material)
        if identifier == 'touch-r1-assembly':
            # The source assembly is Y-up; display its base horizontally.
            upright = Matrix.Rotation(math.pi / 2, 4, 'X')
            for vertex in mesh.vertices:
                vertex.co = upright @ vertex.co
        for polygon in mesh.polygons:
            polygon.use_smooth = True
        low = Vector(tuple(min(v.co[i] for v in mesh.vertices) for i in range(3)))
        high = Vector(tuple(max(v.co[i] for v in mesh.vertices) for i in range(3)))
        center, scale = (low + high) / 2, 2.8 / max(high - low)
        for vertex in mesh.vertices:
            vertex.co = (vertex.co - center) * scale
        # Show the single-shaft servo's horn; the other models share one view.
        camera.location = (5, 7, 5) if identifier == 'touch-r1-servo-rp8-u45h-m-c028' else (5, -7, 5)
        camera.rotation_euler = (-camera.location).to_track_quat('-Z', 'Y').to_euler()
        rotation = camera.rotation_euler.to_quaternion()
        projected = [rotation.inverted() @ v.co for v in mesh.vertices]
        low = [min(v[i] for v in projected) for i in range(2)]
        high = [max(v[i] for v in projected) for i in range(2)]
        shift = rotation @ Vector(((low[0]+high[0])/2, (low[1]+high[1])/2, 0))
        obj.location = -shift
        camera_data.ortho_scale = max(high[0]-low[0], high[1]-low[1]) * 1.20
        scene.render.filepath = str(output / f'{identifier}.png')
        bpy.ops.render.render(write_still=True)
        bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.meshes.remove(mesh)
        print(f'Rendered {identifier}', flush=True)


if __name__ == '__main__':
    main()
