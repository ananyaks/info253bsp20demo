from flask import Flask, request, Response
import json
import logging

from key_service import verify_key

app = Flask(__name__)

app_tasks = {}
max_id = 0


@app.route('/v1/tasks', methods=["POST"])
def add_task():

    arguments = request.get_json()
    global max_id

    if not verify_key(arguments.get("api_key")):
        return "Error: api key not authorized", 401

    tasks = arguments.get("tasks", None)
    if not tasks:
        title = str(arguments.get("title"))

        max_id += 1

        app_tasks[max_id] = {"title": title, "is_completed": False}
        status_code = 201

        response_msg = {"id": max_id}

        resp = Response(json.dumps(response_msg), status=status_code)
        return resp
    
    else:

        response_msg = dict()
        response_msg["tasks"] = list()

        for task in tasks:
            max_id += 1

            app_tasks[max_id] = {"title": str(task["title"]), "is_completed": bool(task["is_completed"])}
            response_msg["tasks"].append({"id": max_id})
            status_code = 201

        resp = Response(json.dumps(response_msg), status=status_code)
        return resp

@app.route('/v1/tasks', methods=["GET"])
def list_all_tasks():

    if not verify_key(request.args.get("api_key")):
        return "Error: api key not authorized", 401

    def build_task(id, task):
        resp_task = task
        resp_task["id"] = id
        return resp_task

    response_msg = dict()
    response_msg["tasks"] = [ build_task(id, task) for id, task in app_tasks.items() ]
    status_code = 200

    resp = Response(json.dumps(response_msg), status=status_code)
    return resp


@app.route('/v1/tasks/<id>', methods=["GET"])
def get_task(id):

    if verify_key(request.args.get("api_key")):
        return "Error: api key not authorized", 401

    response_msg = dict()
    int_id = int(id)

    if int_id in app_tasks:
        response_msg.update(app_tasks[int_id])
        response_msg["id"] = int_id
        status_code = 200
    else:
        response_msg["error"] = "There is no task at that id"
        status_code = 404

    resp = Response(json.dumps(response_msg), status=status_code)
    return resp

@app.route('/v1/tasks', methods=["DELETE"])
def delete_bulk_tasks():

    tasks = request.get_json()["tasks"]

    for task in tasks:
        app_tasks.pop(task["id"], None)
    
    status_code = 204

    resp = Response('', status=status_code)
    return resp

@app.route('/v1/tasks/<id>', methods=["DELETE"])
def delete_task(id):

    response_msg = dict()
    int_id = int(id)

    if int_id in app_tasks:
        del app_tasks[int_id]
    status_code = 204

    resp = Response('', status=status_code)
    return resp


@app.route('/v1/tasks/<id>', methods=["PUT"])
def edit_task(id):

    response_msg = dict()
    int_id = int(id)

    arguments = request.get_json()
    title = str(arguments.get("title"))
    is_completed = bool(arguments.get("is_completed"))

    if int_id in app_tasks:
        app_tasks[int_id]["title"] = title
        app_tasks[int_id]["is_completed"] = is_completed
        status_code = 204
    else:
        response_msg["error"] = "There is no task at that id"
        status_code = 404

    resp = Response(json.dumps(response_msg), status=status_code)
    return resp


@app.route('/v1/tasks/new/endpoint', methods=["POST"])
def create_super_tasks():
    
    arguments = request.get_json()
    title = arguments.get(title)

    sql = f'INSERT INTO tasks (title) values ("{title}")'

    'INSERT INTO tasks (title) VALUES (?)', title

