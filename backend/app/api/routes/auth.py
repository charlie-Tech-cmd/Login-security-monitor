from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_user
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    UserResponse,
)
from app.services.auth_service import auth_service

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(request: RegisterRequest) -> UserResponse:
    try:
        user = auth_service.register(
            email=str(request.email),
            password=request.password,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return UserResponse(
        id=user.id,
        email=user.email,
    )


@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest) -> AuthResponse:
    result = auth_service.login(
        email=str(request.email),
        password=request.password,
    )

    if not result.success or not result.access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result.message or "Authentication failed. Check your credentials or try again later.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return AuthResponse(access_token=result.access_token)


@router.get("/me", response_model=UserResponse)
def get_me(
    user=Depends(get_current_user),
) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
    )
