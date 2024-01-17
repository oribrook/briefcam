import numpy as np
from abc import ABC, abstractmethod
from matplotlib import pyplot as plt


class Shape(ABC):
    def __init__(self, x0: float) -> None:
        self.x0 = x0

    def __str__(self) -> str:
        return (
            "".join(f"{k}={v} " for k, v in self.__dict__.items())
            .strip()
            .replace(" ", ", ")
        )

    @abstractmethod
    def plot(self, block) -> None:
        pass


class Shape2D(Shape):
    dim = 2

    def __init__(self, x0: float, y0: float) -> None:
        super().__init__(x0)
        self.y0 = y0

    def plot(self, block=True) -> None:
        plt.scatter([self.x0], [self.y0], color="red", marker="o")
        plt.title("Shape2D")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.legend()
        plt.grid(True)
        plt.axis("equal")
        plt.show(block=block)


class Line2D(Shape2D):
    def __init__(self, x0: float, y0: float, slope: float) -> None:
        super().__init__(x0, y0)
        self.slope = slope

    def plot(self, x_range=(-1, 1), block=True, label=None, color="black") -> None:
        start_y = self.y_by_x(x_range[0])
        end_y = self.y_by_x(x_range[1])

        plt.plot(
            [x_range[0], x_range[1]],
            [start_y, end_y],
            color=color,
            label=label if label else "line",
        )

        plt.scatter([self.x0], [self.y0], color="blue", marker="o")
        plt.title(
            f"Line y = {round(self.slope, 2)}x + {round(self.y0 - self.slope * self.x0, 2)}"
        )
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.legend()
        plt.grid(True)
        plt.axis("equal")
        plt.show(block=block)

    def y_by_x(self, x: float) -> float:
        # y = mx + c
        # c = y - mx

        c = self.y0 - self.slope * self.x0
        return self.slope * x + c

    @classmethod
    def create_line_by_points(cls, p1: tuple, p2: tuple) -> Shape:
        slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
        return cls(*p1, slope)


class Circle2D(Shape2D):
    def __init__(self, x0: float, y0: float, radius: float) -> None:
        super().__init__(x0, y0)
        self.radius = radius

    def plot(self, points=100, block=True) -> None:
        theta = np.linspace(0, 2 * np.pi, points)
        x = self.x0 + self.radius * np.cos(theta)
        y = self.y0 + self.radius * np.sin(theta)

        plt.plot(x, y, label="Circle", color="black")
        plt.scatter(self.x0, self.y0, color="pink", marker="o", label="center")
        plt.title(f"Circle center: ({self.x0}, {self.y0}) r: {self.radius}")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.legend()
        plt.grid(True)
        plt.axis("equal")
        plt.show(block=block)


class Shape3D(Shape2D):
    dim = 3

    def __init__(self, x0: float, y0: float, z0: float) -> None:
        super().__init__(x0, y0)
        self.z0 = z0


class Line3D(Shape3D):
    def __init__(
        self, x0: float, y0: float, z0: float, a: float, b: float, c: float
    ) -> None:
        super().__init__(x0, y0, z0)
        self.v = (a, b, c)

    def plot(self, t_range=(-1, 1), block=True):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        t = np.linspace(t_range[0], t_range[1], 2)
        x = self.x0 + self.v[0] * t
        y = self.y0 + self.v[1] * t
        z = self.z0 + self.v[2] * t

        ax.plot(x, y, z, label="Line")

        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_zlabel("Z-axis")
        ax.legend()

        plt.show(block=block)
