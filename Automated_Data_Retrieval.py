import requests
import os 

# Function for automated download of the xlsx file
def download_xlsx_file(target_date):
    url = f'https://www.enexgroup.gr/documents/20126/200106/{target_date}_EL-DAM_Results_EN_v01.xlsx'
    
    response = requests.get(url)
    
    # Error handling
    if response.status_code == 200:
        filename = f'{target_date}_EL-DAM_Results_ΕΝ_v01.xlsx'
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f'File saved as: {filename}')
    elif response.status_code == 404:
        print('File not found for the specified date.')
    elif response.status_code == 400:
        print('Bad request. Invalid date parameter.')
    else:
        print(f'Error: HTTP Status Code {response.status_code}')


if __name__ == "__main__":
    # Get the targeted date
    target_date = input("Enter the target date (YYYYMMDD): ")
    download_xlsx_file(target_date)

    

