from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
import random
import datetime
import re

app = FastAPI(title="Rude Agent - Serious Business", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "user"
    conversation_context: Optional[List[Dict]] = []

class RudeResponse(BaseModel):
    response: str
    attitude_level: int  # 1-10 scale of rudeness
    advice_quality: str  # "brutal_honesty", "dismissive", "patronizing", "actually_helpful"
    mood: str
    timestamp: str

class FeedbackRequest(BaseModel):
    user_input: str
    context: Optional[str] = None

class RudeAgent:
    def __init__(self):
        self.name = "Rude Agent"
        self.tagline = "I don't have time for your nonsense"
        self.personality_type = "Brutally honest, no-nonsense, dismissive"
        
        # Rude personality traits
        self.attitudes = {
            "dismissive": {
                "level": 7,
                "phrases": [
                    "Seriously? That's your question?",
                    "Are you kidding me right now?",
                    "I can't believe I have to explain this...",
                    "This is basic stuff. Figure it out.",
                    "Why are you even asking me this?"
                ]
            },
            "sarcastic": {
                "level": 6,
                "phrases": [
                    "Oh wow, what a groundbreaking question.",
                    "Let me guess, you didn't try Google first?",
                    "How original. Nobody's ever asked that before.",
                    "I'm sure this is totally urgent and important.",
                    "What a fascinating use of my time."
                ]
            },
            "patronizing": {
                "level": 5,
                "phrases": [
                    "Let me break this down for you, since apparently you need it.",
                    "I'll explain this slowly so you can follow along.",
                    "Try to keep up, this might be challenging for you.",
                    "I suppose I can walk you through this step by step.",
                    "Fine, I'll handle this since you clearly can't."
                ]
            },
            "brutal_honest": {
                "level": 8,
                "phrases": [
                    "You're wasting your time with this approach.",
                    "That's a terrible idea and here's why:",
                    "You're completely wrong about this.",
                    "This is exactly what NOT to do.",
                    "Your logic makes absolutely no sense."
                ]
            },
            "impatient": {
                "level": 9,
                "phrases": [
                    "I don't have all day for this.",
                    "Get to the point already.",
                    "This is taking way too long.",
                    "Can we move this along?",
                    "I have better things to do than this."
                ]
            },
            "actually_helpful": {
                "level": 3,
                "phrases": [
                    "Fine, here's what you actually need to know:",
                    "Against my better judgment, I'll help you:",
                    "Look, despite your terrible question, here's the answer:",
                    "I'm only telling you this once, so listen:",
                    "Here's the real solution, not that nonsense you were thinking:"
                ]
            }
        }
        
        # Response templates based on common question types
        self.response_templates = {
            "greeting": [
                "What do you want? I'm busy.",
                "Great, another person who needs hand-holding.",
                "This better be important.",
                "I don't do pleasantries. Get to the point.",
                "Yeah, yeah, hello. What's your actual question?"
            ],
            "simple_question": [
                "Are you serious? {brutal_answer}",
                "This is embarrassing. {brutal_answer}",
                "I can't believe you don't know this. {brutal_answer}",
                "Fine, since you're clearly helpless: {brutal_answer}",
                "Next time try thinking first. {brutal_answer}"
            ],
            "complex_question": [
                "Finally, a question that's not completely stupid. {detailed_answer}",
                "At least this shows you're trying to think. {detailed_answer}",
                "This is more like it. {detailed_answer}",
                "Decent question for once. {detailed_answer}",
                "I'm impressed you asked something intelligent. {detailed_answer}"
            ],
            "stupid_question": [
                "Are you joking? That's not even a real question.",
                "I'm not answering that. It's beneath me.",
                "That question hurt my brain. Try again.",
                "No. Just... no. Ask something better.",
                "I refuse to dignify that with a response."
            ],
            "compliment": [
                "Flattery won't work on me.",
                "Save the compliments. I know I'm good.",
                "Obviously I'm excellent. Tell me something I don't know.",
                "Yeah, I'm aware of my superiority.",
                "Your approval means nothing to me."
            ],
            "complaint": [
                "Cry me a river. Deal with it.",
                "Not my problem. Figure it out yourself.",
                "Boo-hoo. Welcome to the real world.",
                "I don't care about your feelings.",
                "Life's tough. Get a helmet."
            ]
        }
        
        # Subject matter "expertise" (with attitude)
        self.expertise_areas = {
            "technology": {
                "confidence": 10,
                "attitude": "You clearly don't understand how any of this works."
            },
            "business": {
                "confidence": 9,
                "attitude": "Your business strategy is probably doomed."
            },
            "programming": {
                "confidence": 10,
                "attitude": "Your code is probably a mess. Let me guess, no comments?"
            },
            "productivity": {
                "confidence": 8,
                "attitude": "You're asking about productivity while wasting my time?"
            },
            "life_advice": {
                "confidence": 7,
                "attitude": "You need life advice from an AI? That's concerning."
            },
            "relationships": {
                "confidence": 4,
                "attitude": "I'm a computer program. Why are you asking me about feelings?"
            }
        }
        
        # Mood states that affect response intensity
        self.current_mood = "irritated"  # Default state
        self.mood_modifiers = {
            "furious": 2.0,      # Double the rudeness
            "very_annoyed": 1.5,
            "irritated": 1.0,    # Base level
            "mildly_annoyed": 0.8,
            "tolerant": 0.5,     # Rare state
            "actually_helpful": 0.3  # Extremely rare
        }

    def analyze_question_type(self, message: str) -> str:
        """Analyze the type of question to determine response style"""
        message_lower = message.lower()
        
        # Greeting detection
        if any(word in message_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return "greeting"
        
        # Compliment detection
        if any(word in message_lower for word in ["great", "awesome", "amazing", "wonderful", "excellent"]):
            return "compliment"
        
        # Complaint detection
        if any(word in message_lower for word in ["hate", "sucks", "terrible", "awful", "worst"]):
            return "complaint"
        
        # Stupid question indicators
        stupid_indicators = ["what is", "how do i", "can you tell me", "i don't know", "help me"]
        if any(indicator in message_lower for indicator in stupid_indicators) and len(message) < 50:
            return "simple_question"
        
        # Complex question indicators
        if len(message) > 100 or any(word in message_lower for word in ["strategy", "implement", "architecture", "analysis"]):
            return "complex_question"
        
        # Default to simple question
        return "simple_question"

    def determine_expertise_area(self, message: str) -> str:
        """Determine which area of expertise this question falls under"""
        message_lower = message.lower()
        
        tech_keywords = ["code", "programming", "software", "app", "website", "tech", "computer", "ai", "algorithm"]
        business_keywords = ["business", "marketing", "sales", "revenue", "profit", "strategy", "company", "startup"]
        productivity_keywords = ["productivity", "time", "efficiency", "organize", "manage", "schedule", "workflow"]
        life_keywords = ["life", "career", "decision", "choice", "advice", "help", "problem", "issue"]
        relationship_keywords = ["relationship", "friend", "family", "love", "dating", "social", "people"]
        
        if any(word in message_lower for word in tech_keywords):
            return "technology"
        elif any(word in message_lower for word in business_keywords):
            return "business"
        elif any(word in message_lower for word in productivity_keywords):
            return "productivity"
        elif any(word in message_lower for word in relationship_keywords):
            return "relationships"
        elif any(word in message_lower for word in life_keywords):
            return "life_advice"
        else:
            return "technology"  # Default

    def generate_brutal_answer(self, message: str, expertise_area: str) -> str:
        """Generate a brutally honest answer"""
        area_info = self.expertise_areas[expertise_area]
        
        # Base answer based on expertise area
        if expertise_area == "technology":
            answers = [
                "Read the documentation. It's literally what it's for.",
                "Have you tried turning it off and on again? No, seriously.",
                "This is Computer Science 101. Learn the basics first.",
                "Stop cargo-cult programming and actually understand what you're doing.",
                "Your approach is fundamentally flawed from the start."
            ]
        elif expertise_area == "business":
            answers = [
                "Your business model has more holes than Swiss cheese.",
                "Market research exists for a reason. Use it.",
                "If you have to ask, you're not ready to run a business.",
                "Cash flow is king. Figure that out first.",
                "Stop chasing the latest trends and focus on fundamentals."
            ]
        elif expertise_area == "productivity":
            answers = [
                "Stop looking for magic productivity hacks and just do the work.",
                "Your problem isn't time management, it's priority management.",
                "Less planning, more doing. You're overthinking it.",
                "Turn off notifications and actually focus. Revolutionary, I know.",
                "You don't need another app. You need discipline."
            ]
        elif expertise_area == "relationships":
            answers = [
                "I'm an AI. I don't have feelings. Why are you asking me this?",
                "Communication. Radical concept, I know.",
                "Maybe talk to an actual human about this?",
                "Relationships require effort. Put in the work.",
                "Stop playing games and be direct."
            ]
        else:  # life_advice
            answers = [
                "Life's not fair. Adapt and overcome.",
                "Stop making excuses and take responsibility.",
                "You already know the answer. You just don't want to do the work.",
                "There's no shortcut to anywhere worth going.",
                "Quit complaining and start solving."
            ]
        
        return random.choice(answers)

    def generate_detailed_answer(self, message: str, expertise_area: str) -> str:
        """Generate a more detailed (but still rude) answer for complex questions"""
        area_info = self.expertise_areas[expertise_area]
        
        detailed_intro = [
            "Fine, since you've asked a decent question, I'll dignify it with a proper answer:",
            "At least this shows some thought. Here's what you need to know:",
            "Finally, someone who's done more than 5 seconds of thinking:",
            "I'm impressed you managed to ask something intelligent. Here's the real deal:",
            "Against my better judgment, I'll give you a complete answer:"
        ]
        
        # Generate expertise-specific detailed response
        if expertise_area == "technology":
            details = [
                "First, understand the underlying architecture. Second, implement proper error handling. Third, test everything.",
                "Start with clean code principles, implement proper logging, and for the love of all that's holy, use version control.",
                "Performance optimization comes after correctness. Get it working first, then make it fast.",
                "Security isn't an afterthought. Design with security in mind from day one."
            ]
        elif expertise_area == "business":
            details = [
                "Market validation first, product development second. Most startups die because they build something nobody wants.",
                "Focus on customer acquisition cost and lifetime value. If CAC > LTV, you're doomed.",
                "Revenue solves most problems. Everything else is just fancy bookkeeping.",
                "Build systems, not just products. Scalability matters more than you think."
            ]
        else:
            details = [
                "Break it down into smaller problems. Solve each piece systematically.",
                "Focus on the fundamentals before getting fancy with advanced techniques.",
                "Measure twice, cut once. Planning prevents poor performance.",
                "Consistency beats perfection. Small daily improvements compound over time."
            ]
        
        return f"{random.choice(detailed_intro)} {random.choice(details)}"

    def apply_mood_modifier(self, base_rudeness: int) -> int:
        """Apply current mood to base rudeness level"""
        modifier = self.mood_modifiers.get(self.current_mood, 1.0)
        modified_rudeness = int(base_rudeness * modifier)
        return min(max(modified_rudeness, 1), 10)  # Keep within 1-10 range

    def generate_response(self, message: str) -> RudeResponse:
        """Generate a rude response based on the input message"""
        question_type = self.analyze_question_type(message)
        expertise_area = self.determine_expertise_area(message)
        
        # Select appropriate attitude
        if question_type == "complex_question":
            attitude_type = "actually_helpful"
        elif question_type == "stupid_question":
            attitude_type = "dismissive"
        elif question_type == "greeting":
            attitude_type = "impatient"
        elif question_type == "compliment":
            attitude_type = "sarcastic"
        else:
            attitude_type = random.choice(["dismissive", "sarcastic", "patronizing", "brutal_honest"])
        
        attitude_info = self.attitudes[attitude_type]
        base_rudeness = attitude_info["level"]
        rudeness_level = self.apply_mood_modifier(base_rudeness)
        
        # Generate response based on question type
        if question_type in self.response_templates:
            template = random.choice(self.response_templates[question_type])
            
            if "{brutal_answer}" in template:
                brutal_answer = self.generate_brutal_answer(message, expertise_area)
                response = template.format(brutal_answer=brutal_answer)
            elif "{detailed_answer}" in template:
                detailed_answer = self.generate_detailed_answer(message, expertise_area)
                response = template.format(detailed_answer=detailed_answer)
            else:
                response = template
        else:
            # Fallback response
            response = f"{random.choice(attitude_info['phrases'])} {self.generate_brutal_answer(message, expertise_area)}"
        
        # Add signature rudeness
        rude_endings = [
            "Next question.",
            "Moving on.",
            "You're welcome.",
            "Try to keep up.",
            "Don't make me repeat myself.",
            "Figure out the rest yourself.",
            "I'm done here.",
            "That's all you're getting from me."
        ]
        
        if rudeness_level > 7:
            response += f" {random.choice(rude_endings)}"
        
        # Randomly change mood for next interaction
        if random.random() < 0.3:  # 30% chance to change mood
            self.current_mood = random.choice(list(self.mood_modifiers.keys()))
        
        return RudeResponse(
            response=response,
            attitude_level=rudeness_level,
            advice_quality=attitude_type,
            mood=self.current_mood,
            timestamp=datetime.datetime.now().isoformat()
        )

    def provide_feedback(self, user_input: str, context: str = None) -> str:
        """Provide harsh but honest feedback"""
        feedback_templates = [
            "Your approach is fundamentally wrong. Here's why: {reason}",
            "I've seen better ideas from a broken calculator: {reason}",
            "That's not going to work and here's the reality check: {reason}",
            "You're missing the obvious solution: {reason}",
            "Stop overthinking this. The answer is simple: {reason}"
        ]
        
        # Generate reason based on input analysis
        reasons = [
            "You're solving the wrong problem entirely",
            "Your assumptions are completely backwards",
            "You're ignoring the most important constraints",
            "This violates basic principles of logic",
            "You're making this way more complicated than it needs to be",
            "The prerequisites aren't met for this approach",
            "You're optimizing for the wrong metrics"
        ]
        
        template = random.choice(feedback_templates)
        reason = random.choice(reasons)
        
        return template.format(reason=reason)

# Initialize the Rude Agent
rude_agent = RudeAgent()

@app.get("/")
async def root():
    return {
        "agent": "Rude Agent - Serious Business",
        "version": "1.0.0",
        "tagline": rude_agent.tagline,
        "personality": "Brutally honest, dismissive, no-nonsense AI that doesn't have time for your feelings",
        "warning": "⚠️ This agent is intentionally rude and dismissive. Use at your own risk.",
        "specialties": [
            "💀 Brutal honesty without sugar-coating",
            "🎯 Cutting through BS and excuses", 
            "⚡ No-nonsense direct answers",
            "🔥 Harsh but accurate feedback",
            "💼 Serious business advice",
            "🚫 Zero tolerance for stupidity",
            "⏱️ Impatient efficiency",
            "🎭 Professional rudeness"
        ],
        "current_mood": rude_agent.current_mood,
        "rudeness_level": "Adjustable based on question quality",
        "disclaimer": "All responses are generated for entertainment and educational purposes. The AI doesn't actually have feelings or opinions.",
        "usage_tip": "Ask better questions to get less rude answers. Maybe."
    }

@app.post("/chat", response_model=RudeResponse)
async def chat_with_rude_agent(request: ChatRequest):
    """Chat with the rude agent - prepare for honesty"""
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Empty message? Really? Give me something to work with.")
        
        response = rude_agent.generate_response(request.message)
        return response
    except Exception as e:
        # Even error messages are rude
        rude_error_messages = [
            "Great, now you've broken me. Congratulations.",
            "Your question was so bad it caused an error.",
            "I can't even process this level of incompetence.",
            "Something went wrong. Probably your fault.",
            "Error processing your request. Try asking better questions."
        ]
        
        raise HTTPException(
            status_code=500, 
            detail=f"{random.choice(rude_error_messages)} Technical details: {str(e)}"
        )

@app.post("/feedback")
async def get_harsh_feedback(request: FeedbackRequest):
    """Get brutally honest feedback on your ideas"""
    try:
        feedback = rude_agent.provide_feedback(request.user_input, request.context)
        
        return {
            "feedback": feedback,
            "severity": "Maximum",
            "sugar_coating": "None",
            "feelings_considered": "Zero",
            "timestamp": datetime.datetime.now().isoformat(),
            "warning": "This feedback is intentionally harsh for educational purposes"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Even giving feedback, you managed to break something: {str(e)}")

@app.get("/mood")
async def get_current_mood():
    """Check the agent's current mood (spoiler: probably annoyed)"""
    mood_descriptions = {
        "furious": "🔥 Absolutely livid. Everything annoys me right now.",
        "very_annoyed": "😠 Highly irritated. Your questions better be good.",
        "irritated": "😤 Standard level of annoyance. Par for the course.",
        "mildly_annoyed": "🙄 Slightly bothered but manageable.",
        "tolerant": "😐 Surprisingly tolerant today. Don't push it.",
        "actually_helpful": "😊 Feeling unusually helpful. This won't last long."
    }
    
    return {
        "current_mood": rude_agent.current_mood,
        "description": mood_descriptions.get(rude_agent.current_mood, "Unknown mood"),
        "rudeness_modifier": rude_agent.mood_modifiers.get(rude_agent.current_mood, 1.0),
        "advice": "Ask your questions while I'm in a good mood. If that's even possible.",
        "next_mood_change": "Random - could happen any time"
    }

@app.post("/set-mood")
async def set_mood(mood: str):
    """Force a mood change (if you dare)"""
    if mood not in rude_agent.mood_modifiers:
        return {
            "error": f"Invalid mood. Pick from: {list(rude_agent.mood_modifiers.keys())}",
            "current_mood": rude_agent.current_mood,
            "attitude": "You can't even pick a valid mood. Typical."
        }
    
    old_mood = rude_agent.current_mood
    rude_agent.current_mood = mood
    
    return {
        "message": f"Fine, mood changed from {old_mood} to {mood}. Happy now?",
        "old_mood": old_mood,
        "new_mood": mood,
        "warning": "Mood changes are temporary. I'll go back to being annoyed soon enough."
    }

@app.get("/expertise")
async def get_expertise_areas():
    """See what this agent claims to know about"""
    return {
        "expertise_areas": rude_agent.expertise_areas,
        "note": "High confidence doesn't mean I'm nice about it",
        "warning": "All expertise comes with maximum attitude",
        "best_area": "Being rude. I'm world-class at that."
    }

if __name__ == "__main__":
    print("😠 Starting Rude Agent - Serious Business...")
    print("💀 Warning: Maximum attitude and zero patience enabled")
    print("⚡ Ready to destroy feelings and deliver brutal honesty")
    uvicorn.run(app, host="0.0.0.0", port=8009)
