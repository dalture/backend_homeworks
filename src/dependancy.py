from fastapi import Header, HTTPException

def check_headers(
    auth_token: str = Header()
):
    if auth_token == "123":
        return True
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")