from fastapi import Form, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import mysql.connector
from passlib.hash import pbkdf2_sha256 as hashfunc  # GANTI bcrypt ➜ pbkdf2_sha256
import random, os

auth_router = APIRouter()
templates = Jinja2Templates(directory="templates")

AVATAR_DIR = "avatars"
AVATARS = os.listdir(AVATAR_DIR)

def get_db():
    return mysql.connector.connect(
        user='root',
        password='',       # ganti jika password root MySQL kamu berbeda
        host='localhost',
        database='chat_app'
    )

@auth_router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@auth_router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@auth_router.post("/register")
def register_user(username: str = Form(...), password: str = Form(...)):
    conn = get_db()
    cursor = conn.cursor()
    
    # Random avatar dari folder avatars
    avatar = random.choice(AVATARS)

    print(f"Registering: {username}, avatar: {avatar}")

    try:
        cursor.execute(
            "INSERT INTO users (username, password, avatar) VALUES (%s, %s, %s)",
            (username, hashfunc.hash(password), avatar)
        )
        conn.commit()
        print("✅ Register success")
        return RedirectResponse("/", status_code=302)
    except Exception as e:
        print("❌ Register error:", e)
        return HTMLResponse("Register failed", status_code=400)

@auth_router.post("/login")
def login_user(username: str = Form(...), password: str = Form(...)):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    if user and hashfunc.verify(password, user["password"]):
        response = RedirectResponse("/chat", status_code=302)
        response.set_cookie("username", user["username"])
        response.set_cookie("avatar", user["avatar"])
        return response

    return HTMLResponse("Invalid credentials", status_code=401)

@auth_router.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    username = request.cookies.get("username")
    avatar = request.cookies.get("avatar")

    if not username:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "username": username,
        "avatar": avatar
    })
