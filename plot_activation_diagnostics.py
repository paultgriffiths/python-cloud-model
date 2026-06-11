import matplotlib.pyplot as plt

cases = ["Original\nPython", "KiD-like"]
ssmax = [0.1604, -0.2454]

plt.figure(figsize=(8,6))
plt.bar(cases, ssmax)
plt.ylabel("Maximum Supersaturation")
plt.title("Activation Diagnostics Comparison")
plt.grid(True, axis="y")
plt.tight_layout()

plt.savefig("Activation_Diagnostics_Comparison.png", dpi=600)

print("Saved Activation_Diagnostics_Comparison.png")
