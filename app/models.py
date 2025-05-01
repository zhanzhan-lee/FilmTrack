from flask_login import UserMixin
from app import db



# -------------------------
# User
# -------------------------
class User(db.Model, UserMixin):  # ⬅ 加上 UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    image_path = db.Column(db.String(200))
    
    cameras = db.relationship('Camera', backref='owner', lazy=True)
    lenses = db.relationship('Lens', backref='owner', lazy=True)
    films = db.relationship('Film', backref='owner', lazy=True)
    rolls = db.relationship('Roll', backref='user', lazy=True)
    photos = db.relationship('Photo', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

# -------------------------
# Camera
# -------------------------
class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    brand = db.Column(db.String(50))
    type = db.Column(db.String(50))        # SLR, Rangefinder, etc
    format = db.Column(db.String(50))      # 35mm, 120, etc
    is_public = db.Column(db.Boolean, default=False)
    image_path = db.Column(db.String(200)) # optional image
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    photos = db.relationship('Photo', backref='camera', lazy=True)

    def __repr__(self):
        return f'<Camera {self.brand} {self.name}>'

# -------------------------
# Lens
# -------------------------
class Lens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50))
    mount_type = db.Column(db.String(50))
    is_public = db.Column(db.Boolean, default=False)
    image_path = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    
    photos = db.relationship('Photo', backref='lens', lazy=True)


    def __repr__(self):
        return f'<Lens {self.brand} {self.name}>'
    
# -------------------------
# Film
# -------------------------
class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50))
    iso = db.Column(db.String(20))
    format = db.Column(db.String(20))     # e.g. 35mm, 120
    is_public = db.Column(db.Boolean, default=False)
    image_path = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    photos = db.relationship('Photo', backref='film', lazy=True)

    def __repr__(self):
        return f'<Film {self.brand} {self.name}>'

# -------------------------
# Roll
# -------------------------
class Roll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    roll_name = db.Column(db.String(100))     # e.g. JapanTrip-HP5
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20))         # e.g. in use / developed
    notes = db.Column(db.Text)

    film = db.relationship('Film')
    photos = db.relationship('Photo', backref='roll', lazy=True)

    def __repr__(self):
        return f'<Roll {self.roll_name or self.id}>'

# -------------------------
# Photo（shot）
# -------------------------
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    image_path = db.Column(db.String(200))
    shot_date = db.Column(db.DateTime)
    shutter_speed = db.Column(db.String(20))
    aperture = db.Column(db.String(20))
    iso = db.Column(db.String(10))
    frame_number = db.Column(db.String(10))
    location = db.Column(db.String(100))

    #  Equipment used (camera, lens, film)
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.id'), nullable=True)
    lens_id = db.Column(db.Integer, db.ForeignKey('lens.id'), nullable=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=True)

     # Optional association with a roll
    roll_id = db.Column(db.Integer, db.ForeignKey('roll.id'), nullable=True)

    def __repr__(self):
        return f'<Photo {self.shot_date} ISO {self.iso}>'
    
# -------------------------
# Share
# -------------------------

class Share(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User who initiated the share
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)    # User who received the share
    start_date = db.Column(db.DateTime, nullable=False)  # Start date of the shared period
    end_date = db.Column(db.DateTime, nullable=False)    # End date of the shared period
    note = db.Column(db.String(200))  # Optional note
    created_at = db.Column(db.DateTime, default=db.func.now())  # Timestamp when the share was created

    # Fields to control shared content
    share_exposure = db.Column(db.Boolean, default=False)        # Shutter speed/ISO distribution
    share_aperture = db.Column(db.Boolean, default=False)        # Aperture distribution
    share_favorite_film = db.Column(db.Boolean, default=False)   # Favorite film preferences
    share_gear = db.Column(db.Boolean, default=False)            # Camera/lens preferences
    share_shoot_time = db.Column(db.Boolean, default=False)      # Shooting time chart

    from_user = db.relationship('User', foreign_keys=[from_user_id], backref='shares_made')  # Relationship to the user who shared
    to_user = db.relationship('User', foreign_keys=[to_user_id], backref='shares_received')  # Relationship to the user who received

    # The same from_user can only have one sharing record with to_user
    __table_args__ = (db.UniqueConstraint('from_user_id', 'to_user_id', name='unique_user_share'),)
