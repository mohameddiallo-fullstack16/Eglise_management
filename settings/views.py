from venv import logger
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import ChurchSettings, ThemePreset
from .forms import ChurchSettingsForm


class AdminRequiredMixin(UserPassesTestMixin):
    """Vérifie les droits d'administration"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.has_admin_access()


@login_required
def settings_dashboard(request):
    """Tableau de bord des paramètres"""
    if not request.user.has_admin_access():
        messages.error(request, "Accès non autorisé.")
        return redirect('dashboard')
    
    settings = ChurchSettings.get_settings()
    
    context = {
        'settings': settings,
    }
    return render(request, 'settings/dashboard.html', context)


@login_required
def update_settings(request):
    """Mettre à jour les paramètres de l'église"""
    if not request.user.has_admin_access():
        messages.error(request, "Accès non autorisé.")
        return redirect('settings:dashboard')
    
    settings = ChurchSettings.get_settings()
    
    if request.method == 'POST':
        form = ChurchSettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            try:
                settings = form.save(commit=False)
                settings.updated_by = request.user
                settings.save()
                messages.success(request, '✅ Paramètres mis à jour avec succès !')
                logger.info("Paramètres mis à jour par %s", request.user.username)
                return redirect('settings:dashboard')
            except ValidationError as e:
                messages.error(request, f"Erreur de validation : {str(e)}")
                logger.error("Validation error in update_settings: %s", str(e))
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {str(e)}")
                logger.error("Unexpected error in update_settings: %s", str(e))
        else:
            messages.error(request, "Le formulaire contient des erreurs. Veuillez vérifier les champs.")
            for field, errors in form.errors.items():
                logger.error("Form error in %s: %s", field, errors)
    else:
        form = ChurchSettingsForm(instance=settings)
    
    context = {
        'form': form,
        'settings': settings,
    }
    return render(request, 'settings/update_settings.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.cache import cache
from .models import ThemePreset, ChurchSettings

@login_required
def theme_gallery(request):
    themes = ThemePreset.objects.all()
    context = {
        'themes': themes,
        'settings': ChurchSettings.get_settings(),
    }
    return render(request, 'settings/theme_gallery.html', context)


@login_required
def apply_theme(request, theme_id):
    """Appliquer un thème pré-défini"""
    if not request.user.has_admin_access():
        messages.error(request, "Accès non autorisé.")
        return redirect('settings:dashboard')
    
    try:
        theme = ThemePreset.objects.get(pk=theme_id)
        if theme.is_active:
            settings = ChurchSettings.get_settings()
            settings.primary_color = theme.primary_color
            settings.secondary_color = theme.secondary_color
            settings.accent_color = theme.accent_color

            settings.save()
            cache.delete('church_settings')  # Vide le cache pour refresh immédiat
            messages.success(request, f'✅ Thème "{theme.name}" appliqué ! Rechargez la page pour voir les changements.')
        else:
            messages.error(request, "Ce thème est désactivé.")
    except ThemePreset.DoesNotExist:
        messages.error(request, 'Thème introuvable.')
    
    return redirect('settings:theme_gallery')


@login_required
def preview_colors(request):
    """Aperçu en temps réel des couleurs"""
    if not request.user.has_admin_access():
        messages.error(request, "Accès non autorisé.")
        return redirect('dashboard')
    
    settings = ChurchSettings.get_settings()
    
    # Récupérer les couleurs du POST ou utiliser les actuelles
    primary = request.GET.get('primary', settings.primary_color)
    secondary = request.GET.get('secondary', settings.secondary_color)
    accent = request.GET.get('accent', settings.accent_color)
    
    context = {
        'settings': settings,
        'preview_primary': primary,
        'preview_secondary': secondary,
        'preview_accent': accent,
    }
    return render(request, 'settings/color_preview.html', context)

