import matplotlib.pyplot as plt

# ---- Data (from your COMPACT COMPARISON output) ----
rows = [
    ["0.5", "1.023e-03", "8.279e-04", "5.356e-04", "Stable"],
    ["1.0", "6.818e-04", "4.869e-04", "1.947e-04", "Stable"],
    ["2.0", "2.220e-16", "-1.835e-04", "-2.127e-04", "Unstable (negative S)"],
]

columns = ["dt (s)", "Peak S (0)", "Peak S (3000)", "Peak S (10000)", "Numerical behaviour"]

# ---- Create figure and table ----
fig, ax = plt.subplots(figsize=(9, 2.2), dpi=150)
ax.axis("off")

table = ax.table(
    cellText=rows,
    colLabels=columns,
    loc="center",
    cellLoc="center",
)

# ---- Styling ----
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.4)

# ---- Save as image ----
plt.tight_layout()
plt.savefig("dt_sensitivity_table.png", dpi=300)
plt.show()
