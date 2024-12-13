import pandas as pd
import os

def transform_adp_data(file_path):
    """
    Transform an ADP CSV file by combining position-specific ranking columns.

    Args:
        file_path (str): Path to the ADP CSV file.

    Returns:
        pd.DataFrame: Transformed DataFrame with combined rankings and position data.
    """
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Melt the WR, RB, TE, and QB columns to create a single 'Rank' column
    df_melted = df.melt(
        id_vars=['Player Team (Bye)', 'Position', 'Scoring'],  # Columns to keep as identifiers
        value_vars=['WR', 'RB', 'TE', 'QB'],                      # Columns to combine
        var_name='Original Position',                             # New column for the original position (WR, RB, TE, QB)
        value_name='Rank'                                         # New column for the combined rank
    )

    # Drop rows where the Rank is missing (NaN)
    df_melted.dropna(subset=['Rank'], inplace=True)

    # Convert the Rank to integers (if applicable)
    df_melted['Rank'] = df_melted['Rank'].astype(int)

    # Return the transformed DataFrame
    return df_melted

def process_all_files(input_folder, output_file):
    """
    Process all ADP files in the input folder and combine them into a single DataFrame.

    Args:
        input_folder (str): Path to the folder containing the ADP CSV files.
        output_file (str): Path to save the combined transformed CSV file.
    """
    # List of ADP files for different formats
    adp_files = ['standard_adp.csv', 'half-ppr_adp.csv', 'ppr_adp.csv']

    # List to store the transformed DataFrames
    all_data = []

    for file in adp_files:
        file_path = os.path.join(input_folder, file)
        print(f"Processing file: {file_path}")
        transformed_df = transform_adp_data(file_path)
        # Append the transformed DataFrame to the list
        all_data.append(transformed_df)

    # Combine all transformed DataFrames
    combined_df = pd.concat(all_data, ignore_index=True)

    # Save the combined DataFrame to a CSV file
    combined_df.to_csv(output_file, index=False)
    print(f"Combined ADP data saved to '{output_file}'")

# Paths
input_folder = 'data/adp'
output_file = 'data/combined_transformed_adp.csv'

# Process all files and save the result
process_all_files(input_folder, output_file)