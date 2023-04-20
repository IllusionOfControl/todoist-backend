# Todoist clone

This project is a Todoist clone application that consists of two parts: a frontend built with React and a backend built with Python, FastAPI framework, and PostgreSQL database. The frontend project is located in the `frontend/` directory in the root of the backend.

### Manual Installation

#### Backend

1. Install PostgreSQL and create a new database.
2. Set the environment variables in your terminal:

```
export POSTGRES_DB=your_db_name
export POSTGRES_PORT=your_db_port
export POSTGRES_USER=your_db_username
export POSTGRES_PASSWORD=your_db_password
```

3. Run the following command to start a PostgreSQL container:

```
docker run --name pgdb --rm -e POSTGRES_USER="$POSTGRES_USER" -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" -e POSTGRES_DB="$POSTGRES_DB" postgres
```

4. Create a new `.env` file in the project root directory and add the following environment variables:

```
APP_ENV=dev
DATABASE_URL=postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB
SECRET_KEY=$(openssl rand -hex 32)
```

5. Run the following command to apply database migrations:

```
alembic upgrade head
```

6. Run the following command to start the backend server:

```
uvicorn app.main:app --reload
```

#### Frontend

1. Change directory to `frontend/`:

```
cd frontend/
```

2. Install the dependencies:

```
npm install
```

3. Start the development server:

```
npm start
```

#### Docker

1. Clone the repository:

```
git clone https://github.com/yourusername/todoist-clone.git
```

2. Navigate to the project root directory:

```
cd todoist-clone/
```

3. Set the environment variables in your terminal:

```
export POSTGRES_DB=your_db_name
export POSTGRES_PORT=your_db_port
export POSTGRES_USER=your_db_username
export POSTGRES_PASSWORD=your_db_password
```

4. Create a new `.env` file in the project root directory and add the following environment variables:

```
APP_ENV=dev
DATABASE_URL=postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB
SECRET_KEY=$(openssl rand -hex 32)
```

5. Run the following command to start the project with Docker:

```
docker-compose up --build
```

6. Access the frontend in your browser at `http://localhost:8000` and the backend API at `http://localhost:8000/api/`.

### Contributing

Contributions are welcome! If you find a bug or have an idea for a new feature, please create a new issue on GitHub or submit a pull request.

### License

This project is licensed under the MIT License. See the `LICENSE` file for details.
