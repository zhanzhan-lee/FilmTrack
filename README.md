

## 🚀 Project Setup

### Prerequisites

- **Operating System**: Ubuntu 24.04 (or WSL with Ubuntu 24.04)
- **Python Version**: Python 3.10 or later

---

### 🛠 Step-by-step Setup Guide

#### 1️⃣ Clone the Project

Start by cloning the project repository:

```bash
git clone https://github.com/your-GitHub-username/CITS3403-Group11-2025.git
cd CITS3403-Group11-2025
```

#### 2️⃣ Install Python and Virtual Environment Support

Make sure Python and the `python3-venv` module are installed on your machine. Run the following commands to install the necessary packages:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

#### 3️⃣ Create and Activate the Virtual Environment

Create a virtual environment to isolate project dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
```

Once activated, your terminal prompt should change to `(venv)`.

#### 4️⃣ Install Project Dependencies

With the virtual environment activated, install the required dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```

This will install all the necessary packages, including Flask and Flask-WTF.

#### 5️⃣ Run the Application 

Set the Flask app environment variables and start the application:

```bash
export FLASK_APP=run.py
export FLASK_ENV=development  # Enable debugging mode
flask run
```

Visit `http://127.0.0.1:5000` in your browser to see the app running.

---

## 🧭 Usage

- **Development Mode**: The application runs in development mode with auto-reloading enabled. Simply run `flask run` to start the app.
- **No Database Setup**: The project currently does not include any database configuration. You can focus on the core functionality of the application.

---

