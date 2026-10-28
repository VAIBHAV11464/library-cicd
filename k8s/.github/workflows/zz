# Library Book Management: CI/CD ka Complete Step-by-Step Guide (Hinglish)

**Approach:** Python Flask web app, jisme home page par menu hai (Add Book, View Books, aur Push 2 mein Issue Book). Web app isliye, kyunki Kubernetes Service ke through CLI `input()` menu expose nahi hota.

**Pipeline:** Source Code → Git/GitHub → GitHub Actions (test) → Docker build + Docker Hub push → Kubernetes deploy + Service

---

## STEP 0: Prerequisites install karo

- VS Code, Python 3.10+, Git, Docker Desktop
- `kubectl` aur **Minikube** (local Kubernetes cluster)
- GitHub account aur Docker Hub account

Check karo:
```bash
python --version
git --version
docker --version
kubectl version --client
minikube version
```

---

## STEP 1: Project folder banao (VS Code mein)

```bash
mkdir library-cicd
cd library-cicd
code .
```

Final structure:
```
library-cicd/
├── app.py
├── test_app.py
├── requirements.txt
├── Dockerfile
├── .gitignore
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
└── .github/
    └── workflows/
        └── ci-cd.yml
```

---

## STEP 2: Push 1 ka code likho (Add + View only)

**requirements.txt**
```
flask==3.0.3
pytest==8.3.2
```

**app.py** (Push 1 version)
```python
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
```

**test_app.py** (Push 1 tests)
```python
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
```

**.gitignore**
```
__pycache__/
*.pyc
venv/
.pytest_cache/
```

---

## STEP 3: Local test karo (push se pehle)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
pytest
python app.py
```
Browser mein `http://localhost:5000` kholo aur check karo. Ab app band kar do.

---

## STEP 4: Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

---

## STEP 5: Kubernetes manifests

**k8s/deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: library-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: library-app
  template:
    metadata:
      labels:
        app: library-app
    spec:
      containers:
        - name: library-app
          image: DOCKERHUB_USER/library-app:IMAGE_TAG
          ports:
            - containerPort: 5000
```

**k8s/service.yaml**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: library-service
spec:
  type: NodePort
  selector:
    app: library-app
  ports:
    - port: 80
      targetPort: 5000
      nodePort: 30007
```

`DOCKERHUB_USER` aur `IMAGE_TAG` placeholders hain. Workflow inhe real values se replace karega, isse har push ka unique tag use hoga.

---

## STEP 6: Docker Hub setup

1. hub.docker.com par login karo.
2. **Account Settings → Personal access tokens → Generate new token** (Read & Write). Token copy karke rakh lo.
3. Repository manually banane ki zarurat nahi, push par auto ban jayegi (ya `library-app` naam se public repo bana lo).

---

## STEP 7: GitHub repo banao (abhi push mat karna)

1. github.com par **New repository** → naam `library-cicd` → empty rakho (README mat add karo).
2. Repo ke **Settings → Secrets and variables → Actions → New repository secret** mein do secrets add karo:
   - `DOCKERHUB_USERNAME` = tumhara Docker Hub username
   - `DOCKERHUB_TOKEN` = Step 6 wala token

---

## STEP 8: Kubernetes cluster + Self-hosted runner

GitHub ka cloud runner tumhare local Minikube tak nahi pahunch sakta. Isliye deploy job tumhari apni machine par **self-hosted runner** se chalayenge.

1. Cluster start karo:
   ```bash
   minikube start --driver=docker
   kubectl get nodes
   ```
2. GitHub repo → **Settings → Actions → Runners → New self-hosted runner**. Apna OS select karo aur wahan jo commands dikhein woh terminal mein ek-ek karke chalao (download, `config`, phir `run`).
3. Runner terminal **chalta hua** rehna chahiye (`./run.cmd` ya `./run.sh`). Status GitHub par **Idle** dikhna chahiye.
4. Windows par ho to Git Bash installed ho (workflow `shell: bash` use karta hai).

---

## STEP 9: GitHub Actions workflow

**.github/workflows/ci-cd.yml**
```yaml
name: Library CI-CD

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push image (unique tag = commit SHA)
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/library-app:${{ github.sha }}

  deploy:
    needs: build
    runs-on: self-hosted
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set image in manifest
        shell: bash
        run: |
          sed -i "s|DOCKERHUB_USER|${{ secrets.DOCKERHUB_USERNAME }}|g; s|IMAGE_TAG|${{ github.sha }}|g" k8s/deployment.yaml
          cat k8s/deployment.yaml

      - name: Deploy to Kubernetes
        shell: bash
        run: |
          kubectl apply -f k8s/deployment.yaml
          kubectl apply -f k8s/service.yaml
          kubectl rollout status deployment/library-app --timeout=120s
```

`github.sha` har commit ka alag hota hai, to Push 1 aur Push 2 ke image tags automatically unique honge.

---

## STEP 10: PUSH 1 (pehla aur sirf ek push)

VS Code terminal mein:
```bash
git init
git branch -M main
git add .
git commit -m "Push 1: add and view books"
git remote add origin https://github.com/<your-username>/library-cicd.git
git push -u origin main
```

Ab GitHub repo ke **Actions** tab mein pipeline dekho: test → build → deploy teeno green hone chahiye.

---

## STEP 11: Push 1 deployment verify karo

```bash
kubectl get pods
kubectl get svc
kubectl describe deployment library-app | findstr Image     # Linux/Mac: grep Image
minikube service library-service --url
```
URL browser mein kholo, ek book add karo aur view karo. **Screenshots** lo: Actions green run, Docker Hub tag, `kubectl get pods/svc`, browser output.

---

## STEP 12: Push 2 ke liye code modify karo (Issue Book)

**app.py** ko is naye version se replace karo:
```python
from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)
books = []


def add_book(title, author):
    if not title or not author or not title.strip() or not author.strip():
        return False
    books.append({"id": len(books) + 1,
                  "title": title.strip(),
                  "author": author.strip(),
                  "available": True})
    return True


def get_books():
    return books


def issue_book(book_id):
    for b in books:
        if b["id"] == book_id:
            if b["available"]:
                b["available"] = False
                return True
            return False
    return False


PAGE = """
<!doctype html>
<title>Library</title>
<h1>Library Book Management</h1>
<p><a href="/">Menu</a> | <a href="/add">1. Add Book</a> | <a href="/books">2. View Available Books</a> | <a href="/issue">3. Issue Book</a></p>
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
    <tr><th>ID</th><th>Title</th><th>Author</th><th>Status</th></tr>
    {% for b in books %}
    <tr><td>{{ b.id }}</td><td>{{ b.title }}</td><td>{{ b.author }}</td>
        <td>{{ 'Available' if b.available else 'Issued' }}</td></tr>
    {% endfor %}
  </table>
  {% else %}<p>No books yet.</p>{% endif %}
{% elif mode == 'issue' %}
  <h2>Issue a Book</h2>
  {% if message %}<p><b>{{ message }}</b></p>{% endif %}
  <form method="post">
    Book ID: <input name="book_id" type="number"><br><br>
    <button type="submit">Issue</button>
  </form>
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


@app.route("/issue", methods=["GET", "POST"])
def issue():
    message = None
    if request.method == "POST":
        try:
            bid = int(request.form.get("book_id"))
            message = ("Book issued successfully!" if issue_book(bid)
                       else "Book not found or already issued.")
        except (TypeError, ValueError):
            message = "Enter a valid book ID."
    return render_template_string(PAGE, mode="issue", message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

**test_app.py** mein ye tests add karo (upar `from app import ... issue_book` bhi import karo):
```python
from app import app, add_book, get_books, issue_book, books


def test_issue_book():
    add_book("Python 101", "Guido")
    assert issue_book(1) is True
    assert get_books()[0]["available"] is False


def test_issue_already_issued_book_fails():
    add_book("Python 101", "Guido")
    issue_book(1)
    assert issue_book(1) is False


def test_issue_invalid_id():
    assert issue_book(99) is False


def test_issue_route():
    client = app.test_client()
    client.post("/add", data={"title": "Clean Code", "author": "Martin"})
    res = client.post("/issue", data={"book_id": "1"})
    assert b"issued successfully" in res.data
```
Purane tests bhi rakho, bas file ke top par `setup_function` wala `books.clear()` rehne do.

Local `pytest` chala ke confirm karo ki sab pass hain.

---

## STEP 13: PUSH 2 (doosra aur last push)

```bash
git add .
git commit -m "Push 2: add issue book option and availability"
git push
```

Runner terminal chalta rehna chahiye. Actions tab mein naya run dekho. Naya commit SHA = naya Docker tag.

---

## STEP 14: Push 2 verify karo

```bash
kubectl get pods
kubectl describe deployment library-app | findstr Image
minikube service library-service --url
```
- Image tag ab Push 1 se **alag** hona chahiye.
- Browser mein book add karo, **Issue Book** se issue karo, phir View mein status **Issued** dikhna chahiye.
- Docker Hub par ab **2 alag tags** dikhne chahiye.

---

## Common problems aur fix

| Problem | Fix |
|---|---|
| Deploy job "Waiting for runner" | Self-hosted runner terminal chalu karo |
| `ImagePullBackOff` | Docker Hub repo public rakho, ya username/secret check karo |
| `sed: not found` (Windows) | Git Bash install karo, `shell: bash` already diya hai |
| `kubectl` runner se kaam nahi kar raha | Runner usi machine par chalao jahan `minikube start` hua hai |
| Docker login fail | Secrets ke naam exact `DOCKERHUB_USERNAME` aur `DOCKERHUB_TOKEN` hon |
| Port access nahi ho raha | `minikube service library-service --url` ka URL use karo |

**Important:** Sirf 2 baar `git push` karna hai. Isliye push se pehle sab kuch (secrets, runner, minikube) ready rakho, aur local par pytest pass karke hi push karo.

Agar kisi step par error aaye to error message yahan paste kar do, main fix bata dunga.