## Overview

### TECHNOLOGIES

* Docker
* Python
* Django
* Django REST Framework
* JWT
* Swagger
* MySQL

### SETUP

Before running Docker, create a .env file in which you write the SECRET_KEY.

Run the project with Docker:

 ```sh
docker-compose up --build
```

Endpoints can be checked in Swagger and DRF.

### RUNNING TESTS

1. Run docker containers
    ```sh
     docker-compose up --build
    ```

2. Run pytest inside web container

   ```sh
    python manage.py test
   ```

3. Create superuser

   ```sh
    python manage.py createsuperuser
   ```
   To create a superuser for Book-project application, use the following command::
    - username: admin
    - email: admin@admin.com
    - password: admin (this easy password is intended solely for testing purposes)
- To test the APIs in Swagger, first, you need to log in to obtain an Access
Token using the default user credentials: admin@admin.com as the email and admin as the password. Once you successfully
log in, you will receive an "access_token." This token grants access to every API endpoint. In swagger add this acces
token in JWT Bearer (not need to add prefix 'Bearer').

### GET JWT ACCESS TOKEN
Go to swagger: /swagger/
1. Get token from login endpoint:
    - In Swagger use this endpoint:
        ```sh
       /login/
        ```
      Use default credentials email: `admin@admin.com` password: `admin` (I added example data so you don't need to
      write anything in payload). Take token from response and add it to swagger 'Authorization JWT Bearer".

### CHECK EXISTING PERMISSIONS FOR THE USER

2. Check existing permissions:
    - In Swagger use this POST endpoint:
        ```sh
       api/user/permissions/
        ```
      
    - Before creating a user and putting the permissions on them, the frontend would look up permission IDs.
    - Don't forget to use "access token" in the "Authorization"
    - 
### CREATE A USER

3. Check all existing users:
    - In Swagger use this POST endpoint:
        ```sh
       /users/
        ```
      The user creation with Administrator permission through this endpoint is disabled. With other roles, it is correct. 
      Don't forget to use "access token" in the "Authorization".
   
### CHECK ALL EXISTING USERS

4. Check all existing users:
    - In Swagger use this endpoint:
        ```sh
       http://localhost:8000/api/v1/rooms/all/
        ```
      Don't forget to use "access token" in the "Authorization".

### CREATE A BOOK

5. Create a book:
    - In Swagger use this POST endpoint:
        ```sh
       /books/
        ```
      
    - Don't need to add any data to the payload because example data has already been included.
    - Don't forget to use "access token" in the "Authorization".

### CHECK ALL EXISTING BOOKS

6. Check all existing books:
    - In Swagger use this GET endpoint:
        ```sh
       /books/
        ```
    - Don't forget to use "access token" in the "Authorization".

### GET SPECIFIC BOOK

7. Get specific book by ID:
    - In Swagger use this endpoint:
        ```sh
       /books/{id}/
        ```
    - Don't forget to use "access token" in the "Authorization".

NOTE: 
Due to a lack of time, I didn't manage to do most of the tasks. So,  improvements that can be made is:
- to create a fixture in which a default book and user are created. This way, before running the container for the second time, there would be no need to delete commands related to user creation.
- create logout endpoint
- to enhance the User model, I suggest making the password and other important functionalities more advanced
- depersonalizate user essential data after User is deleted
- etc.

## Contact
Created by [@enrika](https://www.linkedin.com/in/enrika-vysniauskaite-10bba4196/) - feel free to contact me!

