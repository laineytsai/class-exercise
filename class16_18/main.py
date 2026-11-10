import logging
import json
import fakeredis

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from check_storage import BookStorage

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

class BookInput(BaseModel):
    title: str
    price: float = Field(ge=0)

class BookResponse(BookInput):
    id: int

class BookCache:
    def __init__(self):
        self.client = fakeredis.FakeRedis(decode_responses=True)

    def make_key(self, min_price, limit):
        return f"books:min_price:{float(min_price)}:limit:{limit}"

    def get(self, min_price, limit):
        key = self.make_key(min_price, limit)
        value = self.client.get(key)
        if value is None:
            logger.debug(f"Cache MISS: {key}")
            return None
        logger.debug(f"Cache HIT: {key}")
        return json.loads(value)

    def set(self, min_price, limit, books):
        key = self.make_key(min_price, limit)
        self.client.set(key, json.dumps(books), ex=60)
        logger.debug(f"Cached result: {key}")

    def invalidate(self):
        self.client.flushdb()
        logger.debug("Invalidated book query cache")

app = FastAPI(title="Books Database API")
storage = BookStorage()
cache = BookCache()

@app.get("/books", response_model=list[BookResponse])
def list_books(
    min_price: float = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1)
):
    cached = cache.get(min_price, limit)
    if cached is not None:
        logger.info(f"Listed books: rows={len(cached)}")
        return cached
    books = storage.list_books(min_price, limit)
    cache.set(min_price, limit, books)
    logger.info(f"Listed books: rows={len(books)}")
    return books

@app.post("/books", response_model=BookResponse)
def add_book(book: BookInput):
    title = book.title
    price = book.price
    book_id = storage.add_book(title, price)
    cache.invalidate()
    logger.info(f"New book added: {book_id}")
    return storage.get_book(book_id)

@app.get("/books", response_model=list[BookResponse])
def list_books(
    min_price: float = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1)
    ):
    out = storage.list_books(min_price, limit)
    logger.info(f"{len(out)} books found")
    return out

@app.get("/search/books", response_model=list[BookResponse])
def search_books(
    min_price: float = Query(ge=0),
    max_price: float = Query(ge=0)
):
    if min_price > max_price:
        logger.warning("Min price must be lower than the max")
        raise HTTPException(status_code=400, detail="min_price must not exceed max_price")
    out = storage.search_books(min_price, max_price)
    logger.info(f"{len(out)} found")
    return out


