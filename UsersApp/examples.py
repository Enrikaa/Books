USER_CREATION_PAYLOAD = {
    "username": "John",
    "email": "john@gmail.com",
    "password": "9P#kT3$F@7rA",
    "user_permissions": [30, 31, 32, 9, ]  # Fronted before that should call permissions endpoint to chek permission id
}

USER_LOGIN_PAYLOAD = {
    "username": "admin",
    "password": "admin"
}

BOOK_DETAIL_PAYLOAD = {
    "title": "string",
    "author": "string",
    "publication_date": "2023-08-07",
    "user": 1
}

BOOK_LIST_PAYLOAD = {
    "title": "string",
    "author": "string"
}
