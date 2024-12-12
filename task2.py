import sys
import os
from pytissueoptics import *

# Insert necessary paths for PyTissueOptics if not properly installed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TITLE = "Task 2: Green Light Propagation - 2D Projections"
DESCRIPTION = """Simulating the propagation of green light through a layered skin model and visualizing energy distribution."""

def exampleCode():
    # Number of photons to propagate
    N = 100000 if hardwareAccelerationIsAvailable() else 1000

    # Define layer-specific properties for green light (wavelength ~ 520-550 nm)
    material_epidermis = ScatteringMaterial(mu_s=60.0, mu_a=3.9, g=0.75, n=1.4)
    material_dermis = ScatteringMaterial(mu_s=60.0, mu_a=0.71, g=0.85, n=1.4)
    material_subcutis = ScatteringMaterial(mu_s=60.0, mu_a=0.49, g=0.49, n=1.4)

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

    # Propagate photons through the tissue
    source.propagate(scene, logger=logger)

    # Visualization: Side and front 2D projections
    viewer = Viewer(scene, source, logger)
    print("Reporting simulation statistics...")
    viewer.reportStats()

    print("Generating 2D side projection...")
    viewer.show2D(View2DProjectionX())  # Side view

    print("Generating 2D front projection...")
    viewer.show2D(View2DProjectionY())  # Front view

if __name__ == "__main__":
    exampleCode()
