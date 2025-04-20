from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    brand = db.Column(db.String(50))
    format = db.Column(db.String(50))
    is_public = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Lens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    brand = db.Column(db.String(50))
    mount_type = db.Column(db.String(50))
    is_public = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(200))
    shutter_speed = db.Column(db.String(20))
    aperture = db.Column(db.String(20))
    iso = db.Column(db.String(10))
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.id'))
    lens_id = db.Column(db.Integer, db.ForeignKey('lens.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))




    def __repr__(self):
        return f'<User {self.username}>'