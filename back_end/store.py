from flask import Flask, request, jsonify

app = Flask(__name__)

stores = []


@app.route('/')
def foo():
    return '<strong>Blank Page</strong>'


@app.route('/store', methods=['POST'])
def create_store():
    data = request.get_json()
    new_store = {
        'name': data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store), 201  # for creating(POST), has successfully processed


@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'Store not found'}), 404  # page not found


@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify({'store': stores})


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': data['name'],
                'price': data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item), 201
    return jsonify({'message': 'Store not found'}), 404


@app.route('/store/<string:name>/item', methods=['GET'])
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'Store not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=4340)
