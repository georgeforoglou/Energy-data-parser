import requests
import os 
import pandas as pd
import warnings
from datetime import datetime
import plotly.express as px


# Function to check if the date string matches the format YYYYMMDD 
def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%Y%m%d')
        return True
    except ValueError:
        return False

# Function for aggregated data visualization
def data_visualization(target_date, data):
    fig = px.line(data, x='SORT', y='TOTAL_TRADES', 
                    labels={
                            "SORT": "Sort",
                            "TOTAL_TRADES": "Total trades"
                            },
                    title=f'Energy Trades for {target_date}')
    fig.show()

# Function for automated download of the xlsx file
def download_xlsx_file(target_date):
    url = f'https://www.enexgroup.gr/documents/20126/200106/{target_date}_EL-DAM_Results_EN_v01.xlsx'
    response = requests.get(url)

    # Error handling
    if response.status_code == 200:
        filename = f'{target_date}_EL-DAM_Results_ΕΝ_v01.xlsx'
        if not os.path.isfile(filename):
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f'\nFile saved as: {filename}\n')
        else:
            print('\nFile already exists.\n')
    elif response.status_code == 404:
        print('\nFile not found on ENEX for the specified date.')

    elif response.status_code == 400:
        print('\nBad request. Invalid date parameter.')

    else:
        print(f'\nError: HTTP Status Code {response.status_code}')
    return response.status_code

# Function fro data parsing and filtering
def parse_and_filter_data(target_date):
    filename = f'{target_date}_EL-DAM_Results_ΕΝ_v01.xlsx'
    try:
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            # Read xlsx file
            data = pd.read_excel(filename)

        # Filter rows with side "SELL" and classification "IMPORTS"
        filtered_data = data[(data['SIDE_DESCR'] == 'Sell') & (data['CLASSIFICATION'] == 'Imports')].reset_index(drop=True)
        return filtered_data

    except FileNotFoundError:
        print('File not found in folder.')
        return None

    except Exception as e:
        print(f'Error: {str(e)}')
        return None

# Function for data aggregation
def aggregate_data(target_date):
    filename = f'{target_date}_EL-DAM_Results_ΕΝ_v01.xlsx'
    try:
        filtered_data = parse_and_filter_data(target_date)

        # Group by "Sort" and sum the "Total Trades"
        aggregated_data = filtered_data.groupby('SORT')['TOTAL_TRADES'].sum().reset_index()

        # Format data as a list of dictionaries
        aggregated_data_formatted = [{'SORT': sort, 'TOTAL_TRADES': total_trades} for sort, total_trades in zip(aggregated_data['SORT'], aggregated_data['TOTAL_TRADES'])]
        return aggregated_data_formatted
    
    except FileNotFoundError:
        print(f'File not found in folder.')
        return None
    
    except Exception as e:
        print(f'Error: {str(e)}')
        return None