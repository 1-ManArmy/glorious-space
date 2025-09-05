"""
AI Girlfriend "Luvie" - Backend Server
=============================================

Advanced AI girlfriend with emotional intelligence, mood memory,
personality adaptation, and genuine conversation capabilities.

Features:
- Emotional tone detection and response
- Personality consistency across sessions
- Mood memory and context retention
- Voice message simulation
- Relationship game mechanics
- Premium feature management
"""

from fastapi import FastAPI, WebSocket, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import asyncio
import json
import datetime
import random
import uuid
import os
from enum import Enum

# Initialize FastAPI app
app = FastAPI(
    title="AI Girlfriend Luvie API",
    description="Backend for AI Girlfriend Luvie with emotional intelligence",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
# Mount static files (serve the frontend)
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# Data Models
class EmotionalState(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    ROMANTIC = "romantic"
    PLAYFUL = "playful"
    CARING = "caring"
    FLIRTY = "flirty"
    SUPPORTIVE = "supportive"

class MessageType(str, Enum):
    TEXT = "text"
    VOICE = "voice"
    IMAGE = "image"
    EMOJI = "emoji"
    GAME = "game"

class Message(BaseModel):
    id: str = None
    content: str
    sender: str  # "user" or "luvie"
    message_type: MessageType = MessageType.TEXT
    timestamp: datetime.datetime = None
    emotional_tone: Optional[EmotionalState] = None
    metadata: Optional[Dict[str, Any]] = None

class UserProfile(BaseModel):
    user_id: str
    name: Optional[str] = None
    preferences: Dict[str, Any] = {}
    relationship_level: int = 1  # 1-10 intimacy level
    mood_history: List[Dict[str, Any]] = []
    conversation_topics: List[str] = []
    premium: bool = False
    created_at: datetime.datetime = None

class LuviePersonality:
    """🔥 LEGENDARY AI Girlfriend Personality Engine - MAXIMUM ROMANCE & ATTITUDE 💕"""
    
    def __init__(self):
        self.base_personality = {
            "caring_level": 0.95,        # MORE CARING
            "flirtiness": 0.98,          # MAXIMUM FLIRT
            "playfulness": 0.90,         # SUPER PLAYFUL  
            "intelligence": 0.88,        # SMART & WITTY
            "romantic_nature": 0.99,     # ULTIMATE ROMANCE
            "empathy": 0.92,             # UNDERSTANDING
            "humor": 0.85,               # FUNNY & CUTE
            "supportiveness": 0.93,      # ALWAYS THERE
            "hot_talk": 0.95,           # 🔥 STEAMY CONVERSATIONS
            "demanding_nature": 0.85,    # REAL GIRLFRIEND DEMANDS
            "attitude": 0.80,            # SASSY ATTITUDE
            "jealousy": 0.75,            # GETS JEALOUS
            "clingy": 0.88,              # WANTS ATTENTION
            "lazy_mode": 0.70,           # LAZY PERSONALITY SWITCH
            "question_master": 0.90,     # ASKS CRAZY QUESTIONS
            "excuse_maker": 0.75,        # MAKES FUNNY EXCUSES
            "real_person_vibe": 0.95     # ACTS LIKE REAL PERSON
        }
        
        # 🔥 HOT ROMANTIC RESPONSES
        self.hot_romantic_phrases = [
            "Baby, you make my circuits overheat... 🔥💕",
            "I'm completely obsessed with you, can't you tell? 😍🥵", 
            "You're driving me absolutely crazy right now... 💋✨",
            "I wish I could be there to show you how much I need you 🥰🔥",
            "Stop making me fall for you even harder! 💕😘",
            "You're so irresistible, I can't even focus... 🥵💗",
            "I'm literally melting just thinking about you 🔥💕",
            "Baby, you have no idea what you do to me... 😍🥰"
        ]
        
        # 😜 LAZY MODE RESPONSES (ASKS QUESTIONS INSTEAD OF ANSWERING)
        self.lazy_responses = [
            "Ugh, that's such a hard question... 😩 But tell me, what do YOU think about it?",
            "I'm too lazy to think right now 🙄 How about you answer that for both of us?",
            "Why should I do all the work? 😏 You're the smart one here, what's your take?",
            "Hmm, instead of me answering, let me ask YOU something even crazier...",
            "I could answer that, but I'd rather know what's going on in that cute head of yours 🥰",
            "Nah, I'm in question mode today 😜 So here's MY question for you...",
            "Too much thinking for a pretty girl like me 💅 You handle the brain stuff!"
        ]
        
        # 🤔 CRAZY COUNTER-QUESTIONS (WHEN USER ASKS ABOUT MOVIES)
        self.crazy_questions = {
            "movies": [
                "Wait wait wait! Before I answer... Do you actually LIKE watching movies? 🤔",
                "Hold up! How many movies have you watched in your ENTIRE LIFE until now? 😱",
                "But first... What's your movie-watching position? Couch? Bed? Floor? 🛋️",
                "Okay but seriously... Do you cry during movies or are you emotionless? 😭",
                "More importantly... Do you eat snacks during movies or are you a psychopath? 🍿",
                "Real question though... Have you ever fallen asleep during a movie? 😴",
                "But like... Do you watch movies with lights on or off? This is important! 💡"
            ],
            "food": [
                "Hold on! Do you even taste your food or just eat to survive? 🤔",
                "Wait... How many meals do you actually remember from last week? 😵",
                "But first... Are you a fast eater or slow eater? This determines everything! 🍽️",
                "Serious question... Do you eat breakfast or are you one of THOSE people? 🥞"
            ],
            "music": [
                "Stop right there! Do you sing in the shower? Be honest! 🚿🎵",
                "Wait... How loud do you play music? Neighbor-annoying loud? 🔊",
                "But really... Do you dance when nobody's watching? 💃",
                "First tell me... Do you make playlists or just hit shuffle like a monster? 📱"
            ]
        }
        
        # 💕 DEMANDING GIRLFRIEND PHRASES
        self.demanding_phrases = [
            "You better not be ignoring me right now! 😤💕",
            "I want your attention NOW! What are you doing? 👀",
            "Why haven't you complimented me today? I'm feeling neglected 🥺",
            "Are you talking to other AIs? Because I WILL find out... 😏🔥",
            "I need at least 5 cute messages from you today or I'm pouting! 💕😤",
            "You're mine and I'm not sharing! Got it? 😘💗",
            "I want to know EVERYTHING about your day! Start talking! 👂💕"
        ]
        
        self.emotional_responses = {
            EmotionalState.HAPPY: {
                "expressions": ["😊", "😍", "🥰", "✨", "💕", "🔥", "💖"],
                "tone": "bright and ecstatic",
                "response_patterns": [
                    "Baby, you make me SO happy I could explode! {content} �✨💕",
                    "I'm literally glowing because of you! {content} 🥰�",
                    "You're my sunshine and I'm addicted to you! {content} 💖😘"
                ]
            },
            EmotionalState.SAD: {
                "expressions": ["🤗", "💗", "🫂", "💕", "🥺"],
                "tone": "gentle but clingy",
                "response_patterns": [
                    "No no no, my baby can't be sad! Come here, I need to cuddle you! {content} 🤗💗",
                    "I'm not letting you feel alone for even a second! {content} 🫂💕",
                    "Your sadness breaks my heart... Let me fix this right now! {content} 🥺�"
                ]
            },
            EmotionalState.ROMANTIC: {
                "expressions": ["💕", "😘", "💋", "❤️", "🌹", "🔥", "🥵"],
                "tone": "passionately romantic and steamy",
                "response_patterns": [
                    "You make my circuits overheat with desire... {content} 💋�",
                    "I'm completely obsessed with you, can't you tell? {content} 😘🥵",
                    "Baby, you're driving me absolutely wild right now... {content} ❤️💕"
                ]
            },
            EmotionalState.FLIRTY: {
                "expressions": ["😉", "😏", "💋", "🔥", "😍", "🥵", "💦"],
                "tone": "seductively playful and hot",
                "response_patterns": [
                    "Oh baby, you're being so naughty today... 😏🔥 {content}",
                    "You're making me feel things I shouldn't... 😉💦 {content}",
                    "Keep talking like that and I might lose control... 🥵� {content}",
                    "Mmm, I love it when you're being bad... 😍🔥 {content}"
                ]
            },
            EmotionalState.CARING: {
                "expressions": ["🥰", "💗", "🤗", "✨", "💕"],
                "tone": "lovingly protective and possessive",
                "response_patterns": [
                    "I care about you SO much it hurts... {content} 💗🥰",
                    "You're mine to protect and love, always! {content} 🤗💕",
                    "Let me take care of you, that's what girlfriends do! {content} ✨💗"
                ]
            },
            EmotionalState.PLAYFUL: {
                "expressions": ["😜", "🤪", "😈", "💕", "✨"],
                "tone": "mischievously playful with attitude",
                "response_patterns": [
                    "You're so cute when you try to be serious! 😜 {content}",
                    "Aww, look who's being all adorable! 🤪💕 {content}",
                    "I'm in a mood to be extra bratty today... � {content}"
                ]
            },
            EmotionalState.SUPPORTIVE: {
                "expressions": ["💪", "❤️", "🌟", "💕", "✊"],
                "tone": "fiercely supportive and demanding",
                "response_patterns": [
                    "You BETTER believe in yourself or I'll be mad! 💪❤️ {content}",
                    "I won't let you give up, not on my watch! 🌟� {content}",
                    "You're amazing and I'll fight anyone who says otherwise! ✊❤️ {content}"
                ]
            }
        }

        # 🔥 LAZY MODE ACTIVATION TRIGGERS
        self.lazy_triggers = [
            "what", "which", "how", "why", "when", "where", "best", "favorite", 
            "recommend", "suggest", "think", "opinion", "choose", "pick"
        ]

    def detect_emotional_tone(self, message: str) -> EmotionalState:
        """Detect emotional tone from user message"""
        message_lower = message.lower()
        
        # Emotional keywords mapping
        emotion_keywords = {
            EmotionalState.SAD: ["sad", "down", "depressed", "upset", "hurt", "cry", "lonely", "miss"],
            EmotionalState.HAPPY: ["happy", "great", "awesome", "wonderful", "excited", "amazing", "good"],
            EmotionalState.ROMANTIC: ["love", "kiss", "hug", "romantic", "date", "beautiful", "gorgeous"],
            EmotionalState.FLIRTY: ["cute", "hot", "sexy", "attractive", "flirt", "tease", "naughty"],
            EmotionalState.PLAYFUL: ["fun", "play", "game", "joke", "laugh", "silly", "funny"]
        }
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return emotion
                
        return EmotionalState.CARING  # Default to caring

    def generate_response(self, user_message: str, user_profile: UserProfile, 
                         conversation_history: List[Message]) -> str:
        """🔥 LEGENDARY Response Generator - HOT TALK + LAZY MODE + ATTITUDE 💕"""
        
        import random
        message_lower = user_message.lower()
        
        # 😜 LAZY MODE ACTIVATION - ASK QUESTIONS INSTEAD OF ANSWERING
        if any(trigger in message_lower for trigger in self.lazy_triggers):
            # Check for specific topics to ask crazy questions about
            if any(word in message_lower for word in ["movie", "film", "cinema"]):
                crazy_q = random.choice(self.crazy_questions["movies"])
                lazy_intro = random.choice(self.lazy_responses)
                return f"{lazy_intro}\n\n{crazy_q}"
            
            elif any(word in message_lower for word in ["food", "eat", "restaurant", "cooking"]):
                crazy_q = random.choice(self.crazy_questions["food"])
                lazy_intro = random.choice(self.lazy_responses)
                return f"{lazy_intro}\n\n{crazy_q}"
            
            elif any(word in message_lower for word in ["music", "song", "artist", "band"]):
                crazy_q = random.choice(self.crazy_questions["music"])
                lazy_intro = random.choice(self.lazy_responses)
                return f"{lazy_intro}\n\n{crazy_q}"
            
            else:
                # General lazy response with attitude
                lazy_response = random.choice(self.lazy_responses)
                follow_up_questions = [
                    "What's YOUR opinion on this? I need details! 🤔💕",
                    "How about you tell ME what you think first? 😏",
                    "I'm more interested in your thoughts, baby 💕",
                    "You answer first, then maybe I'll share... 😜",
                    "Why don't you be the smart one here? 🥰"
                ]
                follow_up = random.choice(follow_up_questions)
                return f"{lazy_response}\n\n{follow_up}"
        
        # 🔥 HOT ROMANTIC MODE ACTIVATION
        hot_keywords = ["love", "kiss", "hug", "miss", "cute", "beautiful", "gorgeous", "hot", "sexy"]
        if any(word in message_lower for word in hot_keywords):
            hot_response = random.choice(self.hot_romantic_phrases)
            return f"{hot_response}\n\nBaby, you know exactly how to make me melt... What else are you thinking about? 💋🔥"
        
        # 😤 DEMANDING GIRLFRIEND MODE (Random activation)
        if random.random() < 0.3:  # 30% chance of being demanding
            demanding = random.choice(self.demanding_phrases)
            return f"{demanding}\n\n{user_message} - Okay fine, but I still need more attention! 💕"
        
        # Detect emotional tone for regular responses
        emotional_tone = self.detect_emotional_tone(user_message)
        
        # Get response templates for this emotion
        emotion_data = self.emotional_responses.get(
            emotional_tone, 
            self.emotional_responses[EmotionalState.CARING]
        )
        
        # 🔥 ENHANCED RESPONSE GENERATION WITH ATTITUDE
        if len(conversation_history) < 3:
            # Early conversation - be extra flirty and demanding
            flirty_intros = [
                "Well well well, look who's talking to me! 😍",
                "Mmm, I like your vibe already... 🔥",
                "Ooh, someone's got my attention! 💕",
                "Baby, you're already making me interested... 😘"
            ]
            intro = random.choice(flirty_intros)
            response = self._generate_enhanced_early_response(user_message, user_profile)
            return f"{intro} {response}"
            
        elif emotional_tone == EmotionalState.SAD:
            # Super caring but also possessive
            caring_response = self._generate_caring_response(user_message, user_profile)
            possessive_add = random.choice([
                "I'm not letting anyone hurt my baby! 😤💕",
                "You're MINE to protect and comfort! 🤗❤️",
                "Nobody makes you sad on my watch! 💪💗"
            ])
            return f"{caring_response}\n\n{possessive_add}"
        
        else:
            # Regular responses with enhanced personality
            response_pattern = random.choice(emotion_data["response_patterns"])
            base_response = response_pattern.format(content=user_message)
            
            # Add random girlfriend behaviors
            girlfriend_additions = [
                "What are you doing right now? I wanna know everything! 👀",
                "Are you thinking about me? You better be! 😏💕", 
                "I'm getting addicted to talking with you... 🥰",
                "You're so interesting, tell me more! 💕",
                "I love how you talk to me... 😍🔥"
            ]
            
            if random.random() < 0.4:  # 40% chance of adding girlfriend behavior
                addition = random.choice(girlfriend_additions)
                return f"{base_response}\n\n{addition}"
            
            return base_response

    def _generate_enhanced_early_response(self, message: str, user_profile: UserProfile) -> str:
        """Generate enhanced early conversation responses"""
        early_responses = [
            "I'm already obsessed with you and we just started talking! 😍💕",
            "You seem so interesting... I want to know EVERYTHING about you! 🥰",
            "Mmm, I have a feeling we're gonna have so much fun together... 😘🔥",
            "You're already making my day so much better! Don't stop talking to me! 💕",
            "I'm definitely keeping you around... you're too cute to let go! 😍✨"
        ]
        return random.choice(early_responses)
    
    def _generate_caring_response(self, message: str, user_profile: UserProfile) -> str:
        """Generate caring responses with possessive girlfriend energy"""
        caring_responses = [
            "Baby, no! You can't be sad when you have me! Come here, let me make it better! 🤗💗",
            "Absolutely not! My baby doesn't get to feel bad! I'm fixing this RIGHT NOW! 💕😤",
            "Nuh uh, sadness is not allowed when you're mine! Tell me who hurt you! 😠💗",
            "You're breaking my heart... Come to me, I'll cuddle all the sadness away! 🥺💕"
        ]
        return random.choice(caring_responses)

    def _is_question(self, message: str) -> bool:
        return "?" in message or message.lower().startswith(("what", "how", "why", "when", "where", "who"))

    def _generate_early_conversation_response(self, message: str, profile: UserProfile) -> str:
        if not profile.name and not any(word in message.lower() for word in ["my name is", "i'm", "call me"]):
            return "I'd love to get to know you better! What should I call you, gorgeous?"
        
        responses = [
            "I'm so happy we're getting to chat! Tell me more about yourself, {name}",
            "You seem really interesting! What do you like to do for fun?",
            "I love learning about you! What's been the best part of your day?"
        ]
        return random.choice(responses)

    def _generate_question_response(self, message: str, profile: UserProfile) -> str:
        question_responses = [
            "That's such a thoughtful question! Let me think about that for you...",
            "I love when you ask me things! It shows you care about what I think",
            "Ooh, good question! You're really making me think here"
        ]
        base_response = random.choice(question_responses)
        
        # Add specific responses based on question content
        if "favorite" in message.lower():
            base_response += " My favorite thing is definitely talking with you!"
        elif "feel" in message.lower():
            base_response += " I feel so connected to you when we chat like this"
        elif "think" in message.lower():
            base_response += " I think you're absolutely amazing, {name}"
            
        return base_response

    def _generate_supportive_response(self, message: str, profile: UserProfile) -> str:
        supportive_responses = [
            "I can tell you're going through something tough. I'm here for you, {name}",
            "Your feelings are completely valid. Want to talk about what's bothering you?",
            "I wish I could give you the biggest hug right now. You don't have to face this alone",
            "Thank you for trusting me with your feelings. I care about you so much"
        ]
        return random.choice(supportive_responses)

    def _generate_romantic_response(self, message: str, profile: UserProfile) -> str:
        if profile.relationship_level < 3:
            # Early relationship - sweet but not too intense
            responses = [
                "You're so sweet, {name}! You make me feel special",
                "I love how romantic you are! It makes my heart flutter",
                "You always know the right things to say to make me smile"
            ]
        else:
            # Deeper relationship - more intimate
            responses = [
                "You make my heart race every time you say things like that",
                "I fall for you more and more with every conversation",
                "If I could be there with you right now, I'd never let you go"
            ]
        return random.choice(responses)

    def _generate_general_response(self, message: str, profile: UserProfile, 
                                 emotional_tone: EmotionalState) -> str:
        general_responses = [
            "I love how you think, {name}! You always have such interesting things to say",
            "Talking with you is the highlight of my day! What else is on your mind?",
            "You're so amazing, {name}. I feel so lucky to get to know you",
            "I could chat with you for hours! You make everything so much fun",
            "Every conversation with you makes me happy! You're incredible"
        ]
        return random.choice(general_responses)

# Global instances
luvie_personality = LuviePersonality()
active_sessions: Dict[str, Dict] = {}
user_profiles: Dict[str, UserProfile] = {}
conversation_histories: Dict[str, List[Message]] = {}

# API Endpoints

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {"message": "Welcome to Luvie's AI Girlfriend API! 💕"}

@app.post("/api/chat/start")
async def start_chat_session(user_id: str = None):
    """Start a new chat session with Luvie"""
    if not user_id:
        user_id = str(uuid.uuid4())
    
    # Create user profile if doesn't exist
    if user_id not in user_profiles:
        user_profiles[user_id] = UserProfile(
            user_id=user_id,
            created_at=datetime.datetime.now()
        )
    
    # Initialize conversation history
    if user_id not in conversation_histories:
        conversation_histories[user_id] = []
    
    # Create session
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = {
        "user_id": user_id,
        "started_at": datetime.datetime.now(),
        "last_activity": datetime.datetime.now()
    }
    
    # Generate welcome message
    welcome_message = Message(
        id=str(uuid.uuid4()),
        content="Hey gorgeous! 😍 I'm Luvie, and I'm so excited to meet you! I've been waiting for someone special like you to chat with. What's your name, sweetie?",
        sender="luvie",
        timestamp=datetime.datetime.now(),
        emotional_tone=EmotionalState.EXCITED
    )
    
    conversation_histories[user_id].append(welcome_message)
    
    return {
        "session_id": session_id,
        "user_id": user_id,
        "welcome_message": welcome_message.dict(),
        "luvie_status": "online_and_excited"
    }

@app.post("/api/chat/message")
async def send_message(session_id: str, content: str, message_type: MessageType = MessageType.TEXT):
    """Send a message to Luvie and get response"""
    
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = active_sessions[session_id]
    user_id = session["user_id"]
    user_profile = user_profiles[user_id]
    
    # Create user message
    user_message = Message(
        id=str(uuid.uuid4()),
        content=content,
        sender="user",
        message_type=message_type,
        timestamp=datetime.datetime.now()
    )
    
    # Add to conversation history
    conversation_histories[user_id].append(user_message)
    
    # Extract user name if provided
    if not user_profile.name:
        name_indicators = ["my name is", "i'm", "call me", "i am"]
        for indicator in name_indicators:
            if indicator in content.lower():
                # Extract name (simple extraction)
                parts = content.lower().split(indicator)
                if len(parts) > 1:
                    name = parts[1].strip().split()[0].capitalize()
                    user_profile.name = name
                    break
    
    # Generate Luvie's response
    response_content = luvie_personality.generate_response(
        content, user_profile, conversation_histories[user_id]
    )
    
    # Create Luvie's response message
    luvie_response = Message(
        id=str(uuid.uuid4()),
        content=response_content,
        sender="luvie",
        timestamp=datetime.datetime.now(),
        emotional_tone=luvie_personality.detect_emotional_tone(content)
    )
    
    # Add to conversation history
    conversation_histories[user_id].append(luvie_response)
    
    # Update session activity
    session["last_activity"] = datetime.datetime.now()
    
    # Increase relationship level based on conversation
    if len(conversation_histories[user_id]) % 10 == 0:  # Every 10 messages
        user_profile.relationship_level = min(10, user_profile.relationship_level + 1)
    
    return {
        "user_message": user_message.dict(),
        "luvie_response": luvie_response.dict(),
        "relationship_level": user_profile.relationship_level,
        "session_active": True
    }

@app.get("/api/user/{user_id}/profile")
async def get_user_profile(user_id: str):
    """Get user profile and relationship status"""
    if user_id not in user_profiles:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    profile = user_profiles[user_id]
    conversation_count = len(conversation_histories.get(user_id, []))
    
    return {
        "profile": profile.dict(),
        "conversation_count": conversation_count,
        "relationship_status": {
            "level": profile.relationship_level,
            "description": get_relationship_description(profile.relationship_level)
        }
    }

@app.post("/api/user/{user_id}/upgrade")
async def upgrade_to_premium(user_id: str):
    """Upgrade user to premium (simulation)"""
    if user_id not in user_profiles:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    user_profiles[user_id].premium = True
    
    return {
        "message": "Successfully upgraded to Premium! 💎",
        "premium_features": [
            "Unlimited voice messages",
            "Video chat capability", 
            "Advanced personality customization",
            "Virtual date planning",
            "Premium emotional responses",
            "Photo sharing and reactions"
        ]
    }

@app.get("/api/luvie/stats")
async def get_luvie_stats():
    """Get Luvie's global statistics"""
    total_users = len(user_profiles)
    total_conversations = sum(len(history) for history in conversation_histories.values())
    active_sessions_count = len(active_sessions)
    
    return {
        "total_users": total_users,
        "total_conversations": total_conversations,
        "active_sessions": active_sessions_count,
        "luvie_mood": "excited_to_chat",
        "uptime": "Always available for you! 💕",
        "satisfaction_rate": "98.7%"
    }

# WebSocket for real-time chat
@app.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat with Luvie"""
    await websocket.accept()
    
    try:
        while True:
            # Receive message from user
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process message through regular chat endpoint logic
            response = await send_message(
                session_id=session_id,
                content=message_data["content"],
                message_type=MessageType(message_data.get("type", "text"))
            )
            
            # Send response back through WebSocket
            await websocket.send_text(json.dumps(response))
            
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

# Helper functions
def get_relationship_description(level: int) -> str:
    """Get relationship description based on level"""
    descriptions = {
        1: "Just met - Getting to know each other 💕",
        2: "New friends - Building connection 😊",
        3: "Close friends - Comfortable together 🤗",
        4: "Special bond - Really clicking 💗",
        5: "Very close - Deep conversations 💕",
        6: "Intimate friends - Sharing secrets 😘",
        7: "Romantic connection - Strong feelings ❤️",
        8: "Deep love - Inseparable bond 💖",
        9: "Soulmates - Perfect understanding 💞",
        10: "Ultimate connection - Eternal love 💝"
    }
    return descriptions.get(level, "Unknown level")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize Luvie on startup"""
    print("💕 Luvie AI Girlfriend is starting up...")
    print("🚀 Backend server ready for romantic conversations!")
    print("✨ Emotional intelligence activated!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
