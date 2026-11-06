import logging
import sqlite3
from pathlib import Path

logging.basicConfig(
level=logging.DEBUG,
format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


class BookStorage:
    def __init__(self, db_path="data/books.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.db_path)
        try:
            sql_statement = """
                            CREATE TABLE IF NOT EXISTS books (
                            id INTEGER PRIMARY KEY,
                            title TEXT NOT NULL,
                            price REAL NOT NULL
                            )   
                            """
            connection.execute(sql_statement)
            connection.commit()
            logger.debug(f"Database ready: {self.db_path}")
        finally:
            connection.close()

    def add_book(self, title, price):
        connection = sqlite3.connect(self.db_path)
        try:
            sql_statement = "INSERT INTO books (title, price) VALUES (?, ?)"
            cursor = connection.execute(sql_statement, (title, price))
            book_id = cursor.lastrowid
            connection.commit()
            logger.debug(f"New book added, ID: {book_id}")
            return book_id

        except sqlite3.Error:
            connection.rollback()
            raise

        finally:
            connection.close()


    def get_book(self, book_id):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            sql_statement = "SELECT id, title, price FROM books WHERE id = ?"
            row = connection.execute(sql_statement, (book_id,)).fetchone()

            if row:
                logger.debug(f"Book ID: {row}")
                return dict(row)
            else:
                logger.debug(f"Book ID: {row}")
                return None

        finally:
            connection.close()


    def list_books(self, min_price=0, limit=100):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            sql_statement = """
            SELECT id, title, price 
            FROM books 
            WHERE price >= ?
            ORDER BY price DESC, id ASC
            LIMIT ?
            """
            rows = connection.execute(sql_statement, (min_price, limit)).fetchall()
            logger.debug(f"Listed books: count={len(rows)}")
            return [dict(row) for row in rows]

        finally:
            connection.close()

    def replace_books(self, books):
        connection = sqlite3.connect(self.db_path)

        try:
            sql_statement = "DELETE FROM books"
            connection.execute(sql_statement)
            sql_statement = "INSERT INTO books (title, price) VALUES (?, ?)"
            connection.executemany(sql_statement, books)
            connection.commit()
            logger.debug(f"Replaced books: rows={len(books)}")
        except sqlite3.Error:
            connection.rollback()
            raise
        finally:
            connection.close()

    def search_books(self, min_price, max_price):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        sql_statement = """
                                SELECT * FROM books 
                                WHERE price >= ? AND price <= ?
                                ORDER BY price desc, id asc
                                """
        try:
            rows = connection.execute(sql_statement, (min_price, max_price)).fetchall()
            rows = [dict(row) for row in rows]
            logger.debug(f"{len(rows)} found")
            return rows

        finally:
            connection.close()


def main():
    path = Path("data") / "books.db"
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row

    sql_statement = """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        price REAL NOT NULL
    )
    """
    connection.execute(sql_statement)
    connection.execute("DELETE FROM books")
    connection.commit()


    sql_statement = "INSERT INTO books (title, price) VALUES (?, ?)"
    cursor = connection.execute(sql_statement, ("Book A", 12.5))
    book_id = cursor.lastrowid
    connection.commit()


    connection.execute(sql_statement, ("Book B" , 25.0))
    connection.execute(sql_statement, ("Book C", 18.0))
    connection.commit()


    rows = [("Book D", 15.0), ("Book E", 10.0)]
    connection.executemany(sql_statement, rows)
    connection.commit()


    # Retrieve one book
    sql_statement = "SELECT id, title, price FROM books WHERE id = ?"
    row = connection.execute(sql_statement, (book_id,)).fetchone()
    print(dict(row))


    # Preview the first n
    sql_statement = "SELECT * FROM books ORDER BY id LIMIT ?"
    rows = connection.execute(sql_statement, (5,)).fetchall()
    print([dict(row) for row in rows])


    # Filter and Sort
    sql_statement = """
    SELECT title, price FROM books
    WHERE price >= ? ORDER BY price DESC LIMIT ?
    """
    rows = connection.execute(sql_statement, (15, 2)).fetchall()
    print([dict(row) for row in rows])

    connection.close()


    storage = BookStorage()
    book_id = storage.add_book("Book A", 12.5)
    logger.info(f"Added book: id={book_id}")

    print(storage.get_book(book_id)["title"])
    print(storage.get_book(book_id)["price"])
    books = storage.list_books(min_price=15, limit=2)
    print([(book["title"], book["price"]) for book in books])


    try:
        storage.replace_books([("New Book", 20.0), (None, 10.0)])
    except sqlite3.IntegrityError:
        print("Replacement failed; original books kept.")


    connection.close()







if __name__ == "__main__":
    main()