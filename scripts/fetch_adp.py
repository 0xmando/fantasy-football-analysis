import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def fetch_adp_data(position, scoring):
    """
    Fetch ADP data for a specific position and scoring setting from FantasyPros.

    Args:
        position (str): The position to fetch ('wr', 'rb', 'qb', 'te').
        scoring (str): The scoring setting ('standard', 'half-ppr', 'ppr').

    Returns:
        pd.DataFrame: DataFrame containing the fetched ADP data.
    """
    # Determine the URL based on the scoring format
    if position == 'qb':
        url = f"https://www.fantasypros.com/nfl/adp/qb.php" #Single URL for QB data
    elif scoring == 'standard':
        url = f"https://www.fantasypros.com/nfl/adp/{position}.php"
    elif scoring == 'half-ppr':
        url = f"https://www.fantasypros.com/nfl/adp/half-point-ppr-{position}.php"
    elif scoring == 'ppr':
        url = f"https://www.fantasypros.com/nfl/adp/ppr-{position}.php"
    else:
        print(f"Invalid scoring format: {scoring}")
        return None

    print(f"Fetching ADP data for Position: {position.upper()}, Scoring: {scoring}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Send the request
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data for {position.upper()} ({scoring}). Status Code: {response.status_code}")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')

    if table is None:
        print(f"No table found for {position.upper()} ({scoring}).")
        return None

    # Use pandas to read the HTML table
    try:
        df = pd.read_html(str(table))[0]
        df['Position'] = position.upper()
        df['Scoring'] = scoring
        print(f"Successfully fetched ADP data for {position.upper()} ({scoring}).")
        return df
    except Exception as e:
        print(f"Error parsing table for {position.upper()} ({scoring}): {e}")
        return None

def save_data(df, scoring):
    """
    Save the combined DataFrame to a CSV file in a structured folder.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        scoring (str): The scoring setting ('standard', 'half-ppr', 'ppr').
    """
    # Create the 'data/adp' folder if it doesn't exist
    os.makedirs('data/adp', exist_ok=True)

    # Define the filename
    filename = f"data/adp/{scoring}_adp.csv"

    # Save the DataFrame to CSV
    df.to_csv(filename, index=False)
    print(f"ADP data saved to '{filename}'")

def main():
    positions = ['qb', 'rb', 'wr', 'te']
    scorings = ['standard', 'half-ppr', 'ppr']

    for scoring in scorings:
        all_data = []
        for position in positions:
            # Fetch the data for each position
            df = fetch_adp_data(position, scoring)
            if df is not None:
                all_data.append(df)
            # Be respectful and wait to avoid getting blocked
            time.sleep(3)

        # Combine all positions into a single DataFrame for the scoring format
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            save_data(combined_df, scoring)
        else:
            print(f"No data fetched for scoring format: {scoring}")

if __name__ == "__main__":
    main()