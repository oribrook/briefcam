import math
import argparse
import json
from shape import Line2D
from helpers import plot_points_2D, ShapeEnum
import os


class Estimator:
    """
    Estimate a shape bases on a simple RANSAC algorithm implementation as below (for line):
        1. Draw a line between every pair of input-points,
        2. foreach line:
                Check how many points are not more than
                "threshold" distance away from the line.
        3. choose the best fit line as output
    """

    def __init__(self, threshold: float = 0.1) -> None:
        self.threshold = threshold

    def calculate_distance_from_line2d(self, p: tuple, line: Line2D) -> float:
        # distance formula:
        # d = | (mx0 - y0 + c) / sqrt(m^2+1) |

        c = line.y0 - line.slope * line.x0
        return abs((line.slope * p[0] - p[1] + c) / (math.sqrt(line.slope**2 + 1)))

    def estimate_line2D(self, points: list) -> Line2D:
        max_num_inliers_points = -1
        best_fit_line = None
        for p1 in points:
            for p2 in points:
                if p1 == p2:
                    continue

                num_inlier_points = 0
                line = Line2D.create_line_by_points(p1, p2)
                for p in points:
                    if self.calculate_distance_from_line2d(p, line) < self.threshold:
                        num_inlier_points += 1

                if num_inlier_points > max_num_inliers_points:
                    max_num_inliers_points = num_inlier_points
                    best_fit_line = line

        return best_fit_line


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input_path", type=str, required=True, help="Path to the config file"
    )
    parser.add_argument(
        "--output_path", type=str, required=True, help="Path to the output file"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    return parser.parse_args()


def load_data(path: str) -> dict:
    with open(path, "r") as file:
        data = json.load(file)

    return data


def save_output(data: dict, path: str) -> None:
    with open(path, "w") as file:
        file.write(json.dumps(data))


def validate_input(shapes):
    assert type(shapes) == list, f"Input file should contains list. got: {type(shapes)}"
    for s in shapes:
        assert "shape_type" in s, f"shape {s} is missing 'shape_type' entry"
        assert "shape_params" in s, f"shape {s} is missing 'shape_params' entry"
        assert "inlier_points" in s, f"shape {s} is missing 'inlier_points' entry"
        assert "outlier_points" in s, f"shape {s} is missing 'outlier_points' entry"

        # todo: add validators for the values of the above keys


def main(input_path: str, output_path: str, debug: bool) -> None:
    assert os.path.isfile(input_path), "arg:input_path isn't a file."
    json_shapes = load_data(input_path)
    validate_input(json_shapes)
    estimator = Estimator()

    output_to_be_saved = {}
    for j_shape in json_shapes:
        if j_shape["shape_type"] != ShapeEnum.Line2D:
            print(
                f"\nWARNING: Estimator implemented only for Line2D shape. skipping {j_shape['shape_type']}\n"
            )
            continue

        line = Line2D(**j_shape["shape_params"])
        all_points = j_shape["inlier_points"] + j_shape["outlier_points"]
        estimated_line = estimator.estimate_line2D(all_points)
        output_to_be_saved[str(line)] = estimated_line.__dict__

        if debug:
            print(
                f"Estimator slope: {round(estimated_line.slope, 3)}. real slope: {line.slope}"
            )
            line.plot(
                block=False,
                color="black",
                label="real line",
                x_range=(min(p[0] for p in all_points), max(p[0] for p in all_points)),
            )
            estimated_line.plot(
                block=False,
                x_range=(min(p[0] for p in all_points), max(p[0] for p in all_points)),
                color="orange",
                label="estimated line",
            )
            plot_points_2D(
                inliers=j_shape["inlier_points"], outliers=j_shape["outlier_points"]
            )

    save_output(data=output_to_be_saved, path=output_path)


if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_path, args.output_path, args.debug)
