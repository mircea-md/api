import base64
from typing import Optional

from fastapi import Header, HTTPException
from fastapi.security.utils import get_authorization_scheme_param

from db.crud.user import get_admin_user
from db.mongodb import get_database


async def admin_basic_auth(authorization: Optional[str] = Header(None)) -> bool:
    if not authorization:
        raise HTTPException(status_code=400, detail='No authorization header provided')

    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != 'basic':
        raise HTTPException(status_code=400, detail='No basic authorization provided')

    decoded = base64.b64decode(param).decode("ascii")
    username, _, password = decoded.partition(":")
    if len(username.split(' ')) != 2:
        raise HTTPException(status_code=401, detail='No first name and last name for user name provided')

    cli = await get_database()
    admin = await get_admin_user(username.split(' ')[0], username.split(' ')[1], password, cli)
    if not admin:
        raise HTTPException(status_code=401, detail='No valid user found')

    return True
