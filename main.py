from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.conversations import router as conversations_router
from src.api.messages import router as messages_router
from src.db.models import Base
from src.db.session import engine

# from dotenv import load_dotenv

# load_dotenv()

def initialize_database():
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LangChain Chat App",
    description="A multi-provider chat app with persistent conversations.",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    initialize_database()

# Mount your routers
app.include_router(conversations_router)
app.include_router(messages_router)

# (Optional) Add a root endpoint for health checks or docs
@app.get("/")
def read_root():
    return {"message": "Chat API is running!"}

# To run: uvicorn main:app --reload
