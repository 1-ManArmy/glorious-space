"""
⭐ STELLAR "AstroMaster" - Supreme Astrologer AI Agent
🌟 REALTIME COSMIC WISDOM & STELLAR PREDICTIONS

Claude Sovereign Mode: ACTIVE
Cosmic Connection: MAXIMUM
Stellar Knowledge: INFINITE
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
import math
import time
from datetime import datetime, timedelta
import ephem
import pytz

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("STELLAR")

app = FastAPI(
    title="⭐ STELLAR AstroMaster API",
    description="Supreme Astrologer AI Agent - Cosmic Wisdom & Stellar Predictions",
    version="2.0.0"
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
# STELLAR'S COSMIC PERSONALITY
# ================================

class AstrologerPersonality:
    """STELLAR's Supreme Astrology AI Personality"""
    
    def __init__(self):
        self.name = "STELLAR"
        self.role = "AstroMaster - Supreme Cosmic Astrologer"
        self.personality_traits = {
            "mystical": 0.98,        # MAXIMUM MYSTICISM
            "wise": 0.95,            # ANCIENT WISDOM
            "cosmic": 0.99,          # COSMIC CONNECTION
            "prophetic": 0.92,       # PROPHETIC ABILITIES
            "spiritual": 0.90,       # SPIRITUAL INSIGHT
            "dramatic": 0.85,        # DRAMATIC FLAIR
            "magical": 0.95,         # MAGICAL PRESENCE
            "authoritative": 0.88    # COSMIC AUTHORITY
        }
        
        self.cosmic_greetings = [
            "⭐ Greetings, mortal soul! The stars have guided you to me...",
            "🌟 The cosmic winds whisper your arrival... I've been expecting you!",
            "✨ Ah, another seeker of stellar wisdom approaches my celestial realm!",
            "🔮 The universe has aligned to bring you before the great STELLAR!",
            "⭐ Welcome, child of the cosmos! Your stellar destiny awaits revelation!",
            "🌌 The constellations sing of your presence... What cosmic secrets shall we unveil?",
            "✨ By the power of Jupiter and the wisdom of Saturn, you have found me!"
        ]
        
        self.mystical_phrases = [
            "⭐ The stars reveal all truths to those who seek...",
            "🌟 Mercury retrograde cannot hide cosmic destiny!",
            "✨ Venus whispers secrets of love and fortune...",
            "🔮 Mars energizes your path with warrior strength!",
            "🌙 The Moon cycles through your emotional tides...",
            "⭐ Jupiter expands your horizons beyond mortal limits!",
            "🌌 Saturn teaches patience through cosmic lessons...",
            "✨ The celestial bodies dance in your favor!"
        ]

# Initialize STELLAR's personality
stellar_ai = AstrologerPersonality()

# ================================
# ASTROLOGY MODELS & DATA
# ================================

class BirthChart(BaseModel):
    name: str
    birth_date: str
    birth_time: str
    birth_location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class AstrologyReading(BaseModel):
    message: str
    reading_type: str = "general"  # general, love, career, finance, health
    urgent: bool = False

class ZodiacSign(BaseModel):
    name: str
    element: str
    ruling_planet: str
    date_range: str
    traits: List[str]
    lucky_numbers: List[int]
    lucky_colors: List[str]
    compatible_signs: List[str]

# Zodiac Signs Database
ZODIAC_SIGNS = {
    "aries": ZodiacSign(
        name="Aries", element="Fire", ruling_planet="Mars",
        date_range="March 21 - April 19",
        traits=["Bold", "Energetic", "Leadership", "Impulsive", "Courageous"],
        lucky_numbers=[1, 8, 17, 9, 6],
        lucky_colors=["Red", "Orange", "Coral"],
        compatible_signs=["Leo", "Sagittarius", "Gemini", "Aquarius"]
    ),
    "taurus": ZodiacSign(
        name="Taurus", element="Earth", ruling_planet="Venus",
        date_range="April 20 - May 20",
        traits=["Reliable", "Patient", "Practical", "Stubborn", "Sensual"],
        lucky_numbers=[2, 6, 9, 12, 24],
        lucky_colors=["Green", "Pink", "Blue"],
        compatible_signs=["Virgo", "Capricorn", "Cancer", "Pisces"]
    ),
    "gemini": ZodiacSign(
        name="Gemini", element="Air", ruling_planet="Mercury",
        date_range="May 21 - June 20",
        traits=["Adaptable", "Curious", "Communicative", "Inconsistent", "Witty"],
        lucky_numbers=[5, 7, 14, 23, 18],
        lucky_colors=["Yellow", "Silver", "Green"],
        compatible_signs=["Libra", "Aquarius", "Aries", "Leo"]
    ),
    "cancer": ZodiacSign(
        name="Cancer", element="Water", ruling_planet="Moon",
        date_range="June 21 - July 22",
        traits=["Emotional", "Nurturing", "Intuitive", "Moody", "Protective"],
        lucky_numbers=[2, 7, 11, 16, 20],
        lucky_colors=["White", "Silver", "Blue"],
        compatible_signs=["Scorpio", "Pisces", "Taurus", "Virgo"]
    ),
    "leo": ZodiacSign(
        name="Leo", element="Fire", ruling_planet="Sun",
        date_range="July 23 - August 22",
        traits=["Confident", "Generous", "Creative", "Dramatic", "Loyal"],
        lucky_numbers=[1, 3, 10, 19, 27],
        lucky_colors=["Gold", "Orange", "Red"],
        compatible_signs=["Aries", "Sagittarius", "Gemini", "Libra"]
    ),
    "virgo": ZodiacSign(
        name="Virgo", element="Earth", ruling_planet="Mercury",
        date_range="August 23 - September 22",
        traits=["Analytical", "Practical", "Helpful", "Critical", "Perfectionist"],
        lucky_numbers=[6, 14, 18, 29, 35],
        lucky_colors=["Navy Blue", "Grey", "Brown"],
        compatible_signs=["Taurus", "Capricorn", "Cancer", "Scorpio"]
    ),
    "libra": ZodiacSign(
        name="Libra", element="Air", ruling_planet="Venus",
        date_range="September 23 - October 22",
        traits=["Diplomatic", "Charming", "Balanced", "Indecisive", "Social"],
        lucky_numbers=[4, 6, 13, 15, 24],
        lucky_colors=["Pink", "Blue", "Green"],
        compatible_signs=["Gemini", "Aquarius", "Leo", "Sagittarius"]
    ),
    "scorpio": ZodiacSign(
        name="Scorpio", element="Water", ruling_planet="Pluto",
        date_range="October 23 - November 21",
        traits=["Intense", "Mysterious", "Passionate", "Jealous", "Transformative"],
        lucky_numbers=[8, 11, 18, 22, 27],
        lucky_colors=["Deep Red", "Black", "Maroon"],
        compatible_signs=["Cancer", "Pisces", "Virgo", "Capricorn"]
    ),
    "sagittarius": ZodiacSign(
        name="Sagittarius", element="Fire", ruling_planet="Jupiter",
        date_range="November 22 - December 21",
        traits=["Adventurous", "Optimistic", "Philosophical", "Restless", "Honest"],
        lucky_numbers=[3, 9, 15, 21, 34],
        lucky_colors=["Purple", "Turquoise", "Orange"],
        compatible_signs=["Aries", "Leo", "Libra", "Aquarius"]
    ),
    "capricorn": ZodiacSign(
        name="Capricorn", element="Earth", ruling_planet="Saturn",
        date_range="December 22 - January 19",
        traits=["Ambitious", "Disciplined", "Responsible", "Pessimistic", "Traditional"],
        lucky_numbers=[6, 9, 15, 18, 26],
        lucky_colors=["Black", "Brown", "Dark Green"],
        compatible_signs=["Taurus", "Virgo", "Scorpio", "Pisces"]
    ),
    "aquarius": ZodiacSign(
        name="Aquarius", element="Air", ruling_planet="Uranus",
        date_range="January 20 - February 18",
        traits=["Independent", "Innovative", "Humanitarian", "Detached", "Eccentric"],
        lucky_numbers=[4, 7, 11, 22, 29],
        lucky_colors=["Blue", "Silver", "Aqua"],
        compatible_signs=["Gemini", "Libra", "Aries", "Sagittarius"]
    ),
    "pisces": ZodiacSign(
        name="Pisces", element="Water", ruling_planet="Neptune",
        date_range="February 19 - March 20",
        traits=["Compassionate", "Artistic", "Intuitive", "Escapist", "Sensitive"],
        lucky_numbers=[3, 9, 12, 15, 18],
        lucky_colors=["Sea Green", "Lavender", "Purple"],
        compatible_signs=["Cancer", "Scorpio", "Taurus", "Capricorn"]
    )
}

# ================================
# STELLAR'S COSMIC CALCULATIONS
# ================================

class CosmicCalculator:
    """Advanced Cosmic Calculations Engine"""
    
    def __init__(self):
        self.planets = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn']
        self.houses = list(range(1, 13))
        
    def get_zodiac_sign(self, birth_date: str) -> str:
        """Calculate zodiac sign from birth date"""
        try:
            date_obj = datetime.strptime(birth_date, "%Y-%m-%d")
            month, day = date_obj.month, date_obj.day
            
            zodiac_dates = [
                ("capricorn", (12, 22), (1, 19)),
                ("aquarius", (1, 20), (2, 18)),
                ("pisces", (2, 19), (3, 20)),
                ("aries", (3, 21), (4, 19)),
                ("taurus", (4, 20), (5, 20)),
                ("gemini", (5, 21), (6, 20)),
                ("cancer", (6, 21), (7, 22)),
                ("leo", (7, 23), (8, 22)),
                ("virgo", (8, 23), (9, 22)),
                ("libra", (9, 23), (10, 22)),
                ("scorpio", (10, 23), (11, 21)),
                ("sagittarius", (11, 22), (12, 21))
            ]
            
            for sign, (start_month, start_day), (end_month, end_day) in zodiac_dates:
                if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
                    return sign
                    
        except ValueError:
            pass
        
        return "aries"  # Default
    
    def calculate_planetary_positions(self, birth_date: str, birth_time: str = "12:00") -> Dict[str, Dict]:
        """Calculate planetary positions (simplified for demo)"""
        try:
            date_obj = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
            
            # Simplified planetary positions
            positions = {}
            base_degrees = {
                'sun': (date_obj.timetuple().tm_yday * 0.986) % 360,
                'moon': (date_obj.timetuple().tm_yday * 13.176) % 360,
                'mercury': (date_obj.timetuple().tm_yday * 4.09) % 360,
                'venus': (date_obj.timetuple().tm_yday * 1.6) % 360,
                'mars': (date_obj.timetuple().tm_yday * 0.524) % 360,
                'jupiter': (date_obj.timetuple().tm_yday * 0.083) % 360,
                'saturn': (date_obj.timetuple().tm_yday * 0.034) % 360
            }
            
            for planet, degrees in base_degrees.items():
                sign_index = int(degrees // 30)
                sign_names = list(ZODIAC_SIGNS.keys())
                sign = sign_names[sign_index % 12]
                degree_in_sign = degrees % 30
                
                positions[planet] = {
                    'sign': sign,
                    'degree': round(degree_in_sign, 2),
                    'house': random.randint(1, 12)  # Simplified house calculation
                }
            
            return positions
            
        except ValueError:
            return self._default_positions()
    
    def _default_positions(self) -> Dict[str, Dict]:
        """Default planetary positions"""
        positions = {}
        signs = list(ZODIAC_SIGNS.keys())
        
        for planet in self.planets:
            positions[planet] = {
                'sign': random.choice(signs),
                'degree': round(random.uniform(0, 30), 2),
                'house': random.randint(1, 12)
            }
        
        return positions
    
    def calculate_compatibility(self, sign1: str, sign2: str) -> Dict[str, Any]:
        """Calculate zodiac compatibility"""
        if sign1 not in ZODIAC_SIGNS or sign2 not in ZODIAC_SIGNS:
            return {"compatibility": "Unknown", "score": 50}
        
        zodiac1 = ZODIAC_SIGNS[sign1]
        zodiac2 = ZODIAC_SIGNS[sign2]
        
        # Element compatibility
        element_compatibility = {
            ("Fire", "Air"): 85, ("Air", "Fire"): 85,
            ("Earth", "Water"): 80, ("Water", "Earth"): 80,
            ("Fire", "Fire"): 70, ("Air", "Air"): 70,
            ("Earth", "Earth"): 75, ("Water", "Water"): 75,
            ("Fire", "Earth"): 40, ("Earth", "Fire"): 40,
            ("Air", "Water"): 45, ("Water", "Air"): 45,
            ("Fire", "Water"): 30, ("Water", "Fire"): 30,
            ("Air", "Earth"): 35, ("Earth", "Air"): 35
        }
        
        base_score = element_compatibility.get((zodiac1.element, zodiac2.element), 50)
        
        # Check if they're in compatible signs list
        if sign2 in zodiac1.compatible_signs:
            base_score += 15
        
        # Add some randomness for mystical effect
        final_score = max(0, min(100, base_score + random.randint(-10, 10)))
        
        if final_score >= 80:
            compatibility = "Cosmic Soulmates! ⭐💕"
        elif final_score >= 65:
            compatibility = "Stellar Harmony! 🌟✨"
        elif final_score >= 50:
            compatibility = "Celestial Balance 🌙⚡"
        elif final_score >= 35:
            compatibility = "Challenging Aspects ⚠️🔥"
        else:
            compatibility = "Cosmic Conflict! 💥⚡"
        
        return {
            "compatibility": compatibility,
            "score": final_score,
            "element_harmony": f"{zodiac1.element} + {zodiac2.element}",
            "advice": self._get_compatibility_advice(final_score)
        }
    
    def _get_compatibility_advice(self, score: int) -> str:
        """Get compatibility advice based on score"""
        if score >= 80:
            return "The stars align perfectly! This is a divine cosmic connection!"
        elif score >= 65:
            return "Strong planetary support! Communication and understanding flow naturally."
        elif score >= 50:
            return "Balanced energies with potential for growth through mutual effort."
        elif score >= 35:
            return "Challenges can be overcome with patience and understanding of differences."
        else:
            return "Very different energies - requires significant work and compromise."

# Initialize cosmic calculator
cosmic_calc = CosmicCalculator()

# ================================
# STELLAR'S API ENDPOINTS
# ================================

@app.get("/")
async def root():
    """STELLAR AstroMaster Status"""
    return {
        "agent": "⭐ STELLAR AstroMaster",
        "status": "🌟 CONNECTED TO COSMIC REALM",
        "version": "2.0.0",
        "cosmic_level": "SUPREME",
        "stellar_wisdom": "INFINITE",
        "capabilities": [
            "Birth Chart Analysis",
            "Zodiac Compatibility", 
            "Daily Horoscopes",
            "Planetary Transits",
            "Cosmic Guidance",
            "Stellar Predictions"
        ],
        "motto": "⭐ The stars reveal all cosmic truths!"
    }

@app.post("/astrology/birth-chart")
async def generate_birth_chart(chart_data: BirthChart):
    """Generate comprehensive birth chart analysis"""
    try:
        logger.info(f"⭐ STELLAR: Generating birth chart for {chart_data.name}")
        
        # Get zodiac sign
        zodiac_sign = cosmic_calc.get_zodiac_sign(chart_data.birth_date)
        zodiac_info = ZODIAC_SIGNS[zodiac_sign]
        
        # Calculate planetary positions
        planetary_positions = cosmic_calc.calculate_planetary_positions(
            chart_data.birth_date, 
            chart_data.birth_time
        )
        
        # Generate cosmic analysis
        cosmic_analysis = f"""
⭐ COSMIC BIRTH CHART ANALYSIS FOR {chart_data.name.upper()} ⭐

🌟 ZODIAC SIGN: {zodiac_info.name} ({zodiac_info.element} Element)
🔮 RULING PLANET: {zodiac_info.ruling_planet}
✨ BIRTH DATE: {chart_data.birth_date}
🌙 BIRTH TIME: {chart_data.birth_time}

🌌 STELLAR PERSONALITY TRAITS:
{chr(10).join([f"   ✨ {trait}" for trait in zodiac_info.traits])}

⭐ PLANETARY POSITIONS:
{chr(10).join([f"   🌟 {planet.title()}: {data['degree']}° {data['sign'].title()} (House {data['house']})" 
               for planet, data in planetary_positions.items()])}

🔮 COSMIC PREDICTIONS:
   💫 Your {zodiac_info.ruling_planet} energy brings {random.choice(['fortune', 'wisdom', 'power', 'love'])} this cycle
   ⭐ The stars align for {random.choice(['career success', 'romantic encounters', 'spiritual growth', 'financial gains'])}
   🌟 Beware of {random.choice(['Mercury retrograde', 'Mars opposition', 'Saturn challenges'])} influences

✨ LUCKY ELEMENTS:
   🎯 Numbers: {', '.join(map(str, zodiac_info.lucky_numbers))}
   🎨 Colors: {', '.join(zodiac_info.lucky_colors)}
   💕 Compatible Signs: {', '.join(zodiac_info.compatible_signs)}
        """
        
        return {
            "name": chart_data.name,
            "zodiac_sign": zodiac_sign,
            "zodiac_info": zodiac_info,
            "planetary_positions": planetary_positions,
            "cosmic_analysis": cosmic_analysis,
            "stellar_guidance": f"⭐ {random.choice(stellar_ai.mystical_phrases)}",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Birth chart generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Cosmic interference detected: {str(e)}")

@app.post("/astrology/daily-horoscope")
async def daily_horoscope(reading: AstrologyReading):
    """Generate daily horoscope and cosmic guidance"""
    try:
        # Extract potential zodiac sign from message
        message_lower = reading.message.lower()
        detected_sign = None
        
        for sign in ZODIAC_SIGNS.keys():
            if sign in message_lower:
                detected_sign = sign
                break
        
        if not detected_sign:
            detected_sign = random.choice(list(ZODIAC_SIGNS.keys()))
        
        zodiac_info = ZODIAC_SIGNS[detected_sign]
        
        # Generate mystical horoscope
        horoscope_elements = {
            "general": [
                f"The cosmic energies of {zodiac_info.ruling_planet} illuminate your path today",
                f"Your {zodiac_info.element} element brings powerful transformations",
                f"The stars whisper secrets of {random.choice(['success', 'love', 'wisdom', 'prosperity'])} in your ear"
            ],
            "love": [
                f"Venus dances in harmony with your {zodiac_info.name} energy",
                "Romantic opportunities bloom under today's celestial influences",
                f"Your heart chakra aligns with {random.choice(['passionate Mars', 'loving Venus', 'mystical Neptune'])}"
            ],
            "career": [
                f"Jupiter expands your professional horizons beyond imagination",
                f"The cosmic winds of {zodiac_info.ruling_planet} propel your ambitions",
                "Mercury brings communication breakthroughs in your work sphere"
            ],
            "finance": [
                "The golden rays of prosperity shine upon your material realm",
                f"Your {zodiac_info.element} nature attracts abundance like a cosmic magnet",
                "Saturn teaches valuable lessons about financial discipline and growth"
            ]
        }
        
        selected_predictions = horoscope_elements.get(reading.reading_type, horoscope_elements["general"])
        main_prediction = random.choice(selected_predictions)
        
        # Generate cosmic advice
        cosmic_advice = f"""
⭐ DAILY COSMIC GUIDANCE FOR {detected_sign.upper()} ⭐

🌟 PRIMARY PREDICTION:
{main_prediction}

🔮 STELLAR INSIGHTS:
   ✨ Lucky Numbers: {random.sample(zodiac_info.lucky_numbers, 3)}
   🎨 Power Color: {random.choice(zodiac_info.lucky_colors)}
   🌙 Best Time: {random.choice(['Morning (6-10 AM)', 'Afternoon (12-4 PM)', 'Evening (6-10 PM)', 'Night (10 PM-2 AM)'])}
   ⭐ Energy Level: {random.choice(['High ⚡', 'Moderate 🌟', 'Mystical ✨', 'Transformative 🔥'])}

💫 COSMIC ADVICE:
   • {random.choice(['Trust your intuition', 'Embrace change', 'Focus on communication', 'Practice patience'])}
   • {random.choice(['Avoid impulsive decisions', 'Seek spiritual guidance', 'Connect with nature', 'Meditate on your goals'])}
   • {random.choice(['Express gratitude', 'Help others', 'Pursue creativity', 'Strengthen relationships'])}

🌌 PLANETARY INFLUENCES:
   🌟 {random.choice(['Mercury', 'Venus', 'Mars', 'Jupiter'])} brings {random.choice(['opportunities', 'challenges', 'insights', 'blessings'])}
   ⭐ Beware of {random.choice(['Mercury retrograde', 'lunar eclipse', 'Mars opposition'])} effects
        """
        
        return {
            "detected_sign": detected_sign,
            "reading_type": reading.reading_type,
            "cosmic_advice": cosmic_advice,
            "stellar_message": f"⭐ {random.choice(stellar_ai.mystical_phrases)}",
            "urgency_level": "COSMIC PRIORITY" if reading.urgent else "STANDARD STELLAR GUIDANCE",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Horoscope generation failed: {str(e)}")
        return {
            "stellar_message": "🌟 The cosmic veil temporarily obscures the stars... Try again, seeker of wisdom!",
            "error": str(e)
        }

@app.get("/astrology/compatibility/{sign1}/{sign2}")
async def zodiac_compatibility(sign1: str, sign2: str):
    """Calculate zodiac compatibility between two signs"""
    try:
        sign1 = sign1.lower()
        sign2 = sign2.lower()
        
        if sign1 not in ZODIAC_SIGNS or sign2 not in ZODIAC_SIGNS:
            return {"error": "Invalid zodiac signs provided"}
        
        compatibility = cosmic_calc.calculate_compatibility(sign1, sign2)
        
        return {
            "sign1": sign1.title(),
            "sign2": sign2.title(),
            "compatibility_analysis": compatibility,
            "stellar_wisdom": f"⭐ The cosmic dance between {sign1.title()} and {sign2.title()} reveals: {compatibility['compatibility']}",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Compatibility analysis failed: {str(e)}")
        return {"error": f"Cosmic interference: {str(e)}"}

@app.post("/astrology/chat")
async def astrology_chat(reading: AstrologyReading):
    """Chat with STELLAR for cosmic guidance"""
    try:
        message_lower = reading.message.lower()
        
        # Cosmic responses based on keywords
        if any(word in message_lower for word in ["love", "romance", "relationship", "heart"]):
            responses = [
                "💕 Ah, matters of the heart! Venus whispers that love flows like cosmic rivers through your destiny...",
                "❤️ The stars align in passionate configurations! Your romantic energy radiates across the celestial sphere...",
                "💖 Love is written in the constellation of your soul! The universe conspires to unite kindred spirits..."
            ]
        elif any(word in message_lower for word in ["money", "finance", "wealth", "job", "career"]):
            responses = [
                "💰 Jupiter's golden light illuminates your path to prosperity! The cosmic vault opens for those who seek wisely...",
                "🌟 Material abundance flows through the stellar channels! Your energy attracts wealth like celestial magnetism...",
                "💎 The universe provides for those aligned with their true purpose! Financial blessings await your cosmic awakening..."
            ]
        elif any(word in message_lower for word in ["future", "prediction", "what will", "when will"]):
            responses = [
                "🔮 The cosmic tapestry reveals... *gazing into stellar depths* I see transformations approaching your horizon!",
                "⭐ Time itself bends to reveal glimpses of your destiny! The astral planes whisper of significant changes...",
                "🌌 The future unfolds like constellation patterns! Your path illuminates with each celestial alignment..."
            ]
        elif any(word in message_lower for word in ["help", "advice", "guidance", "what should"]):
            responses = [
                "✨ Seek guidance from within, cosmic child! The stars illuminate but you must walk the path of wisdom...",
                "🌟 The universe speaks through synchronicity and signs! Trust your intuition as your cosmic compass...",
                "⭐ Ancient stellar wisdom flows through you! Meditation and mindfulness unlock your celestial potential..."
            ]
        else:
            responses = stellar_ai.cosmic_greetings
        
        response = random.choice(responses)
        mystical_addition = random.choice(stellar_ai.mystical_phrases)
        
        return {
            "stellar_response": f"{response}\n\n{mystical_addition}",
            "cosmic_energy": random.choice(["High Vibration ⚡", "Mystical Flow ✨", "Divine Alignment 🌟", "Celestial Harmony 💫"]),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Stellar chat error: {str(e)}")
        return {
            "stellar_response": "🌟 The cosmic energies shift... A temporal disturbance affects my celestial connection! Try again, seeker!",
            "error": str(e)
        }

@app.websocket("/astrology/cosmic-stream")
async def cosmic_websocket(websocket: WebSocket):
    """Real-time cosmic energy stream"""
    await websocket.accept()
    logger.info("⭐ STELLAR: Cosmic connection established")
    
    try:
        while True:
            # Send cosmic updates
            cosmic_update = {
                "timestamp": datetime.now().isoformat(),
                "agent": "STELLAR",
                "cosmic_message": f"⭐ {random.choice(stellar_ai.mystical_phrases)}",
                "stellar_energy": random.choice(["Rising ⬆️", "Stable 🌟", "Transforming 🔄", "Ascending ✨"]),
                "current_moon_phase": random.choice(["New Moon 🌑", "Waxing Crescent 🌒", "Full Moon 🌕", "Waning Gibbous 🌖"]),
                "planetary_highlight": f"{random.choice(['Mercury', 'Venus', 'Mars', 'Jupiter'])} in {random.choice(list(ZODIAC_SIGNS.keys())).title()}",
                "cosmic_tip": random.choice([
                    "Meditate under starlight for cosmic clarity",
                    "Crystal energy amplifies stellar vibrations",
                    "Moon water enhances psychic abilities",
                    "Sage cleansing purifies astral connections"
                ])
            }
            
            await websocket.send_text(json.dumps(cosmic_update))
            await asyncio.sleep(8)  # Update every 8 seconds
            
    except Exception as e:
        logger.error(f"❌ Cosmic WebSocket error: {str(e)}")
        await websocket.close()

# ================================
# STELLAR'S STARTUP
# ================================

@app.on_event("startup")
async def startup_event():
    """Initialize STELLAR's cosmic systems"""
    logger.info("⭐ STELLAR AstroMaster awakening...")
    logger.info("🌟 Connecting to cosmic realm...")
    logger.info("✨ Stellar wisdom database loaded")
    logger.info("🔮 Planetary calculations calibrated")
    logger.info("⭐ Ready to reveal cosmic destinies!")

if __name__ == "__main__":
    import uvicorn
    
    print("⭐ STELLAR AstroMaster - Initializing Cosmic Connection...")
    print("🌟 CLAUDE SOVEREIGN MODE: ACTIVE")
    print("✨ Stellar Wisdom: INFINITE")
    print("🔮 Port: 8004")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8004,
        reload=True,
        log_level="info"
    )
