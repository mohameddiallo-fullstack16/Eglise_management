import os
import sys
import django

import theme

# Ajout du chemin du projet au PYTHONPATH
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.settings')
django.setup()

# Import après la configuration de Django
from settings.models import ThemePreset

def create_themes():
    # Suppression des thèmes existants
    theme.objects.all().delete()
    
    themes = [
        {
            "name": "Classique",
            "primary_color": "#4F46E5",
            "secondary_color": "#7C3AED",
            "accent_color": "#10B981",
            "background_color": "#F9FAFB",
            "text_color": "#1F2937",
            "is_active": True
        },
        {
            "name": "Lumière Divine",
            "primary_color": "#FCD34D",
            "secondary_color": "#F59E0B",
            "accent_color": "#EF4444",
            "background_color": "#FEFCE8",
            "text_color": "#451A03"
        },
        {
            "name": "Paix Céleste",
            "primary_color": "#60A5FA",
            "secondary_color": "#38BDF8",
            "accent_color": "#F472B6",
            "background_color": "#EFF6FF",
            "text_color": "#1E40AF"
        },
        {
            "name": "Royal",
            "primary_color": "#7C3AED",
            "secondary_color": "#5B21B6",
            "accent_color": "#FBBF24",
            "background_color": "#FAF5FF",
            "text_color": "#4C1D95"
        },
        {
            "name": "Nature & Espoir",
            "primary_color": "#34D399",
            "secondary_color": "#10B981",
            "accent_color": "#FBBF24",
            "background_color": "#F0FDF4",
            "text_color": "#065F46"
        }
    ]
    
    try:
        for theme_data in themes:
            theme.objects.create(**theme_data)
        print(f"{len(themes)} thèmes créés avec succès !")
    except Exception as e:
        print(f"Erreur lors de la création des thèmes : {str(e)}")

if __name__ == "__main__":
    create_themes()