"""
Advanced Django Admin Configuration
Professional interface for AI agent management
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Avg, Count
from .models import (
    AgentProfile, UserAgentInteraction, AgentLearningData,
    AgentCapability, ConversationMemory, AgentPerformanceMetrics
)
import json


@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    """Advanced agent profile administration"""
    
    list_display = [
        'name', 'agent_type', 'intelligence_display', 'emotional_intelligence_display',
        'creativity_display', 'status_display', 'performance_summary', 'last_interaction'
    ]
    list_filter = ['agent_type', 'is_active', 'created_at']
    search_fields = ['name', 'agent_type', 'description']
    readonly_fields = ['created_at', 'performance_summary_detailed', 'capabilities_display']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'agent_type', 'description', 'is_active')
        }),
        ('Intelligence Metrics', {
            'fields': ('intelligence_level', 'emotional_intelligence', 'creativity_score',
                      'learning_rate', 'adaptation_speed'),
            'classes': ('wide',)
        }),
        ('Advanced Configuration', {
            'fields': ('personality_traits', 'capabilities_display', 'learning_model', 'version'),
            'classes': ('collapse',)
        }),
        ('Performance Analytics', {
            'fields': ('performance_summary_detailed',),
            'classes': ('wide',)
        }),
        ('System Information', {
            'fields': ('created_at', 'last_interaction'),
            'classes': ('collapse',)
        })
    )
    
    def intelligence_display(self, obj):
        """Display intelligence with color coding"""
        color = 'green' if obj.intelligence_level >= 90 else 'orange' if obj.intelligence_level >= 75 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}/100</span>',
            color, obj.intelligence_level
        )
    intelligence_display.short_description = 'Intelligence'
    
    def emotional_intelligence_display(self, obj):
        """Display emotional intelligence with color coding"""
        color = 'green' if obj.emotional_intelligence >= 85 else 'orange' if obj.emotional_intelligence >= 70 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}/100</span>',
            color, obj.emotional_intelligence
        )
    emotional_intelligence_display.short_description = 'Emotional IQ'
    
    def creativity_display(self, obj):
        """Display creativity score with visual indicator"""
        stars = '⭐' * (obj.creativity_score // 20)
        return format_html(
            '<span title="{}/100">{}</span>',
            obj.creativity_score, stars
        )
    creativity_display.short_description = 'Creativity'
    
    def status_display(self, obj):
        """Display agent status with icon"""
        if obj.is_active:
            return format_html('<span style="color: green;">🟢 Active</span>')
        else:
            return format_html('<span style="color: red;">🔴 Inactive</span>')
    status_display.short_description = 'Status'
    
    def performance_summary(self, obj):
        """Quick performance summary"""
        try:
            metrics = AgentPerformanceMetrics.objects.get(agent=obj)
            return format_html(
                '<div>📊 {:.1f}% satisfaction<br>💬 {} conversations</div>',
                metrics.user_satisfaction_score,
                metrics.total_conversations
            )
        except AgentPerformanceMetrics.DoesNotExist:
            return '📊 No data'
    performance_summary.short_description = 'Performance'
    
    def performance_summary_detailed(self, obj):
        """Detailed performance analytics"""
        try:
            metrics = AgentPerformanceMetrics.objects.get(agent=obj)
            interactions_count = UserAgentInteraction.objects.filter(agent=obj).count()
            
            return format_html(
                '''
                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px;">
                    <h4>📈 Performance Analytics</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div><strong>Total Conversations:</strong> {}</div>
                        <div><strong>User Satisfaction:</strong> {:.1f}%</div>
                        <div><strong>Average Rating:</strong> {:.1f}/5.0</div>
                        <div><strong>Task Completion:</strong> {:.1f}%</div>
                        <div><strong>Response Accuracy:</strong> {:.1f}%</div>
                        <div><strong>Learning Progress:</strong> {:.1f}%</div>
                    </div>
                    <div style="margin-top: 10px;">
                        <strong>Grade:</strong> 
                        <span style="background: {}; color: white; padding: 2px 8px; border-radius: 3px;">
                            {}
                        </span>
                    </div>
                </div>
                ''',
                interactions_count,
                metrics.user_satisfaction_score,
                metrics.average_rating,
                metrics.task_completion_rate,
                metrics.response_accuracy,
                metrics.learning_progress_score,
                '#28a745' if metrics.user_satisfaction_score >= 85 else '#ffc107' if metrics.user_satisfaction_score >= 70 else '#dc3545',
                'A+' if metrics.user_satisfaction_score >= 90 else 'A' if metrics.user_satisfaction_score >= 85 else 'B'
            )
        except AgentPerformanceMetrics.DoesNotExist:
            return format_html('<p>No performance data available.</p>')
    performance_summary_detailed.short_description = 'Detailed Performance'
    
    def capabilities_display(self, obj):
        """Display agent capabilities in a formatted way"""
        if obj.capabilities:
            capabilities_html = '<ul>'
            for capability in obj.capabilities[:10]:  # Show first 10
                capabilities_html += f'<li>{capability.replace("_", " ").title()}</li>'
            if len(obj.capabilities) > 10:
                capabilities_html += f'<li><em>... and {len(obj.capabilities) - 10} more</em></li>'
            capabilities_html += '</ul>'
            return format_html(capabilities_html)
        return 'No capabilities defined'
    capabilities_display.short_description = 'Capabilities'


@admin.register(UserAgentInteraction)
class UserAgentInteractionAdmin(admin.ModelAdmin):
    """User interaction tracking admin"""
    
    list_display = [
        'agent_name', 'user_display', 'interaction_type', 'rating_display',
        'created_at', 'feedback_preview'
    ]
    list_filter = ['interaction_type', 'feedback_rating', 'created_at', 'agent__agent_type']
    search_fields = ['agent__name', 'feedback_text']
    readonly_fields = ['created_at', 'updated_at', 'conversation_preview']
    date_hierarchy = 'created_at'
    
    def agent_name(self, obj):
        return obj.agent.name
    agent_name.short_description = 'Agent'
    
    def user_display(self, obj):
        return f'User #{obj.user_id}' if obj.user_id else 'Anonymous'
    user_display.short_description = 'User'
    
    def rating_display(self, obj):
        if obj.feedback_rating:
            stars = '⭐' * obj.feedback_rating
            return format_html('<span title="{}/5">{}</span>', obj.feedback_rating, stars)
        return '—'
    rating_display.short_description = 'Rating'
    
    def feedback_preview(self, obj):
        if obj.feedback_text:
            preview = obj.feedback_text[:50] + '...' if len(obj.feedback_text) > 50 else obj.feedback_text
            return format_html('<em>{}</em>', preview)
        return '—'
    feedback_preview.short_description = 'Feedback Preview'
    
    def conversation_preview(self, obj):
        if obj.conversation_data:
            return format_html(
                '<pre style="background: #f8f9fa; padding: 10px; border-radius: 5px; max-height: 200px; overflow-y: auto;">{}</pre>',
                json.dumps(obj.conversation_data, indent=2)
            )
        return 'No conversation data'
    conversation_preview.short_description = 'Conversation Data'


@admin.register(AgentPerformanceMetrics)
class AgentPerformanceMetricsAdmin(admin.ModelAdmin):
    """Performance metrics administration"""
    
    list_display = [
        'agent_name', 'total_conversations', 'satisfaction_display',
        'rating_display', 'completion_rate_display', 'last_updated'
    ]
    list_filter = ['last_updated', 'agent__agent_type']
    readonly_fields = ['performance_chart', 'trend_analysis']
    
    def agent_name(self, obj):
        return obj.agent.name
    agent_name.short_description = 'Agent'
    
    def satisfaction_display(self, obj):
        color = 'green' if obj.user_satisfaction_score >= 85 else 'orange' if obj.user_satisfaction_score >= 70 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color, obj.user_satisfaction_score
        )
    satisfaction_display.short_description = 'Satisfaction'
    
    def rating_display(self, obj):
        stars = '⭐' * int(obj.average_rating)
        return format_html(
            '<span title="{:.2f}/5.0">{}</span>',
            obj.average_rating, stars
        )
    rating_display.short_description = 'Avg Rating'
    
    def completion_rate_display(self, obj):
        return f'{obj.task_completion_rate:.1f}%'
    completion_rate_display.short_description = 'Completion Rate'
    
    def performance_chart(self, obj):
        """Visual performance representation"""
        metrics = [
            ('Satisfaction', obj.user_satisfaction_score, '#28a745'),
            ('Accuracy', obj.response_accuracy, '#17a2b8'),
            ('Learning', obj.learning_progress_score, '#ffc107'),
            ('Creativity', obj.creativity_rating, '#6f42c1'),
            ('Adaptability', obj.adaptability_score, '#fd7e14')
        ]
        
        chart_html = '<div style="background: white; padding: 15px; border-radius: 5px;">'
        chart_html += '<h4>Performance Metrics</h4>'
        
        for metric, value, color in metrics:
            bar_width = max(1, value)  # Minimum 1% for visibility
            chart_html += f'''
                <div style="margin: 5px 0;">
                    <span style="display: inline-block; width: 100px;">{metric}:</span>
                    <div style="display: inline-block; width: 200px; background: #e9ecef; border-radius: 3px;">
                        <div style="width: {bar_width}%; background: {color}; height: 20px; border-radius: 3px; position: relative;">
                            <span style="position: absolute; right: 5px; line-height: 20px; color: white; font-size: 12px;">
                                {value:.1f}%
                            </span>
                        </div>
                    </div>
                </div>
            '''
        
        chart_html += '</div>'
        return format_html(chart_html)
    performance_chart.short_description = 'Performance Visualization'
    
    def trend_analysis(self, obj):
        """Performance trend analysis"""
        # This would typically involve historical data analysis
        # For now, we'll provide a simplified analysis
        overall_score = (
            obj.user_satisfaction_score + obj.response_accuracy + 
            obj.learning_progress_score + obj.creativity_rating + obj.adaptability_score
        ) / 5
        
        if overall_score >= 85:
            trend_icon = '📈'
            trend_text = 'Excellent Performance'
            trend_color = 'green'
        elif overall_score >= 70:
            trend_icon = '📊'
            trend_text = 'Good Performance'
            trend_color = 'orange'
        else:
            trend_icon = '📉'
            trend_text = 'Needs Improvement'
            trend_color = 'red'
        
        return format_html(
            '<div style="color: {}; font-weight: bold;">{} {}</div>',
            trend_color, trend_icon, trend_text
        )
    trend_analysis.short_description = 'Performance Trend'


@admin.register(AgentCapability)
class AgentCapabilityAdmin(admin.ModelAdmin):
    """Agent capability management"""
    
    list_display = ['agent_name', 'capability_type', 'proficiency_display', 'last_assessed']
    list_filter = ['capability_type', 'last_assessed']
    search_fields = ['agent__name', 'capability_type']
    
    def agent_name(self, obj):
        return obj.agent.name
    agent_name.short_description = 'Agent'
    
    def proficiency_display(self, obj):
        """Display proficiency with progress bar"""
        percentage = obj.proficiency_level * 10
        color = 'green' if percentage >= 80 else 'orange' if percentage >= 60 else 'red'
        
        return format_html(
            '''
            <div style="display: flex; align-items: center;">
                <div style="width: 100px; background: #e9ecef; border-radius: 3px; margin-right: 10px;">
                    <div style="width: {}%; background: {}; height: 15px; border-radius: 3px;"></div>
                </div>
                <span>{:.1f}/10</span>
            </div>
            ''',
            percentage, color, obj.proficiency_level
        )
    proficiency_display.short_description = 'Proficiency'


@admin.register(ConversationMemory)
class ConversationMemoryAdmin(admin.ModelAdmin):
    """Conversation memory management"""
    
    list_display = ['agent_name', 'memory_type', 'importance_display', 'created_at', 'memory_preview']
    list_filter = ['memory_type', 'importance_score', 'created_at']
    search_fields = ['agent__name', 'memory_content']
    readonly_fields = ['memory_content_display']
    
    def agent_name(self, obj):
        return obj.agent.name
    agent_name.short_description = 'Agent'
    
    def importance_display(self, obj):
        """Display importance with visual indicator"""
        if obj.importance_score >= 0.8:
            return format_html('<span style="color: red;">🔥 Critical</span>')
        elif obj.importance_score >= 0.6:
            return format_html('<span style="color: orange;">⚡ High</span>')
        elif obj.importance_score >= 0.4:
            return format_html('<span style="color: blue;">📋 Medium</span>')
        else:
            return format_html('<span style="color: gray;">📝 Low</span>')
    importance_display.short_description = 'Importance'
    
    def memory_preview(self, obj):
        """Preview of memory content"""
        if obj.memory_content:
            content_str = str(obj.memory_content)
            preview = content_str[:50] + '...' if len(content_str) > 50 else content_str
            return format_html('<em>{}</em>', preview)
        return '—'
    memory_preview.short_description = 'Preview'
    
    def memory_content_display(self, obj):
        """Full memory content display"""
        if obj.memory_content:
            return format_html(
                '<pre style="background: #f8f9fa; padding: 10px; border-radius: 5px; max-height: 300px; overflow-y: auto;">{}</pre>',
                json.dumps(obj.memory_content, indent=2)
            )
        return 'No memory content'
    memory_content_display.short_description = 'Memory Content'


@admin.register(AgentLearningData)
class AgentLearningDataAdmin(admin.ModelAdmin):
    """Learning data administration"""
    
    list_display = ['agent_name', 'learning_type', 'success_display', 'improvement_display', 'created_at']
    list_filter = ['learning_type', 'created_at']
    search_fields = ['agent__name', 'learning_type']
    
    def agent_name(self, obj):
        return obj.agent.name
    agent_name.short_description = 'Agent'
    
    def success_display(self, obj):
        """Display success rate with color coding"""
        percentage = obj.success_rate * 100
        color = 'green' if percentage >= 80 else 'orange' if percentage >= 60 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color, percentage
        )
    success_display.short_description = 'Success Rate'
    
    def improvement_display(self, obj):
        """Display improvement rate"""
        percentage = obj.improvement_rate * 100
        color = 'green' if percentage >= 80 else 'orange' if percentage >= 60 else 'red'
        return format_html(
            '<span style="color: {};">📈 {:.1f}%</span>',
            color, percentage
        )
    improvement_display.short_description = 'Improvement'


# Custom admin site configuration
admin.site.site_header = "DevCrown AI Agent Command Center"
admin.site.site_title = "DevCrown AI Admin"
admin.site.index_title = "AI Agent Management System"
