import csv
import os
import requests
from clickhouse_driver import Client
from dateutil import parser
import logging
from tempfile import NamedTemporaryFile
from flask import Blueprint, jsonify, request
from app import Config
from app.utils import token_required

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

main_bp = Blueprint('main', __name__)
client = Client(
    host=Config.CLICKHOUSE_HOST,
    user=Config.CLICKHOUSE_USER,
    password=Config.CLICKHOUSE_PASSWORD,
    secure=True,
    verify=False
)

create_table_query = """
CREATE TABLE IF NOT EXISTS segwise_game_data_table (
    s_no Int32,
    AppID Int32,
    Name String,
    Release_date Date,
    Required_age Int32,
    Price Float64,
    DLC_count Int32,
    About_the_game String,
    Supported_languages Array(String),
    Windows Bool,
    Mac Bool,
    Linux Bool,
    Positive Int32,
    Negative Int32,
    Developers String,
    Publishers String,
    Categories String,
    Genres String,
    Tags String
) ENGINE = MergeTree()
ORDER BY AppID;
"""

client.execute(create_table_query)

def parse_date(date_str):
    try:
        return parser.parse(date_str).date()
    except ValueError:
        return None

def download_csv_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Create a temporary file to save the downloaded content
            with NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
                tmp_file.write(response.content)
                tmp_file_path = tmp_file.name
            return tmp_file_path
        else:
            print(f"Failed to download CSV file from {url}: Status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Failed to download CSV file from {url}: {str(e)}")
        return None

def upload_csv_to_clickhouse(csv_file_path):
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)

            rows = []
            for index, row in enumerate(csv_reader, start=1):
                rows.append({
                    's_no': int(index),
                    'AppID': int(row['AppID']),
                    'Name': row['Name'],
                    'Release_date': parse_date(row['Release date']),
                    'Required_age': int(row['Required age']),
                    'Price': float(row['Price']),
                    'DLC_count': int(row['DLC count']),
                    'About_the_game': row['About the game'],
                    'Supported_languages': eval(row['Supported languages']),
                    'Windows': row['Windows'].lower() == 'true',
                    'Mac': row['Mac'].lower() == 'true',
                    'Linux': row['Linux'].lower() == 'true',
                    'Positive': int(row['Positive']),
                    'Negative': int(row['Negative']),
                    'Developers': row['Developers'],
                    'Publishers': row['Publishers'],
                    'Categories': row['Categories'],
                    'Genres': row['Genres'],
                    'Tags': row['Tags']
                })

            # Batch insert rows
            client.execute(
                'INSERT INTO segwise_game_data_table VALUES',
                rows
            )

        print("Data loaded successfully")
    except Exception as e:
        print(f"Failed to upload CSV file to ClickHouse: {str(e)}")

def delete_local_csv(csv_file_path):
    try:
        os.remove(csv_file_path)
        print(f"Deleted local CSV file: {csv_file_path}")
    except Exception as e:
        print(f"Failed to delete local CSV file: {str(e)}")

@main_bp.route('/upload_csv', methods=['POST'])
@token_required
def handle_upload_csv():
    try:
        data = request.get_json()
        csv_url = data.get('csv_url')
        csv_file_path = download_csv_from_url(csv_url)
        if csv_file_path:
            upload_csv_to_clickhouse(csv_file_path)
            delete_local_csv(csv_file_path)
            return jsonify({'message': 'CSV upload and processing completed.'}), 200
        else:
            return jsonify({'message': 'Failed to download CSV file from provided URL.'}), 400
    except Exception as e:
        logging.error(f"Failed to process CSV upload: {str(e)}")
        return jsonify({'message': 'Internal server error while processing CSV upload.'}), 500
