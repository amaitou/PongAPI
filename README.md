
# Authentication

Authentication is the process of verifying the identity of a user, device, or system to ensure that they are who they claim to be. In the context of web applications and digital systems, authentication is a critical security measure that protects sensitive information and resources from unauthorized access. It typically involves the user providing credentials, such as a username and password, which are then checked against a database or authentication service. More advanced forms of authentication may include multi-factor authentication (MFA), where users must provide additional proof of identity, such as a code sent to their mobile device or a fingerprint scan. Authentication is the first line of defense in securing applications and is often combined with authorization, which controls what authenticated users are allowed to do within a system.

---

# JWT

- ### What is a JSON Web Token (JWT)?

A JSON Web Token (JWT) is a compact, URL-safe token format used for securely transmitting information between parties as a JSON object. The JWT format is defined by the RFC 7519 standard and consists of three main components: a header, a payload, and a signature. The header specifies the type of token (JWT) and the signing algorithm used, such as HMAC SHA256. The payload contains the claims, which are statements about an entity (usually, the user) and additional data. The signature is used to verify the authenticity of the token and to ensure that the token has not been tampered with.

---

- ### Structure of a JWT

A JWT is typically composed of three parts, separated by dots (.), resulting in a string that looks like this:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

> Header

he header typically consists of two parts: the type of token (JWT) and the signing algorithm being used, such as HMAC SHA256 or RSA.

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

> Payload

The payload contains the claims. Claims are statements about an entity (typically, the user) and additional data. There are three types of claims: registered, public, and private claims. Registered claims are predefined and include standard fields like iss (issuer), exp (expiration time), sub (subject), and aud (audience). Public claims are user-defined and must be collision-resistant. Private claims are custom claims agreed upon between parties.

```json
{
  "sub": "1234567890",
  "name": "Amine",
  "iat": 1516239022
}
```

> Signature

The signature is created by taking the encoded header, the encoded payload, a secret, and the algorithm specified in the header. This part of the JWT is used to verify that the message wasn't changed along the way and, in the case of tokens signed with a private key, it can also verify that the sender of the JWT is who it says it is.

---

- ### How does JWT work?


1. **User Login**: When a user logs in with their credentials, the server verifies their identity.
2. **Token Creation**: Upon successful authentication, the server generates a JWT containing the user's information (claims) and signs it using a secret key or a private key.
3. **Token Transmission**: The JWT is sent back to the client (usually in the response body or as a cookie).
4. **Client-Side Storage**: The client stores the JWT, typically in local storage or a cookie, and sends it in the header (Authorization: Bearer <token>) with each subsequent request to the server.

5. **Token Verification**: Upon receiving a request with a JWT, the server verifies the token's signature and checks its validity (e.g., expiration time, issuer). If valid, the server processes the request; otherwise, it returns an error.

---


- ### Advantages of JWT

\- **Stateless Authentication**: JWTs are self-contained; all the information required for authentication is present in the token. This reduces the server's load since there is no need to store session information in the server's memory or database.

\- **Compact and Portable**: JWTs are compact and URL-safe, making them ideal for transmission in HTTP headers or as URL parameters.

\- **Versatility**: JWTs can be used for both authentication (verifying the user's identity) and authorization (granting access to resources).

\- **Cross-Domain Support**: JWTs are language-agnostic and can be easily used across different domains, making them suitable for microservices architecture and cross-domain authentication.

\- **Improved Performance**: Since JWTs are self-contained, there is no need to query the database multiple times to verify user sessions, resulting in improved application performance.

---

# Endpoint

- ### Register a new user

    - Endpoint: /auth/register
    - Method: POST
    - Description: Registers a new user and sends an email verification link.


    #### Request

    - Headers: Content-Type: application/json
    - Body:

        ```json
        {
            "first_name": "Amine",
            "last_name": "Ait Ouazghour",
            "username": "amaitou",
            "gender": "M",
            "email": "aitouazghouramine@gmail.com",
            "password": "Test@12__34",
            "re_password": "Test@12__34"
        }
        ```

        - **first_name (string, required):** The first name of the user.
        - **last_name (string, required):** The last name of the user.
        - **username (string, required):** The username chosen by the user.
        - **gender (string, required):** The gender of the user (e.g., "M" for male, "F" for female).
        - **email (string, required):** The user's email address. This email will be used to send a verification link.
        - **password (string, required):** The user's password.
        - **re_password (string, required):** The user's password confirmation. Must match the password field.
    
    #### Response

    - Status Code: 201 Created
    - Body: If registration is successful, the response will contain:

    ```json
    {
        "success": "User registered successfully, check your email for verification",
        "redirect": true,
        "redirect_url": "/api/login/",
        "data": {
            "id": 1,
            "first_name": "Amine",
            "last_name": "Ait Ouazghour",
            "username": "amaitou",
            "gender": "M",
            "email": "aitouazghouramine@gmail.com"
        }
    }
    ```

    #### Error Response

    - Status Code: 400 Bad Request
    - Body: If there are validation errors, the response will contain:

    ```json
    {
        "error": {
            "field_name": ["Error message for that field."]
        },
        "redirect": true,
        "redirect_url": "/api/register/"
    }

    ```

    #### Notes

    - Ensure the email field is correct and accessible, as it will be used for email verification.
    - The passwords (password and re_password) must match.
    - This endpoint does not require authentication.
    - No Duplicate email or username (one per user)