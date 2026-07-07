from jose import jwt
from datetime import datetime, timedelta

# Secret key (keep this secret in production)
SECRET_KEY = "mysecretkey123"

# Algorithm used to sign the token
ALGORITHM = "HS256"

# Token expiration time (30 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    """
    Create a JWT access token.
    """

    # Copy the user data
    to_encode = data.copy()

    # Set token expiry time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add expiry into token data
    to_encode.update({"exp": expire})

    # Create JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt