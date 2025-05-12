
## Project Setup

### 1. Prerequisites

- **Operating System**: 
    - **Recommand:** Ubuntu 24.04 (or WSL with Ubuntu 24.04)
    - Windows 11
    - MacOS
- **Python Version**: Python 3.10 or later

---

### 2. Step-by-step Setup Guide

#### 1️⃣ Clone the Project

Start by cloning the project repository:

```bash
git clone https://github.com/zhanzhan-lee/CITS3403-Group11-2025.git
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
- **Linux / macOS / WSL:**
```bash
python3 -m venv venv
source venv/bin/activate
```
- **Windows**
```bash
python3 -m venv venv_win
.\venv_win\Scripts\activate   
```


Once activated, your terminal prompt should change to `(venv)` or `(venv_win)`.

#### 4️⃣ Install Project Dependencies

With the virtual environment activated, install the required dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```

This will install all the necessary packages, including Flask and Flask-WTF.

#### 5️⃣ Run the Application 


```bash
flask run
```

Visit `http://127.0.0.1:5000` in your browser to see the app running.

---

## 3. Usage

- **Development Mode**: The application runs in development mode with auto-reloading enabled. Simply run `flask run` to start the app.

---

