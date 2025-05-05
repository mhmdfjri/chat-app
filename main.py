# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from server.auth_api import auth_router
from server.transfer_file import transfer_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(transfer_router)

# Ini untuk serve avatar
app.mount("/avatars", StaticFiles(directory="avatars"), name="avatars")
app.mount("/files", StaticFiles(directory="uploaded_files"), name="files")
app.mount("/style", StaticFiles(directory="style"), name="style")

