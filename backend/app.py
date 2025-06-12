from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["dashboardDB"]

# Valid roles
ROLES = ["admin", "department_manager", "project_manager", "financial_analyst", "employee"]

# Authentication

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = db.users.find_one({"email": email})
    
    if not user or user.get("password") != password:
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": str(user["_id"]),
            "email": user.get("email"),
            "role": user.get("role")
        },
        "token": "dummy-token"
    })

# User Management

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    email = data.get("email")
    name = data.get("name")
    password = data.get("password")
    role = data.get("role", "").strip().lower()

    if not email or not name or not password:
        return jsonify({"error": "All fields are required"}), 400

    if role not in ROLES:
        return jsonify({"error": f"Invalid role: '{role}'"}), 400

    if db.users.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 409

    data["role"] = role
    db.users.insert_one(data)
    return jsonify({"message": "User created"}), 201


@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404


@app.route('/api/users/<user_id>/role', methods=['PATCH'])
def update_role(user_id):
    data = request.json
    new_role = data.get('role')

    if new_role not in ROLES:
        return jsonify({"error": "Invalid role"}), 400

    result = db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"role": new_role}})
    if result.matched_count == 1:
        return jsonify({"message": "Role updated"}), 200
    return jsonify({"error": "User not found"}), 404


@app.route('/api/users', methods=['GET'])
def get_users():
    users = list(db.users.find({}))
    for user in users:
        user["_id"] = str(user["_id"])
    return jsonify(users)

# Leaderboard

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    top_users = list(db.users.find({"role": "employee"}).sort("working_hours", -1).limit(10))
    for user in top_users:
        user["_id"] = str(user["_id"])
    return jsonify(top_users)

# Organisation Management

@app.route('/api/organisations', methods=['POST'])
def create_organisation():
    data = request.json
    oid = data.get("oid", "").strip()
    name = data.get("name", "").strip()

    if not oid or not name:
        return jsonify({"error": "Organisation ID and name are required"}), 400

    if db.organisations.find_one({"oid": oid}):
        return jsonify({"error": "Organisation already exists"}), 409

    db.organisations.insert_one({"oid": oid, "name": name})
    return jsonify({"message": "Organisation created"}), 201


@app.route('/api/organisations', methods=['GET'])
def get_organisations():
    organisations = list(db.organisations.find({}))
    for org in organisations:
        org["_id"] = str(org["_id"])
    return jsonify(organisations)


@app.route('/api/organisations/<oid>', methods=['DELETE'])
def delete_organisation(oid):
    result = db.organisations.delete_one({"oid": oid})
    if result.deleted_count == 0:
        return jsonify({"error": "Organisation not found"}), 404
    db.departments.delete_many({"oid": oid})  # Clean up related departments
    return jsonify({"message": "Organisation and related departments deleted"}), 200

# Department Management

@app.route('/api/departments', methods=['POST'])
def create_department():
    data = request.json
    did = data.get("did", "").strip()
    name = data.get("name", "").strip()
    oid = data.get("oid", "").strip()

    if not did or not name or not oid:
        return jsonify({"error": "All fields required"}), 400

    if not db.organisations.find_one({"oid": oid}):
        return jsonify({"error": "Organisation does not exist"}), 404

    if db.departments.find_one({"did": did}):
        return jsonify({"error": "Department already exists"}), 409

    db.departments.insert_one({"did": did, "name": name, "oid": oid})
    return jsonify({"message": "Department created"}), 201


@app.route('/api/departments/<did>', methods=['DELETE'])
def delete_department(did):
    result = db.departments.delete_one({"did": did})
    if result.deleted_count == 0:
        return jsonify({"error": "Department not found"}), 404
    return jsonify({"message": "Department deleted"}), 200


@app.route('/api/departments', methods=['GET'])
def get_departments():
    departments = list(db.departments.find({}))
    for dept in departments:
        dept["_id"] = str(dept["_id"])
    return jsonify(departments)

@app.route('/api/employees', methods=['GET'])
def get_employees():
    employees = list(db.users.find({"role": {"$in": ["employee", "admin"]}}))
    for emp in employees:
        emp["_id"] = str(emp["_id"])
        emp.pop("password", None)  # Remove password for security
    return jsonify(employees)

@app.route('/api/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    data = request.json
    update_fields = {}

    allowed_fields = ["name", "departmentId", "startDate", "endDate", "budget"]
    for field in allowed_fields:
        if field in data:
            update_fields[field] = data[field]

    if not update_fields:
        return jsonify({"error": "No valid fields to update"})

    result = db.projects.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": update_fields}
    )

    if result.matched_count == 1:
        return jsonify({"message": "Project updated"})
    return jsonify({"error": "Project not found"})

@app.route('/api/projects', methods=['GET'])
def get_all_projects():
    projects = list(db.projects.find({}))
    for proj in projects:
        proj["_id"] = str(proj["_id"])
    return jsonify(projects)


@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.json
    name = data.get("name")
    departmentId = data.get("departmentId")
    startDate = data.get("startDate")
    endDate = data.get("endDate")
    budget = data.get("budget")

    if not name:
        return jsonify({"error": "Project name is required"}), 400

    project = {
        "name": name,
        "departmentId": departmentId,
        "startDate": startDate,
        "endDate": endDate,
        "budget": budget,
        "createdAt": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # ✅ added here
    }

    result = db.projects.insert_one(project)
    project["_id"] = str(result.inserted_id)
    return jsonify(project), 201

@app.route('/api/projects/<project_id>', methods=['GET'])
def get_project_by_id(project_id):
    try:
        project = db.projects.find_one({"_id": ObjectId(project_id)})
        if not project:
            return jsonify({"error": "Project not found"})
        project["_id"] = str(project["_id"])
        return jsonify(project)
    except:
        return jsonify({"error": "Invalid project ID"})
    

@app.route('/api/projects/search', methods=['GET'])
def search_projects():
    query = request.args.get('q', '').lower()
    projects = list(db.projects.find({"name": {"$regex": query, "$options": "i"}}))
    for proj in projects:
        proj["_id"] = str(proj["_id"])
    return jsonify(projects)




if __name__ == '__main__':
    app.run(debug=True)
