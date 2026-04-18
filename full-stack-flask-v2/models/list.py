import uuid
from config.db import get_collection


def serialize_list(lst):
    lst["_id"] = str(lst["_id"])
    return lst


def get_all_lists():
    col = get_collection("lists")
    return [serialize_list(l) for l in col.find()]


def get_list_by_id(list_id):
    col = get_collection("lists")
    return col.find_one({"id": list_id})


def create_list(name):
    doc = {"id": str(uuid.uuid4()), "name": name}
    col = get_collection("lists")
    col.insert_one(doc)
    return serialize_list(doc)


def update_list(list_id, name):
    col = get_collection("lists")
    return col.find_one_and_update(
        {"id": list_id}, {"$set": {"name": name}}, return_document=True
    )


def delete_list(list_id):
    col = get_collection("lists")
    lst = col.find_one_and_delete({"id": list_id})
    if lst:
        get_collection("tasks").delete_many({"list_id": list_id})
    return lst
