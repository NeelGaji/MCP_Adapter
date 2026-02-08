# Example REST API Documentation

This API allows you to manage a todo list application.

## Authentication

All requests require an API key passed in the `X-API-Key` header.

---

## Endpoints

### Create a Todo

**POST** `/todos`

Creates a new todo item.

Request body (JSON):
- `title` (string, required): The title of the todo
- `description` (string, optional): Detailed description
- `due_date` (string, optional): ISO 8601 date format
- `priority` (string): One of "low", "medium", "high" (default: "medium")

Response: Returns the created todo with an `id` field.

---

### Get All Todos

**GET** `/todos`

Retrieves all todos for the authenticated user.

Query parameters:
- `status` (string): Filter by status - "pending", "completed", "all"
- `limit` (integer): Max items to return (default 20, max 100)
- `offset` (integer): Pagination offset

---

### Get a Single Todo

**GET** `/todos/{id}`

Path parameters:
- `id` (integer, required): The todo ID

Returns 404 if not found.

---

### Update a Todo

**PUT** `/todos/{id}`

Updates an existing todo.

Path parameters:
- `id` (integer, required): The todo ID

Request body: Same as create, all fields optional.

---

### Delete a Todo

**DELETE** `/todos/{id}`

Permanently deletes a todo.

---

### Mark Todo Complete

**PATCH** `/todos/{id}/complete`

Marks a todo as completed. Sets `completed_at` timestamp.

---

### Search Todos

**GET** `/search`

Full-text search across todos.

Query parameters:
- `q` (string, required): Search query
- `fields` (string): Comma-separated fields to search: "title", "description"
