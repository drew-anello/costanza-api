from fastapi import FastAPI
from mangum import Mangum
from app.endpoints import quotes, root
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
handler = Mangum(app)

app.include_router(root.router)
app.include_router(quotes.router, tags=["Quotes"])
