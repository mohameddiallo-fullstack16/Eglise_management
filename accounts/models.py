from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur principal'),
        ('secretary', 'Secrétaire'),  # Corrigé l'accent
        ('treasurer', 'Trésorier'),   # Corrigé l'accent
        ('leader', 'Responsable de groupe'),
        ('membre', 'Membre'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='membre',
        verbose_name="Rôle de l'utilisateur"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Numéro de téléphone"
    )
    is_active_membre = models.BooleanField(
        default=True,
        verbose_name="Membre actif"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"  # Corrigé l'accent
    )
    is_validated = models.BooleanField(default=False, verbose_name="Compte validé")

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.get_full_name()} - {self.get_role_display()}"

    # Vérifie si l'utilisateur a accès admin
    def has_admin_access(self):
        if self.is_superuser:  # Superuser Django natif
            return True
        return self.role in ['admin']

    # Vérifie si l'utilisateur a accès finance
    def has_finance_access(self):
        if self.is_superuser:
            return True
        return self.role in ['admin', 'treasurer']

    # Vérifie si l'utilisateur peut gérer les membres (corrigé le nom)
    def has_membres_management_access(self):
        if self.is_superuser:
            return True
        return self.role in ['admin', 'secretary', 'leader']
    

# models.py
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_codes')
    code = models.CharField(max_length=6)  # 6 chiffres
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    max_attempts = models.PositiveSmallIntegerField(default=5)
    used = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['token']),
            models.Index(fields=['expires_at']),
        ]
        verbose_name = "Code de réinitialisation"
        verbose_name_plural = "Codes de réinitialisation"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def can_attempt(self):
        return not self.used and self.attempts < self.max_attempts and not self.is_expired()

    def increment_attempt(self):
        self.attempts += 1
        self.save(update_fields=['attempts'])

    def mark_used(self):
        self.used = True
        self.save(update_fields=['used'])

    def __str__(self):
        return f"Code {self.code} pour {self.user.email}"
    

    