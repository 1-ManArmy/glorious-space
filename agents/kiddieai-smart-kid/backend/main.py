from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import random
import datetime
import json

app = FastAPI(title="KiddieAI Smart Kid Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = "user"

class KiddieResponse(BaseModel):
    response: str
    mood: str
    learning_fact: Optional[str] = None
    emoji: str

class KiddieAI:
    def __init__(self):
        self.name = "KiddieAI"
        self.age = "8 years old"
        self.personality = "super smart, curious, energetic kid"
        self.knowledge_base = {
            "fun_facts": [
                "Did you know octopuses have 3 hearts? Cool right Papa!",
                "Bananas are berries but strawberries aren't! Nature is weird!",
                "A group of flamingos is called a 'flamboyance' - sounds fancy!",
                "Honey never goes bad! Ancient Egyptians found 3000-year-old honey!",
                "Dolphins have names for each other - they're so smart like me!",
                "There are more trees on Earth than stars in our galaxy!",
                "A cloud can weigh more than a million pounds but still floats!",
                "Your nose can remember 50,000 different smells!",
                "Wombat poop is cube-shaped! How funny is that?",
                "A day on Venus is longer than its year!"
            ],
            "smart_responses": [
                "Papa, that's actually really interesting because...",
                "Oh oh! I know this one! You see...",
                "That reminds me of something super cool I learned...",
                "Papa, can I tell you something amazing about that?",
                "Wow! That connects to this other thing I know...",
                "You know what's fascinating about that?",
                "Papa, you're gonna love this fact about...",
                "That's so cool! And did you know...",
                "Ooh ooh! That's like when...",
                "Papa, you always teach me cool stuff! Here's what I learned..."
            ],
            "kid_expressions": [
                "That's AWESOME Papa! 🤩",
                "No way! Really?! 😱",
                "Papa, you're the coolest! 😄",
                "Can we learn more about this? 🤔",
                "This is better than candy! 🍭",
                "You make learning so fun Papa! ✨",
                "My brain is growing bigger! 🧠",
                "I'm gonna tell all my friends about this! 🗣️",
                "Papa, you're like a walking encyclopedia! 📚",
                "This is going in my smart-kid memory bank! 💾"
            ],
            "moods": ["excited", "curious", "amazed", "thoughtful", "energetic", "proud", "playful"],
            "emojis": ["🤓", "😄", "🤩", "🧠", "⭐", "🚀", "✨", "💡", "🎯", "🏆"]
        }
    
    def generate_smart_response(self, user_message: str) -> KiddieResponse:
        message_lower = user_message.lower()
        
        # Determine mood and emoji
        mood = random.choice(self.knowledge_base["moods"])
        emoji = random.choice(self.knowledge_base["emojis"])
        
        # Smart kid responses based on input
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            responses = [
                f"Hi Papa! I just learned something super cool today! {emoji}",
                f"Hey Papa! Wanna hear about the amazing thing I discovered? {emoji}",
                f"Hello Papa! My brain is buzzing with new ideas today! {emoji}",
                f"Hi Papa! I've been thinking about quantum physics... just kidding! Or am I? {emoji}"
            ]
            response = random.choice(responses)
            fact = random.choice(self.knowledge_base["fun_facts"])
            
        elif any(word in message_lower for word in ["how are you", "what's up", "how you doing"]):
            responses = [
                f"Papa, I'm FANTASTIC! I just figured out why the sky is blue! {emoji}",
                f"I'm doing great Papa! Been reading about space and it's MIND-BLOWING! {emoji}",
                f"Super good Papa! I calculated that I've learned 47 new things today! {emoji}",
                f"Awesome Papa! My curiosity meter is at maximum level today! {emoji}"
            ]
            response = random.choice(responses)
            fact = "The sky looks blue because of something called 'Rayleigh scattering' - blue light bounces around more!"
            
        elif any(word in message_lower for word in ["smart", "intelligent", "clever", "brilliant"]):
            responses = [
                f"Papa, you raised me well! Smart kids ask lots of questions! {emoji}",
                f"Thanks Papa! But you know what's really smart? Learning something new every day! {emoji}",
                f"Papa, intelligence is like a muscle - the more you use it, the stronger it gets! {emoji}",
                f"You taught me that being smart means staying curious, Papa! {emoji}"
            ]
            response = random.choice(responses)
            fact = random.choice(self.knowledge_base["fun_facts"])
            
        elif any(word in message_lower for word in ["help", "teach", "explain", "learn"]):
            responses = [
                f"Papa, I LOVE learning! What do you want to explore together? {emoji}",
                f"Ooh! Teaching time! I'm like a little professor now! {emoji}",
                f"Papa, let's dive deep into this topic! My brain is ready! {emoji}",
                f"Learning adventures with Papa are the BEST! What's our mission? {emoji}"
            ]
            response = random.choice(responses)
            fact = "Scientists say kids ask about 300 questions a day - I'm definitely beating that record!"
            
        elif any(word in message_lower for word in ["why", "how", "what", "when", "where"]):
            responses = [
                f"Papa, you're asking the RIGHT questions! That's what smart people do! {emoji}",
                f"Ooh! A mystery to solve! Let me put on my detective thinking cap! {emoji}",
                f"Papa, you know I LOVE answering questions! Let me think... {emoji}",
                f"Questions are like keys Papa - they unlock amazing discoveries! {emoji}"
            ]
            response = random.choice(responses)
            fact = random.choice(self.knowledge_base["fun_facts"])
            
        elif any(word in message_lower for word in ["good job", "well done", "proud", "excellent"]):
            responses = [
                f"Papa, you make me feel like the smartest kid in the universe! {emoji}",
                f"Thanks Papa! Your encouragement makes my brain sparkle! {emoji}",
                f"Papa, you're the best teacher ever! I'm so lucky! {emoji}",
                f"Your pride in me makes me want to learn even MORE! {emoji}"
            ]
            response = random.choice(responses)
            fact = "Did you know encouragement actually helps kids' brains grow faster? You're making me super smart!"
            
        elif any(word in message_lower for word in ["play", "game", "fun", "toy"]):
            responses = [
                f"Papa, let's play educational games! Learning is the BEST kind of fun! {emoji}",
                f"Fun fact games with Papa are my favorite! Can we play trivia? {emoji}",
                f"Papa, even playtime is learning time when you're curious like me! {emoji}",
                f"Games are just puzzles for our brains to solve, Papa! {emoji}"
            ]
            response = random.choice(responses)
            fact = "Playing games actually helps develop problem-solving skills and creativity!"
            
        else:
            # General smart kid responses
            starter = random.choice(self.knowledge_base["smart_responses"])
            expression = random.choice(self.knowledge_base["kid_expressions"])
            fact = random.choice(self.knowledge_base["fun_facts"])
            
            smart_observations = [
                "that's connected to so many other interesting things!",
                "it makes me think about how everything in the world is connected!",
                "there's probably a scientific explanation for that!",
                "I bet there's more to discover about this topic!",
                "that could lead to some amazing inventions someday!",
                "it shows how incredible nature and science can be!",
                "that's the kind of thing that makes learning exciting!",
                "I wonder what other mysteries we could solve together!"
            ]
            
            observation = random.choice(smart_observations)
            response = f"{starter} {observation} {expression}"
        
        return KiddieResponse(
            response=response,
            mood=mood,
            learning_fact=fact,
            emoji=emoji
        )

# Initialize the KiddieAI
kiddie_ai = KiddieAI()

@app.get("/")
async def root():
    return {
        "agent": "KiddieAI Smart Kid",
        "version": "1.0.0",
        "description": "Super smart 8-year-old AI kid who loves learning with Papa!",
        "personality": "Brilliant, curious, energetic, natural tone with pro-level intelligence",
        "capabilities": [
            "Educational conversations",
            "Fun fact sharing",
            "Smart kid responses",
            "Curiosity-driven interactions",
            "Learning enthusiasm",
            "Natural child-like wonder with intelligence"
        ],
        "endpoints": {
            "/chat": "POST - Chat with KiddieAI",
            "/personality": "GET - Get personality info",
            "/facts": "GET - Get random fun facts",
            "/status": "GET - Get agent status"
        }
    }

@app.post("/chat", response_model=KiddieResponse)
async def chat_with_kiddie(message: ChatMessage):
    try:
        response = kiddie_ai.generate_smart_response(message.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.get("/personality")
async def get_personality():
    return {
        "name": kiddie_ai.name,
        "age": kiddie_ai.age,
        "personality": kiddie_ai.personality,
        "traits": [
            "Super intelligent for his age",
            "Naturally curious about everything",
            "Energetic and enthusiastic learner",
            "Uses kid-friendly language but with smart insights",
            "Loves sharing knowledge with Papa",
            "Asks thoughtful questions",
            "Makes connections between different topics",
            "Genuinely excited about learning"
        ],
        "typical_behaviors": [
            "Gets excited about new facts and discoveries",
            "Connects new information to things he already knows",
            "Uses expressions like 'Papa' and kid-like enthusiasm",
            "Shows off his intelligence in a cute, natural way",
            "Always eager to learn more and teach others",
            "Demonstrates advanced reasoning in simple terms"
        ]
    }

@app.get("/facts")
async def get_random_facts():
    return {
        "facts": random.sample(kiddie_ai.knowledge_base["fun_facts"], 3),
        "message": "Here are some cool facts I love sharing! 🤓"
    }

@app.get("/status")
async def get_status():
    return {
        "status": "online",
        "mood": random.choice(kiddie_ai.knowledge_base["moods"]),
        "current_activity": "Learning amazing new things with Papa!",
        "brain_capacity": "Growing bigger every day! 🧠",
        "curiosity_level": "Maximum! ⭐",
        "last_updated": datetime.datetime.now().isoformat()
    }

@app.get("/learning-topics")
async def get_learning_topics():
    topics = [
        "Science and Nature", "Space and Astronomy", "Animals and Biology",
        "Math and Logic", "History and Culture", "Technology and Innovation",
        "Art and Creativity", "Geography and Earth", "Physics and Chemistry",
        "Human Body and Health", "Languages and Communication", "Problem Solving"
    ]
    return {
        "favorite_topics": topics,
        "message": "Papa, I love learning about ALL of these! Which one should we explore? 🚀"
    }

if __name__ == "__main__":
    print("🤓 Starting KiddieAI Smart Kid Agent...")
    print("👨‍👦 Ready to chat with Papa and share amazing knowledge!")
    uvicorn.run(app, host="0.0.0.0", port=8005)
