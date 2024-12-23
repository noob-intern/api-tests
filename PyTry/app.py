from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database"
users = [
    {"id": 1, "name": "Rahim Bhai"},
    {"id": 2, "name": "Karim Bhai"}
]

# READ (GET): Get all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# READ (GET): Get a single user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = next((u for u in users if u['id'] == id), None)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

# CREATE (POST): Add a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400

    new_user = {"id": len(users) + 1, "name": data['name']}
    users.append(new_user)
    return jsonify(new_user), 201

# UPDATE (PUT): Update a user's name by ID
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = next((u for u in users if u['id'] == id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400

    user['name'] = data['name']
    return jsonify(user), 200

# DELETE (DELETE): Remove a user by ID
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user_index = next((index for index, u in enumerate(users) if u['id'] == id), None)
    if user_index is None:
        return jsonify({"error": "User not found"}), 404

    users.pop(user_index)
    return jsonify({"message": "User deleted successfully"}), 200

# Start the server
if __name__ == '__main__':
    app.run(debug=True, port=3000)