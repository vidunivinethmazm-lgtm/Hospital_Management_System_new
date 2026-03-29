from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

app = FastAPI(
    title="Auth Service",
    description="Authentication microservice — register, login and get JWT tokens",
    version="1.0.0",
)

SECRET_KEY = "hospital_mgmt_secret_key_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_db: dict = {}


class UserRegister(BaseModel):
    username: str
    password: str
    role: str = "staff"


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    role: str


@app.get("/", tags=["Health"])
def root():
    return {"service": "Auth Service", "status": "running"}


@app.post("/auth/register", status_code=201, tags=["Auth"])
def register(user: UserRegister):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    users_db[user.username] = {
        "username": user.username,
        "hashed_password": pwd_context.hash(user.password),
        "role": user.role,
    }
    return {"message": f"User '{user.username}' registered successfully", "role": user.role}


@app.post("/auth/login", response_model=TokenResponse, tags=["Auth"])
def login(user: UserLogin):
    db_user = users_db.get(user.username)
    if not db_user or not pwd_context.verify(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": user.username,
        "role": db_user["role"],
        "exp": expire,
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        username=user.username,
        role=db_user["role"],
    )


@app.get("/auth/users", tags=["Auth"])
def list_users():
    return [{"username": u, "role": v["role"]} for u, v in users_db.items()]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8007, reload=True)
