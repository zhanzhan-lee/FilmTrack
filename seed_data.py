from app import create_app, db
from app.models import User, Film, Camera, Lens, Roll, Photo
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

app = create_app()

with app.app_context():
    # 🧽 Clear old data (note that it is only used in the development stage)
    db.session.query(Photo).delete()
    db.session.query(Roll).delete()
    db.session.query(Film).delete()
    db.session.query(Camera).delete()
    db.session.query(Lens).delete()
    db.session.query(User).delete()
    db.session.commit()

    # user
    user = User(
        username="admin",
        password=generate_password_hash("123456")
    )
    db.session.add(user)
    db.session.commit()

    # films

    films = [
        Film(name="Portra 400", brand="Kodak", iso="400", format="35mm", user_id=user.id),
        Film(name="HP5 Plus", brand="Ilford", iso="400", format="35mm", user_id=user.id),
        Film(name="Superia X-TRA 400", brand="Fujifilm", iso="400", format="35mm", user_id=user.id)
    ]

    # cameras
    cameras = [
        Camera(name="Nikon F", brand="Nikon", type="SLR", format="35mm", user_id=user.id),
        Camera(name="Leica IIIG", brand="Leica", type="Rangefinder", format="35mm", user_id=user.id)
    ]

    # lens
    lenses = [
        Lens(name="Nikkor 50mm f/1.4", brand="Nikon", mount_type="F", user_id=user.id),
        Lens(name="Canon 35mm f/2.8 LTM", brand="Canon", mount_type="LTM", user_id=user.id)
    ]

    db.session.add_all(films + cameras + lenses)
    db.session.commit()

    # Create Roll
    roll_names = ["City Walk", "Family Weekend", "Test Shots"]
    base_date = datetime(2025, 1, 1)
    rolls = []

    for i in range(3):
        roll = Roll(
            roll_name=roll_names[i],
            film_id=films[i % len(films)].id,
            user_id=user.id,
            start_date=base_date + timedelta(days=i * 5),
            end_date=base_date + timedelta(days=i * 5 + 2),
            status="scanned",
            notes=f"Example roll {i+1}"
        )
        db.session.add(roll)
        rolls.append(roll)

    db.session.commit()

    # 📸  Add photos (5 per roll)
    shutter_speeds = ["1/30", "1/60", "1/125", "1/250", "1/500"]
    apertures = ["f/2.0", "f/2.8", "f/4.0", "f/5.6", "f/8.0"]
    locations = ["Perth City", "Fremantle", "Kings Park", "UWA", "Cottesloe"]

    for i, roll in enumerate(rolls):
        for j in range(5):
            # Only add 3 for the first roll
            if i == 0 and j < 2:
                continue

            photo = Photo(
                user_id=user.id,
                roll_id=roll.id,
                camera_id=cameras[(i + j) % len(cameras)].id,
                lens_id=lenses[(j % len(lenses))].id,
                film_id=roll.film_id,
                shot_date=roll.start_date + timedelta(hours=j * 3),
                shutter_speed=random.choice(shutter_speeds),
                aperture=random.choice(apertures),
                iso=str(films[i % len(films)].iso),
                frame_number=str(j + 1),
                location=random.choice(locations)
            )
            db.session.add(photo)

    # Add some photos for a different user as well
    for i, roll in enumerate(rolls):
        for j in range(2):
            photo = Photo(
                user_id=100,
                roll_id=roll.id,
                camera_id=cameras[(i + j) % len(cameras)].id,
                lens_id=lenses[(j % len(lenses))].id,
                film_id=roll.film_id,
                shot_date=roll.start_date + timedelta(hours=j * 3),
                shutter_speed=random.choice(shutter_speeds),
                aperture=random.choice(apertures),
                iso=str(films[i % len(films)].iso),
                frame_number=str(j + 1),
                location=random.choice(locations)
            )
            db.session.add(photo)

    db.session.commit()
    print("✅ Sample data inserted successfully using new model structure.")
