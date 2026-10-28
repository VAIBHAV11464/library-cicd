from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)
books = []


def add_book(title, author):
    if not title or not author or not title.strip() or not author.strip():
        return False
    books.append({"id": len(books) + 1,
                  "title": title.strip(),
                  "author": author.strip()})
    return True


def get_books():
    return books


PAGE = """
<!doctype html>
<title>Library</title>
<h1>Library Book Management</h1>
<p><a href="/">Menu</a> | <a href="/add">1. Add Book</a> | <a href="/books">2. View Books</a></p>
<hr>
{% if mode == 'add' %}
  <h2>Add a Book</h2>
  <form method="post">
    Title: <input name="title"><br><br>
    Author: <input name="author"><br><br>
    <button type="submit">Add</button>
  </form>
{% elif mode == 'view' %}
  <h2>Books</h2>
  {% if books %}
  <table border="1" cellpadding="6">
    <tr><th>ID</th><th>Title</th><th>Author</th></tr>
    {% for b in books %}
    <tr><td>{{ b.id }}</td><td>{{ b.title }}</td><td>{{ b.author }}</td></tr>
    {% endfor %}
  </table>
  {% else %}<p>No books yet.</p>{% endif %}
{% else %}
  <p>Choose an option from the menu above.</p>
{% endif %}
"""


@app.route("/")
def home():
    return render_template_string(PAGE, mode="home")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        add_book(request.form.get("title"), request.form.get("author"))
        return redirect(url_for("view"))
    return render_template_string(PAGE, mode="add")


@app.route("/books")
def view():
    return render_template_string(PAGE, mode="view", books=get_books())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)