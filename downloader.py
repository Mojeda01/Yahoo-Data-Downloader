import requests
import os
import pandas as pd
import time

def download_stock_data(stock_symbol, start_date, end_date, retries=3, delay=10):
    # Convert dates to unix timestamps
    start_timestamp = int(pd.Timestamp(start_date).timestamp())
    end_timestamp = int(pd.Timestamp(end_date).timestamp())

    # Construct the Yahoo Finance query URL
    query_url = f"https://query1.finance.yahoo.com/v7/finance/download/{stock_symbol}?period1={start_timestamp}&period2={end_timestamp}&interval=1d&events=history"

    attempt = 0
    while attempt < retries:
        # Send the request and download the CSV
        response = requests.get(query_url)

        # Check if the respons indicates "Too Many Requests"
        if response.status_code == 200:
            # Save the CSV file to the current working dir
            file_name = f"{stock_symbol}_data.csv"
            file_path = os.path.join(os.getcwd(), file_name)

            with open(file_path, "wb") as file:
                file.write(response.content)

            print(f"Data saved to: {file_path}")
            return file_path

        elif response.status_code == 429: # Too many requests
            print(f"Too many requests. Retrying in {delay} seconds...")
            time.sleep(delay) # wait before retrying
            attempt += 1
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            return None

    print("Max tries reached. Could not retreive data")
    return None
    
# Example usage
if __name__ == "__main__":
    stock_symbol = "AAPL" # Example: AAPL for Apple
    start_date = "2020-01-01" # Example start date
    end_date = "2024-09-26" # Example end date
    download_stock_data(stock_symbol, start_date, end_date)
