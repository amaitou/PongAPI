
---
![5-new-things-rest-specification](https://github.com/user-attachments/assets/b38326de-b4c8-406a-9279-6f61c47c0c4b)

---

# Table of content

- [Overview](https://github.com/amaitou/PongAPI/blob/master/README.md#overview)
- [Acknowledgments](https://github.com/amaitou/PongAPI/blob/master/README.md#acknowledgments)
- [Features](https://github.com/amaitou/PongAPI/blob/master/README.md#features)
    - [User Authentication & Authorization](https://github.com/amaitou/PongAPI/blob/master/README.md#user-authentication--authorization)
    - [User Management](https://github.com/amaitou/PongAPI/blob/master/README.md#user-management)
    - [Security Measures](https://github.com/amaitou/PongAPI/blob/master/README.md#security-measures)
- [Installation](https://github.com/amaitou/PongAPI/blob/master/README.md#installation)
- [Security](https://github.com/amaitou/PongAPI/blob/master/README.md#security)
- [License](https://github.com/amaitou/PongAPI/blob/master/README.md#license)

# Overview

The Pong Game **API** provides backend services for managing users, handling authentication, and tracking game statistics for the Pong Game. It was created as part of the Transcendence project under the 42 project initiative.

The **API** is built on **Django REST Framework (DRF)** with **JWT authentication** and other security measures to ensure a safe and seamless experience for users.

---

# Acknowledgments

This **API** was built as part of the Transcendence project under the 42 project initiative. Thanks to the 42 community for their support, and to all contributors who made this project possible.

feel free to check out the entire project via [ft_trans](https://github.com/redavio9/ft_trans)

before we dive into the project, I would like to extend my sincere thanks to the following contributors, whose hard work and dedication made this project possible:

**[Reda Arraji](https://github.com/Redavio9)**: Responsible for the DevOps section, including deployment, infrastructure, and maintaining the chat functionality within the project. His efforts ensured that the project was scalable and well-integrated.

**[Rida Labbiz](https://github.com/rlabbiz)**: Took care of the front-end development, ensuring a seamless and intuitive user experience. Reda's work on the front-end helped bring the game's interface to life.

**[Ali El Amine](https://github.com/Root-07)**: Designed and implemented the tournament logic, enabling users to participate in competitive tournaments. His work added a critical social and competitive layer to the project, making it more engaging for users.

> We made many projects together, and we have grown up professionally together." 🌱

---

# Features

- ### User Authentication & Authorization

    - JWT-based authentication with secure access and refresh tokens.
    - Two-factor authentication (2FA) for added security.
    - Email verification and account management.

    ---

- ### User Management

    - Profile management: update usernames, emails, and passwords.
    - Friend system: add, remove, and manage friends.
    - Track user game stats and history.

    ---

- ### Security Measures

    - Password policies enforce strong, secure passwords.
    - Cookies are marked as HttpOnly to prevent XSS attacks.
    - JWT tokens are used for secure session management.

    ---

#  Installation

if you want to dive deep into this PongAPI you can follow these instructions to run it properly:

- Clone the repository:

```sh
git clone https://github.com/amaitou/PongAPI
cd PongAPI
```

---

- Set up a virtual environment

```
make venv
```

---

- Install dependencies

```
make requirements
```

---

- Configure environment variables

```sh
# 42 Authentication Credentials
CLIENT_ID = "your 42 client id"
CLIENT_SECRET = "your 42 client secret"
REDIRECT = "http://127.0.0.1:8000/api/callback"
AUTH_URL = "https://api.intra.42.fr/oauth/authorize"
TOKEN_URL = "https://api.intra.42.fr/oauth/token"
USER_INFO_URL = "https://api.intra.42.fr/v2/me"

# Secret Key
SECRET_KEY = 'your secret Django from Django settings'

# Short Names
ACCESS_TOKEN = "access_token"
REFRESH_TOKEN = "refresh_token"

# Email Credentials
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = "your email"
EMAIL_HOST_PASSWORD = "you password"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
```

---

- Run migrations

```makefile
make makemigrations
make migrate
```

---

- (Optional) Create a superuser

change these credentials inside **superuser_creation.py**

```python
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='<username>',
        email='<email>',
        password='<password>'
    )
```
then run :

```makefile
make createsuperuser
```

- Run the server

```makefile
make runserver
```

---

# Security

- **JWT Authentication**

    Secure user authentication is done via JWT tokens. The system uses access tokens for authorized requests and refresh tokens for maintaining long-term sessions.

    ---

- **2FA (Two-Factor Authentication)**

    When enabled, users must provide an additional verification code (e.g., from an authenticator app) on login, ensuring an extra layer of security.

    ---

- **Password Policies**
    
    - Minimum length: 8 characters.
    - Must include at least one uppercase letter, one lowercase letter, one digit, and one special character.

    ---

- **Secure Cookies**

    Cookies used for authentication are marked HttpOnly to prevent client-side access via JavaScript, thus reducing the risk of XSS (Cross-Site Scripting) attacks.

    ---

---

# License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/amaitou/PongAPI/blob/master/LICENSE) file for details.
