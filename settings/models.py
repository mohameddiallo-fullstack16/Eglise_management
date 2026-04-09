"""
Modèles pour les paramètres et personnalisation de l'église
"""
from django.db import models
from django.core.validators import RegexValidator
from django.core.cache import cache
from colorfield.fields import ColorField


class ChurchSettings(models.Model):
    """
    Paramètres globaux de l'église (Singleton Pattern)
    Il ne peut y avoir qu'une seule instance de ce modèle
    """
    
    # ========== INFORMATIONS DE BASE ==========
    church_name = models.CharField(
        max_length=200,
        default="Église Manager",
        verbose_name="Nom de l'Église"
    )
    
    slogan = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Slogan/Devise",
        help_text="Ex: Une église qui transforme des vies"
    )
    
    founded_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de Fondation"
    )
    
    # ========== LOGO ET IMAGES ==========
    logo = models.ImageField(
        upload_to='church/logo/',
        blank=True,
        null=True,
        verbose_name="Logo de l'Église",
        help_text="Format PNG recommandé (500x500px)"
    )
    
    favicon = models.ImageField(
        upload_to='church/favicon/',
        blank=True,
        null=True,
        verbose_name="Favicon",
        help_text="Icône pour les onglets (32x32px)"
    )
    
    banner = models.ImageField(
        upload_to='church/banner/',
        blank=True,
        null=True,
        verbose_name="Bannière",
        help_text="Image de couverture (1920x400px)"
    )
    
    # ========== HISTOIRE DE L'ÉGLISE ==========
    history = models.TextField(
        blank=True,
        verbose_name="Histoire de l'Église",
        help_text="Racontez l'histoire et la vision de votre église"
    )
    
    vision = models.TextField(
        blank=True,
        verbose_name="Vision",
        help_text="La vision de l'église"
    )
    
    mission = models.TextField(
        blank=True,
        verbose_name="Mission",
        help_text="La mission de l'église"
    )
    
    core_values = models.TextField(
        blank=True,
        verbose_name="Valeurs Fondamentales",
        help_text="Les valeurs sur lesquelles l'église se base"
    )
    
    # ========== DIRECTION ACTUELLE ==========
    current_pastor = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Pasteur Principal",
        help_text="Nom du pasteur principal actuel"
    )
    
    pastor_since = models.DateField(
        null=True,
        blank=True,
        verbose_name="Pasteur depuis",
        help_text="Date de prise de fonction"
    )
    
    pastor_photo = models.ImageField(
        upload_to='church/leaders/',
        blank=True,
        null=True,
        verbose_name="Photo du Pasteur"
    )
    
    pastor_bio = models.TextField(
        blank=True,
        verbose_name="Biographie du Pasteur"
    )
    
    leadership_team = models.TextField(
        blank=True,
        verbose_name="Équipe de Direction",
        help_text="Liste des autres responsables (un par ligne)"
    )
    
    # ========== CONTACT ==========
    email = models.EmailField(
        blank=True,
        verbose_name="Email Principal"
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone"
    )
    
    whatsapp = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="WhatsApp"
    )
    
    address = models.TextField(
        blank=True,
        verbose_name="Adresse Complète"
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Ville"
    )
    
    country = models.CharField(
        max_length=100,
        default="Niger",
        verbose_name="Pays"
    )
    
    # ========== RÉSEAUX SOCIAUX ==========
    facebook = models.URLField(
        blank=True,
        verbose_name="Facebook"
    )
    
    instagram = models.URLField(
        blank=True,
        verbose_name="Instagram"
    )
    
    youtube = models.URLField(
        blank=True,
        verbose_name="YouTube"
    )
    
    twitter = models.URLField(
        blank=True,
        verbose_name="Twitter/X"
    )
    
    website = models.URLField(
        blank=True,
        verbose_name="Site Web"
    )
    
    # ========== PERSONNALISATION DES COULEURS ==========
    primary_color = ColorField(
        default='#4F46E5',  # Indigo
        verbose_name="Couleur Principale",
        help_text="Couleur principale de l'interface"
    )
    
    secondary_color = ColorField(
        default='#7C3AED',  # Violet
        verbose_name="Couleur Secondaire",
        help_text="Couleur secondaire/accent"
    )
    
    accent_color = ColorField(
        default='#F59E0B',  # Orange
        verbose_name="Couleur d'Accent",
        help_text="Couleur pour les éléments importants"
    )
    
    success_color = ColorField(
        default='#10B981',  # Vert
        verbose_name="Couleur de Succès"
    )
    
    danger_color = ColorField(
        default='#EF4444',  # Rouge
        verbose_name="Couleur de Danger"
    )
    
    warning_color = ColorField(
        default='#F59E0B',  # Orange
        verbose_name="Couleur d'Avertissement"
    )
    
    # ========== HORAIRES DES CULTES ==========
    sunday_service_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Culte Dimanche"
    )
    
    wednesday_service_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Réunion de Prière (Mercredi)"
    )
    
    friday_service_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Réunion Jeunesse (Vendredi)"
    )
    
    custom_services = models.TextField(
        blank=True,
        verbose_name="Autres Services",
        help_text="Autres horaires (un par ligne)"
    )
    
    # ========== PARAMÈTRES TECHNIQUES ==========
    timezone = models.CharField(
        max_length=50,
        default='Africa/Niamey',
        verbose_name="Fuseau Horaire",
        blank=True,
        null=True,
    )
    
    language = models.CharField(
        max_length=10,
        default='fr',
        choices=[
            ('fr', 'Français'),
            ('en', 'English'),
        ],
        verbose_name="Langue",
        blank=True,
        null=True,
    )
    
    enable_whatsapp_notifications = models.BooleanField(
        default=True,
        verbose_name="Activer Notifications WhatsApp"
    )
    
    enable_email_notifications = models.BooleanField(
        default=True,
        verbose_name="Activer Notifications Email"
    )
    
    # ========== MÉTADONNÉES ==========
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Modifié par"
    )
    
    class Meta:
        verbose_name = "Paramètres de l'Église"
        verbose_name_plural = "Paramètres de l'Église"
    
    def __str__(self):
        return f"Paramètres - {self.church_name}"
    
    def save(self, *args, **kwargs):
        # Assurer qu'il n'y a qu'une seule instance (Singleton)
        if not self.pk and ChurchSettings.objects.exists():
            raise ValueError("Il ne peut y avoir qu'une seule configuration d'église")
        
        super().save(*args, **kwargs)
        
        # Vider le cache après modification
        cache.delete('church_settings')
    
    @classmethod
    def get_settings(cls):
        """
        Récupérer les paramètres (avec cache)
        """
        settings = cache.get('church_settings')
        
        if settings is None:
            settings, created = cls.objects.get_or_create(
                pk=1,
                defaults={
                    'church_name': 'Église Manager',
                }
            )
            cache.set('church_settings', settings, 3600)  # Cache 1h
        
        return settings
    
    def get_colors_css(self):
        """
        Retourne les couleurs au format CSS personnalisé
        """
        return f"""
        :root {{
            --color-primary: {self.primary_color};
            --color-secondary: {self.secondary_color};
            --color-accent: {self.accent_color};
            --color-success: {self.success_color};
            --color-danger: {self.danger_color};
            --color-warning: {self.warning_color};
        }}
        """


class ThemePreset(models.Model):
    """
    Thèmes de couleurs pré-définis
    """
    name = models.CharField(max_length=100, verbose_name="Nom du Thème")
    description = models.TextField(blank=True, verbose_name="Description")
    
    primary_color = ColorField(verbose_name="Couleur Principale")
    secondary_color = ColorField(verbose_name="Couleur Secondaire")
    accent_color = ColorField(verbose_name="Couleur d'Accent")
    
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    thumbnail = models.ImageField(
        upload_to='themes/',
        blank=True,
        null=True,
        verbose_name="Aperçu"
    )
    
    class Meta:
        verbose_name = "Thème Pré-défini"
        verbose_name_plural = "Thèmes Pré-définis"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def apply_to_settings(self):
        """Appliquer ce thème aux paramètres"""
        settings = ChurchSettings.get_settings()
        settings.primary_color = self.primary_color
        settings.secondary_color = self.secondary_color
        settings.accent_color = self.accent_color
        settings.save()