from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search import SearchEngine

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"]
)
search_engine = SearchEngine()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/search/")
async def search(query: str):
    hits = await search_engine.search(query)
    return hits


@app.get("/search/charts/{id}/")
async def doc_search(id: str, query: str):
    hits = await search_engine.search_chart(id, query)
    return hits
