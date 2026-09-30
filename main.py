import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Database setup
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")

class User(BaseModel):
    username: str
    password: str

@app.get("/")
def home():
    return {"message": "Backend running!"}

@app.post("/register")
def register(user: User):
    cursor.execute("INSERT INTO users VALUES (?, ?)", (user.username, user.password))
    conn.commit()
    return {"status": "success", "message": f"User {user.username} registered!"}

@app.post("/login")
def login(user: User):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user.username, user.password))
    result = cursor.fetchone()
    if result:
        return {"status": "success", "message": f"{user.username} logged in!"}
    return {"status": "error", "message": "Invalid credentials"}

@app.get("/users")
def get_users():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    return {"users": rows}


