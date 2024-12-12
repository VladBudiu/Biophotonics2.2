import sys
import os

try:
    from pytissueoptics import *
except ImportError as e:
    print(f"Error importing pytissueoptics: {e}")
    sys.exit(1)

# Blood optical properties based on literature values (example values)
BLOOD_PROPERTIES = {
    "mu_s": 200.0,  # Scattering coefficient (1/cm)
    "mu_a": 0.5,    # Absorption coefficient (1/cm)
    "g": 0.98,      # Anisotropy factor
    "n": 1.4        # Refractive index
}

# Function to simulate and visualize energy projections for specified wavelengths
def energy_projections(wavelengths, material_properties):
    for wavelength in wavelengths:
        print(f"Simulating and visualizing energy projections for {wavelength} light...")

        # Define layer-specific properties
        props = material_properties[wavelength]
        material_epidermis = ScatteringMaterial(**props["epidermis"])
        material_dermis = ScatteringMaterial(**props["dermis"])
        material_subcutis = ScatteringMaterial(**props["subcutis"])
        material_blood = ScatteringMaterial(**BLOOD_PROPERTIES)

        # Define layers with thicknesses in cm
        layer_epidermis = Cuboid(a=1.0, b=1.0, c=0.05, position=Vector(0, 0, 0), material=material_epidermis, label="Epidermis")
        layer_dermis = Cuboid(a=1.0, b=1.0, c=0.2, position=Vector(0, 0, 0.05), material=material_dermis, label="Dermis")
        layer_blood = Cuboid(a=1.0, b=1.0, c=0.01, position=Vector(0, 0, 0.22), material=material_blood, label="Blood")
        layer_subcutis = Cuboid(a=1.0, b=1.0, c=0.05, position=Vector(0, 0, 0.25), material=material_subcutis, label="Subcutis")

        # Stack layers to form the skin model
        stacked_tissue = layer_epidermis.stack(layer_dermis, "back").stack(layer_blood, "back").stack(layer_subcutis, "back")

        # Create the scene with the stacked tissue
        scene = ScatteringScene([stacked_tissue])
        logger = EnergyLogger(scene)

        # Define a divergent photon source positioned above the tissue
        source = DivergentSource(position=Vector(0, 0, -0.2), direction=Vector(0, 0, 1), N=10000,
                                 diameter=0.1, divergence=0.4, displaySize=0.2)

        # Propagate photons through the tissue
        source.propagate(scene, logger=logger)

        # Add views at specific depths for energy visualization
        depths = [0.05, 0.15, 0.25]  # Example depths in cm
        for depth in depths:
            logger.addView(View2DSliceZ(position=depth, thickness=0.01, limits=((-1, 1), (-1, 1))))

        # Visualization: 2D projections and energy profiles
        viewer = Viewer(scene, source, logger)
        for depth in depths:
            print(f"Showing 2D energy projection for {wavelength} light at depth: {depth} cm")
            viewer.show2D(View2DSliceZ(position=depth))

        print(f"1D Energy profile for {wavelength} light...")
        viewer.show1D(Direction.X_POS, solidLabel=None, surfaceLabel=None)
       
if __name__ == "__main__":
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

    # Simulate for selected wavelengths
    energy_projections(["Blue", "Green", "NIR"], materials)
