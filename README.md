# Text-to-3D Generator

A web-based text-to-3D generation system that transforms natural language descriptions into downloadable 3D models. Users can enter a text prompt and receive a downloadable `.ply` file containing the generated 3D model.

## 🚀 Features

- **Simple Web Interface**: Enter text prompts through an intuitive web interface
- **Instant Download**: Generate and download 3D models as `.ply` files
- **3D Visualization**: View generated models using the built-in visualization tool
- **Shape-E Integration**: Powered by advanced text-to-3D algorithms
- **No Installation Required**: Run directly in your browser

## 📋 Requirements

- Python 3.8+
- Web browser (Chrome, Firefox, Safari)
- 4GB+ RAM recommended

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Dhairyajeet-singh/text-to-3d.git
cd text-to-3d
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Open your browser and navigate to the provided local URL (typically `http://localhost:5000`)

## 🎯 How to Use

### Step 1: Generate 3D Model
1. Open the web application in your browser
2. Enter a descriptive text prompt (e.g., "a red sports car", "a wooden chair", "a cute robot")
3. Click the generate button
4. Wait for processing to complete

### Step 2: Download Model
1. Once generation is complete, a download link will appear
2. Click the download link to save the `.ply` file to your computer
3. The file will be saved with a unique identifier

### Step 3: Visualize (Optional)
1. Open `vis.py` in a text editor
2. Update the file path to point to your downloaded `.ply` file:
```python
# Update this line with your downloaded file path
model_path = "path/to/your/downloaded/model.ply"
```
3. Run the visualization:
```bash
python vis.py
```

## 📁 Project Structure

```
text-to-3d/
├── models/                 # Pre-trained model files
├── shap-e/                # Shape-E model implementation
├── shap_e_model_cache/    # Cached model data
├── static/                # Web interface assets (CSS, JS, images)
├── templates/             # HTML templates for web interface
├── main.py                # Main web application
├── final_model.py         # Core 3D generation logic
├── mesh_colored.py        # Mesh processing utilities
├── vis.py                 # 3D model visualization tool
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 🎨 Example Prompts

Try these example prompts to get started:

### Simple Objects
- "a red apple"
- "a wooden table"
- "a blue coffee mug"
- "a yellow banana"

### Complex Objects
- "a vintage typewriter"
- "a steampunk robot"
- "a medieval castle"
- "a racing motorcycle"

### Creative Descriptions
- "a cozy armchair with floral patterns"
- "a futuristic spaceship with glowing engines"
- "a delicate glass vase with flowers"
- "a rustic wooden boat on calm water"

## ⚙️ Configuration

The application uses default settings optimized for quality and speed. Advanced users can modify parameters in `final_model.py`:


## 🔧 Technical Details

### Model Architecture
- Built on **Shape-E** foundation model
- Supports text-to-3D generation pipeline
- Outputs colored mesh models in PLY format

### File Formats
- **Input**: Natural language text prompts
- **Output**: PLY (Polygon File Format) with vertex colors
- **Visualization**: Compatible with standard 3D viewers

### Performance
- **Generation Time**: 30-60 seconds per model (depending on complexity)
- **File Size**: Typically 1-5MB per PLY file
- **Supported Prompts**: Works best with concrete object descriptions

## 🐛 Troubleshooting

### Common Issues

**"Generation taking too long"**
- Complex prompts may require more processing time
- Try simpler, more specific descriptions
- Ensure sufficient system memory

**"Download link not appearing"**
- Wait for generation to complete fully
- Check browser console for error messages
- Refresh the page and try again

**"Visualization not working"**
- Verify the file path in `vis.py` is correct
- Ensure the PLY file downloaded successfully
- Check that all visualization dependencies are installed

**"Model looks wrong"**
- Try more descriptive prompts
- Avoid overly abstract concepts
- Use concrete, physical object descriptions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Test thoroughly with various prompts
5. Submit a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built using **Shape-E** by OpenAI
- Web interface powered by Flask/FastAPI
- 3D visualization using Open3D/Matplotlib

## 📚 Tips for Best Results

### Effective Prompt Writing
- **Be specific**: "red leather armchair" vs "chair"
- **Include materials**: "wooden", "metal", "glass", "fabric"
- **Add descriptive details**: "vintage", "modern", "ornate", "simple"
- **Specify colors**: Helps generate more accurate models

### What Works Well
- ✅ Common household objects
- ✅ Furniture and appliances
- ✅ Vehicles and transportation
- ✅ Simple architectural elements
- ✅ Everyday items with clear shapes

### What's Challenging
- ❌ Abstract concepts
- ❌ Complex scenes with multiple objects
- ❌ Highly detailed textures
- ❌ Transparent or translucent materials
- ❌ Very thin or delicate structures

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 4GB | 8GB+ |
| Storage | 2GB free | 5GB+ free |
| GPU | Not required | CUDA-compatible |
| Browser | Chrome 90+ | Latest version |

## 🗺️ Roadmap

- [ ] Support for additional file formats (ply)
- [ ] Real-time generation progress indicator
- [ ] Batch processing for multiple prompts
- [ ] Advanced parameter controls in web UI
- [ ] Model gallery for sharing creations
- [ ] Mobile-responsive interface

---

**Ready to create your first 3D model? Clone the repo and start generating!** 🎯
