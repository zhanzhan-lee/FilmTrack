import unittest
from io import BytesIO
from app import create_app, db
from app.models import User, Film, Roll, Camera, Lens, Photo
from datetime import datetime


class RollPhotoUploadUnitTest(unittest.TestCase):
    def setUp(self):
        print("\nSetting up test environment for Roll and Photo upload")
        self.app = create_app('testing')
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        # Create and login test user
        self.user = User(username='testuser')
        self.user.set_password('password')
        db.session.add(self.user)
        db.session.commit()

        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(self.user.id)

        # Create film, camera, lens with correct field names
        self.film = Film(name='Portra', brand='Kodak', iso='400', format='35mm', user_id=self.user.id)
        self.camera = Camera(name='M6', brand='Leica', type='Rangefinder', format='35mm', user_id=self.user.id)
        self.lens = Lens(name='Planar 50mm', brand='Zeiss', mount_type='M', user_id=self.user.id)

        db.session.add_all([self.film, self.camera, self.lens])
        db.session.commit()

        print("Test user and gear created")

    def tearDown(self):
        print("Cleaning up test environment")
        db.session.remove()
        db.drop_all()
        db.engine.dispose() 
        self.ctx.pop()
        


    def test_upload_roll_success(self):
        print("Testing roll upload")
        data = {
            'film_id': str(self.film.id),
            'roll_name': 'Test Roll',
            'start_date': '2024-05-01',
            'end_date': '2024-05-07',
            'notes': 'Sample test roll'
        }

        response = self.client.post('/shooting/upload_roll', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        print("Roll upload test passed")

    def test_upload_photo_success(self):
        print("Testing photo upload")

        # Create a roll (photo needs roll_id)
        roll = Roll(
            user_id=self.user.id,
            film_id=self.film.id,
            roll_name='Test Roll 2',
            status='in use'
        )
        db.session.add(roll)
        db.session.commit()

        data = {
            'roll_id': str(roll.id),
            'shot_date': '2024-05-07',
            'shutter_speed': '1/250',
            'aperture': '2.8',
            'iso': '400',
            'frame_number': '1',
            'location': 'Test Location',
            'camera_id': str(self.camera.id),
            'lens_id': str(self.lens.id),
            'image': (BytesIO(b'mock photo data'), 'test.jpg')
        }

        response = self.client.post(
            '/shooting/upload_photo',
            data=data,
            content_type='multipart/form-data'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        print("Photo upload test passed")


    def test_edit_roll_success(self):
        print("Testing roll edit")

        # 创建一个 roll
        roll = Roll(
            user_id=self.user.id,
            film_id=self.film.id,
            roll_name='Old Name',
            start_date=datetime(2024, 5, 1),
            end_date=datetime(2024, 5, 5),
            status='in use',
            notes='Old note'
        )
        db.session.add(roll)
        db.session.commit()

        data = {
            'film_id': self.film.id,
            'roll_name': 'New Name',
            'start_date': '2024-05-02',
            'end_date': '2024-05-06',
            'status': 'finished',
            'notes': 'Updated note'
        }

        response = self.client.post(f'/shooting/edit_roll/{roll.id}', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'updated', response.data)
        print("Roll edit test passed")


    def test_edit_photo_success(self):
        print("Testing photo edit")

        # 创建一个 roll 和 photo
        roll = Roll(user_id=self.user.id, film_id=self.film.id, roll_name='Test Roll', status='in use')
        db.session.add(roll)
        db.session.commit()

        photo = Photo(
            user_id=self.user.id,
            roll_id=roll.id,
            film_id=self.film.id,
            image_path='test.jpg',
            frame_number='1'
        )
        db.session.add(photo)
        db.session.commit()

        data = {
            'shutter_speed': '1/1000',
            'aperture': 'f/1.4',
            'iso': '800',
            'frame_number': '10',
            'location': 'New location',
            'camera_id': self.camera.id,
            'lens_id': self.lens.id,
            'shot_date': '2024-05-08'
        }

        response = self.client.post(f'/shooting/edit_photo/{photo.id}', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        print("Photo edit test passed")


    def test_delete_roll_success(self):
        roll = Roll(user_id=self.user.id, film_id=self.film.id, roll_name='To Delete', status='in use')
        db.session.add(roll)
        db.session.commit()

        response = self.client.delete(f'/shooting/delete_roll/{roll.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'deleted', response.data)

    def test_delete_photo_success(self):
        roll = Roll(user_id=self.user.id, film_id=self.film.id, roll_name='Test Roll', status='in use')
        db.session.add(roll)
        db.session.commit()

        photo = Photo(user_id=self.user.id, roll_id=roll.id, film_id=self.film.id, image_path='test.jpg')
        db.session.add(photo)
        db.session.commit()

        response = self.client.post(f'/shooting/delete_photo/{photo.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        
    def test_finish_roll_success(self):
        roll = Roll(user_id=self.user.id, film_id=self.film.id, roll_name='Test Roll', status='in use')
        db.session.add(roll)
        db.session.commit()

        response = self.client.post(f'/shooting/finish_roll/{roll.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
