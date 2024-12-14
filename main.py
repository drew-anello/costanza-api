from fastapi import FastAPI
from mangum import Mangum
from app.endpoints import quotes, root

app = FastAPI()
handler = Mangum(app)

app.include_router(root.router)
app.include_router(quotes.router, tags=["Quotes"])
