import sys
import os
try:
    from pytissueoptics import *
except ImportError as e:
    print(f"Error importing pytissueoptics: {e}")
    sys.exit(1)

# Insert necessary paths for PyTissueOptics if not properly installed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TITLE = "Light Propagation Through Multi-Layered Skin Model with Increased Epidermis Thickness"
DESCRIPTION = """Simulation of light propagation (Blue, Green, Red, NIR) through a three-layer skin model 
representing Epidermis, Dermis, and Subcutis with increased epidermis thickness."""

def simulate_light_propagation(wavelength, material_properties):
    print(f"Simulating {wavelength} light...")

    # Define layer-specific properties
    material_epidermis = ScatteringMaterial(**material_properties["epidermis"])
    material_dermis = ScatteringMaterial(**material_properties["dermis"])
    material_subcutis = ScatteringMaterial(**material_properties["subcutis"])

    # Define layers with updated epidermis thickness
    increased_thickness = 0.1  # Increase epidermis thickness to 0.1 cm
    layer_epidermis = Cuboid(a=1.0, b=1.0, c=increased_thickness, position=Vector(0, 0, 0), material=material_epidermis, label="Epidermis")
    layer_dermis = Cuboid(a=1.0, b=1.0, c=0.2, position=Vector(0, 0, increased_thickness), material=material_dermis, label="Dermis")
    layer_subcutis = Cuboid(a=1.0, b=1.0, c=0.05, position=Vector(0, 0, increased_thickness + 0.2), material=material_subcutis, label="Subcutis")

    # Stack layers to form the skin model
    stacked_tissue = layer_epidermis.stack(layer_dermis, "back").stack(layer_subcutis, "back")

    # Create the scene with the stacked tissue
    scene = ScatteringScene([stacked_tissue])
    logger = EnergyLogger(scene)

    # Define a divergent photon source positioned above the tissue
    source = DivergentSource(position=Vector(0, 0, -0.2), direction=Vector(0, 0, 1), N=10000,
                             diameter=0.1, divergence=0.4, displaySize=0.2)

    # Propagate photons through the tissue
    source.propagate(scene, logger=logger)

    # Add views at specific depths for energy visualization
    depths = [0.05, 0.25]  # Example depths in cm
    for depth in depths:
        logger.addView(View2DSliceZ(position=depth, thickness=0.01, limits=((-1, 1), (-1, 1))))

    # Visualization: 2D projections and energy profiles
    viewer = Viewer(scene, source, logger)
    for depth in depths:
        print(f"Showing 2D view for depth: {depth} cm")
        viewer.show2D(View2DSliceZ(position=depth))

def example_code():
    # Material properties for different wavelengths
    materials = {
        "Blue": {
    "epidermis": {"mu_s": 76.5, "mu_a": 6.85, "g": 0.75, "n": 1.4},
    "dermis": {"mu_s": 76.5, "mu_a": 2.45, "g": 0.85, "n": 1.4},
    "subcutis": {"mu_s": 76.5, "mu_a": 1.45, "g": 0.75, "n": 1.4},
},
"Green": {
    "epidermis": {"mu_s": 60.0, "mu_a": 3.90, "g": 0.75, "n": 1.4},
    "dermis": {"mu_s": 60.0, "mu_a": 0.71, "g": 0.85, "n": 1.4},
    "subcutis": {"mu_s": 60.0, "mu_a": 0.49, "g": 0.75, "n": 1.4},
},
"Red": {
    "epidermis": {"mu_s": 52.5, "mu_a": 2.50, "g": 0.75, "n": 1.4},
    "dermis": {"mu_s": 52.5, "mu_a": 0.41, "g": 0.85, "n": 1.4},
    "subcutis": {"mu_s": 52.5, "mu_a": 0.26, "g": 0.75, "n": 1.4},
},
"NIR": {
    "epidermis": {"mu_s": 40.5, "mu_a": 0.86, "g": 0.75, "n": 1.4},
    "dermis": {"mu_s": 40.5, "mu_a": 0.16, "g": 0.85, "n": 1.4},
    "subcutis": {"mu_s": 40.5, "mu_a": 0.11, "g": 0.75, "n": 1.4},
},

    }

    # Simulate and visualize for each wavelength
    for wavelength, material_properties in materials.items():
        simulate_light_propagation(wavelength, material_properties)

if __name__ == "__main__":
    example_code()
