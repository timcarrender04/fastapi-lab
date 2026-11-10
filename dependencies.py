from fastapi import Header, HTTPException


def get_current_user(x_token: str = Header(...)):
    """Require the header X-Token: secret-token.

    A missing header is 422 (FastAPI treats a required header as a validation error).
    A present but wrong token is 401.
    """
    if x_token != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": "admin"}
