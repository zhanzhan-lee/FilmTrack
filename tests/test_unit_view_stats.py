import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Camera, Lens, Film, Roll, Photo, Share

class ViewStatsUnitTest(unittest.TestCase):
    def setUp(self):
        print("\nSetting up test environment for View Stats")
        self.app = create_app('testing')
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        # Create test users
        self.user1 = User(username='sharer')
        self.user1.set_password('password')
        self.user2 = User(username='viewer')
        self.user2.set_password('password')
        db.session.add_all([self.user1, self.user2])
        db.session.commit()

        # Create sample gear
        self.camera = Camera(name='M6', brand='Leica', user_id=self.user1.id)
        self.lens = Lens(name='50mm', brand='Leica', user_id=self.user1.id)
        self.film = Film(name='Portra 400', brand='Kodak', user_id=self.user1.id)
        db.session.add_all([self.camera, self.lens, self.film])
        db.session.commit()

        # Create sample roll
        self.roll = Roll(film_id=self.film.id, user_id=self.user1.id,
                        roll_name='Test Roll', status='finished')
        db.session.add(self.roll)
        db.session.commit()

        # Create sample photos
        photos = [
            Photo(user_id=self.user1.id, roll_id=self.roll.id,
                 camera_id=self.camera.id, lens_id=self.lens.id,
                 film_id=self.film.id, shutter_speed='1/125',
                 aperture='f/2', location='Location1',
                 shot_date=datetime.now() - timedelta(days=5)),
            Photo(user_id=self.user1.id, roll_id=self.roll.id,
                 camera_id=self.camera.id, lens_id=self.lens.id,
                 film_id=self.film.id, shutter_speed='1/500',
                 aperture='f/8', location='Location2',
                 shot_date=datetime.now() - timedelta(days=2))
        ]
        db.session.add_all(photos)
        db.session.commit()

        # Create share with all options enabled
        self.share = Share(
            from_user_id=self.user1.id,
            to_user_id=self.user2.id,
            start_date=datetime.now() - timedelta(days=30),
            end_date=datetime.now(),
            share_exposure=True,
            share_aperture=True,
            share_gear=True,
            share_favorite_film=True,
            share_shoot_time=True
        )
        db.session.add(self.share)
        db.session.commit()

    def tearDown(self):
        print("Cleaning up test environment")
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.ctx.pop()

    def test_view_stats_page_load(self):
        """Test if view stats page loads correctly"""
        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(self.user2.id)
        
        response = self.client.get('/view_stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Shared Statistics', response.data)

    def test_unauthorized_access(self):
        """Test accessing shared stats without authorization"""
        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(self.user1.id)  # Wrong user

        response = self.client.get(f'/api/shared_stats/{self.share.id}')
        self.assertEqual(response.status_code, 403)

    def test_invalid_share_id(self):
        """Test accessing non-existent share"""
        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(self.user2.id)

        response = self.client.get('/api/shared_stats/999')
        self.assertEqual(response.status_code, 404)

    def test_exposure_data(self):
        """Test exposure data in shared stats"""
        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(self.user2.id)

        response = self.client.get(f'/api/shared_stats/{self.share.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertIn('exposure', data)
        self.assertIn('1/125', data['exposure']['labels'])
        self.assertIn('1/500', data['exposure']['labels'])

    def test_aperture_data(self):
        """Test aperture data in shared stats"""
        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(self.user2.id)

        response = self.client.get(f'/api/shared_stats/{self.share.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertIn('aperture', data)
        self.assertIn('f/2', data['aperture']['labels'])
        self.assertIn('f/8', data['aperture']['labels'])

    def test_gear_data(self):
        """Test gear data in shared stats"""
        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(self.user2.id)

        response = self.client.get(f'/api/shared_stats/{self.share.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertIn('cameras', data)
        self.assertIn('lenses', data)
        self.assertIn('M6', data['cameras']['labels'])
        self.assertIn('50mm', data['lenses']['labels'])

    def test_disabled_sharing_options(self):
        """Test when certain sharing options are disabled"""
        # Update share with some options disabled
        self.share.share_exposure = False
        self.share.share_aperture = False
        db.session.commit()

        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(self.user2.id)

        response = self.client.get(f'/api/shared_stats/{self.share.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertNotIn('exposure', data)
        self.assertNotIn('aperture', data)
        self.assertIn('cameras', data)

    def test_empty_data(self):
        """Test shared stats with no photos"""
        # Delete all photos
        Photo.query.delete()
        db.session.commit()

        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(self.user2.id)

        response = self.client.get(f'/api/shared_stats/{self.share.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertIn('cameras', data)
        self.assertEqual(len(data['cameras']['labels']), 0)