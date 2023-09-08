from flask import Flask, request, jsonify
import mysql.connector
import time

app = Flask(__name__)
# truncate `uuids`;
# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="zeroweb"
)
cursor = db.cursor()

@app.route('/<uuid>', methods=['GET'])
def get_single_uuid(uuid):
    local_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="zeroweb"
    )
    local_cursor = local_db.cursor()
    try:
        print("SELECT uuid FROM uuids WHERE uuid =" + uuid)
        local_cursor.execute("SELECT uuid FROM uuids WHERE uuid = %s", (uuid,))
        result = local_cursor.fetchone()
        if result:
            return jsonify({'uuid': result[0]}), 200
        else:
            return jsonify({'message': 'UUID not found'}), 404
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'message': 'Database error'}), 500
    local_db.close()
    
@app.route('/<uuid>', methods=['POST'])
def post_single_uuid(uuid):
    local_cursor = db.cursor()
    data = request.json['data']
    received_uuid = data['uuid']
    try:
        local_cursor.execute("INSERT INTO uuids (uuid) VALUES (%s)", (received_uuid,))
        db.commit()

        if local_cursor.rowcount > 0:
            return jsonify({'code': 200, 'message': 'Successfully updated UUIDs'}), 200
        else:
            return jsonify({'message': 'UUID not inserted'}), 404
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'message': 'Database error'}), 500

if __name__ == '__main__':
    app.run(port=5001)
