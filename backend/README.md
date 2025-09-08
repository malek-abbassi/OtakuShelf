# OtakuShelf Backend

This is the backend for OtakuShelf, a web application that allows users to search for anime and create a watch list. The backend is built using python and FastAPI.

## Features

- Search for anime by title, genre, or other criteria
- Create and manage a watch list
- User authentication and authorization
- RESTful API for easy integration with frontend

## Technologies Used

- FastAPI (Python web framework)
- Pydantic (Data validation and settings management)

## Getting Started

### Prerequisites

- Python 3.12 or higher (you can use pyenv to manage Python versions)
- pipenv for managing dependencies
- Docker
- Git

### Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/OtakuShelf.git
   cd OtakuShelf
   ```

2. Install dependencies using pipenv:

   ```bash
   pipenv install --dev
   ```

3. Create a `.env` file in the root directory and add the necessary environment variables. You can refer to the `.env.example` file for guidance.

### Running the Application

#### Development Server

Start the development server:

```bash
pipenv run dev
```

The server will be running at `http://localhost:8000`.

#### Production Server

To run the application in a production environment:

```bash
pipenv run start
```

## API Documentation

The API documentation is automatically generated and can be accessed at `http://localhost:8000/docs` when the server is running.
You can also access the alternative documentation at `http://localhost:8000/redoc`.

## Testing

```bash
pipenv run test
```

## Linting and Formatting

### Local Linting and Formatting

The project uses `ruff` for linting and formatting. You can run the following commands:

```bash
pipenv run lint
```

To automatically fix linting issues, run:

```bash
pipenv run lint-fix
```

To format the codebase, run:

```bash
pipenv run format
```

### CI/CD Linting

The project is set up with a GitHub Actions workflow to automatically lint the code on pull requests. This ensures that all code changes adhere to the defined coding standards before being merged.
If the pipeline fails, you can run the linting commands locally to identify and fix issues before pushing your changes again.
