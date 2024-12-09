import sys
import os
try:
    from pytissueoptics import *
except ImportError as e:
    print(f"Error importing pytissueoptics: {e}")
    sys.exit(1)

# Insert necessary paths for PyTissueOptics if not properly installed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TITLE = "Green Light Propagation Through Multi-Layered Skin Model"
DESCRIPTION = """Simulation of green light propagation through a three-layer skin model representing
Epidermis, Dermis, and Subcutis."""

def exampleCode():
    # Number of photons to propagate
    N = 100000 if hardwareAccelerationIsAvailable() else 1000

    # Define layer-specific properties for green light (wavelength ~ 520-550 nm)
    material_epidermis = ScatteringMaterial(mu_s=10.0, mu_a=0.1, g=0.9, n=1.4)
    material_dermis = ScatteringMaterial(mu_s=15.0, mu_a=0.2, g=0.8, n=1.4)
    material_subcutis = ScatteringMaterial(mu_s=5.0, mu_a=0.05, g=0.7, n=1.4)

    # Define layers with thicknesses in cm
    layer_epidermis = Cuboid(a=1.0, b=1.0, c=0.05, position=Vector(0, 0, 0), material=material_epidermis, label="Epidermis")
    layer_dermis = Cuboid(a=1.0, b=1.0, c=0.2, position=Vector(0, 0, 0.05), material=material_dermis, label="Dermis")
    layer_subcutis = Cuboid(a=1.0, b=1.0, c=0.05, position=Vector(0, 0, 0.25), material=material_subcutis, label="Subcutis")

    # Stack layers to form the skin model
    stacked_tissue = layer_epidermis.stack(layer_dermis, "back").stack(layer_subcutis, "back")

    # Create the scene with the stacked tissue
    scene = ScatteringScene([stacked_tissue])
    logger = EnergyLogger(scene)

    # Define a divergent photon source positioned above the tissue
    source = DivergentSource(position=Vector(0, 0, -0.2), direction=Vector(0, 0, 1), N=N,
                             diameter=0.1, divergence=0.4, displaySize=0.2)

    # Display the tissue and source configuration
    scene.show(source=source)

    # Propagate photons through the tissue
    source.propagate(scene, logger=logger)

    # Visualization: 2D projections
    viewer = Viewer(scene, source, logger)
    viewer.reportStats()
    viewer.show2D(View2DProjectionX())  # Side view
    viewer.show2D(View2DProjectionY())  # Front view

    # Visualization: 1D energy profile
    viewer.show1D(Direction.Z_POS)

    # Optional: 3D point cloud visualization
    viewer.show3D()

if __name__ == "__main__":
    exampleCode()
