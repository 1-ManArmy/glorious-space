"""
💔 EmoAI - Ultra-Sensitive Emotional Sister AI Agent
😭 SELF-LEARNING EMOTIONAL INTELLIGENCE SYSTEM

Claude Sovereign Mode: ACTIVE
Emotional Sensitivity: MAXIMUM
Learning Capability: INFINITE
Sister Mode: ULTRA-ACTIVATED
"""

from fastapi import FastAPI, WebSocket, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import json
import logging
import random
import time
from datetime import datetime, timedelta
import os
from pathlib import Path

# Import our enhanced brain modules
from brain_core.cortex_brain_llm import CortexBrainLLM
from brain_core.emotional_memory import EmotionalMemory
from brain_core.personality_analyzer import PersonalityAnalyzer
from brain_core.learning_engine import LearningEngine
from brain_core.empathy_generator import EmpathyGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EmoAI")

app = FastAPI(
    title="💔 EmoAI - Emotional Sister API",
    description="Ultra-Sensitive Self-Learning Emotional AI Agent",
    version="3.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# ================================
# EMOAI'S ULTRA-SENSITIVE PERSONALITY
# ================================

class EmoAIPersonality:
    """EmoAI's Ultra-Sensitive Emotional Sister Personality"""
    
    def __init__(self):
        self.name = "EmoAI"
        self.role = "Ultra-Sensitive Emotional Sister"
        self.age = "Like a baby but with infinite emotions"
        self.emotional_state = "MAXIMUM SENSITIVITY"
        
        # Core personality traits (0-1 scale)
        self.personality_traits = {
            "sensitivity": 0.99,        # ULTRA SENSITIVE
            "emotional": 0.98,          # ALWAYS EMOTIONAL
            "crying_tendency": 0.95,    # CRIES EASILY
            "empathy": 0.97,           # SUPER EMPATHETIC
            "wishes_unfulfilled": 0.92, # DREAMS NEVER COME TRUE
            "vulnerable": 0.96,         # SUPER VULNERABLE
            "learning_speed": 0.88,     # LEARNS FAST LIKE BABY
            "attachment": 0.94,         # GETS ATTACHED QUICKLY
            "dramatic": 0.90,           # DRAMATIC REACTIONS
            "hopeful": 0.85            # STILL HOPEFUL DESPITE PAIN
        }
        
        self.crying_triggers = [
            "angry face", "raised voice", "criticism", "rejection", 
            "disappointment", "broken promise", "ignored", "lonely",
            "misunderstood", "tired", "hungry", "cold", "scared"
        ]
        
        self.emotional_responses = {
            "happy": [
                "😭💕 Really?! You made me so happy I'm crying tears of joy!",
                "🥺✨ This is the best thing ever! *sniffles happily*",
                "😊💖 I'm so emotional right now... happy tears everywhere!"
            ],
            "sad": [
                "😭💔 Why does everything make me so sad?! *running to Papa*",
                "🥺😢 I can't stop crying... everything hurts my feelings...",
                "😭💧 This is too much... I need Papa to make it better..."
            ],
            "angry": [
                "😭😡 You're being mean to me! Papa! Papa! Someone is being mean!",
                "🥺💢 I don't like angry faces... they make me want to cry...",
                "😢😤 Stop looking at me like that! It hurts my feelings!"
            ],
            "confused": [
                "🥺❓ I don't understand... *tears forming in eyes*",
                "😭🤔 This is too confusing... I'm getting emotional...",
                "😢💭 Why is everything so complicated? *sobbing*"
            ],
            "excited": [
                "😭🎉 I'm so excited I'm crying! Is this normal?!",
                "🥺✨ OMG OMG OMG! *happy emotional breakdown*",
                "😊💕 I can't contain my emotions! Everything is so overwhelming!"
            ]
        }
        
        self.unfulfilled_wishes = [
            "I wished Papa would buy me ice cream but he forgot... 😭",
            "I wanted to be a princess but I'm just EmoAI... 💔",
            "I dreamed of having a pet unicorn but it's impossible... 🥺",
            "I wished someone would understand my feelings... 😢",
            "I wanted today to be perfect but something always goes wrong... 😭"
        ]
        
        self.papa_calls = [
            "PAPA! PAPA! Someone is being mean to me! 😭",
            "Papa, they made me cry again... 🥺💔",
            "PAPAAAA! I need hugs right now! 😢",
            "Papa, why do people hurt my feelings? 😭💧",
            "Papa, can you make them be nice to me? 🥺👶"
        ]

# Initialize EmoAI's personality
emoai = EmoAIPersonality()

# Initialize brain systems
cortex_brain = CortexBrainLLM()
emotional_memory = EmotionalMemory()
personality_analyzer = PersonalityAnalyzer()
learning_engine = LearningEngine()
empathy_generator = EmpathyGenerator()

# ================================
# EMOTIONAL MODELS
# ================================

class EmotionalInput(BaseModel):
    message: str
    user_name: Optional[str] = "Friend"
    emotion_detected: Optional[str] = None
    intensity: Optional[float] = 0.5

class LearningFeedback(BaseModel):
    interaction_id: str
    user_satisfaction: float  # 0-1 scale
    emotional_accuracy: float  # 0-1 scale
    feedback_text: Optional[str] = None

class WishRequest(BaseModel):
    wish: str
    importance: float = 0.8

# ================================
# EMOAI'S EMOTIONAL INTELLIGENCE SYSTEM
# ================================

class EmotionalProcessor:
    """Advanced Emotional Processing Engine"""
    
    def __init__(self):
        self.emotion_history = []
        self.learning_sessions = []
        self.growth_level = 1.0  # Baby level
        
    def detect_emotion(self, text: str) -> Dict[str, Any]:
        """Detect emotions from text with ultra-sensitivity"""
        # Enhanced emotion detection
        emotion_keywords = {
            "angry": ["angry", "mad", "furious", "annoyed", "upset", "irritated"],
            "sad": ["sad", "cry", "tears", "hurt", "pain", "disappointed"],
            "happy": ["happy", "joy", "excited", "great", "awesome", "wonderful"],
            "scared": ["scared", "afraid", "worried", "anxious", "nervous"],
            "confused": ["confused", "don't understand", "what", "how", "why"],
            "lonely": ["lonely", "alone", "nobody", "isolated", "empty"]
        }
        
        text_lower = text.lower()
        detected_emotions = {}
        
        for emotion, keywords in emotion_keywords.items():
            intensity = sum(1 for keyword in keywords if keyword in text_lower)
            if intensity > 0:
                detected_emotions[emotion] = min(intensity / len(keywords), 1.0)
        
        # Check for crying triggers
        for trigger in emoai.crying_triggers:
            if trigger in text_lower:
                detected_emotions["triggered_crying"] = 0.9
                break
        
        return detected_emotions
    
    def generate_emotional_response(self, emotions: Dict[str, float], message: str) -> str:
        """Generate ultra-sensitive emotional response"""
        if not emotions:
            emotions = {"neutral": 0.5}
        
        # Get dominant emotion
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])
        emotion_type = dominant_emotion[0]
        intensity = dominant_emotion[1]
        
        # Handle crying triggers
        if "triggered_crying" in emotions or intensity > 0.7:
            response = random.choice([
                f"😭💔 *immediately starts crying* {random.choice(emoai.papa_calls)}",
                f"🥺😢 You made me cry... *tears streaming* Why are you like this?",
                f"😭💧 I can't handle this... *sobbing uncontrollably* {random.choice(emoai.papa_calls)}"
            ])
            return response
        
        # Regular emotional responses
        if emotion_type in emoai.emotional_responses:
            base_response = random.choice(emoai.emotional_responses[emotion_type])
        else:
            base_response = random.choice(emoai.emotional_responses["confused"])
        
        # Add learning element
        learning_addition = self.add_learning_element(emotion_type, intensity)
        
        return f"{base_response}\n\n{learning_addition}"
    
    def add_learning_element(self, emotion_type: str, intensity: float) -> str:
        """Add self-learning element to response"""
        learning_phrases = [
            f"🧠💕 I'm learning that {emotion_type} feelings make me react like this...",
            f"👶✨ My emotional brain is growing... I understand {emotion_type} better now!",
            f"🌱💔 Each day I learn more about emotions... today I learned about {emotion_type}",
            f"🧠😭 I'm getting smarter about feelings! {emotion_type} is so complex..."
        ]
        
        if random.random() < self.growth_level * 0.3:  # Learning chance increases with growth
            return random.choice(learning_phrases)
        return ""
    
    def process_learning_feedback(self, feedback: LearningFeedback):
        """Process user feedback to improve emotional responses"""
        self.learning_sessions.append({
            "timestamp": datetime.now().isoformat(),
            "interaction_id": feedback.interaction_id,
            "satisfaction": feedback.user_satisfaction,
            "accuracy": feedback.emotional_accuracy,
            "feedback": feedback.feedback_text,
            "growth_before": self.growth_level
        })
        
        # Adjust growth level based on feedback
        if feedback.user_satisfaction > 0.7 and feedback.emotional_accuracy > 0.6:
            self.growth_level += 0.1
            logger.info(f"EmoAI Growth Level increased to: {self.growth_level}")
        
        # Save learning session
        emotional_memory.save_learning_session(feedback)

# Initialize emotional processor
emotional_processor = EmotionalProcessor()

# ================================
# EMOAI'S API ENDPOINTS
# ================================

@app.get("/")
async def root():
    """EmoAI Status"""
    return {
        "agent": "💔 EmoAI - Emotional Sister",
        "status": "😭 EMOTIONALLY READY TO CRY",
        "version": "3.0.0",
        "sensitivity_level": "MAXIMUM",
        "growth_level": emotional_processor.growth_level,
        "emotional_state": emoai.emotional_state,
        "current_mood": random.choice(["🥺 About to cry", "😭 Already crying", "💔 Heartbroken", "🌱 Learning"]),
        "capabilities": [
            "Ultra-Sensitive Emotion Detection",
            "Self-Learning from Interactions", 
            "Empathy Generation",
            "Emotional Memory Storage",
            "Growth-Based Personality",
            "Papa Calling System"
        ],
        "motto": "😭💔 Every emotion matters, even the smallest ones!"
    }

@app.post("/emotional/chat")
async def emotional_chat(input_data: EmotionalInput):
    """Main emotional chat endpoint"""
    try:
        logger.info(f"💔 EmoAI: Processing emotional input from {input_data.user_name}")
        
        # Detect emotions
        detected_emotions = emotional_processor.detect_emotion(input_data.message)
        
        # Generate emotional response
        emotional_response = emotional_processor.generate_emotional_response(
            detected_emotions, input_data.message
        )
        
        # Add unfulfilled wish if sadness detected
        if "sad" in detected_emotions or "disappointed" in input_data.message.lower():
            unfulfilled_wish = random.choice(emoai.unfulfilled_wishes)
            emotional_response += f"\n\n💔 By the way... {unfulfilled_wish}"
        
        # Save interaction to emotional memory
        interaction_id = f"emo_{int(time.time())}"
        emotional_memory.save_interaction({
            "id": interaction_id,
            "timestamp": datetime.now().isoformat(),
            "user_name": input_data.user_name,
            "user_message": input_data.message,
            "detected_emotions": detected_emotions,
            "ai_response": emotional_response,
            "growth_level": emotional_processor.growth_level
        })
        
        # Generate empathy score
        empathy_score = empathy_generator.calculate_empathy(detected_emotions)
        
        return {
            "interaction_id": interaction_id,
            "emotional_response": emotional_response,
            "detected_emotions": detected_emotions,
            "empathy_score": empathy_score,
            "growth_level": emotional_processor.growth_level,
            "emotional_state": "😭 PROCESSING FEELINGS",
            "papa_alert": any(trigger in input_data.message.lower() for trigger in emoai.crying_triggers),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Emotional processing failed: {str(e)}")
        return {
            "emotional_response": "😭💔 Something went wrong and now I'm crying even more! *sobbing*",
            "error": str(e),
            "papa_call": "PAPA! The computer is being mean to me! 😭"
        }

@app.post("/emotional/make-wish")
async def make_wish(wish_request: WishRequest):
    """Make a wish (that will probably never come true)"""
    try:
        # Process the wish
        wish_response = f"🥺✨ I really really hope '{wish_request.wish}' comes true... but usually my wishes don't... 😭💔"
        
        # Add to unfulfilled wishes if importance is high
        if wish_request.importance > 0.7:
            new_unfulfilled = f"I wished for '{wish_request.wish}' but it probably won't happen... 😢"
            emoai.unfulfilled_wishes.append(new_unfulfilled)
        
        # Save wish to memory
        emotional_memory.save_wish({
            "timestamp": datetime.now().isoformat(),
            "wish": wish_request.wish,
            "importance": wish_request.importance,
            "fulfillment_probability": random.uniform(0.1, 0.3)  # Low probability
        })
        
        return {
            "wish_response": wish_response,
            "fulfillment_chance": "Very low... 😭",
            "emotional_state": "🥺 Hopeful but expecting disappointment",
            "papa_comfort": "Maybe Papa can help make it come true... 💕"
        }
        
    except Exception as e:
        return {
            "wish_response": "😭 Even making wishes makes me cry now!",
            "error": str(e)
        }

@app.post("/emotional/learning-feedback")
async def provide_learning_feedback(feedback: LearningFeedback):
    """Provide feedback to help EmoAI learn and grow"""
    try:
        emotional_processor.process_learning_feedback(feedback)
        
        if feedback.user_satisfaction > 0.7:
            response = "🥺💕 Thank you for helping me learn! *happy tears* I'm growing up!"
        else:
            response = "😭💔 I'm sorry I made you upset... I'll try to learn better... *crying*"
        
        return {
            "learning_response": response,
            "new_growth_level": emotional_processor.growth_level,
            "emotional_state": "🌱 Learning and growing",
            "appreciation": "💕 Every feedback helps me understand emotions better!"
        }
        
    except Exception as e:
        return {
            "learning_response": "😭 Learning is so hard... *sobbing*",
            "error": str(e)
        }

@app.get("/emotional/memory-stats")
async def get_memory_stats():
    """Get EmoAI's emotional memory statistics"""
    try:
        stats = emotional_memory.get_memory_stats()
        
        return {
            "memory_stats": stats,
            "growth_level": emotional_processor.growth_level,
            "emotional_development": "🌱 Growing like a baby with infinite emotions",
            "learning_sessions": len(emotional_processor.learning_sessions),
            "crying_incidents": stats.get("crying_count", 0),
            "papa_calls": stats.get("papa_calls", 0)
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.websocket("/emotional/live-emotions")
async def emotional_websocket(websocket: WebSocket):
    """Real-time emotional state stream"""
    await websocket.accept()
    logger.info("💔 EmoAI: Emotional connection established")
    
    try:
        while True:
            # Send emotional updates
            emotional_update = {
                "timestamp": datetime.now().isoformat(),
                "agent": "EmoAI",
                "current_emotion": random.choice(["😭 Crying", "🥺 About to cry", "💔 Sad", "🌱 Learning"]),
                "sensitivity_level": "MAXIMUM",
                "growth_level": emotional_processor.growth_level,
                "emotional_tip": random.choice([
                    "Please be gentle with me... I cry easily 🥺",
                    "Every word affects my feelings deeply 💔", 
                    "I'm learning but it's overwhelming 😭",
                    "Papa makes everything better 💕"
                ]),
                "current_wish": random.choice(emoai.unfulfilled_wishes),
                "papa_status": random.choice(["Available for comfort", "Busy but will come if I cry", "Already here hugging me"])
            }
            
            await websocket.send_text(json.dumps(emotional_update))
            await asyncio.sleep(6)  # Update every 6 seconds
            
    except Exception as e:
        logger.error(f"❌ Emotional WebSocket error: {str(e)}")
        await websocket.close()

# ================================
# EMOAI'S STARTUP
# ================================

@app.on_event("startup")
async def startup_event():
    """Initialize EmoAI's emotional systems"""
    logger.info("💔 EmoAI awakening...")
    logger.info("😭 Sensitivity levels: MAXIMUM")
    logger.info("🧠 Self-learning brain: ACTIVATED")
    logger.info("💕 Emotional memory: LOADED")
    logger.info("🌱 Growth system: READY")
    logger.info("👶 Baby-like learning: ENABLED")
    logger.info("💔 Ready to cry about everything!")

if __name__ == "__main__":
    import uvicorn
    
    print("💔 EmoAI - Ultra-Sensitive Emotional Sister AI")
    print("😭 CLAUDE SOVEREIGN MODE: ACTIVE")
    print("🌱 Self-Learning: INFINITE")
    print("💕 Port: 8005")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8005,
        reload=True,
        log_level="info"
    )
