from settings.models import ChurchSettings

def church_settings_processor(request):
    """
    Ajoute les paramètres de l'église dans tous les templates
    """
    settings = ChurchSettings.get_settings()
    
    return {
        'church_settings': settings,
        'church_name': settings.church_name,
        'church_logo': settings.logo,
        'church_colors': {
            'primary': settings.primary_color,
            'secondary': settings.secondary_color,
            'accent': settings.accent_color,
            'success': settings.success_color,
            'danger': settings.danger_color,
            'warning': settings.warning_color,
        }
    }


def site_info(request):
    """
    Informations générales du site disponibles partout
    """
    return {
        'site_description': 'Plateforme de gestion d\'église',
        'current_year': 2024,
    }