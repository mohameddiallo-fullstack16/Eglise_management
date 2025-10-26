# settings_app/context_processors.py

from .models import ChurchSettings

def church_settings(request):
    """
    Ajoute automatiquement les paramètres de l'église (couleurs, logo, etc.)
    dans le contexte de tous les templates.
    """
    try:
        settings = ChurchSettings.objects.first()
    except ChurchSettings.DoesNotExist:
        settings = None

    return {
        'church_settings': settings
    }
