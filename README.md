# FastAPI Project

This project will be based off the course I took.

Added my own twist.

# Steps to create project

> Steps 1-5 creates a working web framework application. 

> Steps 6-7 connects to the database

> Steps 8-9 creates the application (endpoints, services to interact with database, password hashing)

> Steps 10 adds authentication and authorization using JWT 

---

### 1. Create a new folder `MyProject`
1. Initialize `Python` environment `env` with `python3.9 -m venv env `.

<br>

### 2. Create more folders `flexboard` and `backend`

<br>

### 3. In `backend`, create `requirements.txt
1. `requirements.txt` will have all the third party dependencies you need for your project.

<br>

### 4. Create a main Python class, `main.py` and add code from https://fastapi.tiangolo.com/#:~:text=Create%20a%20file,with to test
1. The `app` instance created from `FastAPI` is our web framework.
2. Gives us endpoints via `@app` decorator.
3. We can get `.post`, `.get`, `.put`, `.delete`, `.patch`, etc.

<br>

### 5. Start the program up and test
1. Module Name: `uvicorn`.
2. Parameters: `main:app --reload`.
3. Go to http://127.0.0.1:8000 to see if the app is running.

<br>

### 6. Create a new database in `PGAdmin`, database language shall be `PostgreSQL` as well
1. Usually a right click on `Database` shows `Create >` which then prompts a modal to create a new database.
2. Name it whatever you want and `Save`.

#### 6a. Credentials 
1. Create a new `.env` folder that will house all the environment variables.
   - Usually this file will have secrets coming from `AWS`, other areas.

#### 6b. Create a config file and a session file
1. Create a `config.py` file that will house all the `.env` values.
2. Create a `session.py` file that creates new sessions.
3. Create a `base_class.py` that will have `@as_declarative` which grants us to manipulate tables.
4. Create a `base.py` file that will serve as a bootstrap.
5. In `main.py` import `Base` from `tables.py` to create the tables, `bind` runs the engine.
   - the `.metadata` object is NOT offered in autocomplete, but is available.
   - I learned that the classes we want to be tables *that extended `Base`) must be in the `tables.py` file
     - if not, the tables does not get created. 
6. 

<br>

### 7. Tables are created via the code we have from `SQLAlchemy`
- `users`
- `jobs`

<br>

### 8. Create the `users` and `jobs` endpoints

<br>

### 9. Create the `users` and `jobs` services

<br>

### 10. Support Authentication and Authorization using `JWT`

<br>

### 11. Support the endpoints.
