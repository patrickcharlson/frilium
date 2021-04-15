from django.urls import include, path

from ..apps.core.conf import settings
from ..apps.topics.views import index

app_name = 'frilium'

# Register Frilium Apps
urlpatterns = [
    path('', index, name='index'),
    path('auth/', include('frilium.apps.auth.urls')),
    path('', include('frilium.apps.categories.urls')),
    path('', include('frilium.apps.posts.urls')),
    path('', include('frilium.apps.topics.urls')),
    path('', include('frilium.apps.users.urls')),
]
if settings.FRILIUM_ADMIN_PATH:
    adminpatterns = [
        path('', include('frilium.apps.admin.urls'))
    ]

    admin_prefix = f'{settings.FRILIUM_ADMIN_PATH}/'
    urlpatterns += [
        path(admin_prefix, include((adminpatterns, 'admin'), namespace='admin'))
    ]
