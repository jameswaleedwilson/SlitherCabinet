import json

with open('scene_mesh.json', 'r') as f:
    data = json.load(f)
    print(data["scene_mesh"][0]["name"])
