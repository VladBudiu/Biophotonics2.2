import sys
import os
try:
    from pytissueoptics import *
except ImportError as e:
    print(f"Error importing pytissueoptics: {e}")
    sys.exit(1)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TITLE = "Backscattered Energy for Reflectance PPG"
DESCRIPTION = """Visualizing the amount of backscattered light energy (Blue, Green, IR) 
leaving the skin surface."""

def simulate_backscattered_energy(wavelength, material_properties):
    print(f"Simulating backscattered energy for {wavelength} light...")

    # Define layer-specific properties
    material_epidermis = ScatteringMaterial(**material_properties["epidermis"])
    material_dermis = ScatteringMaterial(**material_properties["dermis"])
    material_subcutis = ScatteringMaterial(**material_properties["subcutis"])

    # Define layers with increased epidermis thickness
    increased_thickness = 0.0
    layer_epidermis = Cuboid(a=1.0, b=1.0, c=increased_thickness, position=Vector(0, 0, 0), material=material_epidermis, label="epidermis")
    layer_dermis = Cuboid(a=1.0, b=1.0, c=0.2, position=Vector(0, 0, increased_thickness), material=material_dermis, label="dermis")
    layer_subcutis = Cuboid(a=1.0, b=1.0, c=0.05, position=Vector(0, 0, increased_thickness + 0.2), material=material_subcutis, label="subcutis")

    # Stack layers to form the skin model
    stacked_tissue = layer_epidermis.stack(layer_dermis, "back").stack(layer_subcutis, "back")

    # Create the scene with the stacked tissue
    scene = ScatteringScene([stacked_tissue])
    logger = EnergyLogger(scene)

    # Validate surface labels
    print("Available surfaces in the epidermis layer:")
    print(layer_epidermis._surfaces.surfaceLabels)  # Print actual surface labels

    # Define a divergent photon source positioned above the tissue
    source = DivergentSource(position=Vector(0, 0, -0.2), direction=Vector(0, 0, 1), N=1000000,  # Increased photons
                             diameter=0.1, divergence=0.4, displaySize=0.2)

    # Propagate photons through the tissue
    source.propagate(scene, logger=logger)

    # Use the correct surface label from the available list
    surface_view = View2DSurfaceZ("epidermis", "epidermis_top", "leaving")
    logger.addView(surface_view)

    # Visualize the backscattered energy with normalized scaling
    print(f"Visualizing backscattered energy for {wavelength} light...")
    logger.showView(surface_view)

def example_code():
    # Material properties for different wavelengths
    materials = {
        "Blue": {
            "epidermis": {"mu_s": 50.0, "mu_a": 0.3, "g": 0.9, "n": 1.4},
            "dermis": {"mu_s": 60.0, "mu_a": 0.4, "g": 0.9, "n": 1.4},
            "subcutis": {"mu_s": 40.0, "mu_a": 0.2, "g": 0.8, "n": 1.4},
        },
        "Green": {
            "epidermis": {"mu_s": 30.0, "mu_a": 0.2, "g": 0.9, "n": 1.4},
            "dermis": {"mu_s": 35.0, "mu_a": 0.25, "g": 0.85, "n": 1.4},
            "subcutis": {"mu_s": 25.0, "mu_a": 0.15, "g": 0.8, "n": 1.4},
        },
        "IR": {
            "epidermis": {"mu_s": 10.0, "mu_a": 0.05, "g": 0.9, "n": 1.4},
            "dermis": {"mu_s": 12.0, "mu_a": 0.07, "g": 0.85, "n": 1.4},
            "subcutis": {"mu_s": 8.0, "mu_a": 0.05, "g": 0.8, "n": 1.4},
        },
    }

    # Simulate and visualize for Blue, Green, and IR light
    for wavelength, material_properties in materials.items():
        simulate_backscattered_energy(wavelength, material_properties)

if __name__ == "__main__":
    example_code()
