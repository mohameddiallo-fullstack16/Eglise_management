from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    # Dashboard
    path('', views.settings_dashboard, name='dashboard'),
    
    # Paramètres
    path('update/', views.update_settings, name='update'),
    
    # Thèmes
    path('themes/', views.theme_gallery, name='theme_gallery'),
    path('themes/<int:theme_id>/apply/', views.apply_theme, name='apply_theme'),
    
    # Aperçu couleurs
    path('colors/preview/', views.preview_colors, name='color_preview'),
]