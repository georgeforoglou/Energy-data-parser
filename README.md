# Energy Data Parsing and Aggregation API Documentation

**Introduction**
The Energy Data Parsing and Aggregation API is a RESTful service designed to fetch, parse, and aggregate energy trade data from a specified XLSX file published on the enexgroup website. This documentation outlines the usage of the API and provides details on the available endpoints and functionality.

Table of Contents
1. Getting Started
2. Computation Functions
3. API Endpoints
3.1. Fetch Energy Data
4. Error Handling
5. Examples

**1. Getting Started:**
To get started with the Energy Data Parsing and Aggregation API, you need to have Python installed on your system, along with the required libraries specified in the requirements.txt.

**2. Computation Functions:**
The API includes several computation functions that perform essential tasks. These functions are responsible for data retrieval, parsing, filtering, aggregation, and visualization.

**3. API Endpoints:**
The API provides the following endpoint for interacting with energy trade data:
Endpoint: http://localhost:5000/api/energy-data?date=YYYYMMDD
Method: GET
Parameters:
date (query parameter): The target date for which you want to retrieve energy trade data in the format YYYYMMDD.
