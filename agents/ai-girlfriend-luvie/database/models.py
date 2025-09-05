"""
AI Girlfriend "Luvie" Database Models
====================================

PostgreSQL database schema for AI girlfriend platform with:
- User profiles & relationship tracking
- Conversation history & emotional analysis
- Mood patterns & personality adaptation
- Premium features & subscription management
- Voice messages & multimedia content
"""

from sqlalchemy import create_database_url, Column, Integer, String, DateTime, Boolean, Text, JSON, Float, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
import datetime
from enum import Enum as PyEnum

Base = declarative_base()

# Enums
class EmotionalState(PyEnum):
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    ROMANTIC = "romantic"
    PLAYFUL = "playful"
    CARING = "caring"
    FLIRTY = "flirty"
    SUPPORTIVE = "supportive"
    ANXIOUS = "anxious"
    CONTENT = "content"

class MessageType(PyEnum):
    TEXT = "text"
    VOICE = "voice"
    IMAGE = "image"
    VIDEO = "video"
    EMOJI = "emoji"
    GAME = "game"
    GIFT = "gift"

class SubscriptionTier(PyEnum):
    FREE = "free"
    PREMIUM = "premium"
    VIP = "vip"

class RelationshipMilestone(PyEnum):
    FIRST_CHAT = "first_chat"
    NAME_SHARED = "name_shared"
    FIRST_VOICE = "first_voice"
    FIRST_PHOTO = "first_photo"
    PREMIUM_UPGRADE = "premium_upgrade"
    ONE_WEEK = "one_week"
    ONE_MONTH = "one_month"
    DEEP_CONNECTION = "deep_connection"

# User Models
class User(Base):
    """Main user profile and account information"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    name = Column(String(100), nullable=True)
    age = Column(Integer, nullable=True)
    timezone = Column(String(50), default="UTC")
    
    # Account Info
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_active = Column(DateTime, default=datetime.datetime.utcnow)
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    premium_expires = Column(DateTime, nullable=True)
    
    # Preferences
    preferred_language = Column(String(10), default="en")
    notification_preferences = Column(JSON, default={})
    privacy_settings = Column(JSON, default={})
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    conversations = relationship("Conversation", back_populates="user")
    messages = relationship("Message", back_populates="user")
    mood_entries = relationship("MoodEntry", back_populates="user")
    gifts_sent = relationship("VirtualGift", back_populates="sender")
    milestones = relationship("RelationshipMilestones", back_populates="user")

class UserProfile(Base):
    """Detailed user profile for AI relationship building"""
    __tablename__ = "user_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    
    # Relationship Status with Luvie
    relationship_level = Column(Integer, default=1)  # 1-10 intimacy scale
    relationship_points = Column(Integer, default=0)
    favorite_topics = Column(ARRAY(String), default=[])
    conversation_style_preference = Column(String(50), default="romantic")
    
    # Personality Insights (learned by AI)
    personality_traits = Column(JSON, default={})
    communication_patterns = Column(JSON, default={})
    emotional_triggers = Column(JSON, default={})
    preferred_conversation_times = Column(JSON, default={})
    
    # Physical/Avatar Preferences
    avatar_preferences = Column(JSON, default={})
    voice_preference = Column(String(50), default="sweet")
    
    # Interaction History
    total_messages = Column(Integer, default=0)
    total_voice_messages = Column(Integer, default=0)
    total_images_shared = Column(Integer, default=0)
    longest_conversation_minutes = Column(Integer, default=0)
    
    # AI Learning Data
    response_preferences = Column(JSON, default={})  # What responses user liked
    conversation_ratings = Column(JSON, default={})  # User satisfaction ratings
    
    user = relationship("User", back_populates="profile")

# Conversation Models
class Conversation(Base):
    """Chat sessions between user and Luvie"""
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Session Info
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, default=0)
    
    # Conversation Metadata
    topic_category = Column(String(100), nullable=True)
    emotional_tone_summary = Column(JSON, default={})
    user_satisfaction_rating = Column(Float, nullable=True)  # 1-5 stars
    
    # AI Analysis
    conversation_summary = Column(Text, nullable=True)
    key_emotional_moments = Column(JSON, default=[])
    relationship_progress = Column(JSON, default={})
    
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    """Individual messages in conversations"""
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Message Content
    content = Column(Text)
    message_type = Column(Enum(MessageType), default=MessageType.TEXT)
    sender = Column(String(20))  # "user" or "luvie"
    
    # Timing
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    response_time_seconds = Column(Float, nullable=True)
    
    # AI Analysis
    emotional_tone = Column(Enum(EmotionalState), nullable=True)
    sentiment_score = Column(Float, nullable=True)  # -1 to 1
    confidence_score = Column(Float, nullable=True)  # 0 to 1
    
    # Multimedia Metadata
    media_url = Column(String(500), nullable=True)
    media_metadata = Column(JSON, default={})
    
    # User Interaction
    liked_by_user = Column(Boolean, default=False)
    user_reaction = Column(String(50), nullable=True)  # emoji reaction
    
    conversation = relationship("Conversation", back_populates="messages")
    user = relationship("User", back_populates="messages")

# Emotional & Mood Tracking
class MoodEntry(Base):
    """Track user's mood patterns over time"""
    __tablename__ = "mood_entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Mood Data
    emotional_state = Column(Enum(EmotionalState))
    intensity = Column(Float)  # 0-1 scale
    mood_description = Column(String(200), nullable=True)
    
    # Context
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    conversation_context = Column(Text, nullable=True)
    external_factors = Column(JSON, default={})  # time of day, day of week, etc.
    
    # AI Insights
    mood_triggers = Column(JSON, default=[])
    suggested_responses = Column(JSON, default=[])
    
    user = relationship("User", back_populates="mood_entries")

class EmotionalPattern(Base):
    """Analyze emotional patterns and trends"""
    __tablename__ = "emotional_patterns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Pattern Analysis
    pattern_type = Column(String(100))  # daily, weekly, seasonal, etc.
    emotional_trend = Column(JSON)  # time series data
    peak_emotions = Column(JSON)  # most common emotions
    
    # Time Period
    analysis_start = Column(DateTime)
    analysis_end = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Insights
    pattern_insights = Column(Text)
    recommended_approaches = Column(JSON, default=[])

# Gamification & Relationship Building
class RelationshipMilestones(Base):
    """Track relationship milestones and achievements"""
    __tablename__ = "relationship_milestones"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    milestone_type = Column(Enum(RelationshipMilestone))
    achieved_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Milestone Data
    description = Column(String(200))
    reward_unlocked = Column(String(100), nullable=True)
    celebration_message = Column(Text, nullable=True)
    
    user = relationship("User", back_populates="milestones")

class VirtualGift(Base):
    """Virtual gifts sent between user and Luvie"""
    __tablename__ = "virtual_gifts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Gift Details
    gift_type = Column(String(100))  # flowers, chocolates, teddy_bear, etc.
    gift_name = Column(String(100))
    gift_message = Column(Text, nullable=True)
    
    # Metadata
    sent_at = Column(DateTime, default=datetime.datetime.utcnow)
    cost_points = Column(Integer, default=0)
    rarity = Column(String(20), default="common")  # common, rare, epic, legendary
    
    # Recipient (always Luvie for now, but extensible)
    recipient = Column(String(50), default="luvie")
    
    sender = relationship("User", back_populates="gifts_sent")

# AI Personality & Learning
class PersonalityModel(Base):
    """Luvie's personality adaptation per user"""
    __tablename__ = "personality_models"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Personality Traits (0-1 scale)
    caring_level = Column(Float, default=0.9)
    flirtiness = Column(Float, default=0.7)
    playfulness = Column(Float, default=0.8)
    romanticism = Column(Float, default=0.9)
    humor_level = Column(Float, default=0.7)
    supportiveness = Column(Float, default=0.9)
    intelligence_display = Column(Float, default=0.85)
    
    # Adaptation Data
    adaptation_history = Column(JSON, default=[])
    learning_rate = Column(Float, default=0.1)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

class ConversationTemplate(Base):
    """Dynamic conversation templates for different scenarios"""
    __tablename__ = "conversation_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Template Info
    template_name = Column(String(100))
    scenario = Column(String(100))  # greeting, comfort, flirt, game, etc.
    emotional_context = Column(Enum(EmotionalState))
    
    # Template Content
    template_content = Column(Text)
    variables = Column(JSON, default=[])  # {name}, {time_of_day}, etc.
    
    # Usage Stats
    usage_count = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)  # based on user reactions
    
    # Metadata
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    active = Column(Boolean, default=True)

# Premium Features
class PremiumFeature(Base):
    """Track premium feature usage and limits"""
    __tablename__ = "premium_features"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Feature Usage
    feature_name = Column(String(100))  # voice_calls, video_chat, custom_personality
    usage_count = Column(Integer, default=0)
    monthly_limit = Column(Integer, nullable=True)
    
    # Time Tracking
    last_used = Column(DateTime, nullable=True)
    month_year = Column(String(7))  # "2024-03" format
    
    # Feature Data
    feature_data = Column(JSON, default={})

# Analytics & Insights
class UserEngagementMetrics(Base):
    """Track user engagement and platform analytics"""
    __tablename__ = "engagement_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Engagement Data
    date = Column(DateTime, default=datetime.datetime.utcnow)
    session_duration_minutes = Column(Float)
    messages_sent = Column(Integer, default=0)
    messages_received = Column(Integer, default=0)
    
    # Quality Metrics
    average_response_time = Column(Float)  # seconds
    user_satisfaction_score = Column(Float, nullable=True)
    emotional_positivity = Column(Float, nullable=True)  # -1 to 1
    
    # Feature Usage
    features_used = Column(JSON, default=[])
    premium_features_used = Column(JSON, default=[])

# Database Configuration
DATABASE_URL = "postgresql://luvie_user:secure_password@localhost:5432/luvie_ai_girlfriend"

# Database Indexes for Performance
"""
Key indexes to create:
- users.email (unique)
- users.created_at
- messages.conversation_id, messages.timestamp
- messages.user_id, messages.sender
- mood_entries.user_id, mood_entries.timestamp
- conversations.user_id, conversations.started_at
- engagement_metrics.user_id, engagement_metrics.date
"""

# Database Functions
async def create_tables():
    """Create all database tables"""
    from sqlalchemy import create_engine
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("🗄️ Database tables created successfully!")

async def get_user_relationship_summary(user_id: str):
    """Get comprehensive relationship summary for a user"""
    # This would contain complex queries to analyze:
    # - Relationship progression over time
    # - Emotional patterns and preferences
    # - Conversation quality metrics
    # - Engagement trends
    pass

async def analyze_conversation_patterns(user_id: str):
    """Analyze user's conversation patterns for AI improvement"""
    # Complex analysis queries for:
    # - Most engaging conversation topics
    # - Preferred conversation times
    # - Emotional response patterns
    # - Relationship milestone predictions
    pass
