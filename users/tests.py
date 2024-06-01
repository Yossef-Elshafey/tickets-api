from rest_framework import status
import requests
from rest_framework.test import APITestCase


class AccountTests(APITestCase):
    url = "http://localhost:8000/api"

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        path = "{}/users/sign-up".format(self.url)
        data = {
            "first_name": "yossef",
            "last_name": "elshafey",
            "email": "foobar@bar.com",
            "password": "1231231",
            "password_compare": "1231231",
        }
        response = self.client.post(path, data, format="json")
        self.assertEqual(len(response.data), 2)  # {token, id}
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sign(self):
        """
        Ensure we can sign in
        """
        path = "{}/users/sign-in".format(self.url)
        data = {"email": "foobar@bar.com", "password": "1231231"}
        # NOTE: add valid or invalid data is possible cause this is hits the db
        res = requests.post(path, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
