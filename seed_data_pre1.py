from app import create_app, db
from app.models import User, Film, Camera, Lens, Roll, Photo
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

app = create_app()

def clear_database():
    """Clear all existing data from the database."""
    db.session.query(Photo).delete()
    db.session.query(Roll).delete()
    db.session.query(Film).delete()
    db.session.query(Camera).delete()
    db.session.query(Lens).delete()
    db.session.query(User).delete()
    db.session.commit()

def create_users():
    """Create sample users."""
    users = [
        User(username="admin", password=generate_password_hash("123456")),
        User(username="user1", password=generate_password_hash("password1")),
        User(username="user2", password=generate_password_hash("password2"))
    ]
    db.session.add_all(users)
    db.session.commit()
    return users

def create_films(users):
    """Create sample films for each user."""
    films = [
        Film(name="Portra 400", brand="Kodak", iso="400", format="35mm", user_id=users[0].id, image_path="Portra 400.jpg"),
        Film(name="Kodak gold 200", brand="Kodak", iso="200", format="35mm", user_id=users[0].id, image_path="Kodak gold 200.png"),
        Film(name="Velvia 100", brand="Fujifilm", iso="100", format="35mm", user_id=users[0].id, image_path="Velvia 100.jpg"),
        Film(name="Superia X-TRA 400", brand="Fujifilm", iso="400", format="35mm", user_id=users[2].id)
    ]
    db.session.add_all(films)
    db.session.commit()
    return films

def create_cameras(users):
    """Create sample cameras for each user."""
    cameras = [
        Camera(name="Nikon F", brand="Nikon", type="SLR", format="35mm", user_id=users[0].id, image_path="nikon_f.jpg"),
        Camera(name="Canon AE-1", brand="Canon", type="SLR", format="35mm", user_id=users[0].id),
        Camera(name="Leica IIIG", brand="Leica", type="Rangefinder", format="35mm", user_id=users[0].id, image_path="leica_iiig.jpg"),
        Camera(name="Pentax K1000", brand="Pentax", type="SLR", format="35mm", user_id=users[2].id)
    ]
    db.session.add_all(cameras)
    db.session.commit()
    return cameras

def create_lenses(users):
    """Create sample lenses for each user."""
    lenses = [
        Lens(name="Nikkor 50mm f/1.4", brand="Nikon", mount_type="F", user_id=users[0].id),
        Lens(name="Leitz 50mm f/3.5 Elmar", brand="Leitz", mount_type="L39", user_id=users[0].id, image_path="leitz_50mm_elmar.jpg"),
        Lens(name="Canon FD 50mm f/1.8", brand="Canon", mount_type="FD", user_id=users[1].id),
        Lens(name="Pentax 50mm f/2", brand="Pentax", mount_type="K", user_id=users[2].id)
    ]
    db.session.add_all(lenses)
    db.session.commit()
    return lenses

def create_rolls(users, films):
    """Create sample rolls for each user."""
    roll_names = ["City Walk", "Family Weekend", "Test Shots", "Holiday Trip"]
    base_date = datetime(2024, 1, 1)
    rolls = []

    for i, user in enumerate(users):
        for j in range(2):  # Two rolls per user
            roll = Roll(
                roll_name=f"{roll_names[j]} ",
                film_id=films[(i + j) % len(films)].id,
                user_id=user.id,
                start_date=base_date + timedelta(days=i * 10 + j * 5),
                end_date=base_date + timedelta(days=i * 10 + j * 5 + 2),
                status="in use",
                notes=f"Example roll {j+1} for {user.username}"
            )
            db.session.add(roll)
            rolls.append(roll)

    db.session.commit()
    return rolls

def create_photos(users, rolls, cameras, lenses, films):
    """Create sample photos for each roll, spread out over the year."""
    shutter_speeds = ["1/30", "1/60", "1/125", "1/250", "1/500"]
    apertures = ["f/2.0", "f/2.8", "f/4.0", "f/5.6", "f/8.0"]
    locations = ["Perth City", "Fremantle", "Kings Park", "UWA", "Cottesloe"]
    current_date = datetime.now()

    for roll in rolls:
        for j in range(5):  # Five photos per roll
            # Spread the shot_date between the roll's start_date and the current date
            days_difference = (current_date - roll.start_date).days
            random_days_offset = random.randint(0, days_difference)
            shot_date = roll.start_date + timedelta(days=random_days_offset)

            photo = Photo(
                user_id=roll.user_id,
                roll_id=roll.id,
                camera_id=cameras[j % len(cameras)].id,
                lens_id=lenses[j % len(lenses)].id,
                film_id=roll.film_id,
                shot_date=shot_date,
                shutter_speed=random.choice(shutter_speeds),
                aperture=random.choice(apertures),
                iso=str(films[j % len(films)].iso),
                frame_number=str(j + 1),
                location=random.choice(locations)
            )
            db.session.add(photo)

    db.session.commit()

with app.app_context():
    # Clear existing data
    clear_database()

    # Create sample data
    users = create_users()
    films = create_films(users)
    cameras = create_cameras(users)
    lenses = create_lenses(users)
    rolls = create_rolls(users, films)
    create_photos(users, rolls, cameras, lenses, films)

    print("✅ Sample data inserted successfully.")