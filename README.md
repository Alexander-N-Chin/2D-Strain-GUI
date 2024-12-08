# 🌐 Graphene Multiaxial Strain Simulation

![alt text](https://github.com/Alexander-N-Chin/Graphene-Multiaxial-Strain-Simulation/blob/main/GUI.png?raw=true)

## 📄 Overview
This project simulates multiaxial strain on graphene and provides interactive visualizations of its electronic structure and lattice geometry. The tool enables users to explore how strain affects the direct lattice, reciprocal lattice, ⚡ energy dispersion, and bandgap properties of graphene.

## ⭐ Features
1. **🕹️ Interactive Graphene Lattice Visualization**
   - **Functionality**: 🖱️ Drag to pan and 🔍 scroll to zoom.
   - **Purpose**: 👀 Visualize the graphene lattice and adjust strain 📊 parameters interactively.

2. **📊 3D Energy Dispersion Plot**
   - **Functionality**: 🖱️ Drag to rotate the 3D plot.
   - **Axes**:
     - X-axis: 🌊 Wave number (k)
     - Y-axis: 🌊 Wave number (k)
     - Z-axis: Energy dispersion
   - **Purpose**: 👀 Visualize conduction and valence band surfaces to understand energy band structure under strain.

3. **📉 2D Contour Plot**
   - **Functionality**: Displays 📊 contours of the conduction band energy dispersion.
   - **Axes**:
     - X-axis: 🌊 Wave number (k)
     - Y-axis: 🌊 Wave number (k)
   - **Purpose**: 🔮 Predict the shape of the reciprocal lattice and visualize shifts in high symmetry points under strain.

4. **⚡ Band Gap Graph**
   - **Functionality**: Tracks the bandgap at high symmetry points along the path M -> Γ -> K -> M.
   - **Note**: Tracks the morphing of high symmetry points, not augmented k-points.
   - **Purpose**: 🔍 Analyze bandgap evolution under varying strain conditions.

5. **🎚️ Strain Input Sliders**
   - **Parameters**:
     - Shear strain
     - Armchair strain
     - Zigzag strain
   - **Purpose**: 🎛️ Dynamically adjust strain values to observe corresponding changes in visualizations.

## 🛠️ Usage Guide
Follow these steps to set up and run the simulation:

### 🖥️ Prerequisites
- 🐍 Python 3.x installed on your system.

### 🧰 Setup
1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On 🪟 Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On 🍎 macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### ▶️ Running the Simulation
1. Run the program:
   ```bash
   python graphene_visualization.py
   ```
2. Explore the 🕹️ interactive GUI:
   - Use 🎚️ sliders to adjust strain.
   - Interact with the lattice and visualizations as described in the **⭐ Features** section.

## 🤝 Contributing
Contributions are welcome! Feel free to submit 📋 issues or 🔀 pull requests.

## ⚖️ License
This project is licensed under the 📝 MIT License. See the `LICENSE` file for details.

## 🙌 Acknowledgments
Thank you for exploring this 🛠️ tool and contributing to the understanding of graphene's 🪨 electronic and structural properties!

