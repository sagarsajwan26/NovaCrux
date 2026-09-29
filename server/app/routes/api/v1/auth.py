from fastapi import APIRouter, HTTPException, status, Depends, Request, Response, Cookie
from app.core.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies.auth import get_current_user
from app.db.session import get_db
from app.schemas.auth import AuthResponse, RegisterRequest, UserResponse

from app.service.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=AuthResponse)
async def register(
    payload: RegisterRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    auth_service = AuthService(db)
    result = (
        await auth_service.register(
            email=payload.email,
            password=payload.email,
            password=payload.password,
            first_name=payload.first_name,
            last_name=payload.last_name,
            tenant_name=payload.tenant_name,
            ip_address=request.client.host if request.client else None,
        ),
    )
    user_agent = request.headers.get("user-agent")

    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=15 * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=False,  # True in production HTTPS
        samesite="lax",
        max_age=30 * 24 * 60 * 60,
    )
    return AuthResponse(
        message="Registration successful.",
        user=UserResponse.model_validate(result["user"]),
    )


@router.post("/refresh")
async def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
):
    if not refresh_token:
        raise InvalidTokenError()

    auth_service = AuthService(db)

    access_token = await auth_service.refresh_access_token(refresh_token)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # True in production
        samesite="lax",
        max_age=15 * 60,
    )

    return {"message": "Access token refreshed."}


@router.post("/logout")
async def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
):
    if refresh_token:
        auth_service = AuthService(db)

        await auth_service.logout(refresh_token=refresh_token)

    response.delete_cookie(
        key="access_token",
    )

    response.delete_cookie(key="access_token")

    response.delete_cookie(
        key="refresh_token",
    )
    return {"message": "Logged out successfully."}
