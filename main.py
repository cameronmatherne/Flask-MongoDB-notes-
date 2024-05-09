from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['460_demonstration']
collection = db['note']



@app.route('/')
def index():
    # find method to read from collection
    records = list(collection.find().sort("timestamp", -1))
    return render_template('index.html', records=records)


@app.route('/create', methods=['POST'])
def create_record():
    data = request.get_json()
    data['timestamp'] = datetime.utcnow()
    # insert_one method to create data
    collection.insert_one(data)
    return jsonify({"message": "Record created successfully"}), 201


@app.route('/update/<string:item_id>', methods=['POST'])
def update_record(item_id):
    data = request.get_json()
    # update_one method to update data
    collection.update_one({'_id': ObjectId(item_id)}, {"$set": data})
    return jsonify({"message": "Record updated successfully"}), 200


@app.route('/delete/<string:item_id>', methods=['DELETE'])
def delete_record(item_id):
    # delete_one method to delete data
    collection.delete_one({'_id': ObjectId(item_id)})
    return jsonify({"message": "Record deleted successfully"}), 200




if __name__ == '__main__':
    app.run(debug=True)
