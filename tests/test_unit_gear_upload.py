import unittest
from io import BytesIO
from app import create_app, db
from app.models import Camera, Lens, Film, User

class GearUploadUnitTest(unittest.TestCase):
    def setUp(self):
        print("\nSetting up test environment")
        self.app = create_app('testing')
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        self.user = User(username='testuser')
        self.user.set_password('password')

        db.session.add(self.user)
        db.session.commit()

        with self.client:
            with self.client.session_transaction() as sess:
                sess['_user_id'] = str(self.user.id)

        print("Test user created and logged in")

    def tearDown(self):
        print("Tearing down test environment")
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_upload_camera_success(self):
        print("Testing camera upload")
        data = {
            'name': 'M6',
            'brand': 'Leica',
            'type': 'Rangefinder',
            'format': '35mm',
            'is_public': 'y',
            'image': (BytesIO(b'mock image data'), 'cams.jpg')
        }
        response = self.client.post('/gear/upload_camera', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        print("Camera upload test passed")

    def test_upload_lens_success(self):
        print("Testing lens upload")
        data = {
            'name': 'Planar',
            'brand': 'Zeiss',
            'mount_type': 'M',
            'is_public': 'y',
            'image': (BytesIO(b'mock lens data'), 'lens.jpg')
        }
        response = self.client.post('/gear/upload_lens', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        print("Lens upload test passed")

    def test_upload_film_success(self):
        print("Testing film upload")
        data = {
            'name': 'Portra',
            'brand': 'Kodak',
            'iso': '400',
            'format': '35mm',
            'is_public': 'y',
            'image': (BytesIO(b'mock film data'), 'film.jpg')
        }
        response = self.client.post('/gear/upload_film', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        print("Film upload test passed")
