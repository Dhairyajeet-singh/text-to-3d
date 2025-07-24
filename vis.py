import trimesh
# Create a simple 3D model (a cube)
mesh = trimesh.load('mesh_colored.ply', process=False)
print(mesh)
mesh.show()