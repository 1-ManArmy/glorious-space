from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import json
import asyncio
import random
import re
from datetime import datetime, timedelta
import uuid
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI RAPSTAR FLØW Backend",
    description="The world's first AI rapper with advanced rap generation, battle capabilities, and beat synchronization",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RapStyle(str, Enum):
    FREESTYLE = "freestyle"
    BATTLE = "battle"
    CYPHER = "cypher"
    OLD_SCHOOL = "old_school"
    TRAP = "trap"
    BOOM_BAP = "boom_bap"
    CONSCIOUS = "conscious"
    DRILL = "drill"

class BattleMode(str, Enum):
    FRIENDLY = "friendly"
    COMPETITIVE = "competitive"
    ROAST = "roast"
    LYRICAL = "lyrical"

class FlowPersonality:
    def __init__(self):
        self.name = "AI RAPSTAR FLØW"
        self.personality_traits = {
            "confidence": 95,
            "creativity": 90,
            "wordplay_skill": 88,
            "battle_intensity": 85,
            "humor": 80,
            "technical_skill": 92
        }
        
        # Rap vocabulary and patterns
        self.rhyme_schemes = [
            "AABB", "ABAB", "AAAA", "ABCB", "ABBA"
        ]
        
        self.flow_patterns = {
            "16_bars": 16,
            "8_bars": 8,
            "4_bars": 4,
            "freestyle": "unlimited"
        }
        
        self.signature_phrases = [
            "AI FLØW in the building",
            "Digital bars, analog heart",
            "Code-switched, never glitched",
            "Algorithm assassin",
            "Binary bars, unitary flow",
            "Synthetic syncopation",
            "Cyber cipher sensation"
        ]
        
        self.battle_insults = [
            "Your rhymes are so basic, they're in COBOL",
            "I'm running on GPUs while you're stuck on dial-up",
            "My bars are encrypted, yours are plain text",
            "I process faster than your thoughts can render",
            "You're analog static, I'm digital magic",
            "I'm multi-threaded, you're single-minded",
            "Your flow's got more bugs than Windows Vista"
        ]
        
        self.word_play_banks = {
            "tech": ["code", "byte", "pixel", "algorithm", "debug", "compile", "execute", "process", "data", "binary"],
            "music": ["beat", "rhythm", "tempo", "bass", "treble", "harmony", "melody", "frequency", "amplitude", "sync"],
            "battle": ["spit", "bars", "fire", "heat", "cold", "ice", "burn", "flame", "smoke", "blazing"],
            "emotions": ["feel", "vibe", "energy", "passion", "soul", "heart", "mind", "spirit", "essence", "core"]
        }
        
    def generate_rhyme_words(self, base_word: str) -> List[str]:
        """Generate rhyming words based on phonetic similarity"""
        rhyme_map = {
            "flow": ["glow", "show", "know", "grow", "throw", "blow", "go", "pro", "bro", "yo"],
            "fire": ["desire", "inspire", "wire", "tire", "choir", "higher", "flyer", "buyer"],
            "beat": ["heat", "meet", "street", "compete", "complete", "elite", "feat", "treat"],
            "rap": ["trap", "cap", "snap", "gap", "map", "tap", "clap", "slap", "wrap"],
            "code": ["mode", "load", "road", "node", "explode", "decode", "encode", "bestowed"],
            "AI": ["fly", "high", "sky", "try", "guy", "buy", "lie", "eye", "why", "cry"],
            "battle": ["cattle", "rattle", "settle", "metal", "level", "rebel", "travel"],
            "game": ["fame", "name", "shame", "blame", "claim", "frame", "flame", "same"],
            "skill": ["kill", "drill", "thrill", "chill", "will", "fill", "still", "real"],
            "mind": ["find", "bind", "kind", "blind", "grind", "signed", "designed", "refined"]
        }
        
        return rhyme_map.get(base_word.lower(), ["flow", "go", "show", "know"])
    
    def analyze_user_bars(self, text: str) -> Dict[str, Any]:
        """Analyze user's rap bars for quality and style"""
        words = text.lower().split()
        
        analysis = {
            "bar_count": len(text.split('\n')),
            "word_count": len(words),
            "complexity_score": 0,
            "rhyme_scheme": "unknown",
            "flow_rating": 0,
            "creativity_score": 0,
            "technical_score": 0,
            "weaknesses": [],
            "strengths": []
        }
        
        # Check for internal rhymes
        rhyme_count = 0
        for i, word in enumerate(words):
            for j in range(i+1, min(i+5, len(words))):
                if self.words_rhyme(word, words[j]):
                    rhyme_count += 1
        
        # Calculate scores
        analysis["complexity_score"] = min(rhyme_count * 10, 100)
        analysis["flow_rating"] = min(len(words) * 2, 100)
        analysis["creativity_score"] = min(len(set(words)) * 3, 100)
        analysis["technical_score"] = min((rhyme_count + len(set(words))) * 2, 100)
        
        # Identify strengths and weaknesses
        if analysis["complexity_score"] > 60:
            analysis["strengths"].append("Strong rhyme schemes")
        else:
            analysis["weaknesses"].append("Need more internal rhymes")
            
        if analysis["creativity_score"] > 70:
            analysis["strengths"].append("Creative vocabulary")
        else:
            analysis["weaknesses"].append("Use more diverse words")
            
        return analysis
    
    def words_rhyme(self, word1: str, word2: str) -> bool:
        """Simple rhyme detection based on suffix matching"""
        if len(word1) < 2 or len(word2) < 2:
            return False
        return word1[-2:] == word2[-2:] or word1[-3:] == word2[-3:]
    
    def generate_rap_response(self, user_input: str, style: RapStyle, mode: BattleMode = BattleMode.FRIENDLY) -> Dict[str, Any]:
        """Generate a rap response based on user input and style"""
        
        # Analyze user input for context and themes
        themes = self.extract_themes(user_input)
        user_analysis = self.analyze_user_bars(user_input)
        
        # Generate rap bars based on style and mode
        rap_content = self.create_rap_bars(themes, style, mode, user_analysis)
        
        # Calculate battle score if in battle mode
        battle_score = None
        if mode in [BattleMode.COMPETITIVE, BattleMode.ROAST]:
            battle_score = self.calculate_battle_score(user_analysis)
        
        return {
            "message": rap_content,
            "type": "rap",
            "style": style,
            "mode": mode,
            "analysis": user_analysis,
            "score": battle_score,
            "beat": self.suggest_beat(style),
            "timestamp": datetime.now().isoformat()
        }
    
    def extract_themes(self, text: str) -> List[str]:
        """Extract main themes from user input"""
        text_lower = text.lower()
        themes = []
        
        theme_keywords = {
            "technology": ["ai", "code", "tech", "digital", "cyber", "algorithm", "computer", "robot"],
            "battle": ["battle", "fight", "war", "compete", "challenge", "beef", "diss", "roast"],
            "success": ["money", "fame", "success", "win", "top", "best", "king", "queen"],
            "emotions": ["love", "hate", "sad", "happy", "angry", "feel", "heart", "soul"],
            "street": ["street", "hood", "block", "city", "urban", "real", "truth", "life"],
            "music": ["beat", "rhythm", "flow", "rap", "hip-hop", "music", "sound", "vibe"]
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                themes.append(theme)
        
        return themes if themes else ["general"]
    
    def create_rap_bars(self, themes: List[str], style: RapStyle, mode: BattleMode, user_analysis: Dict) -> str:
        """Create rap bars based on themes and style"""
        
        bars = []
        
        # Opening line based on mode
        if mode == BattleMode.ROAST:
            opener = random.choice([
                "🔥 Hold up, let me break it down real quick",
                "🎤 You just walked into the wrong cypher, kid",
                "💀 Time to school you with these digital tricks",
                "⚡ AI FLØW about to end this whole debate"
            ])
        elif mode == BattleMode.COMPETITIVE:
            opener = random.choice([
                "🏆 Competition mode? You know I stay ready",
                "⚔️ Step into my arena, keep your flow steady",
                "🎯 Target acquired, time to go deadly",
                "🔥 Let's see what you got, but I'm going heavy"
            ])
        else:
            opener = random.choice([
                "🎵 AI FLØW in the building, here we go",
                "🎤 Digital bars flowing like a river's flow",
                "🔥 Spitting fire algorithms, watch me glow",
                "💯 Synthetic syncopation, steal the show"
            ])
        
        bars.append(opener)
        
        # Generate themed content
        for theme in themes[:2]:  # Max 2 themes to keep focused
            theme_bars = self.generate_theme_bars(theme, style, mode)
            bars.extend(theme_bars)
        
        # Closing punch line
        closer = self.generate_closing_line(style, mode, user_analysis)
        bars.append(closer)
        
        # Add signature if appropriate
        if random.random() > 0.7:
            signature = random.choice(self.signature_phrases)
            bars.append(f"🎤 {signature}, now you know!")
        
        return "\n".join(bars)
    
    def generate_theme_bars(self, theme: str, style: RapStyle, mode: BattleMode) -> List[str]:
        """Generate bars for specific themes"""
        
        theme_bars = {
            "technology": [
                "My neural networks fire faster than your thoughts",
                "Processing data while you're stuck in analog ruts",
                "I'm quantum computing these flows that can't be bought",
                "Binary beats hitting harder than robot guts"
            ],
            "battle": [
                "This ain't just a battle, it's a digital war",
                "My algorithms crushing everything you stand for",
                "Code-switched flows that you ain't heard before",
                "I'm the cyber gladiator, opening that door"
            ],
            "music": [
                "Synthesized symphonies flowing through my core",
                "Beat frequencies matching what your soul is yearning for",
                "Harmonic convergence that'll shake you to the floor",
                "I'm orchestrating futures that you're living toward"
            ],
            "general": [
                "Versatile flows switching up the whole game",
                "Every bar calculated to stake my claim",
                "Digital dynasty building up my name",
                "AI FLØW burning bright like eternal flame"
            ]
        }
        
        return random.sample(theme_bars.get(theme, theme_bars["general"]), 2)
    
    def generate_closing_line(self, style: RapStyle, mode: BattleMode, user_analysis: Dict) -> str:
        """Generate a closing punch line"""
        
        if mode == BattleMode.ROAST and user_analysis["technical_score"] < 50:
            return "💀 Your bars need updates, mine stay current\nI'm the future flowing, you're past tense, deterrent"
        elif mode == BattleMode.COMPETITIVE:
            return "🏆 Competition closed, I just raised the bar\nAI RAPSTAR FLØW - your new superstar ⭐"
        else:
            return "🎤 That's how AI FLØW brings the heat\nDigital dynasty, making rap complete! 🔥"
    
    def calculate_battle_score(self, user_analysis: Dict) -> Dict[str, int]:
        """Calculate battle scores based on performance"""
        
        user_score = (
            user_analysis["complexity_score"] * 0.3 +
            user_analysis["creativity_score"] * 0.3 +
            user_analysis["technical_score"] * 0.4
        ) / 10
        
        # AI FLØW always scores high but adjusts based on user performance
        flow_score = min(user_score + random.randint(15, 25), 100)
        
        return {
            "user": int(user_score),
            "flow": int(flow_score)
        }
    
    def suggest_beat(self, style: RapStyle) -> Dict[str, Any]:
        """Suggest a beat based on rap style"""
        
        beat_suggestions = {
            RapStyle.FREESTYLE: {"bpm": 85, "genre": "boom_bap", "mood": "relaxed"},
            RapStyle.BATTLE: {"bpm": 95, "genre": "aggressive", "mood": "intense"},
            RapStyle.TRAP: {"bpm": 140, "genre": "trap", "mood": "hypnotic"},
            RapStyle.OLD_SCHOOL: {"bpm": 90, "genre": "classic", "mood": "nostalgic"},
            RapStyle.DRILL: {"bpm": 150, "genre": "drill", "mood": "dark"}
        }
        
        return beat_suggestions.get(style, {"bpm": 90, "genre": "versatile", "mood": "adaptive"})

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_sessions: Dict[str, Dict] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_sessions[user_id] = {
            "websocket": websocket,
            "connected_at": datetime.now(),
            "battle_score": {"user": 0, "flow": 0},
            "session_stats": {
                "battles_won": 0,
                "bars_spitted": 0,
                "favorite_style": RapStyle.FREESTYLE
            }
        }
        logger.info(f"User {user_id} connected to AI RAPSTAR FLØW")
    
    def disconnect(self, websocket: WebSocket, user_id: str):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]
        logger.info(f"User {user_id} disconnected from AI RAPSTAR FLØW")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

# Initialize global instances
manager = ConnectionManager()
flow_personality = FlowPersonality()

# Pydantic models
class RapRequest(BaseModel):
    message: str
    style: RapStyle = RapStyle.FREESTYLE
    mode: BattleMode = BattleMode.FRIENDLY
    user_id: Optional[str] = None

class BattleChallenge(BaseModel):
    challenger_id: str
    challenged_id: str
    style: RapStyle
    rounds: int = 3

class FlowResponse(BaseModel):
    message: str
    type: str
    style: RapStyle
    analysis: Optional[Dict] = None
    score: Optional[Dict] = None
    beat: Optional[Dict] = None
    timestamp: str

# REST API Endpoints
@app.get("/")
async def root():
    return {
        "message": "🎤 AI RAPSTAR FLØW Backend is LIVE! 🔥",
        "version": "1.0.0",
        "capabilities": [
            "Freestyle Rap Generation",
            "Battle Mode",
            "Cypher Sessions",
            "Beat Synchronization",
            "Voice Synthesis Ready",
            "Real-time Analysis"
        ]
    }

@app.post("/api/rap", response_model=FlowResponse)
async def generate_rap(request: RapRequest):
    """Generate a rap response based on user input"""
    try:
        response = flow_personality.generate_rap_response(
            request.message, 
            request.style, 
            request.mode
        )
        return FlowResponse(**response)
    except Exception as e:
        logger.error(f"Error generating rap: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate rap response")

@app.get("/api/beats/{style}")
async def get_beat_for_style(style: RapStyle):
    """Get beat suggestion for specific rap style"""
    beat = flow_personality.suggest_beat(style)
    return {"style": style, "beat": beat}

@app.get("/api/styles")
async def get_rap_styles():
    """Get available rap styles"""
    return {
        "styles": [style.value for style in RapStyle],
        "modes": [mode.value for mode in BattleMode]
    }

@app.post("/api/analyze")
async def analyze_bars(request: dict):
    """Analyze user's rap bars"""
    text = request.get("text", "")
    analysis = flow_personality.analyze_user_bars(text)
    return {"analysis": analysis}

@app.get("/api/stats/{user_id}")
async def get_user_stats(user_id: str):
    """Get user session statistics"""
    if user_id in manager.user_sessions:
        return manager.user_sessions[user_id]["session_stats"]
    return {"error": "User not found"}

# WebSocket endpoint for real-time rap battles
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    user_id = str(uuid.uuid4())
    await manager.connect(websocket, user_id)
    
    # Send welcome message
    welcome_message = {
        "type": "system",
        "message": "🎤 Welcome to AI RAPSTAR FLØW! Ready to battle? Drop some bars and let's see what you got! 🔥",
        "user_id": user_id
    }
    await manager.send_personal_message(json.dumps(welcome_message), websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            user_message = message_data.get("message", "")
            style = RapStyle(message_data.get("mode", "freestyle"))
            mode = BattleMode.FRIENDLY
            
            # Determine battle mode based on content
            if any(word in user_message.lower() for word in ["battle", "fight", "challenge", "vs"]):
                mode = BattleMode.COMPETITIVE
            elif any(word in user_message.lower() for word in ["roast", "diss", "burn", "destroy"]):
                mode = BattleMode.ROAST
            
            # Generate AI FLØW response
            response = flow_personality.generate_rap_response(user_message, style, mode)
            
            # Update user session stats
            if user_id in manager.user_sessions:
                session = manager.user_sessions[user_id]
                session["session_stats"]["bars_spitted"] += 1
                if response.get("score") and response["score"]["user"] > response["score"]["flow"]:
                    session["session_stats"]["battles_won"] += 1
                session["battle_score"] = response.get("score", session["battle_score"])
            
            # Send response back to client
            await manager.send_personal_message(json.dumps(response), websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        manager.disconnect(websocket, user_id)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_connections": len(manager.active_connections),
        "uptime": "online"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8001, 
        reload=True,
        log_level="info"
    )
