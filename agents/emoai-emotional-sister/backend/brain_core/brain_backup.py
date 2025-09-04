# 🧠 Enhanced Brain Backup Logger - UPGRADED FOR SELF-LEARNING AI
# File: brain_backup.py
# Claude Sovereign Mode: ACTIVE

import json
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import logging
import argparse
import hashlib
from typing import Dict, List, Any, Optional

class BrainBackupSystem:
    """
    🧠 Advanced Brain Backup & Memory Management System
    Handles AI learning data, emotional memories, and growth tracking
    """
    
    def __init__(self, memory_path: Path = None, backup_dir: Path = None):
        # Default paths for EmoAI system
        self.memory_path = memory_path or Path("memory/cortex_memory.json")
        self.backup_dir = backup_dir or Path("memory/backups")
        self.log_file = self.backup_dir / "brain_backup.log"
        
        # Create directories
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Backup configuration
        self.max_backups = 10
        self.compression_enabled = True
        self.auto_backup_interval = 3600  # 1 hour
        
    def setup_logging(self):
        """Setup enhanced logging for backup operations"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - 🧠 BACKUP - %(message)s"
        )
        self.logger = logging.getLogger("BrainBackup")
        
    def load_brain_memory(self) -> Optional[Dict[str, Any]]:
        """Load brain memory with enhanced error handling"""
        if not self.memory_path.exists():
            self.logger.warning(f"No brain memory file found at: {self.memory_path}")
            return None
            
        try:
            with open(self.memory_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            # Validate brain data structure
            if self.validate_brain_data(data):
                self.logger.info(f"Brain memory loaded successfully - {len(str(data))} bytes")
                return data
            else:
                self.logger.error("Brain memory validation failed")
                return None
                
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error in brain memory: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error loading brain memory: {e}")
            return None
    
    def validate_brain_data(self, data: Dict[str, Any]) -> bool:
        """Validate brain data structure and integrity"""
        required_fields = ["timestamp", "intelligence_level"]
        
        if not isinstance(data, dict):
            return False
            
        # Check for required fields
        for field in required_fields:
            if field not in data:
                self.logger.warning(f"Missing required field: {field}")
                return False
        
        # Validate intelligence level
        if not isinstance(data.get("intelligence_level"), (int, float)):
            return False
            
        return True
    
    def calculate_data_hash(self, data: Dict[str, Any]) -> str:
        """Calculate hash of brain data for integrity checking"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    def create_backup(self, compress: bool = None) -> Optional[Path]:
        """Create intelligent backup of brain memory"""
        data = self.load_brain_memory()
        if data is None:
            return None
            
        compress = compress if compress is not None else self.compression_enabled
        
        # Generate backup metadata
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data_hash = self.calculate_data_hash(data)
        
        # Enhanced backup data with metadata
        backup_data = {
            "backup_metadata": {
                "timestamp": datetime.now().isoformat(),
                "original_file": str(self.memory_path),
                "data_hash": data_hash,
                "intelligence_level": data.get("intelligence_level", 1.0),
                "emotional_intelligence": data.get("emotional_intelligence", 0.5),
                "total_interactions": data.get("total_interactions", 0),
                "backup_version": "3.0.0"
            },
            "brain_data": data
        }
        
        # Create backup file
        backup_filename = f"brain_backup_{timestamp}_{data_hash}"
        backup_file = self.backup_dir / f"{backup_filename}.json"
        
        try:
            if compress:
                backup_file = backup_file.with_suffix(".json.gz")
                with gzip.open(backup_file, "wt", encoding="utf-8") as f:
                    json.dump(backup_data, f, indent=2)
            else:
                with open(backup_file, "w", encoding="utf-8") as f:
                    json.dump(backup_data, f, indent=2)
            
            self.logger.info(f"Brain backup created: {backup_file}")
            print(f"✅ 🧠 Brain backup saved: {backup_file}")
            
            # Auto-cleanup old backups
            self.cleanup_old_backups()
            
            return backup_file
            
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            print(f"❌ Backup failed: {e}")
            return None
    
    def restore_backup(self, backup_file: Path) -> bool:
        """Restore brain memory from backup"""
        try:
            # Load backup data
            if backup_file.suffix == ".gz":
                with gzip.open(backup_file, "rt", encoding="utf-8") as f:
                    backup_data = json.load(f)
            else:
                with open(backup_file, "r", encoding="utf-8") as f:
                    backup_data = json.load(f)
            
            # Extract brain data
            if "brain_data" in backup_data:
                brain_data = backup_data["brain_data"]
                metadata = backup_data.get("backup_metadata", {})
            else:
                # Legacy backup format
                brain_data = backup_data
                metadata = {}
            
            # Validate restored data
            if not self.validate_brain_data(brain_data):
                self.logger.error("Backup validation failed during restore")
                return False
            
            # Create backup of current state before restore
            current_backup = self.create_backup()
            if current_backup:
                self.logger.info(f"Current state backed up before restore: {current_backup}")
            
            # Restore brain memory
            with open(self.memory_path, "w", encoding="utf-8") as f:
                json.dump(brain_data, f, indent=2)
            
            self.logger.info(f"Brain memory restored from: {backup_file}")
            print(f"✅ 🧠 Brain memory restored from: {backup_file}")
            
            if metadata:
                print(f"📊 Restored Intelligence Level: {metadata.get('intelligence_level', 'Unknown')}")
                print(f"💕 Restored Emotional Intelligence: {metadata.get('emotional_intelligence', 'Unknown')}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restore backup: {e}")
            print(f"❌ Restore failed: {e}")
            return False
    
    def cleanup_old_backups(self, max_backups: int = None):
        """Intelligent cleanup of old backups"""
        max_backups = max_backups if max_backups is not None else self.max_backups
        
        # Get all backup files
        backup_patterns = ["brain_backup_*.json", "brain_backup_*.json.gz"]
        all_backups = []
        
        for pattern in backup_patterns:
            all_backups.extend(self.backup_dir.glob(pattern))
        
        # Sort by modification time (newest first)
        all_backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Keep only the newest backups
        for old_backup in all_backups[max_backups:]:
            try:
                old_backup.unlink()
                self.logger.info(f"Deleted old backup: {old_backup}")
                print(f"🗑️ Deleted old backup: {old_backup.name}")
            except Exception as e:
                self.logger.error(f"Failed to delete backup {old_backup}: {e}")
    
    def get_backup_stats(self) -> Dict[str, Any]:
        """Get comprehensive backup statistics"""
        backup_files = list(self.backup_dir.glob("brain_backup_*"))
        
        if not backup_files:
            return {
                "total_backups": 0,
                "disk_usage": 0,
                "oldest_backup": None,
                "newest_backup": None
            }
        
        # Calculate total size
        total_size = sum(f.stat().st_size for f in backup_files)
        
        # Get oldest and newest
        backup_files.sort(key=lambda x: x.stat().st_mtime)
        oldest = backup_files[0]
        newest = backup_files[-1]
        
        return {
            "total_backups": len(backup_files),
            "disk_usage": total_size,
            "disk_usage_mb": round(total_size / (1024 * 1024), 2),
            "oldest_backup": {
                "file": oldest.name,
                "date": datetime.fromtimestamp(oldest.stat().st_mtime).isoformat()
            },
            "newest_backup": {
                "file": newest.name,
                "date": datetime.fromtimestamp(newest.stat().st_mtime).isoformat()
            },
            "compression_enabled": self.compression_enabled,
            "max_backups": self.max_backups
        }
    
    def schedule_auto_backup(self):
        """Schedule automatic backups (placeholder for future implementation)"""
        self.logger.info("Auto-backup scheduling requested")
        print("🕐 Auto-backup scheduling will be implemented in future version")
        
        # Future: Implement background task scheduling
        # This could use APScheduler or similar for real automation

# CLI Interface
def main():
    parser = argparse.ArgumentParser(description="🧠 Enhanced Brain Backup System for EmoAI")
    parser.add_argument("--memory", type=Path, help="Path to brain memory file")
    parser.add_argument("--backup-dir", type=Path, help="Backup directory")
    parser.add_argument("--backup", action="store_true", help="Create new backup")
    parser.add_argument("--restore", type=Path, help="Restore from backup file")
    parser.add_argument("--cleanup", action="store_true", help="Cleanup old backups")
    parser.add_argument("--max-backups", type=int, default=10, help="Max backups to keep")
    parser.add_argument("--compress", action="store_true", help="Enable compression")
    parser.add_argument("--stats", action="store_true", help="Show backup statistics")
    
    args = parser.parse_args()
    
    # Initialize backup system
    backup_system = BrainBackupSystem(args.memory, args.backup_dir)
    
    if args.compress:
        backup_system.compression_enabled = True
    
    if args.max_backups:
        backup_system.max_backups = args.max_backups
    
    # Execute requested action
    if args.backup:
        backup_system.create_backup()
    elif args.restore:
        backup_system.restore_backup(args.restore)
    elif args.cleanup:
        backup_system.cleanup_old_backups()
    elif args.stats:
        stats = backup_system.get_backup_stats()
        print("📊 Brain Backup Statistics:")
        print(json.dumps(stats, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
