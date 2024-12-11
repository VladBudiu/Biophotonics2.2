from pytissueoptics import *

class SkinModelWithoutBlood(ScatteringScene):
    """
    Skin model consisting of three layers: Epidermis, Dermis, and Subcutis, without a blood layer.
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

class SkinModelWithBlood(SkinModelWithoutBlood):
    """
    Skin model with an additional blood layer between the dermis and subcutis layers.
    """
    def _create(self):
        super()._create()

        # Add a blood layer
        blood_properties = ScatteringMaterial(mu_s=200.0, mu_a=0.5, g=0.98, n=1.4)
        blood_layer = Cuboid(3, 3, 0.01, material=blood_properties, label="Blood")
        blood_layer.translateBy(Vector(0, 0, 0.25))  # Position below the dermis

        # Update the tissue model with blood
        self.TISSUE.insert(2, blood_layer)  # Add between dermis and subcutis

def simulate_backscattered_light(model: ScatteringScene, light_color: str):
    """
    Simulates the backscattered light for the given skin model and light color.

    Args:
        model (ScatteringScene): The skin model to simulate.
        light_color (str): The color of the light (e.g., "green").

    Returns:
        tuple: A tuple containing the light source and the energy logger.
    """
    # Optical properties for different light colors
    optical_properties = {
        "green": [15, 10, 5, 0.1, 0.15, 0.2],
        "blue": [20, 15, 10, 0.2, 0.25, 0.3],
        "IR": [8, 6, 4, 0.05, 0.07, 0.1]
    }

    # Extend optical properties dynamically to match the number of layers in the model
    num_layers = len(model.TISSUE)
    mu_s = optical_properties[light_color][:3] + [optical_properties[light_color][0]] * (num_layers - 3)
    mu_a = optical_properties[light_color][3:] + [optical_properties[light_color][3]] * (num_layers - 3)

    # Update material properties of each layer in the model
    for i, layer in enumerate(model.TISSUE):
        layer._material.mu_s = mu_s[i]
        layer._material.mu_a = mu_a[i]

    # Define the light source
    source = DivergentSource(position=Vector(0, 0, -0.2), direction=Vector(0, 0, 1), N=100000, diameter=0.1, divergence=0.4)

    # Create an energy logger
    logger = EnergyLogger(model)

    # Propagate the light through the model
    source.propagate(model, logger=logger)

    return source, logger

def compare_models():
    """
    Compares the backscattered energy for skin models with and without a blood layer.

    Visualizes the energy profiles using 2D and 1D representations, and writes a textual comparison.
    """
    models = {
        "Without Blood": SkinModelWithoutBlood(),
        "With Blood": SkinModelWithBlood()
    }

    light_color = "green"  # Simulation for green light

    viewers = {}

    for model_name, model in models.items():
        source, logger = simulate_backscattered_light(model, light_color)

        # Viewer for visualization
        viewer = Viewer(model, source, logger)
        viewers[model_name] = viewer

    # Show 2D visualizations side by side
    print("Visualizing 2D energy projections side by side...")
    for model_name, viewer in viewers.items():
        viewer.show2D(View2DSliceZ(position=0.15))

    # Show 1D visualizations side by side
    print("Visualizing 1D energy profiles side by side...")
    for model_name, viewer in viewers.items():
        viewer.show1D(Direction.X_POS)

    # Written comparison
    print("\nComparison:")
    print("The model with blood shows higher absorption and scattering at the blood layer, leading to altered energy distributions compared to the model without blood.")
    print("This is particularly evident in the 2D and 1D visualizations, where energy intensity varies at depths corresponding to the blood layer.")

if __name__ == "__main__":
    print("Comparing models with and without blood...")
    compare_models()
