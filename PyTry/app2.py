from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database"
users = [
    {"id": 1, "name": "Rahim Bhai"},
    {"id": 2, "name": "Karim Bhai"}
]

# READ (GET): Get all users (with pagination)
@app.route('/users', methods=['GET'])
def get_users():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    start = (page - 1) * per_page
    end = start + per_page
    paginated_users = users[start:end]
    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": len(users),
        "users": paginated_users
    }), 200

# SEARCH (GET): Search users by name (query parameter)
@app.route('/users/search', methods=['GET'])
def search_users():
    query = request.args.get('q', '').lower()
    matched_users = [u for u in users if query in u['name'].lower()]
    return jsonify(matched_users), 200

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
    token = request.headers.get('Authorization')
    if token != "Bearer mysecrettoken":
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400

    new_user = {"id": len(users) + 1, "name": data['name']}
    users.append(new_user)
    return jsonify(new_user), 201

# UPDATE (PUT): Update a user's name by ID
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    token = request.headers.get('Authorization')
    if token != "Bearer mysecrettoken":
        return jsonify({"error": "Unauthorized"}), 403

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
    token = request.headers.get('Authorization')
    if token != "Bearer mysecrettoken":
        return jsonify({"error": "Unauthorized"}), 403

    user_index = next((index for index, u in enumerate(users) if u['id'] == id), None)
    if user_index is None:
        return jsonify({"error": "User not found"}), 404

    users.pop(user_index)
    return jsonify({"message": "User deleted successfully"}), 200

# Custom error handler for 404
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

# Custom error handler for 500
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Start the server
if __name__ == '__main__':
    app.run(debug=True, port=3000)






"""

Testing:
	•	Get all users with pagination:
GET /users?page=1&per_page=1
	•	Search users:
GET /users/search?q=Rahim
	•	Add user (authenticated):
    curl -X POST http://127.0.0.1:3000/users \
    -H "Authorization: Bearer mysecrettoken" \
    -H "Content-Type: application/json" \
    -d '{"name": "New User"}'
"""