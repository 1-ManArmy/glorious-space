# Admin Configuration for Glorious Space - The Royal Management
# Where Data is Governed with Majesty

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
import json

from .models import (
    CustomUser, Project, ProjectCollaboration, ChatRoom, ChatRoomMembership,
    ChatMessage, AIConversation, AIMessage, Notification, UserActivity,
    SystemConfiguration
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Enhanced User Administration - The Royal Registry
    Manage users with noble features
    """
    
    list_display = [
        'username', 'email', 'display_name', 'title', 'experience_level', 
        'reputation_score', 'is_online', 'last_active', 'is_staff'
    ]
    list_filter = [
        'experience_level', 'is_online', 'is_staff', 'is_active', 
        'theme_preference', 'date_joined'
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'title', 'company']
    ordering = ['-date_joined']
    
    # Enhanced fieldsets for royal management
    fieldsets = UserAdmin.fieldsets + (
        ('Royal Profile', {
            'fields': ('bio', 'avatar', 'location', 'website', 'title', 'company')
        }),
        ('Professional Details', {
            'fields': ('skills', 'experience_level', 'github_username', 'linkedin_url', 'twitter_handle', 'discord_username')
        }),
        ('Royal Preferences', {
            'fields': ('theme_preference', 'notification_preferences', 'privacy_settings')
        }),
        ('Kingdom Statistics', {
            'fields': ('reputation_score', 'total_projects', 'total_contributions', 'badges', 'certifications'),
            'classes': ('collapse',)
        }),
        ('Activity Tracking', {
            'fields': ('last_active', 'is_online'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['last_active', 'total_projects', 'total_contributions']
    
    def display_name(self, obj):
        return obj.display_name
    display_name.short_description = 'Display Name'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Project Administration - The Royal Workshop
    Manage digital masterpieces
    """
    
    list_display = [
        'title', 'owner', 'category', 'status', 'visibility', 'is_featured',
        'view_count', 'like_count', 'created_at'
    ]
    list_filter = [
        'category', 'status', 'visibility', 'is_featured', 'allow_collaboration',
        'created_at', 'updated_at'
    ]
    search_fields = ['title', 'description', 'owner__username', 'tech_stack']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Project Essence', {
            'fields': ('title', 'slug', 'description', 'owner')
        }),
        ('Technical Details', {
            'fields': ('tech_stack', 'category', 'repository_url', 'live_demo_url', 'documentation_url')
        }),
        ('Visual Identity', {
            'fields': ('thumbnail', 'gallery_images', 'demo_video_url')
        }),
        ('Project Management', {
            'fields': ('status', 'visibility', 'is_featured', 'allow_collaboration')
        }),
        ('Engagement Metrics', {
            'fields': ('view_count', 'like_count', 'fork_count', 'download_count'),
            'classes': ('collapse',)
        }),
        ('SEO & Discovery', {
            'fields': ('tags', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['view_count', 'like_count', 'fork_count', 'download_count']
    prepopulated_fields = {'slug': ('title',)}
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner')


@admin.register(ProjectCollaboration)
class ProjectCollaborationAdmin(admin.ModelAdmin):
    """
    Project Collaboration Administration - The Royal Court
    Manage collaborative relationships
    """
    
    list_display = ['project', 'collaborator', 'role', 'joined_at', 'invitation_accepted_at']
    list_filter = ['role', 'joined_at', 'invitation_accepted_at']
    search_fields = ['project__title', 'collaborator__username']
    ordering = ['-joined_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project', 'collaborator')


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    """
    Chat Room Administration - The Communication Chambers
    Manage royal communication spaces
    """
    
    list_display = [
        'name', 'room_type', 'owner', 'member_count', 'message_count',
        'last_activity', 'created_at'
    ]
    list_filter = ['room_type', 'allow_voice_chat', 'allow_video_chat', 'is_moderated']
    search_fields = ['name', 'description', 'owner__username']
    ordering = ['-last_activity']
    
    fieldsets = (
        ('Chamber Details', {
            'fields': ('name', 'slug', 'description', 'room_type', 'owner')
        }),
        ('Chamber Settings', {
            'fields': ('max_members', 'allow_voice_chat', 'allow_video_chat', 'allow_file_sharing', 'is_moderated')
        }),
        ('Activity Metrics', {
            'fields': ('last_activity', 'message_count'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['last_activity', 'message_count']
    prepopulated_fields = {'slug': ('name',)}
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner').prefetch_related('members')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """
    Chat Message Administration - The Royal Scrolls
    Manage communication history
    """
    
    list_display = [
        'sender', 'room', 'message_preview', 'message_type', 
        'is_edited', 'is_pinned', 'created_at'
    ]
    list_filter = ['message_type', 'is_edited', 'is_pinned', 'created_at']
    search_fields = ['content', 'sender__username', 'room__name']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Message Details', {
            'fields': ('room', 'sender', 'content', 'message_type')
        }),
        ('Attachments', {
            'fields': ('attachment_url', 'attachment_metadata'),
            'classes': ('collapse',)
        }),
        ('Message Features', {
            'fields': ('reply_to', 'is_edited', 'edit_history', 'reactions', 'is_pinned'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['edit_history', 'reactions']
    
    def message_preview(self, obj):
        preview = obj.content[:100] + "..." if len(obj.content) > 100 else obj.content
        return preview
    message_preview.short_description = 'Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('sender', 'room', 'reply_to')


@admin.register(AIConversation)
class AIConversationAdmin(admin.ModelAdmin):
    """
    AI Conversation Administration - The Oracle Sessions
    Manage AI conversation sessions
    """
    
    list_display = [
        'title', 'user', 'ai_model', 'mode', 'total_messages',
        'is_active', 'last_message_at', 'created_at'
    ]
    list_filter = ['ai_model', 'mode', 'is_active', 'is_shared', 'created_at']
    search_fields = ['title', 'user__username', 'system_prompt']
    ordering = ['-last_message_at', '-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Conversation Details', {
            'fields': ('title', 'user', 'ai_model', 'mode')
        }),
        ('AI Configuration', {
            'fields': ('system_prompt', 'temperature', 'max_tokens'),
            'classes': ('collapse',)
        }),
        ('Session Metrics', {
            'fields': ('total_messages', 'total_tokens_used', 'estimated_cost'),
            'classes': ('collapse',)
        }),
        ('Status & Sharing', {
            'fields': ('is_active', 'is_shared'),
        }),
    )
    
    readonly_fields = ['total_messages', 'total_tokens_used', 'estimated_cost']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(AIMessage)
class AIMessageAdmin(admin.ModelAdmin):
    """
    AI Message Administration - The Oracle's Wisdom
    Manage AI conversation messages
    """
    
    list_display = [
        'conversation', 'role', 'message_preview', 'model_used',
        'response_time', 'user_rating', 'created_at'
    ]
    list_filter = ['role', 'model_used', 'has_voice_input', 'has_voice_output', 'is_code_block']
    search_fields = ['content', 'conversation__title', 'conversation__user__username']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Message Details', {
            'fields': ('conversation', 'role', 'content')
        }),
        ('Voice Features', {
            'fields': ('has_voice_input', 'voice_input_url', 'has_voice_output', 'voice_output_url'),
            'classes': ('collapse',)
        }),
        ('AI Metadata', {
            'fields': ('model_used', 'response_time', 'tokens_used', 'confidence_score'),
            'classes': ('collapse',)
        }),
        ('Code Analysis', {
            'fields': ('is_code_block', 'programming_language', 'attachments'),
            'classes': ('collapse',)
        }),
        ('User Feedback', {
            'fields': ('user_rating', 'user_feedback'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['response_time', 'tokens_used', 'confidence_score']
    
    def message_preview(self, obj):
        preview = obj.content[:100] + "..." if len(obj.content) > 100 else obj.content
        return preview
    message_preview.short_description = 'Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('conversation', 'conversation__user')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Notification Administration - The Royal Messengers
    Manage user notifications
    """
    
    list_display = [
        'title', 'recipient', 'notification_type', 'priority',
        'is_read', 'created_at', 'read_at'
    ]
    list_filter = ['notification_type', 'priority', 'is_read', 'is_archived', 'email_sent', 'push_sent']
    search_fields = ['title', 'message', 'recipient__username', 'sender__username']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('title', 'message', 'notification_type', 'recipient', 'sender')
        }),
        ('Action & Navigation', {
            'fields': ('action_url', 'action_label'),
            'classes': ('collapse',)
        }),
        ('Related Objects', {
            'fields': ('related_object_type', 'related_object_id'),
            'classes': ('collapse',)
        }),
        ('Status & Priority', {
            'fields': ('priority', 'is_read', 'is_archived')
        }),
        ('Delivery Status', {
            'fields': ('email_sent', 'push_sent'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'read_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'read_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('recipient', 'sender')


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """
    User Activity Administration - The Royal Chronicles
    Track user engagement and actions
    """
    
    list_display = [
        'user', 'activity_type', 'activity_preview', 'ip_address', 'created_at'
    ]
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__username', 'description', 'activity_type']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Activity Details', {
            'fields': ('user', 'activity_type', 'description')
        }),
        ('Context Information', {
            'fields': ('metadata', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Related Objects', {
            'fields': ('related_object_type', 'related_object_id'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']
    
    def activity_preview(self, obj):
        preview = obj.description[:100] + "..." if len(obj.description) > 100 else obj.description
        return preview
    activity_preview.short_description = 'Description'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    """
    System Configuration Administration - The Royal Decrees
    Manage platform-wide settings
    """
    
    list_display = ['key', 'category', 'description_preview', 'is_public', 'is_sensitive', 'updated_at']
    list_filter = ['category', 'is_public', 'is_sensitive', 'created_at']
    search_fields = ['key', 'description', 'category']
    ordering = ['category', 'key']
    
    fieldsets = (
        ('Configuration Details', {
            'fields': ('key', 'value', 'description', 'category')
        }),
        ('Access Control', {
            'fields': ('is_public', 'is_sensitive')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def description_preview(self, obj):
        preview = obj.description[:100] + "..." if len(obj.description) > 100 else obj.description
        return preview
    description_preview.short_description = 'Description'
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'value':
            kwargs['widget'] = admin.widgets.AdminTextareaWidget(attrs={'rows': 10, 'cols': 80})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


# Admin Site Customization - Royal Branding
admin.site.site_header = "Glorious Space - Royal Administration"
admin.site.site_title = "Glorious Space Admin"
admin.site.index_title = "Welcome to the Digital Kingdom Management"

# Register remaining models with basic admin
admin.site.register(ChatRoomMembership)
