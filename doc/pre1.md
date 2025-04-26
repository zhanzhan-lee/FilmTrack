

#  Lab 1 Presentation - Preparation Instructions

# 1. **Setup**

#### 1.1. Pull the Latest Code
Make sure you are on the latest `develop` branch.

```bash
git checkout develop
git pull origin develop
```


#### 1.2. Seed the Database

Run the following script to insert sample data:

```bash
python3 seed_data_pre1.py
```

✅ This will populate the database with users, sample entries, and some data for the GUI.


#### 1.3. Set Up Uploads Folder

1. Go to the Discord group chat and **download the uploads.zip** file sent earlier.
2. Extract the contents of `uploads.zip`.
3. Place the extracted folder **inside** your project at:

```
/app/static/uploads
```

✅ After this step, you will have several **images** and **text samples** available for display on  pages.


---


### `⚠️Next is some content that may be needed for presentation`


# **2. Project Theme and Basic Concepts**

#### 2.1 Basic Process of Film Photography

Film photography typically involves:

1. **Loading the film**  
   Inserting a roll of light-sensitive film into the camera.

2. **Taking photos**  
   Pressing the shutter exposes the film to light, creating a hidden (latent) image.  
   Settings like shutter speed, aperture, and ISO must be manually set.

3. **Developing the film**  
   Chemical processing makes the hidden images visible.

4. **Scanning or printing**  
   Developed film is either scanned into digital form or printed.

🧠 **Core idea**:  
> Film reacts to light and is chemically developed into visible photos.



#### 2.2 Background and Motivation

With the rise of **retro culture**, more people — beginners and veterans — are returning to film photography.

However, **classic mechanical cameras** (like Leica, Nikon F):
- **Do not automatically save** shooting parameters;
- And **each exposure is precious** (📷 **around $1–$3 per shot**, including film and development).

Unlike digital cameras, film users must manually record important shooting details, or they will be lost.



#### 2.3 Project Purpose⚠️

Our project, **FilmTrack**, addresses this by:

- Helping users **log** their cameras, lenses, film, and exposure settings;
- Offering **visual insights** into shooting habits;
- **Preserving memories** behind every single shutter press.

---



# **3. FilmTrack Pages Overview**

| Page | File | Description (How to Introduce) |
|:-----|:-----|:-------------------------------|
| **Home** | `index.html` | Landing page. Brief welcome and navigation intro. Explain what FilmTrack is for. |
| **Rolls** | `shooting.html` | Manage shooting records ("Rolls"). |
| **Gears** | `gear.html` | Manage personal cameras, lenses, films. Shows gear cards. Add/edit gears using modals. |
| **Stats** | `stats.html` | Visual analysis of shooting habits. (Currently placeholder charts for gear usage and exposure trends.) |
| **Share** | `share.html` | Generate public links for selected Rolls or Stats. (Placeholder page.) |
| **Shared Stats** | `shared_stats.html` | Browse shared statistics from other users. (Placeholder page.) |

### 3.0🏠home; login; register 💡`Brief`
**Page File**: `index.html` `login.html` `register.html`



### 3.1🎞️ Rolls Page Overview 💡`Detailed`

**Page File**: `shooting.html`

The **Rolls page** is divided into two main sections:

| Section | Description |
|:--------|:------------|
| **Rolls In Use** | Displays rolls that are currently active (Loaded into the camera). <br> When creating a new Roll, users select an existing **Film** from their Gear collection.<br>💡**Click roll to edit,When you put the mouse on the roll, there will be a shaking animation, which can show.** |
| **Rolls Developed** | Displays rolls that have been finished and developed. <br> Users can upload scanned images for each shot and record exposure parameters (e.g., shutter speed, aperture, ISO).💡**Click roll to edit** |


### 3.2📷 Gears Page Overview 💡`Brief`

**Page File**: `gear.html`

The **Gears page** is divided into three sections:

| Section | Description |
|:--------|:------------|
| **Cameras** | Displays the user's camera collection. Each card shows the model, brand, and type. |
| **Lenses** | Displays the user's lenses, including basic specs like focal length and mount type. |
| **Film** | Displays available film stocks, showing film brand, name, and ISO information. |

💡Click on the card to enter the edit pop-up window to edit or delete, or click add card to add new gear



### 3.3📊 Stats Page Overview💡Detailed

**💡You must know this better than me, can show this in detail in the lab.**

### 3.4🔗 Share Page Overview 💡`Brief+`

**Page File**: `share.html`

- On this page, users **select** what data they want to share, **choose a time range**, and **specify recipients**.
- There is an **option to control** whether others can export the shared data as a PDF.
- Users can also **manage existing shared items** (revoke access if needed).

### 3.5👀 Shared Stats Page Overview 💡`Brief`

**💡Brief description**



---
**The above breakdown is only a suggestion.
Please feel free to adjust the flow and speaking details according to the actual situation during the presentation.**