from flask import Blueprint, request, jsonify
from clickhouse_driver import Client
from app.config import Config
from app.utils import token_required

query_bp = Blueprint('query', __name__)
client = Client(
    host=Config.CLICKHOUSE_HOST,
    user=Config.CLICKHOUSE_USER,
    password=Config.CLICKHOUSE_PASSWORD,
    secure=True,
    verify=False
)


def build_query(filters, aggregates, aggregate_conditions):
    where_clauses = []
    for field, value in filters.items():
        if field == 'Release_date':
            if 'start_date' in value and 'end_date' in value:
                where_clauses.append(f"{field} BETWEEN '{value['start_date']}' AND '{value['end_date']}'")
            elif 'start_date' in value:
                where_clauses.append(f"{field} >= '{value['start_date']}'")
            elif 'end_date' in value:
                where_clauses.append(f"{field} <= '{value['end_date']}'")
            else:
                where_clauses.append(f"{field} = '{value}'")
        elif field in ['Required_age', 'AppID', 'Price', 'DLC_count', 'Positive', 'Negative']:
            where_clauses.append(f"{field} = {value}")
        else:
            where_clauses.append(f"{field} LIKE '%{value}%'")

    query = ""
    if aggregates:
        aggregate_select = ", ".join(aggregates)
        query = f"SELECT {aggregate_select} FROM segwise_game_data_table"
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        if aggregate_conditions:
            query += " HAVING " + " AND ".join(aggregate_conditions)
    else:
        query = "SELECT * FROM segwise_game_data_table"
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

    return query


@query_bp.route('/query', methods=['GET'])
@token_required
def query_data():
    filters = request.args.to_dict()
    aggregates = []
    aggregate_conditions = []
    aggregate_field = filters.pop('aggregate_field', None)
    aggregate_type = filters.pop('aggregate_type', None)
    start_date = filters.pop('start_date', None)
    end_date = filters.pop('end_date', None)

    # Adjust date format for ClickHouse if present
    if start_date or end_date:
        filters['Release_date'] = {}
        if start_date:
            filters['Release_date']['start_date'] = start_date
        if end_date:
            filters['Release_date']['end_date'] = end_date

    # Handle aggregate queries
    if aggregate_field and aggregate_type:
        aggregates.append(f"{aggregate_type}({aggregate_field})")

    query = build_query(filters, aggregates, aggregate_conditions)
    try:
        result = client.execute(query)
        if aggregates:
            return jsonify(result[0][0]), 200
        else:
            return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f"Query execution failed: {str(e)}"}), 500

