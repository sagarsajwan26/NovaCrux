from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import LoginRequest, LoginResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest):
    if data.email != "admin@novacrux.com" or data.password != "admin123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid email or password"
        )
    return LoginResponse(message="Login successful", email=data.email)
