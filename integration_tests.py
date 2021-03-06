from unittest import TestCase
from model import connect_to_db, db, example_data
from server import app
from flask import session


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("Generate", result.data)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        app.config['SESSION_COOKIE_DOMAIN'] = None
        # app.config['SERVER_NAME'] = 'localhost'
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_star_info(self):
        """Test star info page."""

        result = self.client.get("/stars/1")
        self.assertIn("Orion", result.data)

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"username": "Louise", "password": "sky"},
                                  follow_redirects=True)
        self.assertIn("Louise", result.data)

    def test_register(self):
        """Test registration page."""

        result = self.client.post("/register",
                                  data={"username": "NewUser", "password": "new", "user_id": "3"},
                                  follow_redirects=True)
        self.assertIn("Logged In", result.data)

    def test_register_duplicate(self):
        """Test two users can't register the same username"""

        result = self.client.post("/register",
                                  data={"username": "Louise", "password": "new"},
                                  follow_redirects=True)
        self.assertIn("already exists", result.data)

    def test_login_password(self):
        """Test that a user can't log in with the wrong password"""

        result = self.client.post("/login",
                                  data={"username": "Louise", "password": "monkey"},
                                  follow_redirects=True)
        self.assertIn("Wrong password", result.data)

    def test_login_registry(self):
        """Test that a user can't log in if they haven't registered"""

        result = self.client.post("/login",
                                  data={"username": "Rachel", "password": "monkey"},
                                  follow_redirects=True)
        self.assertIn("try again or register", result.data)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '2'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertIn('logged out', result.data)

    def test_false_logout(self):
        """Test you can't logout if not logged in"""

        result = self.client.get('/logout', follow_redirects=True)

        self.assertIn('not logged in', result.data)

    def test_saved_stars(self):
        """test that saved stars show up on user page"""

        result = self.client.post("/login",
                                  data={"username": "ZoeShirah", "password": "stars"},
                                  follow_redirects=True)
        self.assertIn("Polaris", result.data)

    def test_setting_user_location(self):
        """Test that users can set thier location"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'

        result = self.client.get("/set_user_location?lat=83&lng=-122",
                                 follow_redirects=True)
        self.assertIn("your location", result.data)

    def test_clear_session(self):
        """Test that the info in the session clears"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['lat'] = '0.8765'
                sess['d_lat'] = '-70'
                sess['lon'] = '-122'
                sess['d_lon'] = '0.76563'
                sess['time'] = "20071212T09:35"

        result = self.client.get("/clear", follow_redirects=True)
        self.assertIn("DateTime: now", result.data)

    def test_replace_session(self):
        """Test that the info in the session clears but gets replaced with user's defaults"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['lat'] = '0.8765'
                sess['d_lat'] = '-70'
                sess['lon'] = '-122'
                sess['d_lon'] = '0.76563'
                sess['time'] = "20071212T09:35"
                sess['user_id'] = 2

        result = self.client.get("/clear", follow_redirects=True)
        self.assertIn("DateTime: now", result.data)
        self.assertIn("Latitude: 44.00", result.data)

    def test_search_lowercase(self):
        """Test that search will find a star and redirect to its info page"""

        result = self.client.get("/search?name=polaris", follow_redirects=True)
        self.assertIn("Ursa Minor", result.data)

    def test_search_id(self):
        """Test that search will find a star and redirect to its info page"""

        result = self.client.get("/search?name=4", follow_redirects=True)
        self.assertIn("Betelgeuse", result.data)

    def test_search_name_not_found(self):
        """Test that search will handle the case where the name is not found"""

        result = self.client.get("/search?name=monkey", follow_redirects=True)
        self.assertIn("no star with that name", result.data)

    def test_search_number_too_long(self):
        """Test that search will handle the case where the number is not a valid id"""

        result = self.client.get("/search?name=111111111111111111111111", follow_redirects=True)
        self.assertIn("please try again", result.data)

    def test_save_a_star(self):
        """Test that a user can add a star to their profile"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
        result = self.client.get("/add_to_saved/4", follow_redirects=True)
        self.assertIn("Star Added!", result.data)

    def test_already_saved(self):
        """Test that a user can't add a star twice"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
        result = self.client.get("/add_to_saved/3", follow_redirects=True)
        self.assertIn("You have already saved this star!", result.data)

    def test_change_lat_lon(self):
        """Test that a user can change the lat/long of the sky generator"""

        result = self.client.get("/change_defaults?lat=39.7392358&lng=-104.990251",
                                 follow_redirects=True)
        self.assertIn("Latitude: 39.7392358000&deg;", result.data)

    def test_change_datetime(self):
        """Test that the user can change the date/time of the sky generator

        assuming default lat/long of Hackbright"""

        result = self.client.get("/change_defaults?date=2017-02-17T14:05",
                                 follow_redirects=True)
        self.assertIn("DateTime in UTC: 2017-02-17 22:05:00+00:00", result.data)


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def test_login(self):
        """Test that if a user is already logged in they can't log in again"""

        result = self.client.get("/login", follow_redirects=True)
        self.assertIn("already", result.data)

    def test_register(self):
        """Test that if a user is already logged in they can't register again"""

        result = self.client.get("/register", follow_redirects=True)
        self.assertIn("already", result.data)


# class FlaskTestsLoggedOut(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         self.client = app.test_client()

#     def test_important_page(self):
#         """Test that user can't see important page when logged out."""

#         result = self.client.get("/important", follow_redirects=True)
#         self.assertNotIn("You are a valued user", result.data)
#         self.assertIn("You must be logged in", result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
