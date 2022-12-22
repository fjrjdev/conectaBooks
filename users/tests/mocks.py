from addresses.tests.mocks import mock_address

mock_adm = {
    "username": "admin",
    "password": "senhaforte",
    "birth": "2010-10-20",
    "email": "adm@adm.com",
}

mock_user = {
    "username": "user",
    "password": "senhaforte",
    "birth": "2000-08-12",
    "email": "user@user.com",
}

mock_diff = {
    "username": "user_diff",
    "password": "senhaforte",
    "birth": "2000-08-12",
    "email": "user@user.com",
}

mock_user_post = {**mock_user, "address": mock_address}
mock_diff_post = {**mock_diff}

mock_adm_login = {
    "username": "admin",
    "password": "senhaforte",
}

mock_user_login = {
    "username": "user",
    "password": "senhaforte",
}

mock_user_diff_login = {
    "username": "user_diff",
    "password": "senhaforte",
}

# mock_borrowed = {
#     "shipping_method": "Retirada",
# }
