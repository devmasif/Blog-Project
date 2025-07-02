# 📝 Blog Project API

A FastAPI-powered backend for a blogging platform with JWT-based authentication, MongoDB integration, and full CRUD support for posts, comments, and likes. Deployed on Railway.

---

## 🚀 Features

- 🔐 User registration and login (JWT)
- 📝 Create, update, delete blog posts
- 💬 Comment on posts
- ❤️ Like/unlike posts
- 🧾 Swagger UI at `/docs`
- ☁️ Hosted on Railway with `.env` config

---

## 📦 Tech Stack

- **FastAPI** – Python Web Framework
- **MongoDB Atlas** – NoSQL Database
- **Uvicorn** – ASGI Server
- **python-jose** – JWT Tokens
- **Passlib (bcrypt)** – Password Hashing
- **Railway** – Deployment Platform

---

#### 🌐 Live Demo

🔗 [https://blog-project-production-ebfe.up.railway.app/docs](https://blog-project-production-ebfe.up.railway.app/docs)

---

### ⚙️ Setup Instructions

#### 1. Clone the Repo

```bash
git clone https://github.com/devmasif/Blog-Project.git
cd Blog-Project
```

#### 2. Create a `.env` file

```env
MONGO_URI=your_mongodb_uri
DB_NAME=blog_db
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run the app

```bash
uvicorn main:app --reload
```

Visit: `http://127.0.0.1:8000/docs`



Enjoy 😊 

---

