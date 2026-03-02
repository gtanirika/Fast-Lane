"""
Fast Lane - SQLAlchemy Models
Database models for Users, Vehicles, Levels, and Game Statistics
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class User(Base):
    """User model - stores player account information."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Game currency
    coins = Column(Integer, default=0)
    gems = Column(Integer, default=0)
    
    # Progress tracking
    current_level = Column(Integer, default=1)
    level_unlocked = Column(Integer, default=1)  # Highest level unlocked
    best_distance = Column(Float, default=0.0)
    total_coins_earned = Column(Integer, default=0)
    total_gems_earned = Column(Integer, default=0)
    
    # Vehicle selection
    current_vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    
    # Account management
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    vehicles = relationship("Vehicle", back_populates="owner", cascade="all, delete-orphan")
    leaderboard_entry = relationship("Leaderboard", uselist=False, back_populates="user")
    level_progress = relationship("LevelProgress", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', coins={self.coins})>"


class VehicleType(str, enum.Enum):
    """Enum for vehicle types."""
    JEEP = "jeep"
    BIKE = "bike"
    TRUCK = "truck"


class Vehicle(Base):
    """Vehicle model - stores vehicle information and upgrades."""
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Vehicle type
    vehicle_type = Column(String(20), nullable=False)  # jeep, bike, truck
    
    # Upgrade levels (0-5 levels for each)
    engine_level = Column(Integer, default=0)
    suspension_level = Column(Integer, default=0)
    tires_level = Column(Integer, default=0)
    four_wd_level = Column(Integer, default=0)  # Only for Jeep/Truck
    
    # Vehicle stats (dynamically calculated based on upgrades)
    max_torque = Column(Float, default=100.0)  # Affected by engine level
    max_speed = Column(Float, default=50.0)
    weight = Column(Float, default=1000.0)  # kg
    friction = Column(Float, default=0.8)
    bounce_factor = Column(Float, default=0.6)  # Affected by suspension level
    
    # Fuel capacity
    fuel_capacity = Column(Float, default=100.0)
    fuel_consumption_rate = Column(Float, default=0.5)  # per distance unit
    
    # Status
    is_owned = Column(Boolean, default=True)
    is_equipped = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="vehicles")
    
    def __repr__(self):
        return f"<Vehicle(id={self.id}, type={self.vehicle_type}, engine_lv={self.engine_level})>"


class Level(Base):
    """Level model - stores level information and terrain data."""
    __tablename__ = "levels"
    
    id = Column(Integer, primary_key=True, index=True)
    level_number = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    
    # Difficulty and rewards
    difficulty = Column(String(20))  # easy, medium, hard, extreme
    min_level_to_unlock = Column(Integer, default=1)
    
    # Terrain generation
    terrain_type = Column(String(50))  # smooth_hill, rocky, ice, water
    seed = Column(Integer)  # For procedural generation
    max_distance = Column(Float, default=1000.0)
    
    # Rewards
    coin_reward = Column(Integer, default=100)
    gem_reward = Column(Integer, default=5)
    bonus_stars = Column(Integer, default=3)  # Max 3 stars
    
    # Level settings
    gravity = Column(Float, default=9.8)
    wind_speed = Column(Float, default=0.0)
    obstacles_enabled = Column(Boolean, default=True)
    fuel_required = Column(Float, default=100.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    progress_entries = relationship("LevelProgress", back_populates="level", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Level(number={self.level_number}, name='{self.name}', difficulty={self.difficulty})>"


class LevelProgress(Base):
    """LevelProgress model - tracks user progress on each level."""
    __tablename__ = "level_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)
    
    # Progress tracking
    is_unlocked = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    times_played = Column(Integer, default=0)
    
    # Best performance
    best_distance = Column(Float, default=0.0)
    best_time = Column(Float, default=0.0)  # in seconds
    best_coins_collected = Column(Integer, default=0)
    stars_earned = Column(Integer, default=0)  # 0-3 stars
    
    # Last attempt
    last_played = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="level_progress")
    level = relationship("Level", back_populates="progress_entries")
    
    def __repr__(self):
        return f"<LevelProgress(user_id={self.user_id}, level_id={self.level_id}, stars={self.stars_earned})>"


class Leaderboard(Base):
    """Leaderboard model - global rankings for players."""
    __tablename__ = "leaderboard"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Rankings
    total_distance = Column(Float, default=0.0)
    total_coins = Column(Integer, default=0)
    levels_completed = Column(Integer, default=0)
    rank = Column(Integer, default=0)
    
    # Stats
    avg_best_distance = Column(Float, default=0.0)
    playtime_hours = Column(Float, default=0.0)
    
    # Streaks
    current_streak = Column(Integer, default=0)
    best_streak = Column(Integer, default=0)
    
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="leaderboard_entry")
    
    def __repr__(self):
        return f"<Leaderboard(user_id={self.user_id}, rank={self.rank}, distance={self.total_distance})>"


class GameSession(Base):
    """GameSession model - tracks active game sessions."""
    __tablename__ = "game_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    
    # Session data
    distance_traveled = Column(Float, default=0.0)
    coins_collected = Column(Integer, default=0)
    gems_collected = Column(Integer, default=0)
    fuel_used = Column(Float, default=0.0)
    time_elapsed = Column(Float, default=0.0)  # in seconds
    
    # Game state
    is_active = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)
    crashed = Column(Boolean, default=False)
    out_of_fuel = Column(Boolean, default=False)
    
    # Session timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<GameSession(user_id={self.user_id}, level_id={self.level_id}, distance={self.distance_traveled})>"


class UpgradePricing(Base):
    """UpgradePricing model - defines cost and stats for upgrades."""
    __tablename__ = "upgrade_pricing"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Upgrade identification
    upgrade_type = Column(String(50), nullable=False)  # engine, suspension, tires, 4wd
    vehicle_type = Column(String(20), nullable=False)  # jeep, bike, truck
    level = Column(Integer, nullable=False)  # upgrade level (1-5)
    
    # Pricing
    coin_cost = Column(Integer, nullable=False)
    gem_cost = Column(Integer, default=0)
    
    # Stat improvements
    torque_bonus = Column(Float, default=0.0)
    speed_bonus = Column(Float, default=0.0)
    stability_bonus = Column(Float, default=0.0)
    fuel_efficiency_bonus = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<UpgradePricing(type={self.upgrade_type}, level={self.level}, cost={self.coin_cost})>"


class Achievement(Base):
    """Achievement model - in-game achievements and badges."""
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(500))
    icon = Column(String(255))  # Path to achievement icon
    
    # Criteria
    criteria_type = Column(String(50))  # distance, coins_collected, levels_completed, etc.
    criteria_value = Column(Float, nullable=False)
    
    # Reward
    gem_reward = Column(Integer, default=10)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Achievement(name='{self.name}', criteria={self.criteria_type})>"


class UserAchievement(Base):
    """UserAchievement model - tracks user achievements."""
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    
    unlocked = Column(Boolean, default=False)
    unlocked_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<UserAchievement(user_id={self.user_id}, achievement_id={self.achievement_id})>"
