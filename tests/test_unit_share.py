# tests/test_unit_share.py
import warnings
from sqlalchemy.exc import LegacyAPIWarning
warnings.filterwarnings("ignore", category=LegacyAPIWarning)

import unittest
from datetime import datetime
from app import create_app, db
from app.models import User, Share


class ShareUnitTest(unittest.TestCase):
    def setUp(self):
        """Create test app, two users, log Alice in."""
        self.app = create_app('testing')
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        self.alice = User(username='alice')
        self.alice.set_password('pw')
        self.bob = User(username='bob')
        self.bob.set_password('pw')
        db.session.add_all([self.alice, self.bob])
        db.session.commit()

        self.client.post('/login',
                         data={'username': 'alice', 'password': 'pw'},
                         follow_redirects=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    # ---------- helper ----------
    def _post_share(self, recipient='@bob', start='2025-01-01', end='2025-01-31',
                    exposure='y', aperture='', film='', gear='', shoot=''):
        data = {
            'share_users': recipient,
            'start_date':  start,
            'end_date':    end,
            'share_exposure':        exposure,
            'share_aperture':        aperture,
            'share_favorite_film':   film,
            'share_gear':            gear,
            'share_shoot_time':      shoot,
            'message':     'hi'
        }
        return self.client.post('/share', data=data, follow_redirects=True)

    # ---------- tests ----------
    def test_first_share_creates_record(self):
        print("\n✅ Testing: First share creates a new DB record.")
        """First share inserts a new DB row."""
        r = self._post_share()
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Share created', r.data)
        self.assertEqual(Share.query.count(), 1)

    def test_second_share_updates_record(self):
        """Second share updates existing row, not insert."""
        print("\n✅ Testing: Second share updates existing record.")
        self._post_share()
        r = self._post_share(start='2025-02-01', film='y')
        self.assertIn(b'Share updated', r.data)
        self.assertEqual(Share.query.count(), 1)
        share = Share.query.first()
        self.assertTrue(share.share_favorite_film)
        self.assertEqual(share.start_date.date(), datetime(2025, 2, 1).date())

    def test_share_to_nonexistent_user(self):
        """Sharing to @ghost flashes error and keeps DB empty."""
        print("\n✅ Testing: Share to non-existent user is rejected.")
        r = self._post_share(recipient='@ghost')
        self.assertIn(b'Recipient not found', r.data)
        self.assertEqual(Share.query.count(), 0)

    def test_share_to_self_forbidden(self):
        """Sharing to self is blocked and DB unchanged."""
        print("\n✅ Testing: Share to self is forbidden.")
        r = self._post_share(recipient='@alice')
        self.assertIn(b'cannot share with yourself', r.data.lower())
        self.assertEqual(Share.query.count(), 0)

    def test_revoke_deletes_record(self):
        """Revoke endpoint removes the Share row."""
        print("\n✅ Testing: Revoke deletes the existing record.")
        self._post_share()
        sid = Share.query.first().id
        r = self.client.post(f'/share/{sid}/revoke', follow_redirects=True)
        self.assertIn(b'Share revoked', r.data)
        self.assertEqual(Share.query.count(), 0)


if __name__ == '__main__':
    unittest.main()











