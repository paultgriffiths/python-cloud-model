import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 10))

ax.axis("off")

# Box positions
boxes = [
    ("KiD-inspired forcing\nand parcel ascent", 0.5, 0.9),
    ("Supersaturation evolution\n(Sw and Si)", 0.5, 0.72),
    ("Vapour competition\n(R ratio)", 0.5, 0.54),
    ("Liquid and ice evolution\n(qcloud and qice)", 0.5, 0.36),
    ("Bergeron–Findeisen transition", 0.5, 0.18),
]

# Draw boxes
for text, x, y in boxes:

    ax.text(
        x,
        y,
        text,
        ha='center',
        va='center',
        fontsize=12,
        bbox=dict(
            boxstyle="round,pad=0.5",
            edgecolor="black",
            facecolor="white"
        )
    )

# Draw arrows
for i in range(len(boxes) - 1):

    x1, y1 = boxes[i][1], boxes[i][2]
    x2, y2 = boxes[i + 1][1], boxes[i + 1][2]

    ax.annotate(
        "",
        xy=(x2, y2 + 0.06),
        xytext=(x1, y1 - 0.06),
        arrowprops=dict(arrowstyle="->", lw=2)
    )

plt.title(
    "Scientific Workflow of the Mixed-Phase Parcel Model",
    fontsize=14,
    pad=20
)

plt.tight_layout()

plt.savefig(
    "figures/scientific_workflow_summary.png",
    dpi=300
)

plt.show()