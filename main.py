from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
from test_groq import generate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

# class Item(BaseModel):
#     schema: str = None,
#     question: str = None,

@app.get("/", status_code=200)
async def index() -> dict[str, str]:
    return {"message": "hello world"}

@app.post("/test", status_code=200)
async def test(schema: str = Form(...), question: str = Form(...)):
    # print(schema)
    # print(question)
    result = generate(question, schema)
    return result

# items = []
# @app.post("/items")
# def create_item(item: Item):
#     items.append(item)
#     return items

# @app.get("/items/{item_id}")
# def get_item(item_id: int) -> str:
#     item = items[item_id]
#     return item