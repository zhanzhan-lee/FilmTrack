
#  Share Model Documentation 

---

##  Model Definition (`models.py`)

```python
class Share(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    note = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.now())

    # Content sharing controls
    share_exposure = db.Column(db.Boolean, default=False)
    share_aperture = db.Column(db.Boolean, default=False)
    share_favorite_film = db.Column(db.Boolean, default=False)
    share_gear = db.Column(db.Boolean, default=False)
    share_shoot_time = db.Column(db.Boolean, default=False)
    allow_pdf_export = db.Column(db.Boolean, default=False)

    from_user = db.relationship('User', foreign_keys=[from_user_id], backref='shares_made')
    to_user = db.relationship('User', foreign_keys=[to_user_id], backref='shares_received')

    __table_args__ = (
        db.UniqueConstraint('from_user_id', 'to_user_id', name='unique_user_share'),
    )
```

---

##  Functionality Overview

* Each `Share` entry represents a one-to-one sharing permission from one user to another.
* A user can only have **one active share record per recipient**.
* Selected data types and time range can be customized per share.
* Updating a share will overwrite any existing share from the same sender to the same recipient.
---

## 🔁 Update Logic Recommendation

Since the model enforces a unique constraint on `(from_user_id, to_user_id)`, always use **"find-or-update"** logic to avoid duplicate entries:

```python
existing = Share.query.filter_by(from_user_id=current_user.id, to_user_id=form.to_user.data).first()
if existing:
    # Update existing record
    existing.start_date = form.start_date.data
    existing.share_exposure = form.share_exposure.data
    ...
else:
    # Create new share
    new_share = Share(...)
    db.session.add(new_share)

db.session.commit()
```


---

## ✅ Share Field Reference

| Field                 | Controls Access To                      |
| --------------------- | --------------------------------------- |
| `share_exposure`      | Shutter speed / ISO distribution        |
| `share_aperture`      | Aperture usage chart                    |
| `share_favorite_film` | Favorite film usage                     |
| `share_gear`          | Camera / lens preferences               |
| `share_shoot_time`    | Shooting time patterns                  |
| `allow_pdf_export`    | Whether the recipient can export as PDF |

---




##  First-Time Migration Guide

For developers applying the `Share` model for the first time:

---

### ✅ 1. Install dependencies

Make sure your virtual environment is activated, then:

```bash
pip install -r requirements.txt
```

---

### ✅ 2. Initialize migration (only once)

If your project does not yet have a `migrations/` folder:

```bash
flask db init
```

---

### ✅ 3. Generate migration script

After adding the `Share` model to `models.py`:

```bash
flask db migrate -m "Add Share model"
```

---

### ✅ 4. Apply migration to database

```bash
flask db upgrade
```

---

###  Quick Command Recap

```bash
pip install -r requirements.txt
flask db init
flask db migrate -m "Add Share model"
flask db upgrade
```

---

If you later update the model, repeat `migrate` and `upgrade`.
In development only, you may reset migrations by deleting the `migrations/` folder (not recommended in production).

