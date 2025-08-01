from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from sqlalchemy import Integer
from extension import db
import model
import os

app = Flask(__name__)
CORS(app)

config_class = 'DevelopmentConfig'
config_class = os.getenv('FLASK_CONFIG', 'DevelopmentConfig')
app.config.from_object(f'config.{config_class}')

db.init_app(app)

# ========== Initialize Database ==========


@app.before_first_request
def initialize_database():
    with app.app_context():
        model.init_db()


# ========== CA1 & CA2 endpoints ==========
# ========== Routing frontend ==========
@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html', title='Task Tracker - Home'), 200


@app.route('/create_task.html')
def create_task():
    return render_template('create_task.html', title='Task Tracker - Create Task'), 200


@app.route('/update_task.html')
def update_task():
    return render_template('update_task.html', title='Task Tracker - Update Task'), 200


@app.errorhandler(404)  # Routing user from any undefine routes to home page
def page_not_found(e):
    return render_template('index.html', title='Task Tracker - Home'), 200


# ========== API ==========
# Create task
@app.route('/api/tasks', methods=['POST'])
def create_task_api():
    # Get the JSON data from the request
    name = request.form.get('task_name', '').lower().strip()
    description = request.form.get('description', '').lower().strip()
    points = request.form.get('points','').strip()
    image = request.files.get("image")

    # validate json value
    if not name:
        return jsonify({
            "error": "Name cannot be empty."
        }), 400
    elif not description:
        return jsonify({
            "error": "Description cannot be empty."
        }), 400
    elif not points:
        return jsonify({
            "error": "Points cannot be empty."
        }), 400
    elif not points.isdigit():
        return jsonify({
            "error": "Points must be a valid integer."
        }), 400
    elif not image or image.filename == "":
        return jsonify({
            "error": "No image uploaded."
        }), 400

    points = int(points)
    
    # Create user account and profile
    try:
        # write image into application
        image_url = model.save_image(image, 0)
        task_id = model.create_task(name, description, points, image_url)
        task = model.get_task_by_id(task_id)._asdict()
        return jsonify({
            "task_id": task_id,
            "name": task["name"],
            "description": task["description"],
            "points": task["points"],
            "image_url": task["image_url"]
        }), 201
    except Exception as e:
        return jsonify({
            "error": "Task creation failed.",
            "detail": str(e)
        }), 400



# Update task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task_api(task_id):
    name = request.form.get('task_name', '').lower().strip()
    description = request.form.get('description', '').lower().strip()
    points = request.form.get('points','').strip()
    image = request.files.get("image")

    # Get user by user to check if user exist
    task = model.get_task_by_id(task_id)

    # validate json value
    if not name:
        return jsonify({
            "error": "Name cannot be empty."
        }), 400
    elif not description:
        return jsonify({
            "error": "Description cannot be empty."
        }), 400
    elif not points:
        return jsonify({
            "error": "Points cannot be empty."
        }), 400
    elif not points.isdigit():
        return jsonify({
            "error": "Points must be a valid integer."
        }), 400
    elif not task:
        return jsonify({
            "error": "Task ID not found."
        }), 404
    elif not image or image.filename == "":
        return jsonify({
            "error": "No image uploaded."
        }), 400

    points = int(points)
    
    try:
        # write image into application
        image_url = model.save_image(image, 0)
        model.update_task(task_id, name, description, points, image_url)
        task = model.get_task_by_id(task_id)._asdict()
        print(task)
        return jsonify({
            "task_id": task_id,
            "name": task["name"],
            "description": task["description"],
            "points": task["points"],
            "image_url": task["image_url"]
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Task creation failed.",
            "detail": str(e)
        }), 400


# ========== Frontend ==========
# Create task
@app.route('/tasks', methods=['POST'])
def create_task_frontend():
    # Get the JSON data from the request
    name = request.form.get('task_name', '').lower().strip()
    description = request.form.get('description', '').lower().strip()
    points = request.form.get('points','').strip()
    image = request.files.get("image")

    # validate json value
    if not name:
        return jsonify({
            "error": "Name cannot be empty."
        }), 400
    elif not description:
        return jsonify({
            "error": "Description cannot be empty."
        }), 400
    elif not points:
        return jsonify({
            "error": "Points cannot be empty."
        }), 400
    elif not points.isdigit():
        return jsonify({
            "error": "Points must be a valid integer."
        }), 400
    elif not image or image.filename == "":
        return jsonify({
            "error": "No image uploaded."
        }), 400

    points = int(points)
    
    try:
        # write image into application
        image_url = model.save_image(image, 0)
        model.create_task(name, description, points, image_url)
        return render_template("create_task.html"), 200
    except Exception as e:
        return jsonify({
            "error": "Task creation failed.",
            "detail": str(e)
        }), 400


# Update task
@app.route('/update_tasks', methods=['POST'])
def update_task_frontend():
    task_id = int(request.form.get('taskId', ''))
    name = request.form.get('task_name', '').lower().strip()
    description = request.form.get('description', '').lower().strip()
    points = request.form.get('points','').strip()
    image = request.files.get("image")

    # Get user by user to check if user exist
    task = model.get_task_by_id(task_id)

    # validate json value
    if not name:
        return jsonify({
            "error": "Name cannot be empty."
        }), 400
    elif not description:
        return jsonify({
            "error": "Description cannot be empty."
        }), 400
    elif not points:
        return jsonify({
            "error": "Points cannot be empty."
        }), 400
    elif not points.isdigit():
        return jsonify({
            "error": "Points must be a valid integer."
        }), 400
    elif not task:
        return jsonify({
            "error": "Task ID not found."
        }), 404
    elif not image or image.filename == "":
        return jsonify({
            "error": "No image uploaded."
        }), 400
    
    points = int(points)

    try:
        # write image into application
        image_url = model.save_image(image, 0)
        model.update_task(task_id, name, description, points, image_url)
        task = model.get_task_by_id(task_id)._asdict()
        print(task)
        return render_template("update_task.html"), 200
    except Exception as e:
        return jsonify({
            "error": "Task creation failed.",
            "detail": str(e)
        }), 400


# Create user account 
@app.route('/create_user', methods=['POST'])
def create_user_frontend():
    username = request.form.get('username', '').lower().strip()
    password = request.form.get('password', '').lower().strip()
    email = request.form.get('email', '').lower().strip()

    try:
        model.create_user(username, password, email)
        return render_template("create_task.html"), 200
    except Exception as e:
        return jsonify({
            "error": "User creation failed.",
            "detail": str(e)
        }), 400


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
