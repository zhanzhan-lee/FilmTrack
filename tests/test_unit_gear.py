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

    def test_edit_camera_success(self):
        print("Testing camera edit")
        # Upload first
        upload_data = {
            'name': 'Original Cam',
            'brand': 'Leica',
            'type': 'Rangefinder',
            'format': '35mm',
            'is_public': 'y',
            'image': (BytesIO(b'img'), 'cam.jpg')
        }
        upload_resp = self.client.post('/gear/upload_camera', data=upload_data, content_type='multipart/form-data')
        self.assertEqual(upload_resp.status_code, 200)

        # Get ID
        camera = Camera.query.filter_by(name='Original Cam').first()
        self.assertIsNotNone(camera)

        # Edit
        edit_data = {
            'name': 'Updated Cam',
            'brand': 'Canon',
            'type': 'SLR',
            'format': 'Half-frame',
            'is_public': 'y',
            'image': (BytesIO(b'newimg'), 'new.jpg')
        }
        edit_resp = self.client.post(f'/gear/edit_camera/{camera.id}', data=edit_data, content_type='multipart/form-data')
        self.assertEqual(edit_resp.status_code, 200)
        self.assertIn(b'updated', edit_resp.data)
        print("Camera edit test passed")

    def test_edit_lens_success(self):
        print("Testing lens edit")
        # 上传 lens
        upload_data = {
            'name': 'Old Lens',
            'brand': 'Zeiss',
            'mount_type': 'M',
            'is_public': 'y',
            'image': (BytesIO(b'data'), 'lens.jpg')
        }
        self.client.post('/gear/upload_lens', data=upload_data, content_type='multipart/form-data')
        lens = Lens.query.filter_by(name='Old Lens').first()
        self.assertIsNotNone(lens)

        # 编辑 lens（不传 image）
        edit_data = {
            'name': 'Updated Lens',
            'brand': 'Canon',
            'mount_type': 'EF',
            'is_public': 'y'
        }
        response = self.client.post(f'/gear/edit_lens/{lens.id}', data=edit_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'updated', response.data)
        print("Lens edit test passed")


    def test_edit_film_success(self):
        print("Testing film edit")
        # Upload film first
        upload_data = {
            'name': 'Old Film',
            'brand': 'Fuji',
            'iso': '200',
            'format': '35mm',
            'is_public': 'y',
            'image': (BytesIO(b'filmdata'), 'film.jpg')
        }
        self.client.post('/gear/upload_film', data=upload_data, content_type='multipart/form-data')
        film = Film.query.filter_by(name='Old Film').first()
        self.assertIsNotNone(film)

        edit_data = {
            'name': 'Updated Film',
            'brand': 'Ilford',
            'iso': '100',
            'format': '120',
            'is_public': 'y'
        }
        response = self.client.post(f'/gear/edit_film/{film.id}', data=edit_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'updated', response.data)
        print("Film edit test passed")

    def test_delete_film_success(self):
        print("Testing film delete")
        film = Film(name='ToDelete', brand='Kodak', iso='400', format='35mm', user_id=self.user.id)
        db.session.add(film)
        db.session.commit()
        response = self.client.delete(f'/gear/delete_film/{film.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'deleted', response.data)
        print("Film delete test passed")

    def test_delete_lens_success(self):
        print("Testing lens delete")
        lens = Lens(name='ToDelete', brand='Canon', mount_type='EF', user_id=self.user.id)
        db.session.add(lens)
        db.session.commit()
        response = self.client.delete(f'/gear/delete_lens/{lens.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'deleted', response.data)
        print("Lens delete test passed")

    def test_delete_camera_success(self):
        print("Testing camera delete")
        camera = Camera(name='ToDelete', brand='Nikon', type='SLR', format='35mm', user_id=self.user.id)
        db.session.add(camera)
        db.session.commit()

        response = self.client.delete(f'/gear/delete_camera/{camera.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'deleted', response.data)
        print("Camera delete test passed")