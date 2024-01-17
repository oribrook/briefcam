====================================================================================================
USAGE:
 
RUN:
  pip install -r requirements.txt
  generator.py --config_file config_file_path --output_path output_file_path [--debug]  
  estimator.py --input_path generator_output_file_path --output_path output_file_path [--debug]

  * For convenience you can use the default config_file from project files: "config.json"
====================================================================================================

INFO:
  output format:
        Generator:
            json file with: 
                [shape_data1, shape_data2 ..]
                    each shape_data has keys: 
                        {shape_type, 
                        shape_params, 
                        inlier_points, 
                        outlier_points}                        
        Estimator:                        
            json file with: 
                {shape1_str: {estimated_shape1_params}, shape2_str: {..}, ..}
                Example, for Line2d:
                    {"x0=0.08, y0=-0.4, slope=-1.62": {"x0": -1.02, "y0": 1.18, "slope": -1.73},
                    "x0=0.48, y0=0.5,  slope=1.12":  {"x0":  0.2,  "y0": 0.18, "slope": 1.2},}

NOTES:

    1. I added few more config settings:
            radius_range: for circle-radius random-range
            coordinate_range: for x0, y0, z0 random-range.
                      For Lines it determines the scope for inlier points (line length).

            slope_range: for line2D slope random-range
            outlier_range: for outlier points random-range. 

        If the above entries aren't provided by the config file, the generator 
        will use the following default values:
            "radius_range": [0.5, 3],
            "coordinate_range": [-1, 1],
            "slope_range": [-4, 4],
            "outlier_range": [-8, 8]    

    2. I defined the inlier-noise to be:
       For Line: rand(randomness) * (coordinate_range[1] - coordinate_range[0])
       For Circle: rand(randomness) * radius

    3. Due to time constrains, I decided to implement the estimator only for a Line2D.
       So the algorithm knows that the shape is a line, and only needs to estimate the parameters.
