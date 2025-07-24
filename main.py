from flask import Flask, request, jsonify, send_file, render_template_string, render_template, url_for
import argparse
from flask_cors import CORS
import torch
import numpy as np
import trimesh
import os
from datetime import datetime
from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import decode_latent_mesh
import requests
import base64
from dotenv import load_dotenv

load_dotenv()



app = Flask(__name__)
CORS(app)
GITHUB_TOKEN = os.getenv("git_key") 
@app.route("/")
def home():
    return render_template("home.html")
@app.route("/login.html")
def login():
    return render_template("login.html")

def generate_3d(prompt: str, out_path:str = "models/mesh_colored.ply"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 1.  Load models -----------------------------------------------------------------
    model = load_model("text300M", device=device)       # CLIP‑conditioned diffusion prior
    xm     = load_model("transmitter", device=device)   # decodes latent → mesh
    diffusion = diffusion_from_config(load_config("diffusion"))

    # 2.  Sample a latent -------------------------------------------------------------
    latents = sample_latents(
    batch_size=1,
    model=model,
    diffusion=diffusion,
    guidance_scale=12.0,      # 10‑12 is still sharp but a bit faster
    model_kwargs=dict(texts=[prompt]),  # list length must equal batch_size
    device=device,
    progress=True,            # keep the tqdm bar
    clip_denoised=True,
    use_fp16=False,           # P2000 (Pascal) has no fast FP16
    use_karras=True,
    karras_steps=32,          # ⬇ main speed knob: 32 ≈ 18‑22 min on P2000
    sigma_min=1e-4,
    sigma_max=160,
    s_churn=0,
    )

    latent = latents[0]

    # 3.  Decode latent → mesh --------------------------------------------------------
    mesh = decode_latent_mesh(xm, latent)

    # 4.  Convert to trimesh & save ---------------------------------------------------
    verts  = mesh.verts.cpu().numpy()
    faces  = mesh.faces.cpu().numpy()
    colors = torch.stack([mesh.vertex_channels[c] for c in ("R", "G", "B")], 1)
    colors = (colors.clamp(0, 1).cpu().numpy() * 255).astype(np.uint8)

    tm = trimesh.Trimesh(vertices=verts, faces=faces, vertex_colors=colors, process=False)
    tm.export(out_path)
        
    # Your repository configuration
    repo_owner = "Dhairyajeet-singh"
    repo_name = "text-to-3d"
    github_token=GITHUB_TOKEN
    file_path = out_path
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    try:
        # Read file content
        with open(file_path, 'rb') as f:
            content = base64.b64encode(f.read()).decode()
        
        # Create unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        github_path = f"models/mesh_colored_{timestamp}.ply"
        
        # GitHub API endpoint
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{github_path}"
        
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "message": f"Upload mesh file {timestamp}",
            "content": content
        }
        
        response = requests.put(url, json=data, headers=headers)
        
        if response.status_code == 201:
            # Return direct download URL
            download_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{github_path}"
            print(f"File uploaded successfully to GitHub")
            os.remove("models/mesh_colored.ply")
            return download_url
        else:
            print(f"GitHub upload failed: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Error uploading to GitHub: {e}")
        return None
        

@app.route("/chatbot.html", methods=["GET", "POST"])
def chatbot():
    output = None
    if request.method == "POST":
        input_text = request.form["inputText"]
        output=generate_3d(input_text)
    return render_template("chatbot.html", output=output)
        

if __name__ == "__main__": 
    app.run(debug=False, port=5000)
