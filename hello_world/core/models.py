# Models for Glorious Space - The Digital Crown Jewels
# Where Data Becomes Royal Architecture

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
import uuid
import os


class CustomUser(AbstractUser):
    """
    Enhanced User Model - The Digital Nobility
    Extends Django's AbstractUser with royal features
    """
    
    # Profile Information
    bio = models.TextField(max_length=1000, blank=True, help_text="Your royal story")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, help_text="Your noble portrait")
    location = models.CharField(max_length=100, blank=True, help_text="Your kingdom's location")
    website = models.URLField(blank=True, help_text="Your digital castle")
    
    # Professional Details
    title = models.CharField(max_length=100, blank=True, help_text="Your noble title")
    company = models.CharField(max_length=100, blank=True, help_text="Your royal court")
    skills = models.JSONField(default=list, help_text="Your magical abilities")
    experience_level = models.CharField(
        max_length=20,
        choices=[
            ('apprentice', 'Apprentice Mage'),
            ('journeyman', 'Journeyman Developer'),
            ('expert', 'Expert Craftsman'),
            ('master', 'Master Wizard'),
            ('grandmaster', 'Grandmaster Architect'),
        ],
        default='apprentice'
    )
    
    # Social Connections
    github_username = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_handle = models.CharField(max_length=100, blank=True)
    discord_username = models.CharField(max_length=100, blank=True)
    
    # Preferences & Settings
    theme_preference = models.CharField(
        max_length=20,
        choices=[
            ('royal_purple', 'Royal Purple'),
            ('midnight_gold', 'Midnight Gold'),
            ('emerald_crown', 'Emerald Crown'),
            ('sapphire_throne', 'Sapphire Throne'),
        ],
        default='royal_purple'
    )
    notification_preferences = models.JSONField(default=dict, help_text="Notification settings")
    privacy_settings = models.JSONField(default=dict, help_text="Privacy configuration")
    
    # Activity Tracking
    last_active = models.DateTimeField(auto_now=True)
    is_online = models.BooleanField(default=False)
    total_projects = models.PositiveIntegerField(default=0)
    total_contributions = models.PositiveIntegerField(default=0)
    reputation_score = models.PositiveIntegerField(default=0)
    
    # Achievements & Badges
    badges = models.JSONField(default=list, help_text="Earned achievement badges")
    certifications = models.JSONField(default=list, help_text="Professional certifications")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'glorious_users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['last_active']),
            models.Index(fields=['reputation_score']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} - {self.title}"
    
    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.username})
    
    @property
    def display_name(self):
        """Get the best display name for the user"""
        return self.get_full_name() or self.username
    
    @property
    def avatar_url(self):
        """Get avatar URL with fallback"""
        if self.avatar:
            return self.avatar.url
        return f"https://ui-avatars.com/api/?name={self.display_name}&size=150&background=667eea&color=fff"
    
    def add_badge(self, badge_name, badge_data=None):
        """Add achievement badge to user"""
        if badge_data is None:
            badge_data = {}
        
        badge = {
            'name': badge_name,
            'earned_at': timezone.now().isoformat(),
            **badge_data
        }
        
        if badge not in self.badges:
            self.badges.append(badge)
            self.save(update_fields=['badges'])
    
    def update_reputation(self, points):
        """Update user reputation score"""
        self.reputation_score = max(0, self.reputation_score + points)
        self.save(update_fields=['reputation_score'])


# Set the custom user model
User = get_user_model()


class Project(models.Model):
    """
    Project Model - The Digital Masterpieces
    Represents developer projects and portfolios
    """
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, help_text="Your project's royal name")
    slug = models.SlugField(max_length=200, unique=True, help_text="URL-friendly version")
    description = models.TextField(help_text="Describe your masterpiece")
    
    # Project Details
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    collaborators = models.ManyToManyField(User, through='ProjectCollaboration', related_name='collaborated_projects')
    
    # Technical Information
    tech_stack = models.JSONField(default=list, help_text="Technologies used")
    category = models.CharField(
        max_length=50,
        choices=[
            ('web_app', 'Web Application'),
            ('mobile_app', 'Mobile Application'),
            ('desktop_app', 'Desktop Application'),
            ('game', 'Game Development'),
            ('ai_ml', 'AI/Machine Learning'),
            ('blockchain', 'Blockchain/Web3'),
            ('iot', 'Internet of Things'),
            ('data_science', 'Data Science'),
            ('devtools', 'Developer Tools'),
            ('library', 'Library/Framework'),
            ('other', 'Other'),
        ],
        default='web_app'
    )
    
    # Repository & Links
    repository_url = models.URLField(blank=True, help_text="Source code repository")
    live_demo_url = models.URLField(blank=True, help_text="Live demonstration")
    documentation_url = models.URLField(blank=True, help_text="Project documentation")
    
    # Media & Assets
    thumbnail = models.ImageField(upload_to='project_thumbnails/', null=True, blank=True)
    gallery_images = models.JSONField(default=list, help_text="Additional project images")
    demo_video_url = models.URLField(blank=True, help_text="Demo video URL")
    
    # Project Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('planning', 'Planning Phase'),
            ('development', 'In Development'),
            ('testing', 'Testing Phase'),
            ('deployed', 'Deployed'),
            ('maintenance', 'Maintenance'),
            ('archived', 'Archived'),
        ],
        default='planning'
    )
    
    # Visibility & Collaboration
    visibility = models.CharField(
        max_length=20,
        choices=[
            ('public', 'Public'),
            ('private', 'Private'),
            ('team_only', 'Team Only'),
        ],
        default='public'
    )
    is_featured = models.BooleanField(default=False, help_text="Featured on homepage")
    allow_collaboration = models.BooleanField(default=True, help_text="Allow others to contribute")
    
    # Metrics & Engagement
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    fork_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)
    
    # SEO & Discovery
    tags = models.JSONField(default=list, help_text="Project tags for discovery")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'glorious_projects'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['category', 'visibility']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_featured']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.owner.display_name}"
    
    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})
    
    @property
    def thumbnail_url(self):
        """Get thumbnail URL with fallback"""
        if self.thumbnail:
            return self.thumbnail.url
        return f"https://via.placeholder.com/400x300/667eea/ffffff?text={self.title[:20]}"
    
    def increment_view_count(self):
        """Increment project view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


class ProjectCollaboration(models.Model):
    """
    Project Collaboration Model - The Royal Court
    Manages project collaborations and permissions
    """
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    collaborator = models.ForeignKey(User, on_delete=models.CASCADE)
    
    role = models.CharField(
        max_length=20,
        choices=[
            ('viewer', 'Viewer'),
            ('contributor', 'Contributor'),
            ('maintainer', 'Maintainer'),
            ('admin', 'Administrator'),
        ],
        default='contributor'
    )
    
    permissions = models.JSONField(default=dict, help_text="Specific permissions")
    joined_at = models.DateTimeField(auto_now_add=True)
    invitation_accepted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'glorious_project_collaborations'
        unique_together = ['project', 'collaborator']
        indexes = [
            models.Index(fields=['project', 'role']),
            models.Index(fields=['collaborator']),
        ]
    
    def __str__(self):
        return f"{self.collaborator.display_name} - {self.role} on {self.project.title}"


class ChatRoom(models.Model):
    """
    Chat Room Model - The Royal Chambers
    Manages chat rooms and communication spaces
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, help_text="Room name")
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, help_text="Room description")
    
    # Room Configuration
    room_type = models.CharField(
        max_length=20,
        choices=[
            ('public', 'Public Room'),
            ('private', 'Private Room'),
            ('project', 'Project Room'),
            ('team', 'Team Room'),
            ('dm', 'Direct Message'),
        ],
        default='public'
    )
    
    # Participants
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_rooms')
    members = models.ManyToManyField(User, through='ChatRoomMembership', related_name='chat_rooms')
    
    # Settings
    max_members = models.PositiveIntegerField(default=100)
    allow_voice_chat = models.BooleanField(default=True)
    allow_video_chat = models.BooleanField(default=True)
    allow_file_sharing = models.BooleanField(default=True)
    is_moderated = models.BooleanField(default=False)
    
    # Activity
    last_activity = models.DateTimeField(auto_now=True)
    message_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'glorious_chat_rooms'
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['room_type', 'owner']),
            models.Index(fields=['last_activity']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.room_type})"
    
    def get_absolute_url(self):
        return reverse('chat:room', kwargs={'slug': self.slug})


class ChatRoomMembership(models.Model):
    """
    Chat Room Membership Model - The Guest List
    Manages user memberships in chat rooms
    """
    
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    role = models.CharField(
        max_length=20,
        choices=[
            ('member', 'Member'),
            ('moderator', 'Moderator'),
            ('admin', 'Administrator'),
        ],
        default='member'
    )
    
    # Status
    is_muted = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    last_read_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'glorious_chat_memberships'
        unique_together = ['room', 'user']
        indexes = [
            models.Index(fields=['room', 'role']),
            models.Index(fields=['user', 'joined_at']),
        ]
    
    def __str__(self):
        return f"{self.user.display_name} in {self.room.name}"


class ChatMessage(models.Model):
    """
    Chat Message Model - The Royal Scrolls
    Stores chat messages and conversation history
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    
    # Message Content
    content = models.TextField(help_text="Message content")
    message_type = models.CharField(
        max_length=20,
        choices=[
            ('text', 'Text Message'),
            ('image', 'Image'),
            ('file', 'File'),
            ('voice', 'Voice Message'),
            ('video', 'Video Message'),
            ('system', 'System Message'),
            ('code', 'Code Snippet'),
        ],
        default='text'
    )
    
    # Attachments
    attachment_url = models.URLField(blank=True, help_text="Attachment URL")
    attachment_metadata = models.JSONField(default=dict, help_text="File metadata")
    
    # Message Features
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    is_edited = models.BooleanField(default=False)
    edit_history = models.JSONField(default=list, help_text="Edit history")
    
    # Reactions & Engagement
    reactions = models.JSONField(default=dict, help_text="Message reactions")
    is_pinned = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'glorious_chat_messages'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['room', 'created_at']),
            models.Index(fields=['sender', 'created_at']),
            models.Index(fields=['message_type']),
        ]
    
    def __str__(self):
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"{self.sender.display_name}: {preview}"
    
    def add_reaction(self, user, emoji):
        """Add reaction to message"""
        if emoji not in self.reactions:
            self.reactions[emoji] = []
        
        if user.id not in self.reactions[emoji]:
            self.reactions[emoji].append(user.id)
            self.save(update_fields=['reactions'])
    
    def remove_reaction(self, user, emoji):
        """Remove reaction from message"""
        if emoji in self.reactions and user.id in self.reactions[emoji]:
            self.reactions[emoji].remove(user.id)
            if not self.reactions[emoji]:
                del self.reactions[emoji]
            self.save(update_fields=['reactions'])


class AIConversation(models.Model):
    """
    AI Conversation Model - The Digital Oracle
    Manages AI chat sessions and conversation history
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_conversations')
    
    # Conversation Details
    title = models.CharField(max_length=200, help_text="Conversation title")
    ai_model = models.CharField(
        max_length=50,
        choices=[
            ('claude-3', 'Claude 3'),
            ('gpt-4', 'GPT-4'),
            ('gemini-pro', 'Gemini Pro'),
            ('llama-2', 'Llama 2'),
            ('custom', 'Custom Model'),
        ],
        default='claude-3'
    )
    
    # Conversation Mode
    mode = models.CharField(
        max_length=20,
        choices=[
            ('general', 'General Chat'),
            ('code_assistant', 'Code Assistant'),
            ('debug_helper', 'Debug Helper'),
            ('ai_training', 'AI Training'),
            ('web3_guide', 'Web3 Guide'),
            ('canvas_expert', 'Canvas Expert'),
        ],
        default='general'
    )
    
    # Configuration
    system_prompt = models.TextField(blank=True, help_text="Custom system prompt")
    temperature = models.FloatField(
        default=0.7,
        validators=[MinValueValidator(0.0), MaxValueValidator(2.0)],
        help_text="AI temperature setting"
    )
    max_tokens = models.PositiveIntegerField(default=2048, help_text="Maximum response tokens")
    
    # Metadata
    total_messages = models.PositiveIntegerField(default=0)
    total_tokens_used = models.PositiveIntegerField(default=0)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_shared = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_message_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'glorious_ai_conversations'
        ordering = ['-last_message_at', '-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['ai_model', 'mode']),
            models.Index(fields=['last_message_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.display_name}"
    
    def get_absolute_url(self):
        return reverse('ai:conversation', kwargs={'pk': self.pk})


class AIMessage(models.Model):
    """
    AI Message Model - The Oracle's Wisdom
    Stores individual AI conversation messages
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(AIConversation, on_delete=models.CASCADE, related_name='messages')
    
    # Message Details
    role = models.CharField(
        max_length=20,
        choices=[
            ('user', 'User'),
            ('assistant', 'AI Assistant'),
            ('system', 'System'),
        ]
    )
    content = models.TextField(help_text="Message content")
    
    # Voice Features
    has_voice_input = models.BooleanField(default=False)
    voice_input_url = models.URLField(blank=True, help_text="Voice input recording")
    has_voice_output = models.BooleanField(default=False)
    voice_output_url = models.URLField(blank=True, help_text="Voice output audio")
    
    # AI Response Metadata
    model_used = models.CharField(max_length=50, blank=True)
    response_time = models.FloatField(null=True, help_text="Response time in seconds")
    tokens_used = models.PositiveIntegerField(default=0)
    confidence_score = models.FloatField(null=True, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    
    # Message Features
    is_code_block = models.BooleanField(default=False)
    programming_language = models.CharField(max_length=50, blank=True)
    attachments = models.JSONField(default=list, help_text="Message attachments")
    
    # Feedback & Rating
    user_rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="User rating (1-5 stars)"
    )
    user_feedback = models.TextField(blank=True, help_text="User feedback")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'glorious_ai_messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['role', 'created_at']),
        ]
    
    def __str__(self):
        preview = self.content[:100] + "..." if len(self.content) > 100 else self.content
        return f"{self.role}: {preview}"


class Notification(models.Model):
    """
    Notification Model - The Royal Messengers
    Manages user notifications and alerts
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_notifications')
    
    # Notification Details
    title = models.CharField(max_length=200, help_text="Notification title")
    message = models.TextField(help_text="Notification message")
    notification_type = models.CharField(
        max_length=30,
        choices=[
            ('project_invitation', 'Project Invitation'),
            ('project_update', 'Project Update'),
            ('chat_message', 'Chat Message'),
            ('ai_conversation', 'AI Conversation'),
            ('collaboration_request', 'Collaboration Request'),
            ('system_update', 'System Update'),
            ('achievement', 'Achievement Unlocked'),
            ('reminder', 'Reminder'),
            ('security', 'Security Alert'),
        ],
        default='system_update'
    )
    
    # Action & Links
    action_url = models.URLField(blank=True, help_text="URL for notification action")
    action_label = models.CharField(max_length=50, blank=True, help_text="Action button label")
    
    # Related Objects
    related_object_type = models.CharField(max_length=50, blank=True)
    related_object_id = models.CharField(max_length=100, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('urgent', 'Urgent'),
        ],
        default='medium'
    )
    
    # Delivery
    email_sent = models.BooleanField(default=False)
    push_sent = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'glorious_notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['notification_type', 'created_at']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} for {self.recipient.display_name}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])


class UserActivity(models.Model):
    """
    User Activity Model - The Chronicles
    Tracks user activities and engagement
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    
    # Activity Details
    activity_type = models.CharField(
        max_length=30,
        choices=[
            ('login', 'User Login'),
            ('logout', 'User Logout'),
            ('project_created', 'Project Created'),
            ('project_updated', 'Project Updated'),
            ('project_viewed', 'Project Viewed'),
            ('chat_message_sent', 'Chat Message Sent'),
            ('ai_conversation_started', 'AI Conversation Started'),
            ('collaboration_joined', 'Collaboration Joined'),
            ('profile_updated', 'Profile Updated'),
            ('achievement_unlocked', 'Achievement Unlocked'),
        ]
    )
    description = models.TextField(help_text="Activity description")
    
    # Context Data
    metadata = models.JSONField(default=dict, help_text="Activity metadata")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, help_text="Browser/client information")
    
    # Related Objects
    related_object_type = models.CharField(max_length=50, blank=True)
    related_object_id = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'glorious_user_activities'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'activity_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['activity_type', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.display_name} - {self.activity_type}"


class SystemConfiguration(models.Model):
    """
    System Configuration Model - The Royal Decrees
    Manages platform-wide settings and configurations
    """
    
    key = models.CharField(max_length=100, unique=True, help_text="Configuration key")
    value = models.JSONField(help_text="Configuration value")
    description = models.TextField(help_text="Configuration description")
    
    # Metadata
    is_public = models.BooleanField(default=False, help_text="Publicly accessible configuration")
    is_sensitive = models.BooleanField(default=False, help_text="Contains sensitive information")
    category = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General Settings'),
            ('ai', 'AI Configuration'),
            ('chat', 'Chat Settings'),
            ('security', 'Security Settings'),
            ('features', 'Feature Flags'),
            ('integrations', 'Third-party Integrations'),
        ],
        default='general'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'glorious_system_config'
        ordering = ['category', 'key']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['is_public']),
        ]
    
    def __str__(self):
        return f"{self.category}: {self.key}"
