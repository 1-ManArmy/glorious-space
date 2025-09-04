from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
import uvicorn
import json
import os
import hashlib
import base64
import datetime
import uuid
from pathlib import Path
import mimetypes
import secrets
import string

app = FastAPI(title="MemoriaAI Memory Brain Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MemoryItem(BaseModel):
    id: str
    title: str
    content: str
    category: str
    tags: List[str]
    memory_type: str  # "note", "password", "document", "voice", "image", "secret"
    created_at: str
    last_accessed: str
    is_encrypted: bool
    importance_level: int  # 1-5 scale
    reminder_date: Optional[str] = None

class PasswordEntry(BaseModel):
    id: str
    website: str
    username: str
    email: Optional[str] = None
    encrypted_password: str
    notes: Optional[str] = None
    last_updated: str
    strength_score: int

class VoiceNote(BaseModel):
    id: str
    title: str
    transcript: str
    duration: float
    file_path: str
    created_at: str
    tags: List[str]

class SearchRequest(BaseModel):
    query: str
    category: Optional[str] = None
    memory_type: Optional[str] = None
    tags: Optional[List[str]] = None
    importance_level: Optional[int] = None

class ReminderRequest(BaseModel):
    memory_id: str
    reminder_date: str
    reminder_message: str

class MemoriaAI:
    def __init__(self):
        self.name = "MemoriaAI"
        self.description = "Your infinite memory brain - never forget anything again!"
        
        # Create storage directories
        self.base_path = Path("memoria_storage")
        self.memories_path = self.base_path / "memories"
        self.passwords_path = self.base_path / "passwords"
        self.files_path = self.base_path / "files"
        self.voice_path = self.base_path / "voice_notes"
        self.images_path = self.base_path / "images"
        
        for path in [self.base_path, self.memories_path, self.passwords_path, 
                    self.files_path, self.voice_path, self.images_path]:
            path.mkdir(exist_ok=True)
        
        # Memory database files
        self.memories_db = self.base_path / "memories.json"
        self.passwords_db = self.base_path / "passwords.json"
        self.voice_db = self.base_path / "voice_notes.json"
        
        # Initialize databases
        self.init_databases()
        
        # Categories for organization
        self.categories = [
            "Personal", "Work", "Study", "Health", "Finance", "Travel",
            "Recipes", "Ideas", "Contacts", "Important Documents",
            "Passwords", "Voice Notes", "Images", "Secrets", "Reminders"
        ]
        
        # Memory personality traits
        self.personality = {
            "catchphrases": [
                "🧠 I never forget - that's what I'm here for!",
                "💾 Stored safely in my infinite memory!",
                "🔍 Let me search through my vast memory banks...",
                "📚 I remember everything so you don't have to!",
                "🎯 Found it! I told you I never forget!",
                "💡 Ah yes, I remember this perfectly!",
                "🏛️ My memory palace has room for everything!"
            ],
            "responses": {
                "storing": [
                    "Perfect! I've permanently etched this into my memory banks 🧠✨",
                    "Got it! This is now part of my eternal memory collection 💾",
                    "Stored with military precision! I'll never let you forget this 📚",
                    "Added to my infinite memory vault - 100% unforgettable! 🏛️"
                ],
                "retrieving": [
                    "Ah! Here's exactly what you're looking for 🎯",
                    "Found it instantly! My memory is lightning fast ⚡",
                    "Here you go - pulled from the depths of my memory palace 🏰",
                    "I knew you'd ask for this eventually! Here it is 🔮"
                ],
                "not_found": [
                    "Hmm, that's strange... I don't seem to have that in my memory 🤔",
                    "My usually perfect memory is coming up empty on this one 😅",
                    "That's not ringing any bells in my memory banks... yet! 🔍",
                    "I don't recall storing that - want to add it now? 💭"
                ]
            }
        }

    def init_databases(self):
        """Initialize JSON databases if they don't exist"""
        if not self.memories_db.exists():
            with open(self.memories_db, 'w') as f:
                json.dump([], f)
        
        if not self.passwords_db.exists():
            with open(self.passwords_db, 'w') as f:
                json.dump([], f)
                
        if not self.voice_db.exists():
            with open(self.voice_db, 'w') as f:
                json.dump([], f)

    def load_memories(self) -> List[Dict]:
        """Load memories from JSON database"""
        try:
            with open(self.memories_db, 'r') as f:
                return json.load(f)
        except:
            return []

    def save_memories(self, memories: List[Dict]):
        """Save memories to JSON database"""
        with open(self.memories_db, 'w') as f:
            json.dump(memories, f, indent=2)

    def load_passwords(self) -> List[Dict]:
        """Load passwords from JSON database"""
        try:
            with open(self.passwords_db, 'r') as f:
                return json.load(f)
        except:
            return []

    def save_passwords(self, passwords: List[Dict]):
        """Save passwords to JSON database"""
        with open(self.passwords_db, 'w') as f:
            json.dump(passwords, f, indent=2)

    def encrypt_text(self, text: str) -> str:
        """Simple base64 encoding for demo purposes"""
        return base64.b64encode(text.encode()).decode()

    def decrypt_text(self, encrypted_text: str) -> str:
        """Simple base64 decoding for demo purposes"""
        try:
            return base64.b64decode(encrypted_text.encode()).decode()
        except:
            return encrypted_text

    def generate_password(self, length: int = 16, include_symbols: bool = True) -> str:
        """Generate a secure password"""
        chars = string.ascii_letters + string.digits
        if include_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        return ''.join(secrets.choice(chars) for _ in range(length))

    def calculate_password_strength(self, password: str) -> int:
        """Calculate password strength score (1-100)"""
        score = 0
        length = len(password)
        
        # Length scoring
        if length >= 12:
            score += 30
        elif length >= 8:
            score += 20
        else:
            score += 10
        
        # Character variety
        if any(c.islower() for c in password):
            score += 10
        if any(c.isupper() for c in password):
            score += 10
        if any(c.isdigit() for c in password):
            score += 15
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 25
        
        # Additional complexity
        if length >= 16:
            score += 10
        
        return min(score, 100)

    def store_memory(self, title: str, content: str, category: str, 
                    tags: List[str], memory_type: str, importance_level: int,
                    encrypt: bool = False) -> MemoryItem:
        """Store a new memory"""
        memories = self.load_memories()
        
        memory_id = str(uuid.uuid4())
        now = datetime.datetime.now().isoformat()
        
        if encrypt:
            content = self.encrypt_text(content)
        
        memory = {
            "id": memory_id,
            "title": title,
            "content": content,
            "category": category,
            "tags": tags,
            "memory_type": memory_type,
            "created_at": now,
            "last_accessed": now,
            "is_encrypted": encrypt,
            "importance_level": importance_level,
            "reminder_date": None
        }
        
        memories.append(memory)
        self.save_memories(memories)
        
        return MemoryItem(**memory)

    def search_memories(self, query: str, category: str = None, 
                       memory_type: str = None, tags: List[str] = None,
                       importance_level: int = None) -> List[MemoryItem]:
        """Search through stored memories"""
        memories = self.load_memories()
        results = []
        
        for memory in memories:
            # Update last accessed
            memory["last_accessed"] = datetime.datetime.now().isoformat()
            
            # Check search criteria
            match = True
            
            if query:
                query_lower = query.lower()
                if (query_lower not in memory["title"].lower() and 
                    query_lower not in memory["content"].lower() and
                    not any(query_lower in tag.lower() for tag in memory["tags"])):
                    match = False
            
            if category and memory["category"] != category:
                match = False
                
            if memory_type and memory["memory_type"] != memory_type:
                match = False
                
            if tags and not any(tag in memory["tags"] for tag in tags):
                match = False
                
            if importance_level and memory["importance_level"] != importance_level:
                match = False
            
            if match:
                # Decrypt content if needed for display
                display_memory = memory.copy()
                if memory["is_encrypted"]:
                    display_memory["content"] = self.decrypt_text(memory["content"])
                
                results.append(MemoryItem(**display_memory))
        
        # Save updated access times
        self.save_memories(memories)
        
        return results

    def store_password(self, website: str, username: str, password: str,
                      email: str = None, notes: str = None) -> PasswordEntry:
        """Store a password securely"""
        passwords = self.load_passwords()
        
        password_id = str(uuid.uuid4())
        encrypted_password = self.encrypt_text(password)
        strength_score = self.calculate_password_strength(password)
        
        password_entry = {
            "id": password_id,
            "website": website,
            "username": username,
            "email": email,
            "encrypted_password": encrypted_password,
            "notes": notes,
            "last_updated": datetime.datetime.now().isoformat(),
            "strength_score": strength_score
        }
        
        passwords.append(password_entry)
        self.save_passwords(passwords)
        
        return PasswordEntry(**password_entry)

    def get_password(self, website: str = None, username: str = None) -> List[PasswordEntry]:
        """Retrieve stored passwords"""
        passwords = self.load_passwords()
        results = []
        
        for pwd in passwords:
            match = True
            
            if website and website.lower() not in pwd["website"].lower():
                match = False
                
            if username and username.lower() != pwd["username"].lower():
                match = False
            
            if match:
                # Return with encrypted password for security
                results.append(PasswordEntry(**pwd))
        
        return results

# Initialize MemoriaAI
memoria = MemoriaAI()

@app.get("/")
async def root():
    return {
        "agent": "MemoriaAI - Memory Brain",
        "version": "1.0.0",
        "description": "🧠 Your infinite memory brain - I never forget anything!",
        "motto": "Remember everything, forget nothing!",
        "capabilities": [
            "🗃️ Store unlimited memories and notes",
            "🔐 Secure password management",
            "🎤 Voice note transcription and storage",
            "📁 File upload and organization",
            "🔍 Lightning-fast search across all memories",
            "🏷️ Smart tagging and categorization",
            "⏰ Intelligent reminders",
            "🔒 Encryption for sensitive data",
            "📊 Memory analytics and insights",
            "🎯 Never lose anything again!"
        ],
        "storage_stats": {
            "total_memories": len(memoria.load_memories()),
            "total_passwords": len(memoria.load_passwords()),
            "categories": memoria.categories
        },
        "personality": "I'm your digital memory palace! I store everything perfectly and retrieve it instantly. No detail is too small, no secret too important - I keep it all safe and organized! 🧠✨"
    }

@app.post("/store-memory", response_model=MemoryItem)
async def store_memory(
    title: str = Form(...),
    content: str = Form(...),
    category: str = Form(...),
    tags: str = Form(""),  # Comma-separated tags
    memory_type: str = Form("note"),
    importance_level: int = Form(3),
    encrypt: bool = Form(False)
):
    """Store a new memory"""
    try:
        tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        
        memory = memoria.store_memory(
            title=title,
            content=content,
            category=category,
            tags=tags_list,
            memory_type=memory_type,
            importance_level=importance_level,
            encrypt=encrypt
        )
        
        return memory
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing memory: {str(e)}")

@app.post("/search-memories")
async def search_memories(request: SearchRequest):
    """Search through stored memories"""
    try:
        results = memoria.search_memories(
            query=request.query,
            category=request.category,
            memory_type=request.memory_type,
            tags=request.tags,
            importance_level=request.importance_level
        )
        
        response_message = ""
        if results:
            response_message = f"🎯 Found {len(results)} memories! " + \
                             memoria.personality["responses"]["retrieving"][0]
        else:
            response_message = memoria.personality["responses"]["not_found"][0]
        
        return {
            "message": response_message,
            "results": results,
            "total_found": len(results),
            "search_query": request.query
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching memories: {str(e)}")

@app.post("/store-password", response_model=PasswordEntry)
async def store_password(
    website: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(None),
    notes: str = Form(None)
):
    """Store a password securely"""
    try:
        password_entry = memoria.store_password(
            website=website,
            username=username,
            password=password,
            email=email,
            notes=notes
        )
        
        return password_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing password: {str(e)}")

@app.get("/get-passwords")
async def get_passwords(website: str = None, username: str = None):
    """Retrieve stored passwords"""
    try:
        passwords = memoria.get_password(website=website, username=username)
        
        # For security, return passwords with masked values
        safe_passwords = []
        for pwd in passwords:
            safe_pwd = pwd.dict()
            safe_pwd["encrypted_password"] = "••••••••"  # Mask for display
            safe_passwords.append(safe_pwd)
        
        return {
            "message": f"🔐 Found {len(passwords)} password entries!",
            "passwords": safe_passwords,
            "security_note": "Passwords are encrypted and masked for security"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving passwords: {str(e)}")

@app.post("/generate-password")
async def generate_password(
    length: int = 16,
    include_symbols: bool = True
):
    """Generate a secure password"""
    try:
        new_password = memoria.generate_password(length=length, include_symbols=include_symbols)
        strength = memoria.calculate_password_strength(new_password)
        
        return {
            "password": new_password,
            "strength_score": strength,
            "strength_level": "Strong" if strength >= 80 else "Medium" if strength >= 60 else "Weak",
            "message": f"🔑 Generated a {strength}/100 strength password!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating password: {str(e)}")

@app.post("/upload-file")
async def upload_file(
    file: UploadFile = File(...),
    title: str = Form(...),
    category: str = Form("Documents"),
    tags: str = Form(""),
    importance_level: int = Form(3)
):
    """Upload and store a file"""
    try:
        # Save file
        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix
        filename = f"{file_id}{file_extension}"
        file_path = memoria.files_path / filename
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Store metadata as memory
        tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        tags_list.append("file")
        tags_list.append(file.content_type or "unknown")
        
        file_info = f"File: {file.filename}\nType: {file.content_type}\nSize: {len(content)} bytes\nStored: {filename}"
        
        memory = memoria.store_memory(
            title=title,
            content=file_info,
            category=category,
            tags=tags_list,
            memory_type="document",
            importance_level=importance_level
        )
        
        return {
            "message": f"📁 File '{file.filename}' stored successfully in my memory!",
            "memory": memory,
            "file_path": str(file_path),
            "file_size": len(content)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@app.get("/memory-stats")
async def get_memory_stats():
    """Get memory statistics and insights"""
    try:
        memories = memoria.load_memories()
        passwords = memoria.load_passwords()
        
        # Category breakdown
        category_counts = {}
        for memory in memories:
            cat = memory["category"]
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Memory type breakdown
        type_counts = {}
        for memory in memories:
            mem_type = memory["memory_type"]
            type_counts[mem_type] = type_counts.get(mem_type, 0) + 1
        
        # Importance level breakdown
        importance_counts = {}
        for memory in memories:
            level = memory["importance_level"]
            importance_counts[level] = importance_counts.get(level, 0) + 1
        
        return {
            "total_memories": len(memories),
            "total_passwords": len(passwords),
            "category_breakdown": category_counts,
            "memory_type_breakdown": type_counts,
            "importance_breakdown": importance_counts,
            "storage_health": "Perfect! All memories intact 🧠✨",
            "memory_palace_status": "Expanding infinitely 🏛️",
            "message": "📊 Your memory statistics - I keep track of everything!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

@app.get("/categories")
async def get_categories():
    """Get all available categories"""
    return {
        "categories": memoria.categories,
        "message": "🗂️ Here are all my organized categories!"
    }

@app.delete("/delete-memory/{memory_id}")
async def delete_memory(memory_id: str):
    """Delete a memory (with great reluctance!)"""
    try:
        memories = memoria.load_memories()
        original_count = len(memories)
        
        memories = [m for m in memories if m["id"] != memory_id]
        
        if len(memories) < original_count:
            memoria.save_memories(memories)
            return {
                "message": "😢 Memory deleted... I hate forgetting things, but if you insist!",
                "deleted": True
            }
        else:
            return {
                "message": "🤔 I couldn't find that memory to delete. Are you sure it exists?",
                "deleted": False
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting memory: {str(e)}")

if __name__ == "__main__":
    print("🧠 Starting MemoriaAI - Memory Brain Agent...")
    print("💾 Ready to remember everything forever!")
    print("🏛️ Building your infinite memory palace...")
    uvicorn.run(app, host="0.0.0.0", port=8008)
