#!/usr/bin/env python3
"""
Convert VoxelSLAM trajectory (alidarState.txt) to TUM format for EVO evaluation
Usage: python3 convert_to_tum.py /path/to/alidarState.txt
"""

import os
import sys
import numpy as np

def convert_to_tum(input_file, output_file=None):
    """
    Convert VoxelSLAM trajectory to TUM format.
    Input format:
        timestamp x y z qx qy qz qw vx vy vz bgx bgy bgz bax bay baz gx gy gz v6_1 v6_2 v6_3 v6_4 v6_5 v6_6
    Output format (TUM):
        timestamp tx ty tz qx qy qz qw
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist.")
        return False
    
    # If output file not specified, create it in the same directory with _tum suffix
    if output_file is None:
        dir_name = os.path.dirname(input_file)
        base_name = os.path.basename(input_file)
        name_without_ext = os.path.splitext(base_name)[0]
        output_file = os.path.join(dir_name, f"{name_without_ext}_tum.txt")
    
    try:
        with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
            # Write header as comment
            f_out.write("# timestamp tx ty tz qx qy qz qw\n")
            
            line_count = 0
            for line in f_in:
                data = line.strip().split()
                if len(data) < 8:  # Need at least timestamp, position, quaternion
                    print(f"Warning: Line {line_count + 1} has insufficient data, skipping.")
                    continue
                
                # Extract timestamp, position, quaternion
                timestamp = data[0]
                tx, ty, tz = data[1:4]
                qx, qy, qz, qw = data[4:8]
                
                # Write in TUM format
                f_out.write(f"{timestamp} {tx} {ty} {tz} {qx} {qy} {qz} {qw}\n")
                line_count += 1
        
        print(f"Conversion successful! Converted {line_count} poses.")
        print(f"TUM format trajectory saved to: {output_file}")
        return True
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 convert_to_tum.py /path/to/alidarState.txt [/path/to/output.txt]")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    convert_to_tum(input_file, output_file)

if __name__ == "__main__":
    main()
