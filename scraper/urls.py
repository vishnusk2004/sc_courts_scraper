from django.urls import path
from . import views

app_name = 'scraper'

urlpatterns = [
    path('', views.home, name='home'),
    path('start-scraping/', views.start_scraping, name='start_scraping'),
    path('sessions/', views.sessions_list, name='sessions_list'),
    path('session/<str:session_id>/', views.session_detail, name='session_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # API endpoints
    path('api/start-scraping/', views.api_start_scraping, name='api_start_scraping'),
    path('api/session/<str:session_id>/status/', views.api_session_status, name='api_session_status'),
    path('api/session/<str:session_id>/data/', views.api_session_data, name='api_session_data'),
]
