from flask import Flask, request, jsonify

app = Flask(__name__)

todos = [
    {"id": 1, "title": "example_title", "description": "example_description"}
]


@app.route('/')
def blank():
    return '<strong>Blank Page</strong>'


# GET /todos/:id
@app.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    todo = next((todo for todo in todos if todo["id"] == id), None)
    if todo:
        return jsonify({"statusCode": 200, "todo": todo}), 200
    else:
        return jsonify({"statusCode": 404, "message": "Not found"}), 404


# GET /todos
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify({"statusCode": 200, "todos": todos}), 200


# POST /todos
@app.route('/todos', methods=['POST'])
def create_todo():
    new_todo = request.json
    new_todo["id"] = max(todo["id"] for todo in todos) + 1
    todos.append(new_todo)
    return jsonify({"statusCode": 201, "message": "Added successfully"}), 201


# PATCH /todos/:id
@app.route('/todos/<int:id>', methods=['PATCH'])
def update_todo(id):
    updated_data = request.json
    todo = next((todo for todo in todos if todo["id"] == id), None)
    if not todo:
        return jsonify({"statusCode": 404, "message": "Not found"}), 404

    todo.update(updated_data)
    return jsonify({"statusCode": 200, "message": "Updated successfully"}), 200


# DELETE /todos/:id
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = next((todo for todo in todos if todo["id"] == id), None)
    if not todo:
        return jsonify({"statusCode": 404, "message": "Not found"}), 404

    todos.remove(todo)
    return jsonify({"statusCode": 200, "message": "Deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=3107)
