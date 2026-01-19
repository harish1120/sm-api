# SM API - Social Media API

A robust and production-ready REST API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. This API provides a complete backend solution for a social media application with user authentication, posts management, and voting system.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3.12-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)

---

## 🚀 Features

- **User Management**: User registration and authentication
- **Posts API**: Create, read, update, and delete posts
- **Voting System**: Upvote/downvote posts
- **JWT Authentication**: Secure token-based authentication
- **Database Migrations**: Powered by Alembic
- **Containerized**: Docker support for easy deployment
- **CI/CD Pipeline**: Automated testing and deployment
- **Comprehensive Tests**: Full test coverage with pytest

---

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: PostgreSQL with [SQLAlchemy](https://www.sqlalchemy.org/)
- **ORM**: SQLAlchemy 2.0
- **Authentication**: OAuth2 with JWT (PyJWT)
- **Password Hashing**: Bcrypt
- **Migrations**: Alembic
- **Testing**: pytest
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Dependencies**: Poetry/requirements.txt

---

## 📁 Project Structure

```
sm_api/
├── alembic/                 # Database migrations
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
├── app/
│   ├── __init__.py
│   ├── main.py             # Application entry point
│   ├── config.py           # Settings and configuration
│   ├── database.py         # Database connection and session
│   ├── db_tables.py        # SQLAlchemy models (User, Post, Votes)
│   ├── schemas.py          # Pydantic schemas
│   ├── oauth2.py           # JWT authentication utilities
│   ├── utils.py            # Utility functions (password hashing)
│   └── routers/
│       ├── __init__.py
│       ├── auth.py         # Authentication endpoints
│       ├── users.py        # User management endpoints
│       ├── posts.py        # Posts CRUD endpoints
│       └── votes.py        # Voting endpoints
├── test/
│   ├── __init__.py
│   ├── conftest.py         # Pytest fixtures and configuration
│   ├── test_post.py        # Post endpoint tests
│   ├── test_user.py        # User endpoint tests
│   └── test_vote.py        # Vote endpoint tests
├── .github/
│   └── workflows/
│       └── build-deploy.yml # CI/CD pipeline
├── .gitignore
├── alembic.ini
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🏃‍♂️ Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL
- Docker (optional)

### Option 1: Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sm_api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   DATABASE_TYPE=postgresql
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   DATABASE_NAME=sm_api
   DATABASE_USER=your_db_user
   DATABASE_PASSWORD=your_db_password
   SECURITY_KEY=your-super-secret-key
   ALGORITHM=HS256
   EXPIRE_IN=60
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access the API documentation**
   
   Open your browser and navigate to:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

---

### Option 2: Using Docker

1. **Build the Docker image**
   ```bash
   docker build -t sm-api .
   ```

2. **Run the container**
   ```bash
   docker run -d -p 8000:8000 --env-file .env sm-api
   ```

3. **Access the API**
   
   Visit: `http://localhost:8000/docs`

---

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_TYPE` | Database driver (e.g., `postgresql`) | Required |
| `DATABASE_HOST` | Database server hostname | Required |
| `DATABASE_PORT` | Database port | Required |
| `DATABASE_NAME` | Database name | Required |
| `DATABASE_USER` | Database username | Required |
| `DATABASE_PASSWORD` | Database password | Required |
| `SECURITY_KEY` | JWT secret key for token signing | Required |
| `ALGORITHM` | JWT algorithm (e.g., `HS256`) | `HS256` |
| `EXPIRE_IN` | Token expiration time in minutes | `60` |

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login` | User login (returns JWT token) |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Create a new user |

### Posts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/posts/` | Get all posts (with pagination & search) |
| GET | `/posts/{id}` | Get a specific post |
| POST | `/posts/` | Create a new post |
| PUT | `/posts/{id}` | Update a post |
| DELETE | `/posts/{id}` | Delete a post |

### Votes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/votes/` | Vote on a post |

---

## 🧪 Running Tests

### Run all tests
```bash
pytest
```

### Run tests with verbose output
```bash
pytest -v
```

### Run specific test file
```bash
pytest test/test_post.py -v
```

---

## 🔄 CI/CD Pipeline

This project includes a GitHub Actions workflow for automated testing and deployment.

### Workflow: Build and Deploy

**Triggers:**
- Push to any branch
- Pull requests

**Jobs:**
1. **Build**: 
   - Runs on Ubuntu latest
   - Sets up Python 3.12
   - Installs dependencies
   - Runs pytest suite against PostgreSQL test database

2. **Deploy** (requires build to pass):
   - Deploys to production environment

**Secrets Required:**
- `DATABASE_TYPE`
- `DATABASE_HOST`
- `DATABASE_PORT`
- `DATABASE_NAME`
- `DATABASE_USER`
- `DATABASE_PASSWORD`
- `SECURITY_KEY`
- `ALGORITHM`
- `EXPIRE_IN`
- `DOCKER_HUB_USERNAME` (for Docker Hub deployment)
- `DOCKER_HUB_ACCESS_TOKEN` (for Docker Hub deployment)

---

## 📚 Database Models

### User
- `id`: Integer, Primary Key
- `email`: String, Unique
- `password`: String (hashed)
- `created_at`: Timestamp

### Post
- `id`: Integer, Primary Key
- `title`: String
- `content`: String
- `published`: Boolean (default: True)
- `owner_id`: Integer, Foreign Key to User
- `created_at`: Timestamp

### Votes
- `user_id`: Integer, Foreign Key to User (Composite Primary Key)
- `post_id`: Integer, Foreign Key to Post (Composite Primary Key)

---

## 🔐 Security

- Passwords are hashed using **bcrypt**
- Authentication via **JWT tokens**
- Protected endpoints require valid Bearer token
- Input validation using **Pydantic** schemas

---

## 📄 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Support

For support, please open an issue in the GitHub repository.

---

## 🙏 Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [Python JWT Handling](https://pyjwt.readthedocs.io/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/)

