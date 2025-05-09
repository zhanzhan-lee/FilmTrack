
#  Testing Guide 


## 📁 Test Structure

All unit tests are stored under the `tests/` folder in the project root.

```
/tests
├── __init__.py
├── test_unit_gear_upload.py        ← gear upload tests ✅
├── test_unit_roll_upload.py        ← roll + photo tests ✅
├── test_unit_share.py              ← to be added
├── test_unit_stats.py              ← to be added
├── test_unit_share_stats.py        ← to be added
```

Each file focuses on testing a specific module or group of routes.

---

## 🛠️ How to Add a New Test File

1. Create a file inside `tests/` starting with `test_`, for example:

   ```
   test_unit_share.py
   ```

2. Use the following structure:

   ```python
   import unittest
   from app import create_app, db
   from app.models import User

   class ExampleTest(unittest.TestCase):
       def setUp(self):
           self.app = create_app('testing')
           self.client = self.app.test_client()
           self.ctx = self.app.app_context()
           self.ctx.push()
           db.create_all()

           # Create test user
           self.user = User(username='testuser')
           self.user.set_password('123')
           db.session.add(self.user)
           db.session.commit()

           # Simulate login
           with self.client.session_transaction() as sess:
               sess['_user_id'] = str(self.user.id)

       def tearDown(self):
           db.session.remove()
           db.drop_all()
           self.ctx.pop()

       def test_example(self):
           response = self.client.get('/')
           self.assertEqual(response.status_code, 200)
   ```

3. To test POST endpoints, use:

   ```python
   data = {
       'field': 'value',
       'file': (BytesIO(b'data'), 'filename.jpg')
   }
   response = self.client.post('/route', data=data, content_type='multipart/form-data')
   ```
>**⚠️The above is just an example, please test according to actual needs⚠️**
---

## ▶️ How to Run the Tests

Run all tests from the **project root directory**:

```bash
python -m unittest discover -s tests
```

Or run a specific test file:

```bash
python -m unittest tests.test_unit_roll_upload
```

---

## ✅ Testing Environment Setup (Pre-configured)

The testing environment is already set up using Flask's factory pattern with `create_app('testing')`.

### Behind the scenes:

* Uses `TestingConfig` defined in `config.py`:

  ```python
  class TestingConfig:
      TESTING = True
      SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
      WTF_CSRF_ENABLED = False
  ```
* This ensures:

  * ✅ Isolated in-memory database (clean for each test run)
  * ✅ No CSRF issues for form testing
  * ✅ Automatic setup/teardown in each test
  * ✅ No impact on production or development data

You do **not** need to set up or reset the database manually.

---

## 📌 Notes

* Image uploads in tests use `BytesIO(b'mock data')`—no real image files are needed.
* Make sure to use actual model field names when inserting mock data.
* You can simulate GET and POST requests as needed using the Flask `test_client()`.

