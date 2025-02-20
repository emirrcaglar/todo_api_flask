from gettext import find
from flask import Flask, json, jsonify, render_template, request

app = Flask(__name__)

TASKS_FILE = "todo.json"

def read_tasks():
    with open(TASKS_FILE, "r") as f:
        try:
            tasks = [json.loads(line) for line in f.readlines()]
            return tasks
        except FileNotFoundError:
            return []
        
def write_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        for task in tasks:
            f.write(json.dumps(task))

@app.route('/', methods=['GET'])
def view_form():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def tasks():
    tasks = read_tasks()
    return jsonify({'tasks': tasks, 'message': 'List of tasks'})

@app.route('/tasks', methods=['POST'])
def create_task(): 

    # Validate required fields
    task_name = request.form.get('task_name')
    task_description = request.form.get('task_description')
    if not task_name or not task_description:
        return jsonify({'error' : 'task_name and task_description are required'}), 400
    
    
    # Prepare the task data for storage
    task = {
        "task_name" : task_name,
        "task_description" : task_description
    }

    # Read file into tasks
    tasks = read_tasks()

    # Add new task to the tasks list
    tasks.append(task)

    # Write tasks to local txt file
    write_tasks(tasks)

    # Return success message
    return jsonify({'message': f'Task "{task_name}" created successfully'}), 201

@app.route("/tasks/<task_name>", methods=['DELETE'])      
def delete_task(task_name):
    if not task_name:
        return jsonify({'error': 'task_name is required'}), 400

    try:
        # Read all tasks from the file
        tasks = read_tasks()

        # Check if the task exists
        task_found = any(task.get('task_name') for task in tasks)
        if not task_found:
            return jsonify({'error': 'task not found'}), 400

        # Filter the task_name out
        updated_tasks = [task for task in tasks if task.get('task_name') != task_name]

        # Write the filtered tasks to the file
        write_tasks(updated_tasks)

        # Print success message
        return jsonify({'message': f'Deletion of {task_name} was successful'})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500



if __name__ == '__main__':
    app.run(debug=True)
