import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def fetch_fantasy_data(position, scoring):
    """
    Fetch fantasy data for a specific position and scoring setting from FantasyPros.

    Args:
        position (str): The position to fetch ('wr', 'rb', 'qb', 'te').
        scoring (str): The scoring setting ('standard', 'half-ppr', 'ppr').

    Returns:
        pd.DataFrame: DataFrame containing the fetched fantasy data.
    """
    # URL template
    url = f"https://www.fantasypros.com/nfl/stats/{position}.php?scoring={scoring}"
    print(f"Fetching data for Position: {position.upper()}, Scoring: {scoring}")

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
        print(f"Successfully fetched data for {position.upper()} ({scoring}).")
        return df
    except Exception as e:
        print(f"Error parsing table for {position.upper()} ({scoring}): {e}")
        return None

def save_data(df, position, scoring):
    """
    Save the DataFrame to a CSV file in a structured folder.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        position (str): The position ('wr', 'rb', 'qb', 'te').
        scoring (str): The scoring setting ('standard', 'half-ppr', 'ppr').
    """
    # Create the 'data' folder if it doesn't exist
    os.makedirs('data', exist_ok=True)

    # Define the filename
    filename = f"data/{position}_{scoring}_fantasy_stats.csv"

    # Save the DataFrame to CSV
    df.to_csv(filename, index=False)
    print(f"Data saved to '{filename}'")

def main():
    positions = ['wr', 'rb', 'qb', 'te']
    scorings = ['standard', 'half-ppr', 'ppr']

    for scoring in scorings:
        for position in positions:
            # Fetch the data
            df = fetch_fantasy_data(position, scoring)
            if df is not None:
                # Save the data to a CSV file
                save_data(df, position, scoring)
            # Be respectful and wait to avoid getting blocked
            time.sleep(3)

if __name__ == "__main__":
    main()