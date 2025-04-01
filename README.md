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
  
---



# Theme Ideation

## **💡1.FilmTrack**
### 🧠 One-sentence summary:

> **FilmTrack** helps film photographers track their gear and shoots, and visualize their habits — like a smart photo logbook with charts and maps.
### 💡What are we building?

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

---

## 2. Music Practice Tracker
### 🧠 One-sentence summary:

> Helps musicians keep on top of their practice by tracking song progress, identifying skill progression and competition with friends.

### 🤔 What do musicians need?
   - Musicians need to develop specific skills in order to learn and play songs
   - Developing skills requires **repeated practice**, and is something that should be tracked
        - Skills include **instrument specific techniques** such as guitar picking, or **general musical skills** such as rhythm
   - On top of developing skills, musicians need ways to keep track of what songs/parts of songs they have learned, and how long since they have practiced them
   - Additionally, simply having a list of songs that they can play can be useful for **auditions**, **confidence**, or to meet likeminded musicians

### ✅ What can users do?

- Create an account, including a **profile picture**, **favourite genre**, etc.
- Add specific **songs** they are practicing/know how to play
   - Track progress of learning songs, such as a checklist of having learned the **chorus**, **solo** etc.
   - Identify when song was last practiced, to allow the app to remind users to practice this song after a certain amount of time (**spaced repetition**)
   - Upload audio recordings of songs over time to clearly hear progression
   - Add text notes about certain parts/timestamps, etc.
- Add specific **instruments** that they can play
     - Similar to songs, users can track their progress in practicing instrument specific skills
- Automatically see best known songs, and songs that require the most practice
- Compete with friends, such as leaderboards of practice time, or songs learned etc.
- Record custom practice exercises

### 📊 What does the system analyze?

- Most/least praticed songs
- **Detailed** song practice progress
- Time since last practiced
- Most common genres/artists/albums etc.

### 🎯 Why is this a good project?

- Practice is absolutely imperative for musicians, and repetition is vital
- **Meets all Unit requirements: data input, auto-analysis, visualization, sharing**
- No good app currently exists to track this, while using paper can be difficult to keep track of learning hundreds of songs
- Will look visually cool, as we can include nice grid views of songs and images of their album covers, as well as their colour indicating their last practice date
- Usings friends/leaderboards is a cool way to meet the sharing requirement 
