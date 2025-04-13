
### ✅ Step 1: Clone the repo (if you haven't already)
If you haven't cloned the GitHub repo to your local machine:

```bash
git clone https://github.com/your-team-name/your-repo-name.git
cd your-repo-name
```

---

### ✅ Step 2: Pull the latest changes (if you already cloned)
If you already have the repo on your computer, first make sure you're up to date:

```bash
git checkout develop     # or 'main' if you prefer
git pull origin develop
```

---

### ✅ Step 3: Create your own feature branch
Create a new branch from the one you just pulled:

```bash
git checkout -b your-branch-name
```

Example:  
```bash
git checkout -b intro-layout-jay
```

---

### ✅ Step 4: Do your work
Make changes in VS Code as usual.

Then stage and commit them:
```bash
git add .
git commit -m "Add intro layout"
```

---

### ✅ Step 5: Push your branch to GitHub
```bash
git push origin your-branch-name
```

---

### 🔁 After that:
We’ll merge everyone’s branches back into `develop` during our group meetings. This keeps things clean and avoids conflicts.

Let me know if you get stuck anywhere!

