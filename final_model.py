import torch
import numpy as np
import trimesh
from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import decode_latent_mesh

def generate_3d(prompt: str, out_path: str = "mesh_colored.ply"):
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
    print(f"✅ 3D model saved to {out_path}")
def create_3d_model():
    # Create a simple 3D model (a cube)
    mesh = trimesh.load('mesh_colored.ply', process=False)
    print(mesh)
    mesh.show()
if __name__ == "__main__":
    prompt = input("Enter a prompt for the 3D model: ").strip()
    generate_3d(prompt)
    create_3d_model()