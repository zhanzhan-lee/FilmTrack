from app import create_app, db
from app.models import User, Camera, Lens, Film, Photo, Roll
from werkzeug.security import generate_password_hash

app = create_app()

def clear_database():
    db.session.query(Camera).delete()
    db.session.query(Lens).delete()
    db.session.query(Film).delete()
    #db.session.query(Photo).delete()
    #db.session.query(Roll).delete()
    db.session.query(User).delete()
    db.session.commit()

def seed():
    # ---------- User 1: Alice ----------
    alice = User(username="alice", password=generate_password_hash("alice123"))
    db.session.add(alice)
    db.session.commit()

    alice_c1 = Camera(name="Leica IIIG", brand="Leica", type="Rangefinder", format="35mm", user_id=alice.id, image_path="leica_iiig.jpg")
    alice_c3 = Camera(name="Canon AE-1", brand="Canon", type="SLR", format="35mm", user_id=alice.id, image_path="canon_ae1.jpg")

    alice_l1 = Lens(name="Leitz Elmar 50mm f/3.5", brand="Leitz", mount_type="M39", user_id=alice.id, image_path="leitz_elmar_50.jpg")
    alice_l3 = Lens(name="Canon FD 50mm f/1.8", brand="Canon", mount_type="FD", user_id=alice.id, image_path="canon_fd_50_18.jpg")

    f2 = Film(name="Kodak Ektachrome E100", brand="Kodak", iso="100", format="35mm", user_id=alice.id, image_path="kodak_e100.jpg")
    f3 = Film(name="Kodak Portra 160", brand="Kodak", iso="160", format="35mm", user_id=alice.id, image_path="portra_160.jpg")
    f4 = Film(name="Fujifilm Velvia 100", brand="Fujifilm", iso="100", format="35mm", user_id=alice.id, image_path="velvia_100.jpg")
    f5 = Film(name="Ilford HP5 Plus 400", brand="Ilford", iso="400", format="35mm", user_id=alice.id, image_path="hp5_plus.jpg")

    db.session.add_all([alice_c1, alice_c3, alice_l1, alice_l3, f2, f3, f4, f5])

    # ---------- User 2: Bob ----------
    bob = User(username="bob", password=generate_password_hash("bob123"))
    db.session.add(bob)
    db.session.commit()

    bob_c1 = Camera(name="Nikon F", brand="Nikon", type="SLR", format="35mm", user_id=bob.id, image_path="nikon_f.jpg")
    bob_c2 = Camera(name="Nikon FM2", brand="Nikon", type="SLR", format="35mm", user_id=bob.id, image_path="nikon_fm2.jpg")
    bob_l1 = Lens(name="Nikkor-S 50mm f/1.4", brand="Nikon", mount_type="F", user_id=bob.id, image_path="nikkor_50_14.jpg")
    bob_l2 = Lens(name="Nikkor-P 105mm f/2.5", brand="Nikon", mount_type="F", user_id=bob.id, image_path="nikkor_105_25.jpg")
    f6 = Film(name="Kodak Ultramax 400", brand="Kodak", iso="400", format="35mm", user_id=bob.id, image_path="ultramax_400.jpg")
    f7 = Film(name="Kodak Portra 400", brand="Kodak", iso="400", format="35mm", user_id=bob.id, image_path="portra_400.jpg")

    db.session.add_all([bob_c1, bob_c2, bob_l1, bob_l2, f6, f7])

    # ---------- User 3: Carol ----------
    carol = User(username="carol", password=generate_password_hash("carol123"))
    db.session.add(carol)
    db.session.commit()

    carol_c1 = Camera(name="Hasselblad 500C", brand="Hasselblad", type="SLR", format="120", user_id=carol.id, image_path="hasselblad_500c.jpg")
    carol_c2 = Camera(name="Mamiya RB67", brand="Mamiya", type="SLR", format="120", user_id=carol.id, image_path="mamiya_rb67.jpg")
    carol_l1 = Lens(name="Carl Zeiss Planar 80mm f/2.8", brand="Zeiss", mount_type="V", user_id=carol.id, image_path="zeiss_planar_80.jpg")
    carol_l2 = Lens(name="Mamiya-Sekor 90mm f/3.8", brand="Mamiya", mount_type="RB67", user_id=carol.id, image_path="mamiya_90_38.jpg")
    f8 = Film(name="Fujifilm Velvia 50", brand="Fujifilm", iso="50", format="120", user_id=carol.id, image_path="velvia_50.jpg")
    f9 = Film(name="Kodak Portra 160", brand="Kodak", iso="160", format="120", user_id=carol.id, image_path="portra_160.jpg")

    db.session.add_all([carol_c1, carol_c2, carol_l1, carol_l2, f8, f9])

    db.session.commit()


with app.app_context():
    clear_database()
    seed()
    print("✅ Users and gear seeded with image names.")
