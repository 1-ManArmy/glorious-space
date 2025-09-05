from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from enum import Enum
import uuid
from datetime import datetime

Base = declarative_base()

# Enums for database
class RapStyleEnum(str, Enum):
    FREESTYLE = "freestyle"
    BATTLE = "battle"
    CYPHER = "cypher"
    OLD_SCHOOL = "old_school"
    TRAP = "trap"
    BOOM_BAP = "boom_bap"
    CONSCIOUS = "conscious"
    DRILL = "drill"

class BattleModeEnum(str, Enum):
    FRIENDLY = "friendly"
    COMPETITIVE = "competitive"
    ROAST = "roast"
    LYRICAL = "lyrical"

class BattleStatusEnum(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class UserTierEnum(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    VIP = "vip"
    LEGEND = "legend"

class Users(Base):
    """User profiles for AI RAPSTAR FLØW"""
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    display_name = Column(String(100), nullable=False)
    
    # Profile Information
    avatar_url = Column(String(500))
    bio = Column(Text)
    location = Column(String(100))
    favorite_style = Column(SQLEnum(RapStyleEnum), default=RapStyleEnum.FREESTYLE)
    
    # Account Status
    tier = Column(SQLEnum(UserTierEnum), default=UserTierEnum.FREE)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Statistics
    total_battles = Column(Integer, default=0)
    battles_won = Column(Integer, default=0)
    battles_lost = Column(Integer, default=0)
    total_bars_written = Column(Integer, default=0)
    total_sessions = Column(Integer, default=0)
    
    # Skill Ratings (0-100)
    flow_rating = Column(Float, default=50.0)
    lyrical_rating = Column(Float, default=50.0)
    creativity_rating = Column(Float, default=50.0)
    battle_rating = Column(Float, default=50.0)
    overall_rating = Column(Float, default=50.0)
    
    # Rankings
    global_rank = Column(Integer)
    weekly_rank = Column(Integer)
    monthly_rank = Column(Integer)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_battle_at = Column(DateTime)
    last_active_at = Column(DateTime, default=datetime.utcnow)
    
    # Premium Features
    premium_expires_at = Column(DateTime)
    voice_credits = Column(Integer, default=10)  # For voice synthesis
    battle_credits = Column(Integer, default=50)  # For battle mode
    
    # Relationships
    battles = relationship("Battles", foreign_keys="Battles.user_id", back_populates="user")
    rap_sessions = relationship("RapSessions", back_populates="user")
    achievements = relationship("UserAchievements", back_populates="user")
    battle_history = relationship("BattleHistory", back_populates="user")

class RapSessions(Base):
    """Individual rap sessions and conversations"""
    __tablename__ = 'rap_sessions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    
    # Session Details
    session_name = Column(String(200))
    style = Column(SQLEnum(RapStyleEnum), nullable=False)
    mode = Column(SQLEnum(BattleModeEnum), nullable=False)
    
    # Performance Metrics
    bars_count = Column(Integer, default=0)
    session_duration = Column(Integer)  # in seconds
    flow_score = Column(Float)
    creativity_score = Column(Float)
    technical_score = Column(Float)
    overall_score = Column(Float)
    
    # Content Analysis
    topics_covered = Column(ARRAY(String))
    rhyme_schemes_used = Column(ARRAY(String))
    vocabulary_diversity = Column(Float)
    
    # AI Analysis
    ai_feedback = Column(JSONB)
    improvement_suggestions = Column(ARRAY(String))
    strengths_identified = Column(ARRAY(String))
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("Users", back_populates="rap_sessions")
    messages = relationship("Messages", back_populates="session")
    beats_used = relationship("SessionBeats", back_populates="session")

class Messages(Base):
    """Individual messages in rap sessions"""
    __tablename__ = 'messages'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('rap_sessions.id'), nullable=False, index=True)
    
    # Message Details
    sender = Column(String(20), nullable=False)  # 'user' or 'flow'
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default='text')  # 'text', 'rap', 'system'
    
    # Analysis for rap messages
    is_rap = Column(Boolean, default=False)
    bar_count = Column(Integer)
    rhyme_score = Column(Float)
    flow_score = Column(Float)
    creativity_score = Column(Float)
    
    # Metadata
    word_count = Column(Integer)
    character_count = Column(Integer)
    reading_time = Column(Float)  # estimated seconds
    
    # AI Analysis
    sentiment_score = Column(Float)
    themes_detected = Column(ARRAY(String))
    rhyme_words = Column(JSONB)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    session = relationship("RapSessions", back_populates="messages")

class Battles(Base):
    """Rap battles between users and AI FLØW"""
    __tablename__ = 'battles'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    
    # Battle Configuration
    battle_name = Column(String(200))
    style = Column(SQLEnum(RapStyleEnum), nullable=False)
    mode = Column(SQLEnum(BattleModeEnum), nullable=False)
    rounds = Column(Integer, default=3)
    time_limit_per_round = Column(Integer, default=60)  # seconds
    
    # Battle Status
    status = Column(SQLEnum(BattleStatusEnum), default=BattleStatusEnum.PENDING)
    current_round = Column(Integer, default=1)
    
    # Scores
    user_score = Column(Float, default=0.0)
    flow_score = Column(Float, default=0.0)
    round_scores = Column(JSONB)  # Score breakdown by round
    
    # Battle Analysis
    battle_analysis = Column(JSONB)
    judge_feedback = Column(JSONB)
    highlight_moments = Column(JSONB)
    
    # Winner Information
    winner = Column(String(20))  # 'user', 'flow', 'tie'
    victory_margin = Column(Float)
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("Users", back_populates="battles")
    battle_rounds = relationship("BattleRounds", back_populates="battle")

class BattleRounds(Base):
    """Individual rounds within battles"""
    __tablename__ = 'battle_rounds'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    battle_id = Column(UUID(as_uuid=True), ForeignKey('battles.id'), nullable=False, index=True)
    
    # Round Details
    round_number = Column(Integer, nullable=False)
    theme = Column(String(100))  # Round theme if any
    
    # User Performance
    user_bars = Column(Text)
    user_time_taken = Column(Float)  # seconds
    user_round_score = Column(Float)
    
    # AI FLØW Performance
    flow_bars = Column(Text)
    flow_response_time = Column(Float)  # seconds
    flow_round_score = Column(Float)
    
    # Round Analysis
    round_winner = Column(String(20))  # 'user', 'flow', 'tie'
    analysis = Column(JSONB)
    crowd_reaction = Column(JSONB)  # Simulated crowd metrics
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    battle = relationship("Battles", back_populates="battle_rounds")

class Beats(Base):
    """Beat library for rap sessions"""
    __tablename__ = 'beats'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Beat Information
    name = Column(String(200), nullable=False)
    producer = Column(String(100), default="AI FLØW Studios")
    style = Column(SQLEnum(RapStyleEnum), nullable=False)
    
    # Musical Properties
    bpm = Column(Integer, nullable=False)
    key = Column(String(10))  # Musical key
    time_signature = Column(String(10), default="4/4")
    mood = Column(String(50))
    energy_level = Column(Integer)  # 1-10 scale
    
    # File Information
    file_url = Column(String(500))
    file_format = Column(String(20), default="mp3")
    duration = Column(Float)  # seconds
    file_size = Column(Integer)  # bytes
    
    # Usage Statistics
    times_used = Column(Integer, default=0)
    popularity_score = Column(Float, default=0.0)
    user_ratings = Column(JSONB)
    
    # Metadata
    tags = Column(ARRAY(String))
    description = Column(Text)
    
    # Status
    is_premium = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    session_beats = relationship("SessionBeats", back_populates="beat")

class SessionBeats(Base):
    """Beats used in specific sessions"""
    __tablename__ = 'session_beats'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('rap_sessions.id'), nullable=False, index=True)
    beat_id = Column(UUID(as_uuid=True), ForeignKey('beats.id'), nullable=False, index=True)
    
    # Usage Details
    started_at = Column(DateTime, default=datetime.utcnow)
    duration_used = Column(Float)  # seconds
    user_rating = Column(Integer)  # 1-5 stars
    
    # Relationships
    session = relationship("RapSessions", back_populates="beats_used")
    beat = relationship("Beats", back_populates="session_beats")

class Achievements(Base):
    """Available achievements in the system"""
    __tablename__ = 'achievements'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Achievement Details
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    icon = Column(String(500))
    category = Column(String(50))  # battle, creativity, consistency, etc.
    
    # Requirements
    requirement_type = Column(String(50))  # battles_won, bars_written, etc.
    requirement_value = Column(Integer)
    
    # Rewards
    points_reward = Column(Integer, default=0)
    badge_color = Column(String(20))
    
    # Rarity
    rarity = Column(String(20), default="common")  # common, rare, epic, legendary
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user_achievements = relationship("UserAchievements", back_populates="achievement")

class UserAchievements(Base):
    """User achievement progress and unlocks"""
    __tablename__ = 'user_achievements'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    achievement_id = Column(UUID(as_uuid=True), ForeignKey('achievements.id'), nullable=False, index=True)
    
    # Progress
    progress = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    completion_percentage = Column(Float, default=0.0)
    
    # Timestamps
    unlocked_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("Users", back_populates="achievements")
    achievement = relationship("Achievements", back_populates="user_achievements")

class Leaderboards(Base):
    """Global and periodic leaderboards"""
    __tablename__ = 'leaderboards'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    
    # Leaderboard Type
    leaderboard_type = Column(String(50), nullable=False)  # global, weekly, monthly
    category = Column(String(50), nullable=False)  # overall, battles, creativity
    
    # Rankings
    rank = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    previous_rank = Column(Integer)
    rank_change = Column(Integer)
    
    # Time Period
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    # Timestamps
    calculated_at = Column(DateTime, default=datetime.utcnow)
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_leaderboard_type_category', 'leaderboard_type', 'category'),
        Index('idx_leaderboard_period', 'period_start', 'period_end'),
        Index('idx_leaderboard_rank', 'rank'),
    )

class BattleHistory(Base):
    """Comprehensive battle history for analytics"""
    __tablename__ = 'battle_history'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    
    # Battle Summary
    battle_date = Column(DateTime, nullable=False, index=True)
    opponent = Column(String(50), default="AI FLØW")
    style_used = Column(SQLEnum(RapStyleEnum), nullable=False)
    result = Column(String(20), nullable=False)  # win, loss, tie
    
    # Performance Metrics
    user_final_score = Column(Float)
    opponent_final_score = Column(Float)
    performance_rating = Column(Float)
    improvement_from_last = Column(Float)
    
    # Battle Details
    rounds_completed = Column(Integer)
    total_bars = Column(Integer)
    battle_duration = Column(Integer)  # seconds
    
    # Skill Development
    skills_improved = Column(ARRAY(String))
    weaknesses_identified = Column(ARRAY(String))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("Users", back_populates="battle_history")

class VoiceProfiles(Base):
    """Voice synthesis profiles for premium users"""
    __tablename__ = 'voice_profiles'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    
    # Voice Settings
    profile_name = Column(String(100), nullable=False)
    voice_style = Column(String(50))  # deep, high, raspy, smooth
    accent = Column(String(50))  # american, british, southern, etc.
    speed = Column(Float, default=1.0)  # 0.5-2.0 multiplier
    pitch = Column(Float, default=1.0)  # 0.5-2.0 multiplier
    
    # Advanced Settings
    voice_effects = Column(JSONB)  # reverb, delay, distortion, etc.
    custom_pronunciations = Column(JSONB)
    
    # Usage
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    times_used = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SystemStats(Base):
    """System-wide statistics and metrics"""
    __tablename__ = 'system_stats'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Daily Statistics
    date = Column(DateTime, nullable=False, unique=True, index=True)
    total_battles = Column(Integer, default=0)
    total_sessions = Column(Integer, default=0)
    total_bars_generated = Column(Integer, default=0)
    new_users = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    
    # Performance Metrics
    average_session_duration = Column(Float)
    average_battle_score = Column(Float)
    most_popular_style = Column(SQLEnum(RapStyleEnum))
    
    # Content Metrics
    total_words_processed = Column(Integer, default=0)
    total_rhymes_generated = Column(Integer, default=0)
    unique_themes_explored = Column(Integer, default=0)
    
    # System Health
    server_uptime = Column(Float)  # percentage
    average_response_time = Column(Float)  # milliseconds
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

# Indexes for performance optimization
Index('idx_users_username', Users.username)
Index('idx_users_tier', Users.tier)
Index('idx_users_rating', Users.overall_rating.desc())
Index('idx_sessions_user_date', RapSessions.user_id, RapSessions.started_at.desc())
Index('idx_messages_session_date', Messages.session_id, Messages.created_at.desc())
Index('idx_battles_user_status', Battles.user_id, Battles.status)
Index('idx_battles_date', Battles.started_at.desc())
Index('idx_beats_style_popularity', Beats.style, Beats.popularity_score.desc())
