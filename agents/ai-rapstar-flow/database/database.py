"""
AI RAPSTAR FLØW - Database Configuration
Advanced database setup for rap battles, beats, and user analytics
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
from typing import Generator
import logging

from .models import Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://flow_user:flow_password@localhost:5432/ai_rapstar_flow_db"
)

# For development/testing with SQLite
SQLITE_URL = "sqlite:///./ai_rapstar_flow.db"

# Choose database based on environment
DB_URL = DATABASE_URL if os.getenv("ENVIRONMENT") == "production" else SQLITE_URL

# Create engine
if "sqlite" in DB_URL:
    engine = create_engine(
        DB_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True  # Set to False in production
    )
else:
    engine = create_engine(
        DB_URL,
        pool_size=20,
        max_overflow=30,
        pool_pre_ping=True,
        echo=True  # Set to False in production
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Error creating database tables: {e}")
        return False

def get_db() -> Generator[Session, None, None]:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database with default data"""
    try:
        create_tables()
        
        # Import models after engine creation
        from .models import (
            Achievements, Beats, RapStyleEnum, UserTierEnum, 
            BattleModeEnum, BattleStatusEnum
        )
        
        db = SessionLocal()
        
        # Create default achievements
        default_achievements = [
            {
                "name": "First Battle",
                "description": "Complete your first rap battle with AI FLØW",
                "category": "battle",
                "requirement_type": "battles_completed",
                "requirement_value": 1,
                "points_reward": 100,
                "rarity": "common",
                "badge_color": "bronze"
            },
            {
                "name": "Lyrical Genius",
                "description": "Write 1000 bars",
                "category": "creativity",
                "requirement_type": "bars_written",
                "requirement_value": 1000,
                "points_reward": 500,
                "rarity": "rare",
                "badge_color": "silver"
            },
            {
                "name": "Battle Veteran",
                "description": "Win 50 battles",
                "category": "battle",
                "requirement_type": "battles_won",
                "requirement_value": 50,
                "points_reward": 1000,
                "rarity": "epic",
                "badge_color": "gold"
            },
            {
                "name": "Flow Master",
                "description": "Achieve 90+ overall rating",
                "category": "skill",
                "requirement_type": "overall_rating",
                "requirement_value": 90,
                "points_reward": 2000,
                "rarity": "legendary",
                "badge_color": "diamond"
            },
            {
                "name": "Freestyle King",
                "description": "Complete 100 freestyle sessions",
                "category": "creativity",
                "requirement_type": "freestyle_sessions",
                "requirement_value": 100,
                "points_reward": 750,
                "rarity": "epic",
                "badge_color": "purple"
            },
            {
                "name": "Battle Royale",
                "description": "Win 10 battles in a row",
                "category": "battle",
                "requirement_type": "consecutive_wins",
                "requirement_value": 10,
                "points_reward": 1500,
                "rarity": "legendary",
                "badge_color": "rainbow"
            }
        ]
        
        # Check if achievements already exist
        existing_achievements = db.query(Achievements).count()
        if existing_achievements == 0:
            for achievement_data in default_achievements:
                achievement = Achievements(**achievement_data)
                db.add(achievement)
            
            logger.info("✅ Default achievements created!")
        
        # Create default beats
        default_beats = [
            {
                "name": "Classic Boom Bap",
                "style": RapStyleEnum.BOOM_BAP,
                "bpm": 90,
                "key": "C minor",
                "mood": "nostalgic",
                "energy_level": 6,
                "tags": ["classic", "old-school", "vintage"],
                "description": "Classic 90s boom bap beat with hard-hitting drums",
                "is_premium": False
            },
            {
                "name": "Trap Heat",
                "style": RapStyleEnum.TRAP,
                "bpm": 140,
                "key": "G minor",
                "mood": "energetic",
                "energy_level": 9,
                "tags": ["trap", "modern", "heavy"],
                "description": "Modern trap beat with 808s and hi-hats",
                "is_premium": False
            },
            {
                "name": "Battle Zone",
                "style": RapStyleEnum.BATTLE,
                "bpm": 95,
                "key": "D minor",
                "mood": "aggressive",
                "energy_level": 10,
                "tags": ["battle", "aggressive", "intense"],
                "description": "Intense battle beat designed for rap battles",
                "is_premium": False
            },
            {
                "name": "Freestyle Flow",
                "style": RapStyleEnum.FREESTYLE,
                "bpm": 85,
                "key": "F major",
                "mood": "relaxed",
                "energy_level": 5,
                "tags": ["freestyle", "chill", "smooth"],
                "description": "Smooth beat perfect for freestyle sessions",
                "is_premium": False
            },
            {
                "name": "Drill Sergeant",
                "style": RapStyleEnum.DRILL,
                "bpm": 150,
                "key": "Bb minor",
                "mood": "dark",
                "energy_level": 8,
                "tags": ["drill", "dark", "aggressive"],
                "description": "Dark drill beat with menacing undertones",
                "is_premium": True
            },
            {
                "name": "Conscious Vibes",
                "style": RapStyleEnum.CONSCIOUS,
                "bpm": 80,
                "key": "E major",
                "mood": "thoughtful",
                "energy_level": 4,
                "tags": ["conscious", "peaceful", "deep"],
                "description": "Thoughtful beat for conscious rap",
                "is_premium": True
            }
        ]
        
        # Check if beats already exist
        existing_beats = db.query(Beats).count()
        if existing_beats == 0:
            for beat_data in default_beats:
                beat = Beats(**beat_data)
                db.add(beat)
            
            logger.info("✅ Default beats created!")
        
        # Commit all changes
        db.commit()
        db.close()
        
        logger.info("✅ Database initialized successfully with default data!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error initializing database: {e}")
        if db:
            db.rollback()
            db.close()
        return False

def reset_database():
    """Reset database (DROP ALL TABLES) - Use with caution!"""
    try:
        logger.warning("⚠️ RESETTING DATABASE - ALL DATA WILL BE LOST!")
        Base.metadata.drop_all(bind=engine)
        logger.info("✅ Database reset successfully!")
        return init_database()
    except Exception as e:
        logger.error(f"❌ Error resetting database: {e}")
        return False

def get_database_info():
    """Get database information and statistics"""
    try:
        from .models import (
            Users, RapSessions, Messages, Battles, Beats, 
            Achievements, SystemStats
        )
        
        db = SessionLocal()
        
        info = {
            "database_url": DB_URL.split("@")[-1] if "@" in DB_URL else DB_URL,
            "engine_info": str(engine.url),
            "table_counts": {
                "users": db.query(Users).count(),
                "rap_sessions": db.query(RapSessions).count(),
                "messages": db.query(Messages).count(),
                "battles": db.query(Battles).count(),
                "beats": db.query(Beats).count(),
                "achievements": db.query(Achievements).count(),
                "system_stats": db.query(SystemStats).count()
            },
            "tables_created": True
        }
        
        db.close()
        return info
        
    except Exception as e:
        logger.error(f"❌ Error getting database info: {e}")
        return {"error": str(e), "tables_created": False}

# Database health check
def health_check():
    """Check database connection health"""
    try:
        db = SessionLocal()
        # Simple query to test connection
        db.execute("SELECT 1")
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"❌ Database health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    # Initialize database when script is run directly
    print("🎤 AI RAPSTAR FLØW - Database Initialization")
    print("=" * 50)
    
    if init_database():
        print("✅ Database setup completed successfully!")
        
        # Print database info
        info = get_database_info()
        print("\n📊 Database Information:")
        print(f"Database URL: {info.get('database_url', 'N/A')}")
        print(f"Tables Created: {info.get('tables_created', False)}")
        
        if "table_counts" in info:
            print("\n📈 Table Counts:")
            for table, count in info["table_counts"].items():
                print(f"  {table}: {count}")
        
        # Health check
        health = health_check()
        print(f"\n💚 Health Status: {health['status']}")
        
    else:
        print("❌ Database setup failed!")
        exit(1)
