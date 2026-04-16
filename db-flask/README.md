# Todo API

Small Flask app that exposes a simple in-memory todo API.

## What It Does

- lists all tasks
- gets one task by id
- creates a new task
- updates an existing task
- deletes a task
- returns JSON errors for common request problems

## Project Files

- `app.py` starts the Flask app and registers blueprints
- `routes.py` contains the todo endpoints
- `errors.py` contains JSON error handlers
- `models.py` holds the in-memory task list
- `tests/` contains the pytest suite

## Requirements

- Python 3
- packages from `requirements.txt`

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run The App

From inside the `my-first-flask` folder:

```powershell
python app.py
```

The app runs on:

```text
http://127.0.0.1:5000
```

## Endpoints

### `GET /tasks`

Returns all tasks.

### `GET /tasks/<task_id>`

Returns one task by id.

### `POST /tasks`

Creates a task.

Example body:

```json
{
  "title": "Buy milk"
}
```

### `PUT /tasks/<task_id>`

Updates `title` and/or `completed`.

Example body:

```json
{
  "title": "Buy milk and bread",
  "completed": true
}
```

### `DELETE /tasks/<task_id>`

Deletes a task by id.

## Error Handling

This app returns JSON errors for:

- missing task ids
- invalid or missing JSON body
- missing `title`
- blank `title`
- invalid update fields
- invalid `completed` type

Example error response:

```json
{
  "ERROR": "404 Not Found: missing not found"
}
```

## Run Tests

From inside the `my-first-flask` folder:

```powershell
python -m pytest -q tests
```

## Notes

- data is stored in memory only
- restarting the server resets the tasks list
