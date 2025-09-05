# URL Configuration for Glorious Space - The Developer's Crown Jewel
# Royal Routes to Digital Excellence

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Admin Interface Customization
admin.site.site_header = "Glorious Space Administration"
admin.site.site_title = "Glorious Space Admin"
admin.site.index_title = "Welcome to the Developer's Kingdom"

urlpatterns = [
    # Royal Admin Portal
    path('admin/', admin.site.urls),
    
    # Core Application Routes - The Heart of Our Kingdom
    path('', include('hello_world.core.urls', namespace='core')),
    
    # AI Agents Management - The Crown Jewel
    path('agents/', include('backend.apps.agents.urls', namespace='agents')),
    
    # Keycloak Authentication - Royal Gateway
    path('auth/', include('hello_world.core.auth_urls', namespace='auth')),
    
    # OAuth2 Provider - Token Gateway
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    
    # Django Allauth - Social Authentication
    path('accounts/', include('allauth.urls')),
    
    # API Routes - The Digital Crown Jewels - Coming Soon
    # path('api/v1/', include('api.urls', namespace='api')),
    
    # REST Framework Browsable API
    path('api-auth/', include('rest_framework.urls')),
]

# Development-only routes
if settings.DEBUG:
    # Django Browser Reload for Hot Reloading
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    
    # Static and Media files serving in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom Error Pages - Elegant Failure Handling (TODO: Implement these views)
# handler404 = 'hello_world.core.views.custom_404'
# handler500 = 'hello_world.core.views.custom_500'
# handler403 = 'hello_world.core.views.custom_403'
# handler400 = 'hello_world.core.views.custom_400'
