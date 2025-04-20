

# 📷 Database Structure Documentation  


---

## 🧑‍💼 1. `User` – User Table

Represents a registered user in the system. Each user can own their own cameras, lenses, films, rolls (film sessions), and photos.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer (PK) | Unique user ID |
| `username` | String | Unique username |
| `password` | String | Hashed password |

### Relationships

- A user can own:
  - Multiple `Camera`, `Lens`, and `Film` entries
  - Multiple `Roll` entries (film shooting sessions)
  - Multiple `Photo` entries (each photo is linked to a user)

---

## 📷 2. `Camera` – Camera Table

Represents a film camera owned or used by the user.

| Field | Type | Description |
|-------|------|-------------|
| `id` | PK | Camera ID |
| `name` | String | Camera model (e.g. "Leica IIIG") |
| `brand` | String | Manufacturer (e.g. Leica, Nikon) |
| `type` | String | Type: SLR / Rangefinder / Compact |
| `format` | String | Film format: 35mm / 120 etc |
| `is_public` | Boolean | Whether it's a system-wide preset |
| `image_path` | String | Optional photo of the camera |
| `user_id` | FK → User.id | Owner of the camera |

---

## 🔍 3. `Lens` – Lens Table

Represents a lens used during photography.

| Field | Type | Description |
|-------|------|-------------|
| `id` | PK | Lens ID |
| `name` | String | Lens model name |
| `brand` | String | Brand |
| `mount_type` | String | Mount type (e.g. M-mount, F-mount) |
| `is_public` | Boolean | Whether it's system-defined |
| `user_id` | FK → User.id | Owner |

---

## 🎞 4. `Film` – Film Type Table

Represents a **film stock definition**, e.g. "Kodak Portra 400".

> ✅ **Note:** This is a product/model definition, **not an actual film roll**.

| Field | Type | Description |
|-------|------|-------------|
| `id` | PK | Film ID |
| `name` | String | Film name (e.g. Portra 400) |
| `brand` | String | Film brand (e.g. Kodak) |
| `iso` | String | ISO rating (e.g. 400) |
| `format` | String | Film format: 35mm / 120 |
| `is_public` | Boolean | Whether it's a system-preset |
| `user_id` | FK → User.id | Creator of the film entry (if user-defined) |

---

## 📦 5. `Roll` – Film Session Table  

Represents **a single roll of film being used in the real world**. Used for grouping photos, tracking the start/end date of a shooting session.

> 📌 Roll is optional for each photo, but useful for organizing projects or sessions.

| Field | Type | Description |
|-------|------|-------------|
| `id` | PK | Roll ID |
| `film_id` | FK → Film.id | Which film type was used |
| `user_id` | FK → User.id | Owner |
| `roll_name` | String | Optional label for the roll (e.g. "JapanTrip_HP5") |
| `start_date` / `end_date` | DateTime | Date range of use |
| `status` | String | "in use", "scanned", "developed" etc |
| `notes` | Text | Optional notes |

---

## 📸 6. `Photo` – Individual Photo Table (Core Data)

Represents a **single shutter release**: one frame shot on a film roll.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | PK | Photo ID |
| `user_id` | FK → User.id | Photographer |
| `roll_id` | FK → Roll.id (optional) | Which roll this photo belongs to |
| `camera_id` | FK → Camera.id | Camera used |
| `lens_id` | FK → Lens.id (optional) | Lens used |
| `film_id` | FK → Film.id (optional) | Film used |
| `image_path` | String | Image path or scan (optional) |
| `shot_date` | DateTime | Time of the shot |
| `shutter_speed` | String | e.g. "1/250" |
| `aperture` | String | e.g. "f/2.8" |
| `iso` | String | ISO used |
| `frame_number` | String | Frame number on the roll (e.g. 15) |
| `location` | String | Shot location |

---

## 🔗 Entity Relationships Overview

```text
User ──< Camera
     └─< Lens
     └─< Film
     └─< Roll ──< Photo
                └── camera_id → Camera
                └── lens_id → Lens
                └── film_id → Film
```

- `User` owns all data.
- `Photo` directly links to equipment used and optionally to a `Roll`.
- `Roll` is for grouping photos, not enforcing camera/lens selection.

---

## 📊 Guide for Data Analysis (stats.html)

| Task | Source Table | Fields | Notes |
|------|--------------|--------|-------|
| Most used film | `Photo` or `Roll` | `film_id` | Count film usage |
| Most used camera/lens | `Photo` | `camera_id`, `lens_id` | group_by & count |
| Exposure trends | `Photo` | `shutter_speed`, `aperture`, `iso` | Build histograms |
| Time trend | `Photo` | `shot_date` | Monthly/weekly charts |
| Heatmap (day+hour) | `Photo` | `shot_date` | Weekday + hour split |
| Location map | `Photo` | `location` | For maps / tag clouds |

---

## 🧠Confusing concepts !!!



### 1. Why do film cameras use film roll? What is that


> In short:  
> 🎞️ A **film Roll** is like a **hardware-constrained, analog memory card**, that is:
> - fixed in size (e.g. 36 shots),
> - non-reusable,
> - requires offline “export” (development),
> - and stores photos you can only see later.

---

### 2. 🎞️ What’s the Difference Between the Tabe: `Film` and `Roll`?

#### 📦 `Film` = **The Film Stock Definition**

`Film` in the database refers to the **type of film** — like a product definition.

It describes:
- Brand (e.g. Kodak, Ilford)
- Model (e.g. Portra 400, HP5 Plus)
- ISO rating (e.g. 400)
- Format (35mm / 120)

This is a static entity. Every photographer can use the same `Film` definition, but they use it in the form of rolls.

> 🟡 **Think of it like a product catalog entry.**

---

#### 🎞 `Roll` = **A Real-Life Film Roll Being Used**

A `Roll` represents a single **physical film roll** that a user actually used in their camera.

Each roll:
- Is based on a specific `Film` model
- Has a user-defined name (e.g. “March Trip – Portra 400”)
- Records the start and end of shooting dates
- Tracks status (e.g. “in use”, “scanned”, “developed”)
- Contains multiple `Photo` records

> 🟢 **Think of it as the "instance" of using that film stock.**

---

### 📸 Real-World Analogy

Imagine you buy a 5-pack of **Kodak Portra 400** film (same `Film` definition).  
You load one roll into your Nikon F camera and shoot it during a weekend trip.

You just created:
- A new **`Roll`** for that trip (with `film_name` → Portra 400)
- 36 **`Photo`** records — one for each shutter press

Each photo:
- Records its own shutter/aperture/time
- Inherits the film via its roll
- May even use different lenses or shooting locations

---



