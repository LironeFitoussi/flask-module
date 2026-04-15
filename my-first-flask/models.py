import uuid


tasks = [
    {
        "id": str(uuid.uuid4()),
        "title": "Learn Flask",
        "completed": False,
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Build API",
        "completed": False,
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Test with Postman",
        "completed": True,
    },
]
