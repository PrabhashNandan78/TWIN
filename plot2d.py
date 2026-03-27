import matplotlib.pyplot as plt
import matplotlib.lines as mlines


def plot_farm(encoded_plants, title="Farm Digital Twin"):
    xs = [p["x"] for p in encoded_plants]
    ys = [p["y"] for p in encoded_plants]
    sizes = [p["size"] * 1200 for p in encoded_plants]  # ✅ FIX
    colors = [p["color"] for p in encoded_plants]

    plt.figure(figsize=(6, 6))
    plt.scatter(xs, ys, s=sizes, c=colors, alpha=0.85)

    plt.xlabel("X position (m)")
    plt.ylabel("Y position (m)")
    plt.title(title)
    plt.grid(True)
    plt.axis("equal")

    # Optional legend
    green = mlines.Line2D([], [], color='green', marker='o',
                          linestyle='None', markersize=10, label='Low stress')
    red = mlines.Line2D([], [], color='red', marker='o',
                        linestyle='None', markersize=10, label='High stress')
    plt.legend(handles=[green, red], loc='upper right')

    plt.show()
