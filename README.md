# QA practice: Authors and Posts API Project

This is a Django-based REST API designed specifically for QA engineers to practice and refine their testing skills. It provides a realistic environment for testing API endpoints using tools like Postman, curl, and Swagger/OpenAPI.

[Russian version of README](README_RU.md)
[QA Engineer Guide](QA_GUIDE.md) — **Open this once everything is installed!**

Key features for testing:
- **Authentication**: JWT-based authentication flow.
- **CRUD Operations**: Create, Read, Update, and Delete actions for Authors and Posts.
- **Filtering & Sorting**: Advanced querying on the Posts endpoint.
- **Documentation**: Integrated Swagger and Redoc for API exploration.

## Installation and Running

Follow these steps to set up the project locally on any operating system (Windows, macOS, or Linux).

### 1. Prerequisites
- **Python 3.8+** must be installed on your system.
- **pip** (Python package installer).

### 2. Set up a Virtual Environment (Recommended)
Creating a virtual environment keeps the project dependencies isolated.

**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
With the virtual environment activated, install the required packages:
```bash
pip install django djangorestframework djangorestframework-simplejwt drf-spectacular django-filter pytest-django
```

### 4. Run Migrations
Set up the local SQLite database:
```bash
python manage.py migrate
```

### 5. Collect Static Files
Collect static files into the `staticfiles` directory:
```bash
python manage.py collectstatic --noinput
```

### 6. Prepopulate Database (Optional)
If you want to start with some sample data (10 authors and 142 posts):
```bash
python manage.py loaddata dummy_data.json
```
**Warning:** This command will overwrite existing data in the database if the objects (like authors or posts) have the same IDs as the ones in the fixture.

### 7. Create a Superuser (Optional)
If you want to access the Django Admin interface at `/admin/` for managing data with UI:
```bash
python manage.py createsuperuser
```

### 8. Run the Development Server
Start the API server:
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`.

## Authentication

Authentication is handled via JWT (JSON Web Tokens) for authors. This is separate from Django's built-in user authentication.

### Via Curl

1. **Register/Create an Author:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/authors/ \
        -H "Content-Type: application/json" \
        -d '{"username": "myuser", "password": "mypassword", "full_name": "My Name"}'
   ```

2. **Obtain JWT Token:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/login/ \
        -H "Content-Type: application/json" \
        -d '{"username": "myuser", "password": "mypassword"}'
   ```
   This will return an `access` and `refresh` token.

3. **Make Authenticated Requests:**
   Include the access token in the `Authorization` header:
   ```bash
   curl -X GET http://127.0.0.1:8000/api/posts/ \
        -H "Authorization: Bearer <your_access_token>"
   ```

### Via Postman

1. **Obtain Token:**
   - Create a `POST` request to `http://127.0.0.1:8000/api/login/`.
   - In the **Body** tab, select `raw` and `JSON`.
   - Provide your `username` and `password`.
   - Send the request and copy the `access` token from the response.

2. **Authenticated Request:**
   - Create a new request (e.g., `POST` to `http://127.0.0.1:8000/api/posts/`).
   - In the **Authorization** tab, select **Auth Type**: `Bearer Token`.
   - Paste the `access` token into the **Token** field.
   - Send the request.

### Authenticating in Swagger

1. Navigate to `http://127.0.0.1:8000/api/docs/swagger/`.
2. Find the `/api/login/` endpoint and click **Try it out**.
3. Enter your credentials and execute.
4. Copy the `access` token.
5. Click the **Authorize** button at the top of the page.
6. Enter `Bearer <your_access_token>` (or just the token depending on the configuration, but usually `Bearer <token>`) in the value field.
7. Click **Authorize** and then **Close**. Now subsequent requests made through Swagger will be authenticated.

## API Documentation and Endpoints

- **Swagger UI:** [http://127.0.0.1:8000/api/docs/swagger/](http://127.0.0.1:8000/api/docs/swagger/)
- **Redoc:** [http://127.0.0.1:8000/api/docs/redoc/](http://127.0.0.1:8000/api/docs/redoc/)
- **OpenAPI Schema (JSON):** [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

### Main Endpoints:

- `POST /api/authors/` - Register a new author (Public)
- `GET /api/authors/` - List authors (Public)
- `GET /api/authors/{id}/` - Retrieve author details (Public)
- `PATCH/PUT /api/authors/{id}/` - Update self (Authenticated, Owner only)
- `DELETE /api/authors/{id}/` - Delete self (Authenticated, Owner only)
- `POST /api/login/` - Obtain JWT tokens (Public)
- `GET /api/posts/` - List posts (Public, supports filtering by `status` and `author`, and sorting by `created_at`, `updated_at`)
- `POST /api/posts/` - Create a post (Authenticated)
- `GET /api/posts/{id}/` - Retrieve post details (Public)
- `PATCH/PUT /api/posts/{id}/` - Update post (Authenticated, Owner only)
- `DELETE /api/posts/{id}/` - Delete post (Authenticated, Owner only)

## Running Tests

Run tests using pytest:
```bash
pytest
```
