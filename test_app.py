from app import app, add_book, get_books, books


def setup_function():
    books.clear()


def test_add_book():
    assert add_book("Python 101", "Guido") is True
    assert len(get_books()) == 1


def test_add_empty_book_fails():
    assert add_book("", "") is False
    assert len(get_books()) == 0


def test_home_page():
    client = app.test_client()
    assert client.get("/").status_code == 200


def test_add_and_view_route():
    client = app.test_client()
    client.post("/add", data={"title": "Clean Code", "author": "Martin"})
    res = client.get("/books")
    assert b"Clean Code" in res.data