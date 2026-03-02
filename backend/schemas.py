"""
Fast Lane - Pydantic Schemas
Request and Response validation schemas for FastAPI
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import re


# Email validation regex pattern
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


# ============== AUTH SCHEMAS ==============

class SignUpRequest(BaseModel):
    """Schema for user sign-up."""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    password_confirm: str = Field(..., min_length=8, max_length=100)
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format."""
        if not EMAIL_PATTERN.match(v):
            raise ValueError("Invalid email format")
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validate password complexity."""
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        return v
    
    @field_validator('password_confirm')
    @classmethod
    def passwords_match(cls, v, info):
        """Ensure passwords match."""
        if 'password' in info.data and v != info.data['password']:
            raise ValueError("Passwords do not match")
        return v


class LoginRequest(BaseModel):
    """Schema for user login."""
    email: str = Field(..., min_length=5, max_length=100)
    password: str
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format."""
        if not EMAIL_PATTERN.match(v):
            raise ValueError("Invalid email format")
        return v


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # in seconds
    user: Optional['UserResponse'] = None


class TokenData(BaseModel):
    """Schema for token data."""
    user_id: int
    username: str


# ============== USER SCHEMAS ==============

class UserBase(BaseModel):
    """Base user schema."""
    username: str
    email: str


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    username: Optional[str] = None
    email: Optional[str] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None


class UserStats(BaseModel):
    """User statistics schema."""
    total_coins: int
    total_gems: int
    current_level: int
    level_unlocked: int
    best_distance: float
    total_coins_earned: int
    total_gems_earned: int


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    coins: int
    gems: int
    current_level: int
    level_unlocked: int
    best_distance: float
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """Detailed user response with vehicles."""
    vehicles: List['VehicleResponse'] = []
    stats: Optional[UserStats] = None
    
    class Config:
        from_attributes = True


# ============== VEHICLE SCHEMAS ==============

class VehicleBase(BaseModel):
    """Base vehicle schema."""
    vehicle_type: str  # jeep, bike, truck
    engine_level: int = Field(default=0, ge=0, le=5)
    suspension_level: int = Field(default=0, ge=0, le=5)
    tires_level: int = Field(default=0, ge=0, le=5)
    four_wd_level: int = Field(default=0, ge=0, le=3)


class VehicleCreate(VehicleBase):
    """Schema for creating a vehicle."""
    pass


class VehicleUpgrade(BaseModel):
    """Schema for upgrading a vehicle."""
    upgrade_type: str  # engine, suspension, tires, 4wd
    level: int = Field(..., ge=1, le=5)


class VehicleResponse(VehicleBase):
    """Schema for vehicle response."""
    id: int
    user_id: int
    max_torque: float
    max_speed: float
    weight: float
    friction: float
    bounce_factor: float
    fuel_capacity: float
    is_owned: bool
    is_equipped: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============== LEVEL SCHEMAS ==============

class LevelBase(BaseModel):
    """Base level schema."""
    level_number: int
    name: str
    description: Optional[str] = None
    difficulty: str  # easy, medium, hard, extreme
    terrain_type: str


class LevelCreate(LevelBase):
    """Schema for creating a level."""
    min_level_to_unlock: int = 1
    coin_reward: int = 100
    gem_reward: int = 5
    max_distance: float = 1000.0


class LevelResponse(LevelBase):
    """Schema for level response."""
    id: int
    min_level_to_unlock: int
    coin_reward: int
    gem_reward: int
    bonus_stars: int
    max_distance: float
    gravity: float
    wind_speed: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class LevelProgressBase(BaseModel):
    """Base level progress schema."""
    is_unlocked: bool = False
    is_completed: bool = False


class LevelProgressResponse(LevelProgressBase):
    """Schema for level progress response."""
    id: int
    user_id: int
    level_id: int
    times_played: int
    best_distance: float
    best_time: float
    best_coins_collected: int
    stars_earned: int
    last_played: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ============== GAME SESSION SCHEMAS ==============

class GameSessionCreate(BaseModel):
    """Schema for creating a game session."""
    level_id: int
    vehicle_id: int


class GameSessionUpdate(BaseModel):
    """Schema for updating game session."""
    distance_traveled: float
    coins_collected: int
    gems_collected: int
    fuel_used: float
    time_elapsed: float
    crashed: bool = False
    out_of_fuel: bool = False
    is_completed: bool = False


class GameSessionResponse(BaseModel):
    """Schema for game session response."""
    id: int
    user_id: int
    level_id: int
    vehicle_id: int
    distance_traveled: float
    coins_collected: int
    gems_collected: int
    fuel_used: float
    time_elapsed: float
    is_active: bool
    is_completed: bool
    crashed: bool
    out_of_fuel: bool
    started_at: datetime
    ended_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ============== LEADERBOARD SCHEMAS ==============

class LeaderboardResponse(BaseModel):
    """Schema for leaderboard entry."""
    id: int
    user_id: int
    username: str
    total_distance: float
    total_coins: int
    levels_completed: int
    rank: int
    avg_best_distance: float
    current_streak: int
    best_streak: int


class LeaderboardListResponse(BaseModel):
    """Schema for leaderboard list response."""
    entries: List[LeaderboardResponse]
    total_players: int
    user_rank: Optional[int] = None


# ============== UPGRADE SCHEMAS ==============

class UpgradePricingResponse(BaseModel):
    """Schema for upgrade pricing."""
    id: int
    upgrade_type: str
    vehicle_type: str
    level: int
    coin_cost: int
    gem_cost: int
    torque_bonus: float
    speed_bonus: float
    stability_bonus: float
    fuel_efficiency_bonus: float
    
    class Config:
        from_attributes = True


class UpgradeShopResponse(BaseModel):
    """Schema for upgrade shop display."""
    engine_upgrades: List[UpgradePricingResponse]
    suspension_upgrades: List[UpgradePricingResponse]
    tires_upgrades: List[UpgradePricingResponse]
    four_wd_upgrades: List[UpgradePricingResponse]


# ============== ACHIEVEMENT SCHEMAS ==============

class AchievementResponse(BaseModel):
    """Schema for achievement response."""
    id: int
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    criteria_type: str
    criteria_value: float
    gem_reward: int
    
    class Config:
        from_attributes = True


class UserAchievementResponse(BaseModel):
    """Schema for user achievement response."""
    achievement_id: int
    achievement: AchievementResponse
    unlocked: bool
    unlocked_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ============== COMMON RESPONSE SCHEMAS ==============

class SuccessResponse(BaseModel):
    """Standard success response."""
    success: bool = True
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: str
    status_code: int


class PaginatedResponse(BaseModel):
    """Schema for paginated responses."""
    items: List
    total: int
    page: int
    page_size: int
    total_pages: int


# Update forward references
Token.update_forward_refs()
UserDetailResponse.update_forward_refs()
