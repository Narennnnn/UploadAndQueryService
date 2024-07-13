import csv
import os
import requests
from clickhouse_driver import Client
from dateutil import parser
import logging
from tempfile import NamedTemporaryFile
from flask import Blueprint, jsonify, request
from concurrent.futures import ThreadPoolExecutor, as_completed
from app import Config
from app.utils import token_required

main_bp = Blueprint('main', __name__)
client = Client(
    host=Config.CLICKHOUSE_HOST,
    user=Config.CLICKHOUSE_USER,
    password=Config.CLICKHOUSE_PASSWORD,
    secure=True,
    verify=False,
    settings={
        'async_insert': 1,
        'wait_for_async_insert': 1
    }
)

create_table_query = """
CREATE TABLE IF NOT EXISTS insert_bulk_game_data (
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

create_buffer_table_query = """
CREATE TABLE IF NOT EXISTS insert_bulk_game_data_buffer (
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
) ENGINE = Buffer(default, insert_bulk_game_data, 16, 10, 60, 100000, 1000000, 10000000, 100000000);
"""

def create_tables():
    try:
        client.execute(create_table_query)
        client.execute(create_buffer_table_query)
        print("Tables created or verified successfully.")
    except Exception as e:
        print(f"Failed to create or verify the tables: {str(e)}")

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

def process_batch(rows):
    local_client = Client(
        host=Config.CLICKHOUSE_HOST,
        user=Config.CLICKHOUSE_USER,
        password=Config.CLICKHOUSE_PASSWORD,
        secure=True,
        verify=False
    )
    try:
        local_client.execute('INSERT INTO insert_bulk_game_data_buffer VALUES', rows)
        print(f"Processed batch with {len(rows)} rows.")
    except Exception as e:
        print(f"Failed to upload batch to ClickHouse: {str(e)}")
    finally:
        local_client.disconnect()

def upload_csv_to_clickhouse(csv_file_path):
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            rows = []
            batch_size = 50000
            with ThreadPoolExecutor(max_workers=4) as executor:  # Use 4 threads for parallel processing
                futures = []
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

                    if len(rows) >= batch_size:
                        futures.append(executor.submit(process_batch, rows))
                        rows = []

                if rows:
                    futures.append(executor.submit(process_batch, rows))

                for future in as_completed(futures):
                    future.result()  # Raise any exceptions that occurred

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
            create_tables()
            upload_csv_to_clickhouse(csv_file_path)
            delete_local_csv(csv_file_path)
            return jsonify({'message': 'CSV upload and processing completed.'}), 200
        else:
            return jsonify({'message': 'Failed to download CSV file from provided URL.'}), 400
    except Exception as e:
        logging.error(f"Failed to process CSV upload: {str(e)}")
        return jsonify({'message': 'Internal server error while processing CSV upload.'}), 500
'''
Creating two tables in this context is an optional optimization step. Here's why it's done:

Main Table and Buffer Table
1. Main Table (insert_bulk_game_data): This is the primary table where your data will be stored for querying and analysis.
    It is designed with the appropriate schema and order by clause for efficient storage and retrieval.
2. Buffer Table (insert_bulk_game_data_buffer): This is an auxiliary table that acts as an intermediate buffer for data inserts.
    The purpose of this table is to handle high-frequency inserts efficiently. Data is initially inserted into this buffer table and periodically flushed into the main table.

Reasons for Using a Buffer Table
Batch Inserts: ClickHouse is optimized for batch inserts. By using a buffer table, you can accumulate small, frequent inserts into larger batches before moving them to the main table.
Performance Improvement: Insert operations are less costly when they are batched. This reduces the overhead associated with each insert operation.
Improved Concurrency: The buffer table can handle concurrent inserts better by buffering them and then performing a single bulk insert into the main table.

First approach took neary 12 mins and this particular approach took around 13.6 mins to upload completely to ClickHouse
'''