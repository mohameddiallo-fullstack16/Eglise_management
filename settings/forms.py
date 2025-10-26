from django import forms
from .models import ChurchSettings

class ChurchSettingsForm(forms.ModelForm):
    """Formulaire pour les paramètres de l'église"""
    
    class Meta:
        model = ChurchSettings
        fields = [
            # Informations de base
            'church_name', 'slogan', 'founded_date',
            
            # Images
            'logo', 'banner',
            
            # Histoire
            'history', 'vision', 'mission', 'core_values',
            
            # Direction
            'current_pastor', 'pastor_since', 'pastor_photo', 
            'pastor_bio', 'leadership_team',
            
            # Contact
            'email', 'phone', 'whatsapp', 'address', 'city', 'country',
            
            # Réseaux sociaux
            'facebook', 'instagram', 'youtube', 'twitter', 'website',
            
            # Couleurs
            'primary_color', 'secondary_color', 'accent_color',
            'success_color', 'danger_color', 'warning_color',
            
            # Horaires
            'sunday_service_time', 'wednesday_service_time', 
            'friday_service_time', 'custom_services',
            
            # Techniques
            'timezone', 'language', 
            'enable_whatsapp_notifications', 'enable_email_notifications',
        ]
        
        widgets = {
            'church_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Nom de votre église'
            }),
            'slogan': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Ex: Une église qui transforme des vies'
            }),
            'founded_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'history': forms.Textarea(attrs={
                'rows': 6,
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Racontez l\'histoire de votre église...'
            }),
            'vision': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Quelle est votre vision ?'
            }),
            'mission': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Quelle est votre mission ?'
            }),
            'core_values': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Liste des valeurs fondamentales...'
            }),
            'current_pastor': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Nom du pasteur principal'
            }),
            'pastor_since': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'pastor_bio': forms.Textarea(attrs={
                'rows': 5,
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Biographie du pasteur...'
            }),
            'leadership_team': forms.Textarea(attrs={
                'rows': 5,
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Liste des responsables (un par ligne)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'contact@eglise.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': '+227 XX XX XX XX'
            }),
            'whatsapp': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': '+227 XX XX XX XX'
            }),
            'address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Adresse complète'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Niamey'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Niger'
            }),
            'facebook': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'https://facebook.com/votre-page'
            }),
            'instagram': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'https://instagram.com/votre-compte'
            }),
            'youtube': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'https://youtube.com/@votre-chaine'
            }),
            'twitter': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'https://twitter.com/votre-compte'
            }),
            'website': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'https://votre-site.com'
            }),
            'sunday_service_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'wednesday_service_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'friday_service_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'custom_services': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Samedi 15h: École du dimanche\nJeudi 18h: Intercession'
            }),
            'timezone': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'language': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'primary_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'w-full h-10 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'value': '#000000'  # Valeur par défaut pour l'input color
            }),
            'secondary_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'w-full h-10 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'value': '#000000'
            }),
            'accent_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'w-full h-10 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'value': '#000000'
            }),
            'success_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'w-full h-10 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'value': '#000000'
            }),
            'danger_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'w-full h-10 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'value': '#000000'
            }),
            'warning_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'w-full h-10 border rounded-lg focus:ring-2 focus:ring-blue-500',
                'value': '#000000'
            }),
            'enable_whatsapp_notifications': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-blue-600 focus:ring-blue-500'
            }),
            'enable_email_notifications': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-blue-600 focus:ring-blue-500'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pré-remplir les valeurs des champs de couleur si elles existent
        if self.instance.pk:
            self.fields['primary_color'].initial = self.instance.primary_color or '#000000'
            self.fields['secondary_color'].initial = self.instance.secondary_color or '#000000'
            self.fields['accent_color'].initial = self.instance.accent_color or '#000000'
            self.fields['success_color'].initial = self.instance.success_color or '#000000'
            self.fields['danger_color'].initial = self.instance.danger_color or '#000000'
            self.fields['warning_color'].initial = self.instance.warning_color or '#000000'
            
