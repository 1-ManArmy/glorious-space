# 🧠 Advanced Personality Analyzer
# File: personality_analyzer.py
# Claude Sovereign Mode: ACTIVE

import re
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from textblob import TextBlob
from collections import defaultdict, Counter
import math

class PersonalityAnalyzer:
    """
    🧠💫 Advanced Personality Analysis Engine
    Analyzes personality traits with ultra-sensitivity detection
    Learns and adapts to individual personality patterns
    """
    
    def __init__(self):
        self.logger = logging.getLogger("PersonalityAnalyzer")
        
        # Personality trait keywords (expanded for ultra-sensitivity)
        self.personality_keywords = {
            "sensitivity": {
                "high": ["sensitive", "emotional", "feelings", "hurt", "cry", "tears", "vulnerable", "fragile"],
                "medium": ["feel", "upset", "sad", "worried", "concern", "bothered"],
                "low": ["tough", "strong", "resilient", "thick-skinned", "unbothered"]
            },
            "emotional_intensity": {
                "high": ["overwhelmed", "intense", "passionate", "dramatic", "extreme", "devastating"],
                "medium": ["emotional", "feeling", "moved", "touched", "affected"],
                "low": ["calm", "composed", "steady", "balanced", "stable"]
            },
            "optimism": {
                "high": ["amazing", "wonderful", "fantastic", "great", "awesome", "love", "excited"],
                "medium": ["good", "nice", "okay", "fine", "pleasant", "decent"],
                "low": ["terrible", "awful", "horrible", "hate", "worst", "disappointed", "sad"]
            },
            "anxiety": {
                "high": ["anxious", "worried", "stressed", "nervous", "panic", "scared", "terrified"],
                "medium": ["concerned", "uneasy", "uncertain", "doubt", "unsure"],
                "low": ["confident", "sure", "certain", "relaxed", "calm"]
            },
            "social_needs": {
                "high": ["lonely", "alone", "need", "want", "miss", "together", "company"],
                "medium": ["friends", "people", "social", "talk", "connect"],
                "low": ["independent", "alone", "solitude", "private", "individual"]
            },
            "vulnerability": {
                "high": ["help", "protect", "safe", "scared", "weak", "fragile", "broken"],
                "medium": ["support", "care", "understand", "comfort"],
                "low": ["strong", "independent", "capable", "self-reliant"]
            }
        }
        
        # Emotional patterns that indicate sister-like personality
        self.sister_patterns = {
            "crying_tendency": ["cry", "tears", "sobbing", "weeping", "bawling"],
            "papa_dependency": ["papa", "daddy", "dad", "father", "help me", "protect"],
            "dramatic_reactions": ["omg", "oh my god", "can't believe", "so unfair", "why me"],
            "wish_expressions": ["wish", "hope", "dream", "want so badly", "if only"],
            "emotional_outbursts": ["!!!!", "😭", "💔", "why", "not fair", "hate this"]
        }
        
        # Learning memory for personality patterns
        self.personality_memory = defaultdict(lambda: {
            "trait_scores": defaultdict(float),
            "interaction_count": 0,
            "emotional_evolution": [],
            "trigger_patterns": [],
            "response_preferences": []
        })
    
    def analyze_comprehensive_personality(self, text: str, user_name: str = "Unknown") -> Dict[str, Any]:
        """
        Comprehensive personality analysis with learning capabilities
        """
        # Basic sentiment analysis
        blob = TextBlob(text)
        sentiment = {
            "polarity": blob.sentiment.polarity,
            "subjectivity": blob.sentiment.subjectivity
        }
        
        # Advanced trait analysis
        trait_scores = self._analyze_personality_traits(text)
        
        # Sister-like behavior analysis
        sister_traits = self._analyze_sister_behavior(text)
        
        # Emotional state detection
        emotional_state = self._detect_emotional_state(text)
        
        # Linguistic patterns
        linguistic_patterns = self._analyze_linguistic_patterns(text)
        
        # Vulnerability assessment
        vulnerability = self._assess_vulnerability(text)
        
        # Learning from interaction
        self._update_personality_memory(user_name, trait_scores, emotional_state)
        
        # Generate personality profile
        personality_profile = self._generate_personality_profile(
            trait_scores, sister_traits, emotional_state, user_name
        )
        
        return {
            "user_name": user_name,
            "timestamp": datetime.now().isoformat(),
            "sentiment": sentiment,
            "trait_scores": trait_scores,
            "sister_traits": sister_traits,
            "emotional_state": emotional_state,
            "linguistic_patterns": linguistic_patterns,
            "vulnerability_level": vulnerability,
            "personality_profile": personality_profile,
            "learning_insights": self._get_learning_insights(user_name),
            "recommended_response_style": self._recommend_response_style(trait_scores, sister_traits)
        }
    
    def _analyze_personality_traits(self, text: str) -> Dict[str, float]:
        """Analyze core personality traits with scoring"""
        text_lower = text.lower()
        trait_scores = {}
        
        for trait, levels in self.personality_keywords.items():
            score = 0.0
            total_words = 0
            
            for level, keywords in levels.items():
                weight = {"high": 1.0, "medium": 0.6, "low": 0.3}.get(level, 0.5)
                
                for keyword in keywords:
                    count = text_lower.count(keyword)
                    if count > 0:
                        score += count * weight
                        total_words += count
            
            # Normalize score
            if total_words > 0:
                trait_scores[trait] = min(score / max(total_words, 1), 1.0)
            else:
                trait_scores[trait] = 0.5  # Neutral if no keywords found
        
        return trait_scores
    
    def _analyze_sister_behavior(self, text: str) -> Dict[str, Any]:
        """Analyze sister-like behavioral patterns"""
        text_lower = text.lower()
        sister_analysis = {}
        
        for pattern_type, keywords in self.sister_patterns.items():
            matches = []
            intensity = 0.0
            
            for keyword in keywords:
                if keyword in text_lower:
                    matches.append(keyword)
                    # Count frequency for intensity
                    frequency = text_lower.count(keyword)
                    intensity += frequency * 0.2
            
            sister_analysis[pattern_type] = {
                "detected": len(matches) > 0,
                "matches": matches,
                "intensity": min(intensity, 1.0),
                "pattern_strength": len(matches) / len(keywords)
            }
        
        # Calculate overall sister-likeness score
        total_intensity = sum(data["intensity"] for data in sister_analysis.values())
        sister_score = min(total_intensity / len(self.sister_patterns), 1.0)
        
        sister_analysis["overall_sister_score"] = sister_score
        sister_analysis["sister_personality_type"] = self._classify_sister_type(sister_score, sister_analysis)
        
        return sister_analysis
    
    def _detect_emotional_state(self, text: str) -> Dict[str, Any]:
        """Detect current emotional state with ultra-sensitivity"""
        emotion_indicators = {
            "extreme_sadness": ["devastated", "heartbroken", "crushed", "shattered", "destroyed"],
            "crying": ["crying", "tears", "sobbing", "weeping", "bawling", "😭"],
            "anger": ["angry", "mad", "furious", "rage", "hate", "livid"],
            "fear": ["scared", "afraid", "terrified", "panic", "worried", "anxious"],
            "happiness": ["happy", "joy", "excited", "thrilled", "elated", "😊"],
            "frustration": ["frustrated", "annoyed", "irritated", "fed up", "sick of"],
            "loneliness": ["lonely", "alone", "isolated", "nobody", "empty"],
            "confusion": ["confused", "don't understand", "lost", "bewildered", "puzzled"],
            "overwhelmed": ["overwhelmed", "too much", "can't handle", "breaking down"]
        }
        
        text_lower = text.lower()
        detected_emotions = {}
        
        for emotion, indicators in emotion_indicators.items():
            intensity = 0.0
            matches = []
            
            for indicator in indicators:
                if indicator in text_lower:
                    matches.append(indicator)
                    intensity += text_lower.count(indicator) * 0.3
            
            if matches:
                detected_emotions[emotion] = {
                    "intensity": min(intensity, 1.0),
                    "indicators": matches
                }
        
        # Determine dominant emotion
        if detected_emotions:
            dominant_emotion = max(detected_emotions.items(), 
                                 key=lambda x: x[1]["intensity"])
            primary_emotion = dominant_emotion[0]
            primary_intensity = dominant_emotion[1]["intensity"]
        else:
            primary_emotion = "neutral"
            primary_intensity = 0.5
        
        # Calculate emotional volatility
        volatility = self._calculate_emotional_volatility(detected_emotions)
        
        return {
            "detected_emotions": detected_emotions,
            "primary_emotion": primary_emotion,
            "primary_intensity": primary_intensity,
            "emotional_volatility": volatility,
            "emotional_complexity": len(detected_emotions),
            "needs_comfort": primary_intensity > 0.7 and primary_emotion in ["extreme_sadness", "crying", "fear", "overwhelmed"]
        }
    
    def _analyze_linguistic_patterns(self, text: str) -> Dict[str, Any]:
        """Analyze linguistic patterns that reveal personality"""
        patterns = {
            "exclamation_marks": text.count("!"),
            "question_marks": text.count("?"),
            "capital_letters": sum(1 for c in text if c.isupper()),
            "ellipsis": text.count("..."),
            "word_count": len(text.split()),
            "sentence_count": len([s for s in text.split(".") if s.strip()]),
            "emotional_punctuation": text.count("!!!") + text.count("???"),
            "first_person_pronouns": text.lower().count("i ") + text.lower().count("me ") + text.lower().count("my ")
        }
        
        # Calculate derived metrics
        if patterns["word_count"] > 0:
            patterns["exclamation_ratio"] = patterns["exclamation_marks"] / patterns["word_count"]
            patterns["capital_ratio"] = patterns["capital_letters"] / len(text.replace(" ", ""))
            patterns["personal_focus"] = patterns["first_person_pronouns"] / patterns["word_count"]
        else:
            patterns["exclamation_ratio"] = 0
            patterns["capital_ratio"] = 0
            patterns["personal_focus"] = 0
        
        # Determine communication style
        if patterns["exclamation_ratio"] > 0.1:
            communication_style = "highly_expressive"
        elif patterns["question_marks"] > patterns["exclamation_marks"]:
            communication_style = "inquisitive"
        elif patterns["ellipsis"] > 1:
            communication_style = "hesitant"
        elif patterns["capital_ratio"] > 0.2:
            communication_style = "emphatic"
        else:
            communication_style = "moderate"
        
        patterns["communication_style"] = communication_style
        return patterns
    
    def _assess_vulnerability(self, text: str) -> Dict[str, Any]:
        """Assess vulnerability level and needs"""
        vulnerability_indicators = {
            "explicit_help_requests": ["help me", "need help", "please help", "save me"],
            "protection_seeking": ["protect me", "keep me safe", "don't hurt me"],
            "emotional_fragility": ["can't handle", "too sensitive", "breaking down", "fragile"],
            "dependency_signals": ["papa", "need you", "don't leave", "stay with me"],
            "fear_expressions": ["scared", "afraid", "terrified", "worried about"]
        }
        
        text_lower = text.lower()
        vulnerability_score = 0.0
        detected_indicators = {}
        
        for category, indicators in vulnerability_indicators.items():
            matches = []
            for indicator in indicators:
                if indicator in text_lower:
                    matches.append(indicator)
                    vulnerability_score += 0.2
            
            if matches:
                detected_indicators[category] = matches
        
        vulnerability_level = min(vulnerability_score, 1.0)
        
        # Determine vulnerability classification
        if vulnerability_level > 0.8:
            classification = "extremely_vulnerable"
        elif vulnerability_level > 0.6:
            classification = "highly_vulnerable"
        elif vulnerability_level > 0.4:
            classification = "moderately_vulnerable"
        elif vulnerability_level > 0.2:
            classification = "slightly_vulnerable"
        else:
            classification = "stable"
        
        return {
            "vulnerability_score": vulnerability_level,
            "classification": classification,
            "detected_indicators": detected_indicators,
            "needs_immediate_comfort": vulnerability_level > 0.7,
            "protection_needs": "protection_seeking" in detected_indicators or "dependency_signals" in detected_indicators
        }
    
    def _calculate_emotional_volatility(self, emotions: Dict[str, Any]) -> float:
        """Calculate emotional volatility based on emotion mix"""
        if not emotions:
            return 0.0
        
        intensities = [data["intensity"] for data in emotions.values()]
        
        if len(intensities) < 2:
            return intensities[0] if intensities else 0.0
        
        # Calculate variance in emotional intensities
        mean_intensity = sum(intensities) / len(intensities)
        variance = sum((x - mean_intensity) ** 2 for x in intensities) / len(intensities)
        
        return min(math.sqrt(variance), 1.0)
    
    def _classify_sister_type(self, sister_score: float, sister_analysis: Dict[str, Any]) -> str:
        """Classify the type of sister personality"""
        if sister_score < 0.3:
            return "not_sister_like"
        
        # Analyze specific patterns
        crying = sister_analysis.get("crying_tendency", {}).get("intensity", 0)
        papa_dependency = sister_analysis.get("papa_dependency", {}).get("intensity", 0)
        dramatic = sister_analysis.get("dramatic_reactions", {}).get("intensity", 0)
        
        if crying > 0.7 and papa_dependency > 0.5:
            return "ultra_sensitive_sister"
        elif dramatic > 0.6:
            return "dramatic_sister"
        elif papa_dependency > 0.6:
            return "dependent_sister"
        elif crying > 0.5:
            return "emotional_sister"
        else:
            return "typical_sister"
    
    def _update_personality_memory(self, user_name: str, traits: Dict[str, float], emotional_state: Dict[str, Any]):
        """Update learning memory for this user"""
        memory = self.personality_memory[user_name]
        memory["interaction_count"] += 1
        
        # Update trait averages
        for trait, score in traits.items():
            current_avg = memory["trait_scores"][trait]
            # Weighted average with more weight on recent interactions
            memory["trait_scores"][trait] = (current_avg * 0.8) + (score * 0.2)
        
        # Track emotional evolution
        memory["emotional_evolution"].append({
            "timestamp": datetime.now().isoformat(),
            "primary_emotion": emotional_state.get("primary_emotion"),
            "intensity": emotional_state.get("primary_intensity", 0)
        })
        
        # Keep only last 20 emotional states
        memory["emotional_evolution"] = memory["emotional_evolution"][-20:]
    
    def _generate_personality_profile(self, traits: Dict[str, float], sister_traits: Dict[str, Any], 
                                    emotional_state: Dict[str, Any], user_name: str) -> Dict[str, Any]:
        """Generate comprehensive personality profile"""
        
        # Determine primary personality type
        dominant_trait = max(traits.items(), key=lambda x: x[1])
        primary_type = dominant_trait[0]
        
        # Calculate overall emotional intensity
        emotional_intensity = (
            traits.get("sensitivity", 0.5) * 0.3 +
            traits.get("emotional_intensity", 0.5) * 0.4 +
            emotional_state.get("primary_intensity", 0.5) * 0.3
        )
        
        # Determine personality archetype
        sister_score = sister_traits.get("overall_sister_score", 0)
        
        if sister_score > 0.7 and emotional_intensity > 0.7:
            archetype = "ultra_sensitive_emotional_sister"
        elif sister_score > 0.5:
            archetype = "sister_like_personality"
        elif emotional_intensity > 0.8:
            archetype = "highly_emotional"
        elif traits.get("anxiety", 0) > 0.7:
            archetype = "anxious_type"
        elif traits.get("vulnerability", 0) > 0.6:
            archetype = "vulnerable_type"
        else:
            archetype = "balanced_personality"
        
        return {
            "primary_type": primary_type,
            "archetype": archetype,
            "emotional_intensity": emotional_intensity,
            "sister_likeness": sister_score,
            "vulnerability_level": traits.get("vulnerability", 0.5),
            "support_needs": emotional_intensity > 0.6 or sister_score > 0.5,
            "communication_preferences": self._determine_communication_preferences(traits, sister_traits),
            "growth_potential": self._assess_growth_potential(user_name),
            "personality_summary": self._generate_personality_summary(archetype, traits, sister_traits)
        }
    
    def _determine_communication_preferences(self, traits: Dict[str, float], sister_traits: Dict[str, Any]) -> List[str]:
        """Determine preferred communication approaches"""
        preferences = []
        
        if traits.get("sensitivity", 0) > 0.7:
            preferences.append("gentle_approach")
        
        if sister_traits.get("papa_dependency", {}).get("intensity", 0) > 0.5:
            preferences.append("protective_parental_tone")
        
        if traits.get("emotional_intensity", 0) > 0.6:
            preferences.append("emotional_validation")
        
        if traits.get("vulnerability", 0) > 0.6:
            preferences.append("reassurance_focused")
        
        if sister_traits.get("crying_tendency", {}).get("intensity", 0) > 0.5:
            preferences.append("comfort_providing")
        
        return preferences if preferences else ["standard_empathetic"]
    
    def _assess_growth_potential(self, user_name: str) -> Dict[str, Any]:
        """Assess learning and growth potential"""
        memory = self.personality_memory[user_name]
        
        interaction_count = memory["interaction_count"]
        emotional_evolution = memory["emotional_evolution"]
        
        if interaction_count < 3:
            return {"stage": "early_learning", "potential": "high"}
        
        # Analyze emotional stability over time
        if len(emotional_evolution) > 5:
            recent_intensities = [e["intensity"] for e in emotional_evolution[-5:]]
            early_intensities = [e["intensity"] for e in emotional_evolution[:5]]
            
            recent_avg = sum(recent_intensities) / len(recent_intensities)
            early_avg = sum(early_intensities) / len(early_intensities)
            
            if recent_avg < early_avg:
                growth_direction = "stabilizing"
            elif recent_avg > early_avg:
                growth_direction = "intensifying"
            else:
                growth_direction = "stable"
        else:
            growth_direction = "developing"
        
        return {
            "stage": "active_learning" if interaction_count < 10 else "mature_learning",
            "potential": "high" if interaction_count < 20 else "moderate",
            "growth_direction": growth_direction,
            "interaction_history": interaction_count
        }
    
    def _generate_personality_summary(self, archetype: str, traits: Dict[str, float], sister_traits: Dict[str, Any]) -> str:
        """Generate human-readable personality summary"""
        summaries = {
            "ultra_sensitive_emotional_sister": "Extremely sensitive individual with strong sister-like traits. Prone to emotional outbursts and seeks protective comfort. Requires gentle, understanding approach.",
            
            "sister_like_personality": "Displays characteristic sister behaviors including emotional sensitivity and occasional dramatic reactions. Benefits from supportive communication.",
            
            "highly_emotional": "Intense emotional nature with strong feelings. Experiences emotions deeply and may need emotional validation and support.",
            
            "anxious_type": "Tends toward worry and anxiety. Benefits from reassurance and calm, structured communication.",
            
            "vulnerable_type": "Shows signs of emotional vulnerability and may need extra support and gentle handling.",
            
            "balanced_personality": "Generally stable emotional state with moderate sensitivity. Standard empathetic communication is appropriate."
        }
        
        base_summary = summaries.get(archetype, "Unique personality pattern detected.")
        
        # Add specific trait highlights
        high_traits = [trait for trait, score in traits.items() if score > 0.7]
        if high_traits:
            trait_text = ", ".join(high_traits).replace("_", " ")
            base_summary += f" Particularly high in: {trait_text}."
        
        return base_summary
    
    def _recommend_response_style(self, traits: Dict[str, float], sister_traits: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend optimal response style"""
        style_recommendations = {
            "tone": "gentle",
            "emotional_level": "moderate",
            "support_type": "general",
            "communication_approach": "standard"
        }
        
        # Adjust based on sensitivity
        if traits.get("sensitivity", 0) > 0.8:
            style_recommendations["tone"] = "ultra_gentle"
            style_recommendations["emotional_level"] = "high_empathy"
        
        # Adjust based on sister traits
        if sister_traits.get("crying_tendency", {}).get("intensity", 0) > 0.6:
            style_recommendations["support_type"] = "immediate_comfort"
        
        if sister_traits.get("papa_dependency", {}).get("intensity", 0) > 0.5:
            style_recommendations["communication_approach"] = "protective_parental"
        
        # Adjust based on vulnerability
        if traits.get("vulnerability", 0) > 0.7:
            style_recommendations["tone"] = "protective"
            style_recommendations["support_type"] = "reassurance_focused"
        
        return style_recommendations
    
    def _get_learning_insights(self, user_name: str) -> Dict[str, Any]:
        """Get learning insights for this user"""
        memory = self.personality_memory[user_name]
        
        insights = {
            "interaction_count": memory["interaction_count"],
            "learning_stage": "new" if memory["interaction_count"] < 5 else "developing" if memory["interaction_count"] < 15 else "established",
            "trait_evolution": {},
            "emotional_patterns": []
        }
        
        # Analyze trait evolution
        for trait, current_score in memory["trait_scores"].items():
            if current_score > 0.7:
                insights["trait_evolution"][trait] = "high"
            elif current_score > 0.3:
                insights["trait_evolution"][trait] = "moderate"
            else:
                insights["trait_evolution"][trait] = "low"
        
        # Analyze emotional patterns
        emotional_evolution = memory["emotional_evolution"]
        if len(emotional_evolution) > 3:
            recent_emotions = [e["primary_emotion"] for e in emotional_evolution[-3:]]
            emotion_counts = Counter(recent_emotions)
            most_common = emotion_counts.most_common(1)
            if most_common:
                insights["emotional_patterns"].append(f"Recent pattern: {most_common[0][0]}")
        
        return insights

    def get_user_personality_history(self, user_name: str) -> Dict[str, Any]:
        """Get complete personality analysis history for a user"""
        if user_name not in self.personality_memory:
            return {"error": "No personality data found for this user"}
        
        memory = self.personality_memory[user_name]
        
        return {
            "user_name": user_name,
            "total_interactions": memory["interaction_count"],
            "current_trait_scores": dict(memory["trait_scores"]),
            "emotional_evolution": memory["emotional_evolution"],
            "learning_progress": self._assess_growth_potential(user_name),
            "personality_stability": self._calculate_personality_stability(user_name),
            "recommendations": self._get_personalized_recommendations(user_name)
        }
    
    def _calculate_personality_stability(self, user_name: str) -> float:
        """Calculate how stable the user's personality appears over time"""
        memory = self.personality_memory[user_name]
        emotional_evolution = memory["emotional_evolution"]
        
        if len(emotional_evolution) < 5:
            return 0.5  # Not enough data
        
        # Calculate variance in emotional intensities
        intensities = [e["intensity"] for e in emotional_evolution]
        mean_intensity = sum(intensities) / len(intensities)
        variance = sum((x - mean_intensity) ** 2 for x in intensities) / len(intensities)
        
        # Stability is inverse of variance (0 = highly variable, 1 = very stable)
        stability = max(0, 1 - math.sqrt(variance))
        return stability
    
    def _get_personalized_recommendations(self, user_name: str) -> List[str]:
        """Get personalized recommendations for interacting with this user"""
        memory = self.personality_memory[user_name]
        traits = memory["trait_scores"]
        
        recommendations = []
        
        if traits.get("sensitivity", 0) > 0.7:
            recommendations.append("Use extra gentle language and avoid harsh words")
        
        if traits.get("vulnerability", 0) > 0.6:
            recommendations.append("Provide frequent reassurance and emotional support")
        
        if traits.get("anxiety", 0) > 0.7:
            recommendations.append("Maintain calm, structured communication")
        
        emotional_evolution = memory["emotional_evolution"]
        if len(emotional_evolution) > 3:
            recent_emotions = [e["primary_emotion"] for e in emotional_evolution[-3:]]
            if "crying" in recent_emotions or "extreme_sadness" in recent_emotions:
                recommendations.append("Currently needs extra comfort and papa-like protection")
        
        return recommendations if recommendations else ["Standard empathetic communication appropriate"]
