Perfect — now that I’ve confirmed your Blueprint registration is done in the **top-level `__init__.py` file inside your Flask app module**, here’s the finalized **English `.md` documentation** reflecting that setup:

---

# 📘 Flask Blueprint Structure Documentation

This project follows a modular design using **Flask Blueprints**, which enables clean code separation and easier maintenance. All Blueprints are registered in the **top-level `app/__init__.py`** file (not in `routes/__init__.py` or `run.py`).

---

## 🔧 Blueprint Modules Overview (`app/routes/`)

| Blueprint       | File Name       | Responsibilities |
|------------------|------------------|-------------------|
| `main`           | `main.py`        | Homepage (`/`), basic pages like intro/about |
| `auth`           | `auth.py`        | User authentication: login, register, logout |
| `upload`         | `upload.py`      | Uploading cameras, lenses, films, and photos |
| `stats`          | `stats.py`       | Statistical views and user activity analysis |
| `share`          | `share.py`       | Sharing charts and insights |

Each Blueprint is imported and registered manually inside `app/__init__.py`.

---

## 🧩 Blueprint Registration in `app/__init__.py`

```python
from .routes.main import main
from .routes.auth import auth
from .routes.upload import upload
from .routes.stats import stats
from .routes.share import share

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(upload)
app.register_blueprint(stats)
app.register_blueprint(share)
```

- Blueprints are registered using `app.register_blueprint(...)` within the `create_app()` factory function.
- This also initializes Flask extensions like `SQLAlchemy` and `Flask-Login`.

---

## 📁 Template Organization (`app/templates/`)

| Blueprint | Associated Templates                        |
|-----------|---------------------------------------------|
| `main`    | `index.html`, `about.html`, `contact.html` |
| `auth`    | `login.html`, `register.html`              |
| `upload`  | `upload_camera.html`, etc.                 |
| `stats`   | `stats.html`                               |
| `share`   | `share.html`                               |

All templates extend a common base layout `base.html`.

---

## 📁 Static Resources (`app/static/`)

- **CSS Files**
  - `navbar.css`: Navbar styling
  - `stats.css`: Styling for charts and insights pages

- **JS Files**
  - `base-navbar.js`: Navbar interactivity
  - `stats-charts.js`: Renders statistical graphs

---

## ✅ Best Practices

- Each module is scoped to a specific functionality for modularity.
- Blueprint names and file names match for clarity.
- Keep template and static files aligned with their corresponding Blueprint.
- Register all Blueprints centrally in `app/__init__.py` for maintainability.

---

📄 **Author:** Project Team  
🕒 **Last Updated:** April 21, 2025  

---

需要我保存成 `Blueprint_Structure.md` 并生成文件吗？可以直接下载使用。