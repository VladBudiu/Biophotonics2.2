from pytissueoptics import *

class SkinModel(ScatteringScene):
    """
    Skin model consisting of three layers: Epidermis, Dermis, and Subcutis,
    with optical properties defined for green light.
    """
    TISSUE = []

    def __init__(self, worldMaterial=ScatteringMaterial()):
        self._create()
        super().__init__(self.TISSUE, worldMaterial, ignoreIntersections=True)

    def _create(self):
        # Optical properties for green light
        n = [1.4, 1.4, 1.44]  # Refractive indices
        mu_s = [15, 10, 5]    # Scattering coefficients (cm^-1)
        mu_a = [0.1, 0.15, 0.2]  # Absorption coefficients (cm^-1)
        g = 0.9  # Anisotropy factor (assumed constant)

        # Thicknesses of each layer (cm)
        thickness = [0.05, 0.2, 0.1]  # Epidermis, Dermis, Subcutis

        # Dimensions of the skin model (width x height)
        width = 3
        height = 3

        # Create layers
        epidermis = Cuboid(width, height, thickness[0], material=ScatteringMaterial(mu_s[0], mu_a[0], g, n[0]), label="Epidermis")
        dermis = Cuboid(width, height, thickness[1], material=ScatteringMaterial(mu_s[1], mu_a[1], g, n[1]), label="Dermis")
        subcutis = Cuboid(width, height, thickness[2], material=ScatteringMaterial(mu_s[2], mu_a[2], g, n[2]), label="Subcutis")

        # Align layers correctly and stack them
        dermis.translateBy(Vector(0, 0, thickness[0]))
        subcutis.translateBy(Vector(0, 0, thickness[0] + thickness[1]))

        self.TISSUE = [epidermis, dermis, subcutis]

# Function to simulate and log backscattered light
def simulate_backscattered_light(skin_model, light_color):
    # Define optical properties for different light colors
    optical_properties = {
        "green": [15, 10, 5, 0.1, 0.15, 0.2],
        "blue": [20, 15, 10, 0.2, 0.25, 0.3],
        "IR": [8, 6, 4, 0.05, 0.07, 0.1]
    }

    mu_s, mu_a = optical_properties[light_color][:3], optical_properties[light_color][3:]

    # Update materials in the skin model for the selected light color
    for i, layer in enumerate(skin_model.TISSUE):
        layer._material.mu_s = mu_s[i]  # Corrected to _material
        layer._material.mu_a = mu_a[i]  # Corrected to _material

    # Set up the light source
    source = DivergentSource(position=Vector(0, 0, -0.2), direction=Vector(0, 0, 1), N=10000, diameter=0.1, divergence=0.4)

    # Logger to capture energy leaving the surface
    logger = EnergyLogger(skin_model)

    # Propagate light through the model
    source.propagate(skin_model, logger=logger)

    return source, logger

# Function to visualize backscattered energy using the library's 1D visualization method
def plot_backscattered_energy():
    skin_model = SkinModel()

    light_colors = ["green", "blue", "IR"]

    for color in light_colors:
        source, logger = simulate_backscattered_light(skin_model, color)

        # Viewer for visualization
        viewer = Viewer(skin_model, source, logger)
        print(f"Visualizing 1D energy profile for {color.capitalize()} light...")
        viewer.show1D(Direction.X_POS)

# Example instantiation
if __name__ == "__main__":
    print("Simulating backscattered light for different colors...")
    plot_backscattered_energy()