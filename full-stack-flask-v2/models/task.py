import uuid
from config.db import get_collection


def serialize_task(task):
    task["_id"] = str(task["_id"])
    return task


def get_tasks_for_list(list_id):
    col = get_collection("tasks")
    return [serialize_task(t) for t in col.find({"list_id": list_id})]


def get_task_by_id(task_id):
    col = get_collection("tasks")
    return col.find_one({"id": task_id})


def create_task(list_id, title):
    doc = {"id": str(uuid.uuid4()), "list_id": list_id, "title": title, "completed": False}
    col = get_collection("tasks")
    col.insert_one(doc)
    return serialize_task(doc)


def update_task(task_id, update):
    col = get_collection("tasks")
    return col.find_one_and_update(
        {"id": task_id}, {"$set": update}, return_document=True
    )


def delete_task(task_id):
    col = get_collection("tasks")
    return col.find_one_and_delete({"id": task_id})
