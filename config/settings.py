"""
Fast Lane - Configuration Settings
Application-wide configuration and environment variables
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings managed through environment variables.
    
    Can be overridden by .env file or OS environment variables.
    """
    
    # ============== APP CONFIGURATION ==============
    app_name: str = "Fast Lane"
    app_version: str = "1.0.0"
    app_description: str = "Hill Climb Racing Clone - Full-stack Web Application"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # ============== SERVER ==============
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))
    reload: bool = os.getenv("RELOAD", "True").lower() == "true"
    
    # ============== DATABASE ==============
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./database/fast_lane.db"
    )
    database_echo: bool = os.getenv("DATABASE_ECHO", "False").lower() == "true"
    
    # ============== JWT & SECURITY ==============
    secret_key: str = os.getenv(
        "SECRET_KEY",
        "change-this-to-a-random-secret-key-in-production"
    )
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )
    
    # ============== CORS ==============
    cors_origins: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "*",  # Allow all origins in development
    ]
    cors_credentials: bool = True
    cors_methods: list = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    cors_headers: list = ["*"]
    
    # ============== GAME CONFIGURATION ==============
    # Physics
    default_gravity: float = 9.8
    max_wind_speed: float = 30.0
    
    # Level system
    total_levels: int = 15
    starting_level: int = 1
    starting_coins: int = 0
    starting_gems: int = 0
    
    # Vehicle parameters
    jeep_weight: float = 1500.0  # kg
    bike_weight: float = 200.0
    truck_weight: float = 3000.0
    
    default_fuel_capacity: float = 100.0
    default_fuel_consumption: float = 0.5
    
    # Upgrade costs (in coins)
    upgrade_base_cost: int = 500
    upgrade_cost_multiplier: float = 1.5
    
    # Rewards
    base_coin_reward: int = 100
    base_gem_reward: int = 5
    coin_multiplier_per_level: float = 1.2
    gem_multiplier_per_level: float = 1.1
    
    # ============== LEADERBOARD ==============
    leaderboard_update_frequency: int = 3600  # seconds (1 hour)
    leaderboard_top_count: int = 100
    
    # ============== LOGGING ==============
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "logs/fast_lane.log")
    
    # ============== FEATURES ==============
    enable_leaderboard: bool = True
    enable_achievements: bool = True
    enable_multiplayer: bool = False  # Future feature
    enable_analytics: bool = True
    
    # ============== RATE LIMITING ==============
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 60  # seconds
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Initialize settings instance
settings = Settings()


# ============== VALIDATION ==============

def validate_settings():
    """
    Validate critical settings and warn about insecure configurations.
    """
    warnings = []
    
    # Check secret key
    if settings.secret_key == "change-this-to-a-random-secret-key-in-production":
        warnings.append(
            "⚠️  WARNING: Using default SECRET_KEY. "
            "Change in production via .env file!"
        )
    
    # Check debug mode
    if settings.debug:
        warnings.append(
            "⚠️  WARNING: Debug mode is enabled. "
            "Disable in production (DEBUG=False)"
        )
    
    # Check CORS configuration
    if "*" in settings.cors_origins:
        warnings.append(
            "⚠️  WARNING: CORS allows all origins (*). "
            "Restrict in production for security."
        )
    
    # Check database
    if "sqlite" in settings.database_url and settings.debug is False:
        warnings.append(
            "⚠️  WARNING: Using SQLite in production. "
            "Consider using PostgreSQL for better performance."
        )
    
    # Print all warnings
    if warnings:
        print("\n" + "="*60)
        print("🔐 SECURITY CONFIGURATION CHECK")
        print("="*60)
        for warning in warnings:
            print(warning)
        print("="*60 + "\n")


# Configuration presets for different environments
class DevelopmentSettings(Settings):
    """Development environment configuration."""
    debug: bool = True
    database_echo: bool = True
    cors_origins: list = ["*"]


class ProductionSettings(Settings):
    """Production environment configuration."""
    debug: bool = False
    database_echo: bool = False
    cors_origins: list = ["https://yourdomain.com"]


class TestingSettings(Settings):
    """Testing environment configuration."""
    debug: bool = True
    database_url: str = "sqlite:///./test.db"
    access_token_expire_minutes: int = 30


def get_settings() -> Settings:
    """
    Get settings based on environment.
    
    Returns:
        Settings instance for current environment
    """
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionSettings()
    elif env == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()


# ============== SHORTCUTS ==============
def get_database_url() -> str:
    """Get formatted database URL."""
    return settings.database_url


def get_cors_config() -> dict:
    """Get CORS middleware configuration."""
    return {
        "allow_origins": settings.cors_origins,
        "allow_credentials": settings.cors_credentials,
        "allow_methods": settings.cors_methods,
        "allow_headers": settings.cors_headers,
    }


def get_jwt_config() -> dict:
    """Get JWT configuration."""
    return {
        "secret_key": settings.secret_key,
        "algorithm": settings.algorithm,
        "access_token_expire_minutes": settings.access_token_expire_minutes,
    }


if __name__ == "__main__":
    # Print all settings when run directly
    print("\n" + "="*60)
    print("FAST LANE - CONFIGURATION")
    print("="*60)
    
    print("\n📱 APP CONFIGURATION")
    print(f"  App Name: {settings.app_name}")
    print(f"  Version: {settings.app_version}")
    print(f"  Debug: {settings.debug}")
    
    print("\n🌐 SERVER CONFIGURATION")
    print(f"  Host: {settings.host}")
    print(f"  Port: {settings.port}")
    
    print("\n📊 DATABASE CONFIGURATION")
    print(f"  URL: {settings.database_url}")
    print(f"  Echo: {settings.database_echo}")
    
    print("\n🎮 GAME CONFIGURATION")
    print(f"  Total Levels: {settings.total_levels}")
    print(f"  Default Gravity: {settings.default_gravity}")
    print(f"  Starting Coins: {settings.starting_coins}")
    print(f"  Starting Gems: {settings.starting_gems}")
    
    print("\n🔐 SECURITY CONFIGURATION")
    print(f"  Algorithm: {settings.algorithm}")
    print(f"  Token Expiry: {settings.access_token_expire_minutes} minutes")
    
    print("\n✅ Configuration validated\n")
    
    validate_settings()
