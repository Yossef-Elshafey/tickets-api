"""
    users endpoints test using request module

    --- Endpoint ---
    users/sign-in => {email, password} return token, id
    users/sign-up => {first_name, last_name, email, password, password_compare} return token, id
    users/sign-out => {Headers:{Authorization:"token ${token}"}} return "" 204
    users/me => {Headers:{Authorization:"token ${token}"}} return user record except password
"""

import requests


class UsersTest:
    url = "http://localhost:8000/api"

    def manage_response(self, res, url):
        json = res.json()
        extract_url = url.split("/")[3::]  # excape until /api
        print("/".join(extract_url), json)

    def sign_up(self, **kwargs):
        current_url = "{}/users/sign-up".format(self.url)
        res = requests.post(current_url, kwargs, timeout=1)
        self.manage_response(res, current_url)

    def sign_in(self, **kwargs):
        current_url = "{}/users/sign-in".format(self.url)
        res = requests.post(current_url, kwargs, timeout=1)
        self.manage_response(res, current_url)

    def me(self, tok):
        current_url = "{}/users/me".format(self.url)
        header = {"Authorization": "Token {}".format(tok)}
        res = requests.get(current_url, headers=header)
        self.manage_response(res, current_url)

    def sign_out(self, tok):
        current_url = "{}/users/sign-out".format(self.url)
        header = {"Authorization": "Token {}".format(tok)}

        res = requests.get(current_url, headers=header)
        self.manage_response(res, current_url)


# UsersTest().sign_in(email="foobar@bar.com", password="1231231")
# UsersTest().sign_up(
#     first_name="yossef",
#     last_name="elshafey",
#     email="foobar@bar.com",
#     password="1231231",
#     password_compare="1231231",
# )

# to use .me or .sign_out copy the token came from sign-up or sign_in responses


# UsersTest().me(tok=)
# UsersTest().sign_out(tok=)
