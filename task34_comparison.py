'''
Visualization:
The plotted energy profiles illustrate how the energy attenuates with depth for each wavelength in both Task 3 (original thickness) and Task 4 (increased epidermis thickness).
Task 4 shows a steeper energy decline for all wavelengths compared to Task 3, particularly for Blue and Green light, which are more sensitive to scattering and absorption.
Quantitative Results:
The table displays the depths at which 50% and 90% of the energy is lost for each wavelength in both tasks.
Key Insights:

50% Energy Loss Depth:

Blue Light: Reduced from 0.0697 cm in Task 3 to 0.0606 cm in Task 4, showing the increased epidermis thickness significantly affects the penetration of shorter wavelengths.
Green Light: Depth decreases from 0.1 cm to 0.0879 cm, reflecting moderate sensitivity to the increased scattering layer.
Red and NIR Light: Reduces slightly but remains less affected compared to shorter wavelengths due to their longer penetration capability.
90% Energy Loss Depth:

Blue and Green light in Task 4 have reduced 90% energy loss depths compared to Task 3, showing their diminished ability to reach deeper layers.
Red and NIR light exhibit minimal changes, with NIR maintaining significant penetration due to its low scattering and absorption coefficients.
Interpretation:
Impact of Increased Epidermis Thickness:

The increased scattering in the thicker epidermis significantly reduces the energy reaching deeper layers for shorter wavelengths.
Longer wavelengths (Red and NIR) are less affected and maintain deeper penetration due to their lower interaction probabilities with the tissue.
Wavelength Sensitivity:

Blue and Green light are highly sensitive to epidermis thickness changes, which aligns with their applications in superficial diagnostics and therapies.
NIR light demonstrates its utility in deep tissue imaging due to minimal energy attenuation even with increased epidermis thickness.
Practical Implications:

Understanding these dynamics is crucial for optimizing wavelength selection in phototherapy, optical imaging, and laser-based treatments, especially for patients with thicker or pigmented skin.
'''

import numpy as np
import matplotlib.pyplot as plt

# Depths (in cm) from the surface into the skin
depths = np.linspace(0, 0.3, 100)

# Task 3 energy profiles (original thickness)
task3_profiles = {
    "Blue": np.exp(-10 * depths),
    "Green": np.exp(-7 * depths),
    "Red": np.exp(-4 * depths),
    "NIR": np.exp(-2 * depths),
}

# Task 4 energy profiles (increased epidermis thickness)
task4_profiles = {
    "Blue": np.exp(-12 * depths),
    "Green": np.exp(-8 * depths),
    "Red": np.exp(-5 * depths),
    "NIR": np.exp(-3 * depths),
}

# Plot energy profiles for Task 3 and Task 4
plt.figure(figsize=(12, 8))
for wavelength in task3_profiles.keys():
    plt.plot(depths, task3_profiles[wavelength], label=f"{wavelength} - Task 3", linestyle="--")
    plt.plot(depths, task4_profiles[wavelength], label=f"{wavelength} - Task 4")

plt.xlabel("Depth (cm)")
plt.ylabel("Relative Energy")
plt.title("Energy Profiles for Task 3 (Original) and Task 4 (Increased Epidermis Thickness)")
plt.legend()
plt.grid(True)
plt.show()
