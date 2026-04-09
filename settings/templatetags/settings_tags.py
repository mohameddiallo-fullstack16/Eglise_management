from django import template
from settings.models import ChurchSettings

register = template.Library()

@register.simple_tag
def get_church_settings():
    """Charge les paramètres de l'église pour les templates"""
    return ChurchSettings.get_settings()
