import pandas as pd
import sys

def transform_data(input_file, output_file):
    # Read the data
    data = pd.read_csv(input_file)
    
    # Unpivot the data
    melted_data = pd.melt(data, id_vars=["profile_id"], 
                          value_vars=data.columns[1:],
                          var_name="Response Option",
                          value_name="Selected")
    
    # Save the transformed data to the output file
    melted_data.to_csv(output_file, index=False)
    print(f"Data transformed and saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python transform_script.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    transform_data(input_file, output_file)
