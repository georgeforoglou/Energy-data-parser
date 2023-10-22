from flask import Flask, request, jsonify
import logging
from Parser import *
import plotly.express as px


app = Flask(__name__)

# Create a custom logger
logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

# Create a file handler and set a logging format
file_handler = logging.FileHandler('api.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

@app.route('/api/energy-data', methods=['GET'])
def get_energy_data():
    # Get the target date from the query parameter 
    target_date = request.args.get('date')

    # Validate the date
    if not is_valid_date(target_date):
        logger.error('Invalid date format or date is out of range')
        return jsonify('Invalid date format or date is out of range'), 400

    # Download data, filter and aggregate
    status = download_xlsx_file(target_date=target_date)
    aggregated_data = aggregate_data(target_date)

    # Return the aggregated data in JSON format
    if aggregated_data is not None:
        data_visualization(target_date, aggregated_data)
        logger.info('Data fetched and aggregated successfully')
        return jsonify(aggregated_data), status
    else:
        if status == 404:
            logger.warning('File not found on ENEX for the specified date.')
            return jsonify('File not found on ENEX for the specified date.'), status
        elif status == 400:
            logger.warning('Bad request. Invalid date parameter.')
            return jsonify('Bad request. Invalid date parameter.'), status
        else:
            logger.error(f'Error: HTTP Status Code {status}')
            return jsonify(f'Error: HTTP Status Code {status}'), status

if __name__ == '__main__':
    app.run(debug=True)
