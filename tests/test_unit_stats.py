import unittest
from datetime import datetime
from app import create_app, db
from app.models import User, Camera, Lens, Film, Roll, Photo


class StatsUnitTest(unittest.TestCase):
    def setUp(self):
        print("\nSetting up test environment for Stats")
        self.app = create_app('testing')
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        # Create test user
        self.user = User(username='testuser')
        self.user.set_password('password')
        db.session.add(self.user)
        db.session.commit()

        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(self.user.id)

        # Create sample gear
        self.camera1 = Camera(name='M6', brand='Leica', type='Rangefinder', 
                            format='35mm', user_id=self.user.id)
        self.camera2 = Camera(name='F3', brand='Nikon', type='SLR', 
                            format='35mm', user_id=self.user.id)
        
        self.lens1 = Lens(name='50mm', brand='Leica', mount_type='M', 
                         user_id=self.user.id)
        self.lens2 = Lens(name='35mm', brand='Leica', mount_type='M', 
                         user_id=self.user.id)
        
        self.film1 = Film(name='Portra 400', brand='Kodak', iso='400', 
                         format='35mm', user_id=self.user.id)
        self.film2 = Film(name='HP5', brand='Ilford', iso='400', 
                         format='35mm', user_id=self.user.id)
        
        db.session.add_all([self.camera1, self.camera2, self.lens1, 
                           self.lens2, self.film1, self.film2])
        db.session.commit()

        # Create sample rolls and photos
        self.roll1 = Roll(film_id=self.film1.id, user_id=self.user.id,
                         roll_name='Test Roll 1', status='finished')
        db.session.add(self.roll1)
        db.session.commit()

        # Add sample photos with various settings
        photos = [
            Photo(user_id=self.user.id, roll_id=self.roll1.id,
                 camera_id=self.camera1.id, lens_id=self.lens1.id,
                 film_id=self.film1.id, shutter_speed='1/125',
                 aperture='f/2', iso='400', location='Perth',
                 shot_date=datetime(2024, 5, 1)),
            Photo(user_id=self.user.id, roll_id=self.roll1.id,
                 camera_id=self.camera1.id, lens_id=self.lens2.id,
                 film_id=self.film1.id, shutter_speed='1/500',
                 aperture='f/8', iso='400', location='Sydney',
                 shot_date=datetime(2024, 5, 2)),
            Photo(user_id=self.user.id, roll_id=self.roll1.id,
                 camera_id=self.camera2.id, lens_id=self.lens2.id,
                 film_id=self.film1.id, shutter_speed='1/500',
                 aperture='f/8', iso='400', location='Sydney',
                 shot_date=datetime(2024, 5, 3))
        ]
        db.session.add_all(photos)
        db.session.commit()

    def tearDown(self):
        print("Cleaning up test environment")
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.ctx.pop()

    def test_stats_page_load(self):
        """Test if stats page loads correctly"""
        response = self.client.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Stats', response.data)

    def test_shutter_speed_distribution(self):
        """Test shutter speed distribution API endpoint"""
        response = self.client.get('/api/shutter-speed-distribution')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('labels', data)
        self.assertIn('data', data)
        self.assertIn('1/125', data['labels'])
        self.assertIn('1/500', data['labels'])
        self.assertEqual([2, 1], data['data'])
        self.assertEqual(3, data['total'])

    def test_aperture_distribution(self):
        """Test aperture distribution API endpoint"""
        response = self.client.get('/api/aperture-distribution')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('labels', data)
        self.assertIn('data', data)
        self.assertIn('f/2', data['labels'])
        self.assertIn('f/8', data['labels'])

    def test_gear_stats(self):
        """Test gear usage statistics API endpoints"""
        # Test cameras endpoint
        response = self.client.get('/api/cameras-chart-preference')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('M6', data['labels'])
        
        # Test lenses endpoint
        response = self.client.get('/api/lenses-chart-preference')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('50mm', data['labels'])
        self.assertIn('35mm', data['labels'])

    def test_film_stats(self):
        """Test film usage statistics"""
        response = self.client.get('/api/film-chart-preference')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('Portra 400', data['labels'])

    def test_location_stats(self):
        """Test location statistics API endpoint"""
        response = self.client.get('/api/top-locations')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('labels', data)
        self.assertIn('data', data)
        self.assertIn('Perth', data['labels'])
        self.assertIn('Sydney', data['labels'])

    def test_monthly_trend(self):
        """Test monthly shooting trend API endpoint"""
        response = self.client.get('/api/monthly-trend')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('labels', data)
        self.assertIn('data', data)
        self.assertEqual(len(data['labels']), 6)  # Should have 6 months

    def test_monthly_trend_empty_data(self):
        """Test monthly trend with no photos"""
        # Delete all photos
        Photo.query.delete()
        db.session.commit()

        response = self.client.get('/api/monthly-trend')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['labels']), 6)  # Should still have 6 months
        self.assertEqual(sum(data['data']), 0)    # All values should be 0

    def test_gear_stats_with_unused_gear(self):
        """Test gear stats when some gear has never been used"""
        # Add unused camera
        unused_camera = Camera(name='unused', brand='test', type='test',
                             format='35mm', user_id=self.user.id)
        db.session.add(unused_camera)
        db.session.commit()

        response = self.client.get('/api/cameras-chart-preference')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertNotIn('unused', data['labels'])  # Unused camera shouldn't appear

    def test_location_stats_with_null_locations(self):
        """Test location stats with null location values"""
        # Add photo with null location
        photo = Photo(user_id=self.user.id, roll_id=self.roll1.id,
                     camera_id=self.camera1.id, lens_id=self.lens1.id,
                     film_id=self.film1.id, shutter_speed='1/125',
                     aperture='f/2', iso='400', location=None,
                     shot_date=datetime(2024, 5, 1))
        db.session.add(photo)
        db.session.commit()

        response = self.client.get('/api/top-locations')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertNotIn(None, data['labels'])  # Null locations should be filtered out

    def test_film_stats_with_deleted_film(self):
        """Test film stats when referenced film is deleted"""
        # Delete a film that's used in photos
        db.session.delete(self.film1)
        db.session.commit()

        response = self.client.get('/api/film-chart-preference')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertNotIn('Portra 400', data['labels'])

    def test_stats_unauthorized_access(self):
        """Test accessing stats without being logged in"""
        with self.client.session_transaction() as sess:
            sess.clear()  # Clear session to simulate logged out state

        response = self.client.get('/stats')
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_aperture_distribution_invalid_data(self):
        """Test aperture distribution with invalid aperture values"""
        # Add photo with invalid aperture
        photo = Photo(user_id=self.user.id, roll_id=self.roll1.id,
                     camera_id=self.camera1.id, lens_id=self.lens1.id,
                     film_id=self.film1.id, shutter_speed='1/125',
                     aperture='invalid', iso='400', location='Test',
                     shot_date=datetime(2024, 5, 1))
        db.session.add(photo)
        db.session.commit()

        response = self.client.get('/api/aperture-distribution')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('invalid', data['labels'])  # Should handle invalid data

    def test_monthly_trend_future_dates(self):
        """Test monthly trend with future dates"""
        # Add photo with future date
        future_photo = Photo(user_id=self.user.id, roll_id=self.roll1.id,
                           camera_id=self.camera1.id, lens_id=self.lens1.id,
                           film_id=self.film1.id, shutter_speed='1/125',
                           aperture='f/2', iso='400', location='Future',
                           shot_date=datetime(2025, 12, 1))
        db.session.add(future_photo)
        db.session.commit()

        response = self.client.get('/api/monthly-trend')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['labels']), 6)  # Should still only show last 6 months

    def test_cross_user_data_isolation(self):
        """Test that users can't see each other's stats"""
        # Create second user with their own photos
        user2 = User(username='testuser2')
        user2.set_password('password')
        db.session.add(user2)
        db.session.commit()

        photo2 = Photo(user_id=user2.id, roll_id=self.roll1.id,
                      camera_id=self.camera1.id, lens_id=self.lens1.id,
                      film_id=self.film1.id, shutter_speed='1/1000',
                      aperture='f/1.4', iso='400', location='User2Location',
                      shot_date=datetime(2024, 5, 1))
        db.session.add(photo2)
        db.session.commit()

        # Check that first user can't see second user's data
        response = self.client.get('/api/top-locations')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertNotIn('User2Location', data['labels'])
