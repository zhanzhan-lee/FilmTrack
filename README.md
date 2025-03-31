# CITS3403-Group11-2025


## ✅ **Project Requirements (Summary)**

### 📌 **Core Functional Requirements**
1. **User Registration/Login**  
   - Users must be able to create an account or log in.

2. **Upload Data**  
   - Users can upload private data (any format: manual, file, external source).

3. **Automated Data Analysis**  
   - The app automatically analyzes the uploaded data.

4. **Data Visualization**  
   - Results must be visualized (charts, maps, text summary, etc.).

5. **Selective Sharing**  
   - Users can share their data/analysis with **specific** other users.

---

### 📄 **Required Views (Pages)**
1. **Introductory View**  
   - Explains app purpose, allows sign-up/login.

2. **Upload Data View**  
   - Interface for uploading or entering data.

3. **Visualize Data View**  
   - Shows visual analysis of user’s own or shared data.

4. **Share Data View**  
   - Selectively share data/results with chosen users.

---

### 🎯 **Design Principles**
- **Engaging**: Visually appealing, keeps user interested.  
- **Effective**: Provides useful value (info, insight, or community).  
- **Intuitive**: Easy to understand and navigate.

---



### ⚠️ **Important Rules**
- **Do NOT start coding until after Week 6 lecture.**
- Focus only on **discussing the application purpose and idea** with your team now.
- Ask facilitators if you’re unsure about your idea’s suitability.

# Theme Ideation

## **💡1.FilmTrack**
### 🧠 One-sentence summary:

> **FilmTrack** helps film photographers track their gear and shoots, and visualize their habits — like a smart photo logbook with charts and maps.
### What are we building?

   **FilmTrack** is a web app for **film photography lovers** to:

   - Record what they used to shoot (camera, lens, film, settings)
   - See **automatic analysis** of their shooting habits
   - Visualize results using **charts, maps, and labels**
   - Share their photo logs with others
### 🤔 What is film photography?

- It uses **old-school cameras with film rolls** (e.g. 36 shots per roll)
- You **manually set** the shutter speed, aperture, focus
- You can't preview photos — you wait to develop the film
- Film costs money and time, so each shot matters

📒 Many film photographers write down info after each shoot.  
FilmTrack helps **digitize, organize, and visualize** that info.

### 🧱 How is the data organized?

We use 4 levels to keep everything structured:

```
User
 └── Camera (e.g. Leica iiiG)
       └── Lens (e.g. elmar 50mm f/3.5)
             └── Film Roll ( KodakGold200> one shooting session)
                   └── Shot (each photo's settings + preview)
```

### ✅ What can users do?

- Create account, manage their **cameras & lens list**
- Add new **film roll records**
- Upload **preview photos** and photo settings
- Automatically see:
  - Most used film/lens/camera
  - Shooting trends over time
  - Shooting locations on a map
- Display **labels under each photo** (e.g. camera + film + settings)
- Share a film roll or summary via link
### 📊 What does the system analyze?

- 🎞️ Most used film type
- 🔍 Most used lens or camera
- 🕐 Monthly shooting trends
- 🗺️ Where the user shoots (map view)
- 📷 Common settings (e.g. shutter speed, ISO)
- 🏷️ Labels under each photo like:  
  `Leica iiiG | elmar 50mm f/3.5 | Kodak Gold 200 | 1/250s | f/5.6`

### 🎯 Why is this a good project?

- Real photographers need this — most use notebooks or Excel
- **Meets all Unit requirements: data input, auto-analysis, visualization, sharing**
- Data structure is clean and great for learning full-stack dev
- Looks good (photos + charts + maps)
- No real competitor exists — we’re solving a real niche problem
