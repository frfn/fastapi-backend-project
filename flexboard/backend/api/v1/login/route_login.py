from datetime import timedelta
from typing import Optional

from fastapi import Depends, APIRouter, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from api_models.token import Token, TokenData
from config import config_object
from database.orm_models.user import User
from database.session import get_database
from services.token_service import token_service
from services.user_service import user_service

router: APIRouter = APIRouter()

# This returns a string, the JWT, aka the bearer token.
# tokenUrl: Token URL is the URL of the service that will generate the token.
# https://fastapi.tiangolo.com/tutorial/security/first-steps/#fastapis-oauth2passwordbearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login/token')

credentials_exception: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


@router.post("/token", response_model=Token)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_database)):
    # form_data.username can either be an email or username.
    # form_data is from OAuth2, so we must use the username attribute.
    """
    Sets a httponly cookie with "Authorization" as the key and Bear "token123" as the value. ex. "Authorization | Bearer token123"
    """

    user: User = user_service.get_user_by_email_or_username(form_data.username, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username not found.",
            headers={"WWW-Authenticate": "Bearer"},  # Not added by me. Copy and pasted from FastAPI docs.
        )

    parsed_bcrypt_password: str = user.hashed_password.split("}")[1]

    is_valid: bool = user_service.authenticate_user(form_data.password, parsed_bcrypt_password)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},  # Not added by me. Copy and pasted from FastAPI docs.
        )

    access_token_expires: timedelta = timedelta(minutes=int(config_object.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))

    access_token: str = token_service.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    # setting the bearer token -- learned this for the Front End if needed.
    response.set_cookie("Authorization", f"Bearer {access_token}", httponly=True)

    return Token(access_token=access_token, token_type="bearer")


async def get_current_user_from_token(token: str = Depends(oauth2_scheme), session: Session = Depends(get_database)) -> User:
    """
    This is a dependency function, to be used like: "user: User = Depends(get_current_user_from_token)"
    The "token" is the "param" variable separated from the incoming string "Bearer ey123123".

    We do NOT pass anything to this method.

    :param token: an OAuth2PasswordBearer instance, also a callable (a method that returns something)
    :param session: a session object for persistence
    """
    try:
        payload: dict = jwt.decode(token, config_object.JWT_SECRET_KEY, algorithms=[config_object.JWT_ALGORITHM])

        # 'sub' is subject, 'username' is the email.
        username: Optional[str] = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data: TokenData = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user: User = user_service.get_user_by_email_or_username(token_data.username, session)

    if user is None:
        raise credentials_exception

    return user
