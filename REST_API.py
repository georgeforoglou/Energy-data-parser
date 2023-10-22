from flask import Flask, request, jsonify
from Parser import *
import plotly.express as px


app = Flask(__name__)

@app.route('/api/energy-data', methods=['GET'])
def get_energy_data():
    # Get the target date from the query parameter
    target_date = request.args.get('date')

    # Validate the date
    if not is_valid_date(target_date):
        return jsonify('Invalid date format or date is out of range'), 400

    # Download data, filter and aggregate
    status = download_xlsx_file(target_date=target_date)
    aggregated_data = aggregate_data(target_date)

    # Return the aggregated data in JSON format
    if aggregated_data is not None:
        data_visualization(target_date, aggregated_data)

        return jsonify(aggregated_data), status
    else:
        if status == 404:
            return jsonify('File not found on ENEX for the specified date.'), status
        elif status == 400:
            return jsonify('Bad request. Invalid date parameter.'), status
        else:
            return jsonify(f'Error: HTTP Status Code {status}'), status

if __name__ == '__main__':
    app.run(debug=True)
