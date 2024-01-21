import argparse
import random
import json
from helpers import plot_points_2D, ShapeEnum
from shape import Line2D, Circle2D, Shape
import numpy as np
import os


class Generator:
    def __init__(self, config: dict) -> None:
        self.validate_config(config)
        self.config = config

    @classmethod
    def validate_config(cls, config):
        assert type(config) == dict, f"Config type should be dict. (got {type(config)})"

        for shape_type in [
            "shapes",
            "num_points",
            "randomness",
            "radius_range",
            "coordinate_range",
            "slope_range",
            "outlier_range",
        ]:
            assert shape_type in config, f"Config is missing {shape_type} entry"

        for shape_type, amount in config["shapes"].items():
            assert shape_type in ShapeEnum.__dict__, f"Unknown shape: {amount}"
            assert type(amount) in [
                float,
                int,
            ], f"Requested amount for {shape_type} ({amount}) isn't numeric."
            assert int(amount) == float(
                amount
            ), f"Amount for {shape_type} should be int. got: {amount}"

        assert type(config["num_points"]) == int, f"config.num_points isn't int"
        assert float(config["num_points"]) >= 0, f"config.num_points isn't positive"
        assert type(config["randomness"]) in [
            float,
            int,
        ], f"config.randomness isn't numeric. got: {config['randomness']}"
        assert (
            0 <= float(config["randomness"]) <= 1
        ), f"config.randomness should be in range [0-1]. got: {config['randomness']}"

        for range_entry in [
            "radius_range",
            "coordinate_range",
            "slope_range",
            "outlier_range",
        ]:
            assert type(config[range_entry]) == list, f"Config.{range_entry} should be list"
            assert len(config[range_entry]) == 2, f"Config.{range_entry} length should be 2"
            for item in config[range_entry]:
                assert type(item) in [
                    float,
                    int,
                ], f"Config.{range_entry} values aren't numeric"

    def generate_shapes(self) -> list:
        shapes = []
        for shape_type, num in self.config["shapes"].items():
            for _ in range(num):
                x0 = random.uniform(
                    self.config["coordinate_range"][0],
                    self.config["coordinate_range"][1],
                )
                y0 = random.uniform(
                    self.config["coordinate_range"][0],
                    self.config["coordinate_range"][1],
                )

                if shape_type == ShapeEnum.Line2D:
                    slope = random.uniform(
                        self.config["slope_range"][0], self.config["slope_range"][1]
                    )
                    shapes.append(Line2D(x0, y0, slope))
                elif shape_type == ShapeEnum.Circle2D:
                    radius = random.uniform(
                        self.config["radius_range"][0], self.config["radius_range"][1]
                    )
                    shapes.append(Circle2D(x0, y0, radius))
                else:
                    raise (f"Not implemented (or unknown) config-shape: {shape_type}")

        return shapes

    def generate_outliers(self, dim: int) -> list:
        res = []
        for _ in range(int(self.config["num_points"] * 0.2)):
            new_point = []
            for _ in range(dim):
                new_point.append(
                    random.uniform(
                        self.config["outlier_range"][0], self.config["outlier_range"][1]
                    )
                )
            res.append(tuple(new_point))

        return res

    def generate_inliers(self, shape: Shape) -> list:
        num_points = int(self.config["num_points"] * 0.8)
        randomness = self.config["randomness"]

        inlier_points = []
        if shape.__class__.__name__ == ShapeEnum.Line2D:
            rand_factor = (
                self.config["coordinate_range"][1] - self.config["coordinate_range"][0]
            )

            for x in np.linspace(
                self.config["coordinate_range"][0],
                self.config["coordinate_range"][1],
                num_points,
            ):
                y = (
                    shape.y_by_x(x)
                    + random.uniform(-randomness, randomness) * rand_factor
                )
                x = x + random.uniform(-randomness, randomness) * rand_factor
                inlier_points.append((x, y))

        elif shape.__class__.__name__ == ShapeEnum.Circle2D:
            for theta in np.linspace(0, 2 * np.pi, num_points):
                x = (
                    shape.x0
                    + shape.radius * np.cos(theta)
                    + random.uniform(-randomness, randomness) * shape.radius
                )
                y = (
                    shape.y0
                    + shape.radius * np.sin(theta)
                    + random.uniform(-randomness, randomness) * shape.radius
                )
                inlier_points.append((x, y))
        else:
            raise (f"Not implemented generator for shape: {shape.__class__.__name__}")

        return inlier_points


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config_file", type=str, required=True, help="Path to the config file"
    )
    parser.add_argument(
        "--output_path", type=str, required=True, help="Path to the output file"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    return parser.parse_args()


def load_config(path):
    with open(path, "r") as file:
        config = json.load(file)

    if "radius_range" not in config:
        config["radius_range"] = [0.5, 3]
    if "coordinate_range" not in config:
        config["coordinate_range"] = [-1, 1]
    if "slope_range" not in config:
        config["slope_range"] = [-4, 4]
    if "outlier_range" not in config:
        config["outlier_range"] = [-8, 8]

    return config


def save_output(data, path):
    with open(path, "w") as file:
        file.write(json.dumps(data))


def main(config_file: str, output_path: str, debug: bool) -> None:
    assert os.path.isfile(config_file), "arg:config_file isn't a file."
    config = load_config(path=config_file)
    Generator.validate_config(config)
    generator = Generator(config=config)
    shapes = generator.generate_shapes()

    output_to_be_saved = []
    for s in shapes:
        outlier_points = generator.generate_outliers(s.dim)
        inliers_points = generator.generate_inliers(shape=s)

        output_to_be_saved.append(
            {
                "shape_type": s.__class__.__name__,
                "shape_params": s.__dict__,
                "inlier_points": inliers_points,
                "outlier_points": outlier_points,
            }
        )

        if debug:
            s.plot(block=False)
            plot_points_2D(outliers=outlier_points, inliers=inliers_points)

    save_output(data=output_to_be_saved, path=output_path)


if __name__ == "__main__":
    args = parse_arguments()
    main(args.config_file, args.output_path, args.debug)
