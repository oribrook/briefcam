from matplotlib import pyplot as plt


class ShapeEnum:
    Line2D = "Line2D"
    Circle2D = "Circle2D"
    Line3D = "Line3D"


def plot_points_2D(inliers: list, outliers: list) -> None:
    for dot in inliers:
        plt.scatter([dot[0]], [dot[1]], color="green", marker="o")

    for dot in outliers:
        plt.scatter([dot[0]], [dot[1]], color="red", marker="o")

    plt.grid(True)
    plt.axis("equal")
    plt.show()
