"""
Fast Lane - Database Configuration
Database connection, session management, and initialization
"""

import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from backend.models import Base

# Database URL from environment or SQLite fallback
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./database/fast_lane.db"
)

# Engine configuration
if "sqlite" in DATABASE_URL:
    # SQLite specific
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # PostgreSQL or other databases
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        echo=False,
    )

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI to get database session.
    Usage in route: def some_route(db: Session = Depends(get_db))
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables.
    Run this once during startup.
    """
    print("🔧 Initializing database...")
    
    try:
        # Create all tables from models
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized successfully!")
        print(f"📊 Database URL: {DATABASE_URL}")
        
        # Create database directory if using SQLite
        if "sqlite" in DATABASE_URL:
            db_dir = os.path.dirname(DATABASE_URL.replace("sqlite:///./", ""))
            os.makedirs(db_dir, exist_ok=True)
    
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        raise


def drop_db():
    """
    Drop all tables (use with caution!).
    """
    print("⚠️  WARNING: Dropping all database tables...")
    response = input("Type 'YES' to confirm: ")
    
    if response.upper() == "YES":
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped!")
    else:
        print("❌ Operation cancelled")


def seed_db():
    """
    Seed the database with initial data (levels, vehicles, etc.).
    """
    from backend.models import (
        Level, UpgradePricing, Achievement,
        VehicleType
    )
    from sqlalchemy.orm import Session
    
    db: Session = SessionLocal()
    
    try:
        print("🌱 Seeding database with initial data...")
        
        # ===== LEVEL SEEDING =====
        levels_data = [
            {
                "level_number": 1,
                "name": "Gentle Start",
                "description": "Get familiar with your vehicle controls",
                "difficulty": "easy",
                "terrain_type": "smooth_hill",
                "seed": 12345,
                "max_distance": 500.0,
                "coin_reward": 50,
                "gem_reward": 2,
                "min_level_to_unlock": 1,
                "gravity": 9.8,
                "wind_speed": 0.0,
            },
            {
                "level_number": 2,
                "name": "Mountain Pass",
                "description": "Navigate through winding mountain roads",
                "difficulty": "easy",
                "terrain_type": "smooth_hill",
                "seed": 23456,
                "max_distance": 750.0,
                "coin_reward": 75,
                "gem_reward": 3,
                "min_level_to_unlock": 1,
                "gravity": 9.8,
                "wind_speed": 2.0,
            },
            {
                "level_number": 3,
                "name": "Rocky Terrain",
                "description": "Climb over rocky, uneven ground",
                "difficulty": "medium",
                "terrain_type": "rocky",
                "seed": 34567,
                "max_distance": 1000.0,
                "coin_reward": 100,
                "gem_reward": 5,
                "min_level_to_unlock": 2,
                "gravity": 9.8,
                "wind_speed": 3.0,
            },
            {
                "level_number": 4,
                "name": "Ice Peak",
                "description": "Slippery ice makes control challenging",
                "difficulty": "medium",
                "terrain_type": "ice",
                "seed": 45678,
                "max_distance": 1200.0,
                "coin_reward": 120,
                "gem_reward": 6,
                "min_level_to_unlock": 3,
                "gravity": 9.8,
                "wind_speed": 5.0,
            },
            {
                "level_number": 5,
                "name": "Water Crossing",
                "description": "Navigate through water and mud",
                "difficulty": "medium",
                "terrain_type": "water",
                "seed": 56789,
                "max_distance": 1500.0,
                "coin_reward": 150,
                "gem_reward": 7,
                "min_level_to_unlock": 4,
                "gravity": 9.8,
                "wind_speed": 0.0,
            },
            {
                "level_number": 6,
                "name": "Steep Ascent",
                "description": "Extreme vertical climb requires power",
                "difficulty": "hard",
                "terrain_type": "smooth_hill",
                "seed": 67890,
                "max_distance": 2000.0,
                "coin_reward": 200,
                "gem_reward": 10,
                "min_level_to_unlock": 5,
                "gravity": 10.5,
                "wind_speed": 7.0,
            },
            {
                "level_number": 7,
                "name": "Volcanic Wasteland",
                "description": "Dodge lava flows and hot springs",
                "difficulty": "hard",
                "terrain_type": "rocky",
                "seed": 78901,
                "max_distance": 2500.0,
                "coin_reward": 250,
                "gem_reward": 12,
                "min_level_to_unlock": 6,
                "gravity": 11.0,
                "wind_speed": 6.0,
            },
            {
                "level_number": 8,
                "name": "Arctic Blizzard",
                "description": "Blizzard conditions and ice everywhere",
                "difficulty": "hard",
                "terrain_type": "ice",
                "seed": 89012,
                "max_distance": 3000.0,
                "coin_reward": 300,
                "gem_reward": 15,
                "min_level_to_unlock": 7,
                "gravity": 9.8,
                "wind_speed": 10.0,
            },
            {
                "level_number": 9,
                "name": "Canyon Jump",
                "description": "Jump across massive canyons",
                "difficulty": "extreme",
                "terrain_type": "rocky",
                "seed": 90123,
                "max_distance": 3500.0,
                "coin_reward": 400,
                "gem_reward": 20,
                "min_level_to_unlock": 8,
                "gravity": 12.0,
                "wind_speed": 8.0,
            },
            {
                "level_number": 10,
                "name": "The Peak",
                "description": "Reach the world's highest mountain",
                "difficulty": "extreme",
                "terrain_type": "smooth_hill",
                "seed": 1234,
                "max_distance": 4000.0,
                "coin_reward": 500,
                "gem_reward": 25,
                "min_level_to_unlock": 9,
                "gravity": 11.5,
                "wind_speed": 12.0,
            },
            {
                "level_number": 11,
                "name": "Meteor Crater",
                "description": "Navigate an alien landscape",
                "difficulty": "extreme",
                "terrain_type": "rocky",
                "seed": 11234,
                "max_distance": 5000.0,
                "coin_reward": 600,
                "gem_reward": 30,
                "min_level_to_unlock": 10,
                "gravity": 13.0,
                "wind_speed": 9.0,
            },
            {
                "level_number": 12,
                "name": "Dark Abyss",
                "description": "Race in complete darkness",
                "difficulty": "extreme",
                "terrain_type": "water",
                "seed": 21234,
                "max_distance": 5500.0,
                "coin_reward": 700,
                "gem_reward": 35,
                "min_level_to_unlock": 11,
                "gravity": 10.0,
                "wind_speed": 15.0,
            },
            {
                "level_number": 13,
                "name": "Infinite Climb",
                "description": "Procedurally generated infinite ascent",
                "difficulty": "extreme",
                "terrain_type": "smooth_hill",
                "seed": 31234,
                "max_distance": 9999.0,
                "coin_reward": 1000,
                "gem_reward": 50,
                "min_level_to_unlock": 12,
                "gravity": 14.0,
                "wind_speed": 20.0,
            },
            {
                "level_number": 14,
                "name": "Dimension X",
                "description": "Reality bends in strange ways",
                "difficulty": "extreme",
                "terrain_type": "rocky",
                "seed": 41234,
                "max_distance": 6000.0,
                "coin_reward": 800,
                "gem_reward": 40,
                "min_level_to_unlock": 13,
                "gravity": 15.0,
                "wind_speed": 25.0,
            },
            {
                "level_number": 15,
                "name": "Ultimate Challenge",
                "description": "The hardest level - Do you have what it takes?",
                "difficulty": "extreme",
                "terrain_type": "ice",
                "seed": 51234,
                "max_distance": 7000.0,
                "coin_reward": 1500,
                "gem_reward": 75,
                "min_level_to_unlock": 14,
                "gravity": 16.0,
                "wind_speed": 30.0,
            },
        ]
        
        # Check if levels already exist
        existing_count = db.query(Level).count()
        if existing_count == 0:
            for level_data in levels_data:
                level = Level(**level_data)
                db.add(level)
            db.commit()
            print(f"✅ Seeded {len(levels_data)} levels")
        else:
            print(f"⏭️  Levels already exist ({existing_count} found), skipping...")
        
        # ===== UPGRADE PRICING SEEDING =====
        upgrades_data = [
            # JEEP UPGRADES
            {"upgrade_type": "engine", "vehicle_type": "jeep", "level": 1, "coin_cost": 500, "torque_bonus": 10.0},
            {"upgrade_type": "engine", "vehicle_type": "jeep", "level": 2, "coin_cost": 1000, "torque_bonus": 15.0},
            {"upgrade_type": "engine", "vehicle_type": "jeep", "level": 3, "coin_cost": 1500, "torque_bonus": 20.0},
            {"upgrade_type": "engine", "vehicle_type": "jeep", "level": 4, "coin_cost": 2000, "gem_cost": 5, "torque_bonus": 25.0},
            {"upgrade_type": "engine", "vehicle_type": "jeep", "level": 5, "coin_cost": 3000, "gem_cost": 10, "torque_bonus": 30.0},
            
            {"upgrade_type": "suspension", "vehicle_type": "jeep", "level": 1, "coin_cost": 300, "stability_bonus": 5.0},
            {"upgrade_type": "suspension", "vehicle_type": "jeep", "level": 2, "coin_cost": 600, "stability_bonus": 10.0},
            {"upgrade_type": "suspension", "vehicle_type": "jeep", "level": 3, "coin_cost": 900, "stability_bonus": 15.0},
            {"upgrade_type": "suspension", "vehicle_type": "jeep", "level": 4, "coin_cost": 1200, "gem_cost": 3, "stability_bonus": 20.0},
            {"upgrade_type": "suspension", "vehicle_type": "jeep", "level": 5, "coin_cost": 1800, "gem_cost": 7, "stability_bonus": 25.0},
            
            {"upgrade_type": "tires", "vehicle_type": "jeep", "level": 1, "coin_cost": 400, "speed_bonus": 5.0},
            {"upgrade_type": "tires", "vehicle_type": "jeep", "level": 2, "coin_cost": 800, "speed_bonus": 10.0},
            {"upgrade_type": "tires", "vehicle_type": "jeep", "level": 3, "coin_cost": 1200, "speed_bonus": 15.0},
            {"upgrade_type": "tires", "vehicle_type": "jeep", "level": 4, "coin_cost": 1600, "gem_cost": 4, "speed_bonus": 20.0},
            {"upgrade_type": "tires", "vehicle_type": "jeep", "level": 5, "coin_cost": 2400, "gem_cost": 8, "speed_bonus": 25.0},
            
            {"upgrade_type": "4wd", "vehicle_type": "jeep", "level": 1, "coin_cost": 600, "stability_bonus": 10.0},
            {"upgrade_type": "4wd", "vehicle_type": "jeep", "level": 2, "coin_cost": 1200, "gem_cost": 5, "stability_bonus": 20.0},
            {"upgrade_type": "4wd", "vehicle_type": "jeep", "level": 3, "coin_cost": 2000, "gem_cost": 10, "stability_bonus": 30.0},
            
            # BIKE UPGRADES (Lighter, faster, cheaper)
            {"upgrade_type": "engine", "vehicle_type": "bike", "level": 1, "coin_cost": 400, "torque_bonus": 8.0},
            {"upgrade_type": "engine", "vehicle_type": "bike", "level": 2, "coin_cost": 800, "torque_bonus": 12.0},
            {"upgrade_type": "engine", "vehicle_type": "bike", "level": 3, "coin_cost": 1200, "torque_bonus": 16.0},
            {"upgrade_type": "engine", "vehicle_type": "bike", "level": 4, "coin_cost": 1600, "gem_cost": 4, "torque_bonus": 20.0},
            {"upgrade_type": "engine", "vehicle_type": "bike", "level": 5, "coin_cost": 2400, "gem_cost": 8, "torque_bonus": 24.0},
            
            {"upgrade_type": "suspension", "vehicle_type": "bike", "level": 1, "coin_cost": 250, "stability_bonus": 4.0},
            {"upgrade_type": "suspension", "vehicle_type": "bike", "level": 2, "coin_cost": 500, "stability_bonus": 8.0},
            {"upgrade_type": "suspension", "vehicle_type": "bike", "level": 3, "coin_cost": 750, "stability_bonus": 12.0},
            {"upgrade_type": "suspension", "vehicle_type": "bike", "level": 4, "coin_cost": 1000, "gem_cost": 2, "stability_bonus": 16.0},
            {"upgrade_type": "suspension", "vehicle_type": "bike", "level": 5, "coin_cost": 1500, "gem_cost": 5, "stability_bonus": 20.0},
            
            {"upgrade_type": "tires", "vehicle_type": "bike", "level": 1, "coin_cost": 350, "speed_bonus": 6.0},
            {"upgrade_type": "tires", "vehicle_type": "bike", "level": 2, "coin_cost": 700, "speed_bonus": 12.0},
            {"upgrade_type": "tires", "vehicle_type": "bike", "level": 3, "coin_cost": 1050, "speed_bonus": 18.0},
            {"upgrade_type": "tires", "vehicle_type": "bike", "level": 4, "coin_cost": 1400, "gem_cost": 3, "speed_bonus": 24.0},
            {"upgrade_type": "tires", "vehicle_type": "bike", "level": 5, "coin_cost": 2100, "gem_cost": 6, "speed_bonus": 30.0},
            
            # TRUCK UPGRADES (Heavier, stronger, expensive)
            {"upgrade_type": "engine", "vehicle_type": "truck", "level": 1, "coin_cost": 700, "torque_bonus": 15.0},
            {"upgrade_type": "engine", "vehicle_type": "truck", "level": 2, "coin_cost": 1400, "torque_bonus": 20.0},
            {"upgrade_type": "engine", "vehicle_type": "truck", "level": 3, "coin_cost": 2100, "torque_bonus": 25.0},
            {"upgrade_type": "engine", "vehicle_type": "truck", "level": 4, "coin_cost": 2800, "gem_cost": 7, "torque_bonus": 30.0},
            {"upgrade_type": "engine", "vehicle_type": "truck", "level": 5, "coin_cost": 4200, "gem_cost": 14, "torque_bonus": 35.0},
            
            {"upgrade_type": "suspension", "vehicle_type": "truck", "level": 1, "coin_cost": 400, "stability_bonus": 7.0},
            {"upgrade_type": "suspension", "vehicle_type": "truck", "level": 2, "coin_cost": 800, "stability_bonus": 14.0},
            {"upgrade_type": "suspension", "vehicle_type": "truck", "level": 3, "coin_cost": 1200, "stability_bonus": 21.0},
            {"upgrade_type": "suspension", "vehicle_type": "truck", "level": 4, "coin_cost": 1600, "gem_cost": 4, "stability_bonus": 28.0},
            {"upgrade_type": "suspension", "vehicle_type": "truck", "level": 5, "coin_cost": 2400, "gem_cost": 8, "stability_bonus": 35.0},
            
            {"upgrade_type": "tires", "vehicle_type": "truck", "level": 1, "coin_cost": 500, "speed_bonus": 3.0},
            {"upgrade_type": "tires", "vehicle_type": "truck", "level": 2, "coin_cost": 1000, "speed_bonus": 6.0},
            {"upgrade_type": "tires", "vehicle_type": "truck", "level": 3, "coin_cost": 1500, "speed_bonus": 9.0},
            {"upgrade_type": "tires", "vehicle_type": "truck", "level": 4, "coin_cost": 2000, "gem_cost": 5, "speed_bonus": 12.0},
            {"upgrade_type": "tires", "vehicle_type": "truck", "level": 5, "coin_cost": 3000, "gem_cost": 10, "speed_bonus": 15.0},
            
            {"upgrade_type": "4wd", "vehicle_type": "truck", "level": 1, "coin_cost": 800, "stability_bonus": 15.0},
            {"upgrade_type": "4wd", "vehicle_type": "truck", "level": 2, "coin_cost": 1600, "gem_cost": 7, "stability_bonus": 30.0},
            {"upgrade_type": "4wd", "vehicle_type": "truck", "level": 3, "coin_cost": 2800, "gem_cost": 14, "stability_bonus": 45.0},
        ]
        
        existing_upgrades = db.query(UpgradePricing).count()
        if existing_upgrades == 0:
            for upgrade_data in upgrades_data:
                upgrade = UpgradePricing(**upgrade_data)
                db.add(upgrade)
            db.commit()
            print(f"✅ Seeded {len(upgrades_data)} upgrade prices")
        else:
            print(f"⏭️  Upgrades already exist ({existing_upgrades} found), skipping...")
        
        # ===== ACHIEVEMENTS SEEDING =====
        achievements_data = [
            {
                "name": "First Step",
                "description": "Complete level 1",
                "criteria_type": "level_completed",
                "criteria_value": 1,
                "gem_reward": 5,
            },
            {
                "name": "Halfway There",
                "description": "Unlock level 8",
                "criteria_type": "level_unlocked",
                "criteria_value": 8,
                "gem_reward": 25,
            },
            {
                "name": "Legend",
                "description": "Complete all 15 levels",
                "criteria_type": "levels_completed",
                "criteria_value": 15,
                "gem_reward": 100,
            },
            {
                "name": "Coin Collector",
                "description": "Collect 10,000 coins",
                "criteria_type": "coins_collected",
                "criteria_value": 10000,
                "gem_reward": 50,
            },
            {
                "name": "Distance Master",
                "description": "Travel 100 km total distance",
                "criteria_type": "total_distance",
                "criteria_value": 100000,
                "gem_reward": 75,
            },
            {
                "name": "Gem Hunter",
                "description": "Collect 500 gems",
                "criteria_type": "gems_collected",
                "criteria_value": 500,
                "gem_reward": 100,
            },
            {
                "name": "Vehicle Master",
                "description": "Own all 3 vehicles",
                "criteria_type": "vehicles_owned",
                "criteria_value": 3,
                "gem_reward": 40,
            },
            {
                "name": "Upgrade Enthusiast",
                "description": "Upgrade all vehicle stats to max",
                "criteria_type": "max_upgrades",
                "criteria_value": 1,
                "gem_reward": 150,
            },
        ]
        
        existing_achievements = db.query(Achievement).count()
        if existing_achievements == 0:
            for achievement_data in achievements_data:
                achievement = Achievement(**achievement_data)
                db.add(achievement)
            db.commit()
            print(f"✅ Seeded {len(achievements_data)} achievements")
        else:
            print(f"⏭️  Achievements already exist ({existing_achievements} found), skipping...")
        
        print("\n✅ Database seeding completed!")
    
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    seed_db()
