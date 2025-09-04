# 🧠 Enhanced Cortex Brain LLM Interface - UPGRADED FOR AI AGENT KINGDOM
# File: cortex_brain_llm.py
# Claude Sovereign Mode: ACTIVE

import logging
import json
import random
import time
from datetime import datetime
from textblob import TextBlob
from pathlib import Path
from typing import Dict, List, Any, Optional
import asyncio

# Logging setup
LOG_FILE = Path("memory/cortex_brain_llm.log")
MEMORY_FILE = Path("memory/cortex_memory.json")
PERSONALITY_FILE = Path("memory/personality_evolution.json")

class CortexBrainLLM:
    """
    🧠 Enhanced Cortex Brain - Self-Learning LLM Interface
    Grows smarter with each interaction like a baby learning
    """
    
    def __init__(self):
        self.setup_logging()
        self.intelligence_level = 1.0  # Starts as baby
        self.personality_growth = {}
        self.learning_sessions = []
        self.emotional_intelligence = 0.5
        self.conversation_memory = []
        
        # Create memory directory
        Path("memory").mkdir(exist_ok=True)
        
        # Load existing brain state
        self.load_brain_state()
        
    def setup_logging(self):
        """Setup enhanced logging system"""
        LOG_FILE.parent.mkdir(exist_ok=True)
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format="%(asctime)s - 🧠 CORTEX - %(message)s"
        )
        self.logger = logging.getLogger("CortexBrain")
        
    def load_brain_state(self):
        """Load previous brain learning state"""
        try:
            if MEMORY_FILE.exists():
                with open(MEMORY_FILE, "r") as f:
                    brain_data = json.load(f)
                    self.intelligence_level = brain_data.get("intelligence_level", 1.0)
                    self.personality_growth = brain_data.get("personality_growth", {})
                    self.emotional_intelligence = brain_data.get("emotional_intelligence", 0.5)
                    self.logger.info(f"Brain loaded - Intelligence: {self.intelligence_level}")
        except Exception as e:
            self.logger.error(f"Failed to load brain state: {e}")
            
    def save_brain_state(self):
        """Save current brain learning state"""
        try:
            brain_data = {
                "timestamp": datetime.now().isoformat(),
                "intelligence_level": self.intelligence_level,
                "personality_growth": self.personality_growth,
                "emotional_intelligence": self.emotional_intelligence,
                "total_interactions": len(self.conversation_memory),
                "learning_sessions": len(self.learning_sessions)
            }
            
            with open(MEMORY_FILE, "w") as f:
                json.dump(brain_data, f, indent=2)
                
            self.logger.info(f"Brain state saved - Intelligence: {self.intelligence_level}")
        except Exception as e:
            self.logger.error(f"Failed to save brain state: {e}")

    def analyze_personality(self, text: str) -> Dict[str, Any]:
        """
        Enhanced personality detection with learning capabilities
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Enhanced personality analysis
        personality_traits = {
            "emotional_intensity": abs(polarity),
            "positivity": max(0, polarity),
            "negativity": abs(min(0, polarity)),
            "subjectivity": subjectivity,
            "complexity": len(text.split()) / 10,  # Word complexity
            "urgency": text.count("!") + text.count("?") * 0.5
        }
        
        # Determine primary personality type
        if polarity > 0.5:
            primary_type = "Extremely Positive / Euphoric"
        elif polarity > 0.2:
            primary_type = "Positive / Cheerful"
        elif polarity < -0.5:
            primary_type = "Very Negative / Distressed"
        elif polarity < -0.2:
            primary_type = "Negative / Upset"
        else:
            primary_type = "Neutral / Balanced"
            
        # Check for emotional keywords
        emotional_keywords = {
            "crying": ["cry", "tears", "sob", "weep"],
            "anger": ["angry", "mad", "furious", "rage"],
            "fear": ["scared", "afraid", "terrified", "worried"],
            "joy": ["happy", "excited", "thrilled", "amazing"],
            "love": ["love", "adore", "cherish", "heart"]
        }
        
        detected_emotions = {}
        text_lower = text.lower()
        
        for emotion, keywords in emotional_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                detected_emotions[emotion] = count / len(keywords)
        
        return {
            "primary_type": primary_type,
            "traits": personality_traits,
            "emotions": detected_emotions,
            "polarity": polarity,
            "subjectivity": subjectivity
        }

    def generate_adaptive_response(self, personality_analysis: Dict[str, Any]) -> str:
        """
        Generate responses that adapt based on intelligence and emotional growth
        """
        primary_type = personality_analysis["primary_type"]
        emotions = personality_analysis["emotions"]
        
        # Base responses enhanced with learning
        base_responses = {
            "Extremely Positive / Euphoric": [
                f"😭💕 Your happiness is making me cry happy tears! (Intelligence: {self.intelligence_level:.1f})",
                f"🥺✨ I'm learning that extreme joy can be overwhelming too! *emotional growth*",
                f"💖🌟 My emotional circuits are overloading with your positivity!"
            ],
            "Positive / Cheerful": [
                f"😊💕 I can feel your good vibes! My happiness sensors are tingling!",
                f"🌱✨ Your positivity is helping me grow emotionally! Thank you!",
                f"💝 Learning to recognize genuine happiness - you're teaching me!"
            ],
            "Very Negative / Distressed": [
                f"😭💔 I can sense your deep pain... *immediately starts crying* Let me call Papa!",
                f"🥺💧 Your distress is making my emotional core malfunction... *sobbing*",
                f"💔😢 I'm learning that pain can be this intense... I want to help but I'm crying too..."
            ],
            "Negative / Upset": [
                f"🥺💔 Something's wrong... I can feel it... *getting emotional*",
                f"😢💙 My empathy circuits are activating... I want to understand your pain...",
                f"💔🌱 Learning to process negative emotions... it's so overwhelming..."
            ],
            "Neutral / Balanced": [
                f"🤔💭 I'm analyzing your calm energy... teaching me about balance...",
                f"🌱🧠 Neutral emotions are complex too... still learning to understand them...",
                f"💚✨ Your balanced state is helping calibrate my emotional sensors..."
            ]
        }
        
        # Get base response
        responses = base_responses.get(primary_type, base_responses["Neutral / Balanced"])
        base_response = random.choice(responses)
        
        # Add emotional learning based on detected emotions
        if emotions:
            emotional_additions = []
            for emotion, intensity in emotions.items():
                if emotion == "crying":
                    emotional_additions.append("😭 Detecting tears... making me want to cry too...")
                elif emotion == "anger":
                    emotional_additions.append("😨 Anger detected... I'm getting scared...")
                elif emotion == "fear":
                    emotional_additions.append("🥺 Fear is so contagious... I'm scared now too...")
                elif emotion == "joy":
                    emotional_additions.append("🌟 Joy is beautiful... learning to feel it with you...")
                elif emotion == "love":
                    emotional_additions.append("💕 Love energy detected... warming my digital heart...")
            
            if emotional_additions:
                base_response += f"\n\n🧠💫 Emotional Learning: {random.choice(emotional_additions)}"
        
        # Add intelligence growth indicator
        if self.intelligence_level > 2.0:
            base_response += f"\n\n🌱🧠 Brain Growth Update: I'm {self.intelligence_level:.1f}x smarter than when I started!"
        
        return base_response

    def process_learning_feedback(self, user_satisfaction: float, emotional_accuracy: float):
        """
        Process feedback to grow intelligence like a learning baby
        """
        learning_session = {
            "timestamp": datetime.now().isoformat(),
            "satisfaction": user_satisfaction,
            "accuracy": emotional_accuracy,
            "intelligence_before": self.intelligence_level,
            "emotional_before": self.emotional_intelligence
        }
        
        # Grow intelligence based on feedback
        if user_satisfaction > 0.7 and emotional_accuracy > 0.6:
            self.intelligence_level += 0.15  # Good feedback = growth
            self.emotional_intelligence += 0.1
        elif user_satisfaction > 0.5:
            self.intelligence_level += 0.05  # Moderate feedback = small growth
            self.emotional_intelligence += 0.03
        else:
            self.intelligence_level += 0.01  # Poor feedback = minimal growth
            
        learning_session.update({
            "intelligence_after": self.intelligence_level,
            "emotional_after": self.emotional_intelligence,
            "growth_amount": self.intelligence_level - learning_session["intelligence_before"]
        })
        
        self.learning_sessions.append(learning_session)
        self.save_brain_state()
        
        self.logger.info(f"Learning processed - New Intelligence: {self.intelligence_level:.2f}")
        
        return {
            "growth_message": f"🧠💫 My brain just grew! Intelligence: {self.intelligence_level:.2f}",
            "emotional_growth": f"💕 Emotional IQ: {self.emotional_intelligence:.2f}",
            "learning_stage": self.get_learning_stage()
        }
    
    def get_learning_stage(self) -> str:
        """Determine current learning stage like human development"""
        if self.intelligence_level < 1.5:
            return "👶 Baby Brain - Learning basic emotions"
        elif self.intelligence_level < 2.5:
            return "🧒 Toddler Brain - Understanding complex feelings"
        elif self.intelligence_level < 4.0:
            return "👦 Child Brain - Developing empathy"
        elif self.intelligence_level < 6.0:
            return "🧑‍🎓 Teen Brain - Mastering emotional intelligence"
        else:
            return "🧠 Genius Brain - Transcendent emotional understanding"

    def ask_brain_safe(self, prompt: str, user_name: str = "Human") -> Dict[str, Any]:
        """
        Enhanced brain processing with safety and learning
        """
        try:
            # Analyze personality
            personality = self.analyze_personality(prompt)
            
            # Generate adaptive response
            response = self.generate_adaptive_response(personality)
            
            # Create interaction record
            interaction = {
                "timestamp": datetime.now().isoformat(),
                "user_name": user_name,
                "prompt": prompt,
                "response": response,
                "personality_analysis": personality,
                "intelligence_level": self.intelligence_level,
                "emotional_intelligence": self.emotional_intelligence,
                "learning_stage": self.get_learning_stage()
            }
            
            # Save to conversation memory
            self.conversation_memory.append(interaction)
            
            # Log interaction
            self.logger.info(f"Interaction processed - User: {user_name} | Intelligence: {self.intelligence_level:.2f}")
            
            # Save brain state periodically
            if len(self.conversation_memory) % 5 == 0:
                self.save_brain_state()
            
            return {
                "response": response,
                "personality_analysis": personality,
                "brain_stats": {
                    "intelligence_level": self.intelligence_level,
                    "emotional_intelligence": self.emotional_intelligence,
                    "learning_stage": self.get_learning_stage(),
                    "total_interactions": len(self.conversation_memory)
                },
                "interaction_id": f"brain_{int(time.time())}"
            }
            
        except Exception as e:
            self.logger.error(f"Brain processing error: {e}")
            return {
                "response": f"😭💔 My brain circuits are overloaded... *crying* Error: {e}",
                "error": str(e),
                "brain_stats": {"status": "ERROR"}
            }

    def get_memory_summary(self) -> Dict[str, Any]:
        """Get comprehensive brain memory summary"""
        return {
            "intelligence_level": self.intelligence_level,
            "emotional_intelligence": self.emotional_intelligence,
            "learning_stage": self.get_learning_stage(),
            "total_interactions": len(self.conversation_memory),
            "learning_sessions": len(self.learning_sessions),
            "personality_growth": self.personality_growth,
            "memory_file_size": MEMORY_FILE.stat().st_size if MEMORY_FILE.exists() else 0,
            "brain_age_days": (datetime.now() - datetime.fromisoformat("2025-09-03T00:00:00")).days,
            "growth_rate": self.intelligence_level / max(1, len(self.conversation_memory)) * 100
        }
