# URL-Shortening-Service

## Overview

Its a simple RESTful API that allows users to shorten long URLs. The API provide endpoints to create, retrieve, update, and delete short URLs. It also provide statistics on the number of times a short URL has been accessed.

## Main Functional Requirements

1. **Create a new short URL**

Create a new short URL using the POST method

The endpoint validate the request body and return a 201 Created status code with the newly created short URL or a 400 Bad Request status code with error messages in case of validation errors. Short codes must be unique and be generated randomly.

2. **Retrieve an original URL from a short URL**

Retrieve the original URL from a short URL using the GET method.
The endpoint return a 200 OK status code with the original URL or a 404 Not Found status code if the short URL was not found.
The frontend is responsible for retrieving the original URL using the short URL and redirecting the user to the original URL.

3. **Update an existing short URL**

Update an existing short URL using the PUT method.
The endpoint  validate the request body and return a 200 OK status code with the updated short URL.
or a 400 Bad Request status code with error messages in case of validation errors. It  return a 404 Not Found status code if the short URL was not found.

4. **Delete an existing short URL**

Delete an existing short URL using the DELETE method
The endpoint  return a 204 No Content status code if the short URL was successfully deleted or a 404 Not Found status code if the short URL was not found.

5. **Get statistics on the short URL**

Get statistics for a short URL using the GET method.
The endpoint  return a 200 OK status code with the statistics or a 404 Not Found status code if the short URL was not found.

6. **Minimal frontend to interact with the API**

## 📈 Project Status

> **Current Phase:** In progress

## ⚙️ Installation & Setup

### Requirements

- Python 3.9+
- FastApi[Standard]

### Local Setup

1. Clone the repository.
2. Create a env
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

    > Required libraries include:
    ```text
    fastapi
    fastapi-cli
    h11
    httpcore
    httptools
    httpx
    idna
    Jinja2
    markdown-it-py
    MarkupSafe
    mdurl
   ```
4. Run the server:

    use this commands:
    ```text
    $env:PYTHONPATH='.'
    fastapi dev backend/api/main.py
    ```
5. Run the frontend page
## 🗂️ Project Structure

```
URL Shortening Service
├── backend
│   ├── data         # Data access
│   ├── logic        # Business logic
│   ├── models       # Domain and ORM models
│   ├── api/routes   # FastAPI
│   └── tests        # tests
├── frontend
```

https://roadmap.sh/projects/url-shortening-service