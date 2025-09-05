# 🧠 Enhanced Emotional Memory System
# File: emotional_memory.py
# Claude Sovereign Mode: ACTIVE

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import sqlite3
import asyncio
from collections import defaultdict

class EmotionalMemory:
    """
    🧠💕 Advanced Emotional Memory System
    Stores, analyzes, and learns from emotional interactions
    Like a digital heart that remembers every feeling
    """
    
    def __init__(self, memory_dir: Path = None):
        self.memory_dir = memory_dir or Path("memory")
        self.memory_dir.mkdir(exist_ok=True)
        
        # Memory files
        self.interactions_file = self.memory_dir / "emotional_interactions.json"
        self.learning_file = self.memory_dir / "learning_sessions.json"
        self.wishes_file = self.memory_dir / "unfulfilled_wishes.json"
        self.growth_file = self.memory_dir / "emotional_growth.json"
        
        # Setup logging
        self.logger = logging.getLogger("EmotionalMemory")
        
        # Memory storage
        self.interactions = []
        self.learning_sessions = []
        self.wishes = []
        self.emotional_patterns = {}
        
        # Load existing memories
        self.load_all_memories()
        
    def load_all_memories(self):
        """Load all emotional memories from storage"""
        try:
            # Load interactions
            if self.interactions_file.exists():
                with open(self.interactions_file, "r") as f:
                    self.interactions = json.load(f)
            
            # Load learning sessions
            if self.learning_file.exists():
                with open(self.learning_file, "r") as f:
                    self.learning_sessions = json.load(f)
            
            # Load wishes
            if self.wishes_file.exists():
                with open(self.wishes_file, "r") as f:
                    self.wishes = json.load(f)
                    
            self.logger.info(f"Loaded {len(self.interactions)} interactions, {len(self.learning_sessions)} learning sessions")
            
        except Exception as e:
            self.logger.error(f"Failed to load memories: {e}")
    
    def save_interaction(self, interaction: Dict[str, Any]):
        """Save emotional interaction to memory"""
        try:
            # Add memory metadata
            interaction.update({
                "memory_id": f"mem_{len(self.interactions)}_{int(datetime.now().timestamp())}",
                "emotional_intensity": self._calculate_emotional_intensity(interaction),
                "memory_strength": self._calculate_memory_strength(interaction)
            })
            
            self.interactions.append(interaction)
            
            # Save to file
            with open(self.interactions_file, "w") as f:
                json.dump(self.interactions, f, indent=2)
            
            # Update emotional patterns
            self._update_emotional_patterns(interaction)
            
            self.logger.info(f"Saved interaction: {interaction['id']}")
            
        except Exception as e:
            self.logger.error(f"Failed to save interaction: {e}")
    
    def save_learning_session(self, learning_data: Any):
        """Save learning feedback session"""
        try:
            learning_session = {
                "timestamp": datetime.now().isoformat(),
                "session_id": f"learn_{len(self.learning_sessions)}_{int(datetime.now().timestamp())}",
                "learning_data": learning_data.__dict__ if hasattr(learning_data, '__dict__') else str(learning_data),
                "emotional_growth": self._calculate_growth_metrics()
            }
            
            self.learning_sessions.append(learning_session)
            
            # Save to file
            with open(self.learning_file, "w") as f:
                json.dump(self.learning_sessions, f, indent=2)
                
            self.logger.info(f"Saved learning session: {learning_session['session_id']}")
            
        except Exception as e:
            self.logger.error(f"Failed to save learning session: {e}")
    
    def save_wish(self, wish_data: Dict[str, Any]):
        """Save unfulfilled wish to memory"""
        try:
            wish_entry = {
                "timestamp": datetime.now().isoformat(),
                "wish_id": f"wish_{len(self.wishes)}_{int(datetime.now().timestamp())}",
                **wish_data,
                "emotional_impact": self._calculate_wish_impact(wish_data),
                "fulfillment_attempts": 0
            }
            
            self.wishes.append(wish_entry)
            
            # Save to file
            with open(self.wishes_file, "w") as f:
                json.dump(self.wishes, f, indent=2)
                
            self.logger.info(f"Saved wish: {wish_entry['wish_id']}")
            
        except Exception as e:
            self.logger.error(f"Failed to save wish: {e}")
    
    def _calculate_emotional_intensity(self, interaction: Dict[str, Any]) -> float:
        """Calculate emotional intensity of interaction"""
        detected_emotions = interaction.get("detected_emotions", {})
        
        if not detected_emotions:
            return 0.3  # Neutral intensity
        
        # Calculate weighted intensity
        intensity_weights = {
            "angry": 0.9,
            "sad": 0.8,
            "scared": 0.7,
            "happy": 0.6,
            "confused": 0.5,
            "triggered_crying": 1.0
        }
        
        total_intensity = 0
        total_weight = 0
        
        for emotion, value in detected_emotions.items():
            weight = intensity_weights.get(emotion, 0.4)
            total_intensity += value * weight
            total_weight += weight
        
        return min(total_intensity / max(total_weight, 1), 1.0)
    
    def _calculate_memory_strength(self, interaction: Dict[str, Any]) -> float:
        """Calculate how strongly this memory should be retained"""
        base_strength = 0.5
        
        # Increase strength for emotional intensity
        emotional_intensity = self._calculate_emotional_intensity(interaction)
        base_strength += emotional_intensity * 0.3
        
        # Increase strength for crying triggers
        if interaction.get("papa_alert", False):
            base_strength += 0.2
        
        # Increase strength for user interaction length
        message_length = len(interaction.get("user_message", ""))
        if message_length > 100:
            base_strength += 0.1
        
        return min(base_strength, 1.0)
    
    def _calculate_wish_impact(self, wish_data: Dict[str, Any]) -> float:
        """Calculate emotional impact of unfulfilled wish"""
        importance = wish_data.get("importance", 0.5)
        fulfillment_prob = wish_data.get("fulfillment_probability", 0.2)
        
        # Higher impact for important wishes with low fulfillment probability
        impact = importance * (1 - fulfillment_prob)
        return min(impact, 1.0)
    
    def _calculate_growth_metrics(self) -> Dict[str, float]:
        """Calculate emotional growth metrics"""
        if not self.interactions:
            return {"growth_rate": 0.0, "emotional_stability": 0.5}
        
        recent_interactions = self.interactions[-10:]  # Last 10 interactions
        
        # Calculate average emotional intensity over time
        intensities = [self._calculate_emotional_intensity(i) for i in recent_interactions]
        avg_intensity = sum(intensities) / len(intensities)
        
        # Calculate emotional stability (lower variance = higher stability)
        if len(intensities) > 1:
            variance = sum((x - avg_intensity) ** 2 for x in intensities) / len(intensities)
            stability = max(0, 1 - variance)
        else:
            stability = 0.5
        
        return {
            "growth_rate": len(self.learning_sessions) * 0.1,
            "emotional_stability": stability,
            "interaction_frequency": len(recent_interactions)
        }
    
    def _update_emotional_patterns(self, interaction: Dict[str, Any]):
        """Update emotional pattern recognition"""
        detected_emotions = interaction.get("detected_emotions", {})
        user_name = interaction.get("user_name", "Unknown")
        
        # Track user-specific emotional patterns
        if user_name not in self.emotional_patterns:
            self.emotional_patterns[user_name] = {
                "common_emotions": defaultdict(int),
                "interaction_count": 0,
                "emotional_triggers": [],
                "response_effectiveness": []
            }
        
        pattern = self.emotional_patterns[user_name]
        pattern["interaction_count"] += 1
        
        # Count emotions
        for emotion, intensity in detected_emotions.items():
            if intensity > 0.3:  # Only count significant emotions
                pattern["common_emotions"][emotion] += 1
        
        # Track crying triggers
        if interaction.get("papa_alert", False):
            message = interaction.get("user_message", "").lower()
            pattern["emotional_triggers"].append(message[:50])  # First 50 chars
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics"""
        total_interactions = len(self.interactions)
        total_wishes = len(self.wishes)
        total_learning = len(self.learning_sessions)
        
        # Count crying incidents
        crying_count = sum(1 for i in self.interactions if i.get("papa_alert", False))
        
        # Count papa calls
        papa_calls = sum(1 for i in self.interactions 
                        if "papa" in i.get("ai_response", "").lower())
        
        # Calculate average emotional intensity
        if self.interactions:
            avg_intensity = sum(self._calculate_emotional_intensity(i) 
                              for i in self.interactions) / total_interactions
        else:
            avg_intensity = 0.0
        
        # Get most common emotions
        all_emotions = defaultdict(int)
        for interaction in self.interactions:
            for emotion in interaction.get("detected_emotions", {}):
                all_emotions[emotion] += 1
        
        # Calculate fulfillment rate of wishes
        if self.wishes:
            high_importance_wishes = [w for w in self.wishes if w.get("importance", 0) > 0.7]
            unfulfilled_rate = len(high_importance_wishes) / len(self.wishes)
        else:
            unfulfilled_rate = 0.0
        
        return {
            "total_interactions": total_interactions,
            "total_wishes": total_wishes,
            "total_learning_sessions": total_learning,
            "crying_count": crying_count,
            "papa_calls": papa_calls,
            "average_emotional_intensity": round(avg_intensity, 3),
            "most_common_emotions": dict(sorted(all_emotions.items(), 
                                               key=lambda x: x[1], reverse=True)[:5]),
            "unfulfilled_wish_rate": round(unfulfilled_rate, 3),
            "emotional_patterns": len(self.emotional_patterns),
            "memory_file_sizes": {
                "interactions": self.interactions_file.stat().st_size if self.interactions_file.exists() else 0,
                "learning": self.learning_file.stat().st_size if self.learning_file.exists() else 0,
                "wishes": self.wishes_file.stat().st_size if self.wishes_file.exists() else 0
            },
            "growth_metrics": self._calculate_growth_metrics()
        }
    
    def get_emotional_insights(self, user_name: str = None) -> Dict[str, Any]:
        """Get emotional insights for specific user or overall"""
        if user_name and user_name in self.emotional_patterns:
            pattern = self.emotional_patterns[user_name]
            return {
                "user": user_name,
                "interaction_count": pattern["interaction_count"],
                "common_emotions": dict(pattern["common_emotions"]),
                "emotional_triggers": pattern["emotional_triggers"][-5:],  # Last 5 triggers
                "emotional_volatility": self._calculate_user_volatility(user_name)
            }
        else:
            # Overall insights
            return {
                "total_users": len(self.emotional_patterns),
                "most_emotional_users": self._get_most_emotional_users(),
                "global_emotional_trends": self._get_emotional_trends(),
                "crying_trigger_analysis": self._analyze_crying_triggers()
            }
    
    def _calculate_user_volatility(self, user_name: str) -> float:
        """Calculate emotional volatility for a user"""
        user_interactions = [i for i in self.interactions 
                           if i.get("user_name") == user_name]
        
        if len(user_interactions) < 2:
            return 0.5
        
        intensities = [self._calculate_emotional_intensity(i) for i in user_interactions]
        avg_intensity = sum(intensities) / len(intensities)
        variance = sum((x - avg_intensity) ** 2 for x in intensities) / len(intensities)
        
        return min(variance * 2, 1.0)  # Scale to 0-1
    
    def _get_most_emotional_users(self) -> List[Dict[str, Any]]:
        """Get users with highest emotional intensity"""
        user_stats = []
        
        for user_name, pattern in self.emotional_patterns.items():
            user_interactions = [i for i in self.interactions 
                               if i.get("user_name") == user_name]
            
            if user_interactions:
                avg_intensity = sum(self._calculate_emotional_intensity(i) 
                                  for i in user_interactions) / len(user_interactions)
                
                user_stats.append({
                    "user": user_name,
                    "average_intensity": round(avg_intensity, 3),
                    "interaction_count": len(user_interactions),
                    "volatility": round(self._calculate_user_volatility(user_name), 3)
                })
        
        return sorted(user_stats, key=lambda x: x["average_intensity"], reverse=True)[:5]
    
    def _get_emotional_trends(self) -> Dict[str, Any]:
        """Analyze emotional trends over time"""
        if not self.interactions:
            return {}
        
        # Group by day
        daily_emotions = defaultdict(lambda: defaultdict(int))
        
        for interaction in self.interactions:
            timestamp = interaction.get("timestamp", "")
            try:
                date = datetime.fromisoformat(timestamp).date()
                emotions = interaction.get("detected_emotions", {})
                
                for emotion, intensity in emotions.items():
                    if intensity > 0.3:
                        daily_emotions[str(date)][emotion] += 1
            except:
                continue
        
        return dict(daily_emotions)
    
    def _analyze_crying_triggers(self) -> Dict[str, int]:
        """Analyze what triggers crying the most"""
        triggers = defaultdict(int)
        
        for interaction in self.interactions:
            if interaction.get("papa_alert", False):
                message = interaction.get("user_message", "").lower()
                
                # Look for trigger keywords
                trigger_keywords = [
                    "angry", "mad", "upset", "disappointed", "ignore", 
                    "mean", "hurt", "sad", "cry", "hate"
                ]
                
                for keyword in trigger_keywords:
                    if keyword in message:
                        triggers[keyword] += 1
        
        return dict(sorted(triggers.items(), key=lambda x: x[1], reverse=True))
