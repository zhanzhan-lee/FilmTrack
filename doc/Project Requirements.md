# 🧩 Project Requirements

---

## 🎯 1. Theme Requirements (What our app must do)
We are required to build a **data analytics web application**. The application must:

### ✅ Include the following core views/pages:
| View | Description |
|------|-------------|
| **Intro / Login View** | A landing page that explains the purpose of the app and allows users to sign up or log in |
| **Upload Data View** | Allows users to upload or input data (manually or via files/devices) |
| **Visualise Data View** | Automatically analyses and displays the uploaded or shared data (e.g. via charts, graphs, summaries) |
| **Share Data View** | Enables users to selectively share results with specific other users of the system |

### ✅ Data and analysis are flexible
You can define what kind of data your app will use, and what "analysis" means in your context. Example ideas:
- **Fitness tracker**: upload workouts, track stats, share progress with friends.
- **Statistical tool**: upload CSV data, perform clustering, regression, etc.
- **Course planner**: upload course info, generate optimal study schedules.
- **Tournament manager**: input match results, show rankings, share with teams.
- **Disease outbreak visualizer**: upload location/time data, plot on map.
- **News sentiment analyzer**: run NLP analysis and score news articles.


---

## ⚙️ 2. Technical Requirements (How our app must be built)

Our application must be implemented using **only the following technologies**:

### 🖥️ **Frontend**

| Allowed | Description |
|---------|-------------|
| **HTML** | Structure and content of all pages |
| **CSS** | Styling via raw CSS or one of the following frameworks (you must choose only one):<br>- Bootstrap<br>- Tailwind CSS<br>- Semantic UI<br>- Foundation |
| **jQuery** | Required for all DOM manipulation and dynamic behavior |
| ❌ Not allowed | React, Angular, Vue, SASS/SCSS, other CSS frameworks or build tools |

---

### 🔁 **Frontend–Backend Communication**

| Allowed | Description |
|---------|-------------|
| **AJAX** | Use jQuery's AJAX methods to send/receive data |
| **WebSockets** | Optional: for real-time communication |
| ❌ Not allowed | `fetch` API, GraphQL, other modern libraries/frameworks for communication |

---

### 🧠 **Backend**

| Allowed | Description |
|---------|-------------|
| **Flask** | Must be used as the server-side web framework |
| ❌ Not allowed | Django, FastAPI, Express, Node.js, PHP, etc. |

---

### 🗃️ **Database**

| Allowed | Description |
|---------|-------------|
| **SQLite** | Must be used as the database backend |
| **SQLAlchemy** | All database interaction must go through SQLAlchemy ORM (no raw SQL allowed) |
| ❌ Not allowed | MySQL, PostgreSQL, MongoDB, Firebase, raw SQL queries |

---

### 📦 **Other Libraries (Optional/Allowed)**

You are free to use additional JavaScript or Python libraries to support features, **as long as they are not core tools**. Examples:

| Purpose | Examples |
|---------|----------|
| **Charts / Visualisation** | Chart.js, Plotly, D3.js |
| **NLP / Data Analysis** | TextBlob, NLTK, Scikit-learn, Pandas |
| **Maps / Geo Data** | Leaflet.js, Mapbox |
| **Styling / Icons** | Google Fonts, FontAwesome |

---

## 🛠️ Project Setup & GitHub Requirements

- Use a **private GitHub repository** for your group.
- Your `README.md` must include:
  - App purpose and usage description
  - A table with UWA ID, name, and GitHub username for each group member
  - Instructions to run the app
  - Instructions to run tests

### Final Submission:
- Make your GitHub repository **public** for marking
- Submit a `.zip` containing:
  - All source code (well-commented)
  - `requirements.txt` (generate with `pip freeze > requirements.txt`)
  - README file
  - Tests folder
  - Sample database (optional)
  - `deliverables/` folder
- ❗ **Do NOT include** the virtual environment folder or `.git/` — you will lose marks if submitted

---

## 📆 Project Timeline (Agile-based Deliverables)

| Stage | Date | Description |
|-------|------|-------------|
| 🔍 Idea & Planning | Now until Week 6 | Define your idea and team roles. No coding yet. |
| 🧪 **Design Presentation** | Week 8 (Apr 28 – May 2) | Present your concept & static HTML/CSS mockups (no backend logic) |
| ⚙️ **Functionality Demo** | Week 9 (May 5 – May 9) | Demo basic backend interaction (e.g. save data, display it) |
| 📦 **Final Project Submission** | Late May | Submit working app, codebase & documentation |
| 🎤 **Final Group Presentation** | Final Week | 12-minute demo + Q&A; all team members must present |

---

## 🤝 Agile & Collaboration Requirements

You will be assessed on your **development methodology**, not just your code. This includes:

- Use **GitHub Issues** to track features, bugs, and tasks
- Use **GitHub Projects** (kanban board) to manage progress
- Use **Pull Requests** for all new features, with reviews and meaningful commit messages
- Use **Git Tags** to mark intermediate milestones
- Collaborate clearly via GitHub, and ensure all team members contribute

---

