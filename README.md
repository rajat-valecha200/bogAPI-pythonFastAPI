Here you go, Rajat — a complete README.md and Postman API collection with sample data setup. You’ll also get some JSON for seeding.
# 📝 Blog API – FastAPI + PostgreSQL + JWT Auth

A simple blog backend with user registration/login, JWT authentication, and CRUD operations for blog posts, including file uploads.

## 🔧 Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT (using `python-jose`)
- Pydantic
- Uvicorn

## 📁 Project Structure

```

blogAPI/
│
├── app/
│   ├── **init**.py
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routes/
│       ├── users.py
│       └── posts.py
│
├── .env
├── requirements.txt
└── uploads/

````

## ⚙️ Setup Instructions

### 1. Clone Repo and Create Virtual Environment

```bash
git clone https://github.com/rajat-valecha200/bogAPI-pythonFastAPI.git
cd blogAPI
python -m venv venv
venv\Scripts\activate  # on Windows
# OR
source venv/bin/activate  # on Mac/Linux
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure `.env`

Create a `.env` file in root:

```
DATABASE_URL=postgresql://postgres:yourpassword@localhost/blogdb
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> Make sure PostgreSQL is running and the `blogdb` database is created.

### 4. Run the App

```bash
uvicorn app.main:app --reload
```

### 5. API Docs

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔐 Authentication

Use `/users/register` to create a user, then `/users/login` to get a JWT token.

Use the JWT token in the **Authorization Header**:

```
Authorization: Bearer <token>
```

---

## 📬 Sample API Endpoints

| Method | Endpoint        | Description             |
| ------ | --------------- | ----------------------- |
| POST   | /users/register | Register user           |
| POST   | /users/login    | Get JWT token           |
| POST   | /posts/         | Create a post           |
| GET    | /posts/         | List all posts          |
| GET    | /posts/{id}     | Get post by ID          |
| PUT    | /posts/{id}     | Update post (auth only) |
| DELETE | /posts/{id}     | Delete post (auth only) |
| POST   | /posts/upload/  | Upload post image       |

---

## 📦 Sample Data (JSON)

### 👤 Users

```json
{
  "email": "testuser@example.com",
  "password": "password123"
}
```

### 📝 Posts

```json
{
  "title": "First Post",
  "content": "This is my first blog post!",
  "image": "example.png"
}
```

---
