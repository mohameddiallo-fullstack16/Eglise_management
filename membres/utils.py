from io import BytesIO
import os
from django.conf import settings
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from PIL import Image, ImageDraw
import qrcode


def generate_qr_code(data):
    """Génère un QR code optimisé"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#2563eb", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer


def create_circular_photo(photo_path, size=80):
    """
    Crée une photo circulaire nette avec bordure.
    
    CORRECTIF FLOU : on travaille en résolution 2× (size * SCALE) puis on
    sauvegarde à cette résolution — ReportLab se charge de réduire proprement
    à l'affichage, ce qui évite l'effet de flou par upscaling.
    """
    SCALE = 2  # facteur de sur-échantillonnage
    render_size = size * SCALE

    try:
        img = Image.open(photo_path).convert("RGBA")

        # ── Recadrage carré centré ──────────────────────────────────────────
        min_side = min(img.size)
        left = (img.width - min_side) // 2
        top  = (img.height - min_side) // 2
        img  = img.crop((left, top, left + min_side, top + min_side))

        # ── Redimensionnement HAUTE RÉSOLUTION ─────────────────────────────
        img = img.resize((render_size, render_size), Image.Resampling.LANCZOS)

        # ── Masque circulaire en haute résolution ───────────────────────────
        mask = Image.new('L', (render_size, render_size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, render_size, render_size), fill=255)

        # ── Composition finale ─────────────────────────────────────────────
        output = Image.new('RGBA', (render_size, render_size), (255, 255, 255, 0))
        output.paste(img, (0, 0), mask)

        buffer = BytesIO()
        output.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer
    except Exception:
        return None


def generate_member_card(member, include_photo=True, include_qr=True):
    """
    Carte de membre professionnelle avec design épuré
    Format: 350×220 px (équivalent CR80)
    """

    # ── Configuration ──────────────────────────────────────────────────────
    card_width, card_height = 350, 220

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(card_width, card_height))

    church_config  = getattr(settings, 'CHURCH_CONFIG', {})
    primary_color  = HexColor(church_config.get('PRIMARY_COLOR', '#2563eb'))

    # ── Fond blanc + bordure ───────────────────────────────────────────────
    c.setFillColor(HexColor('#FFFFFF'))
    c.rect(0, 0, card_width, card_height, fill=1, stroke=0)

    c.setStrokeColor(HexColor('#e5e7eb'))
    c.setLineWidth(2)
    c.rect(0, 0, card_width, card_height, fill=0, stroke=1)

    # ── Bande supérieure colorée ───────────────────────────────────────────
    header_height = 60
    c.setFillColor(primary_color)
    c.rect(0, card_height - header_height, card_width, header_height, fill=1, stroke=0)

    # Logo église
    logo_path = os.path.join(settings.MEDIA_ROOT, church_config.get('LOGO_PATH', ''))
    logo_size = 35
    if os.path.exists(logo_path):
        try:
            logo_img = Image.open(logo_path).convert("RGBA")
            logo_img.thumbnail((logo_size * 2, logo_size * 2), Image.Resampling.LANCZOS)
            logo_buffer = BytesIO()
            logo_img.save(logo_buffer, format='PNG')
            logo_buffer.seek(0)
            c.drawImage(ImageReader(logo_buffer), 15, card_height - 50,
                        width=logo_size, height=logo_size, mask='auto')
        except Exception:
            pass

    # Nom de l'église
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(HexColor('#FFFFFF'))
    church_name = church_config.get('NAME', 'Église')
    c.drawString(60, card_height - 30, church_name.upper())

    c.setFont("Helvetica", 8)
    c.drawString(60, card_height - 42, "CARTE DE MEMBRE")

    # ── Photo du membre ────────────────────────────────────────────────────
    photo_size = 80
    photo_x    = 15
    photo_y    = card_height - header_height - photo_size - 12

    if include_photo and getattr(member, 'photo', None):
        try:
            # On demande create_circular_photo à taille d'affichage ;
            # la fonction gère elle-même la résolution 2× en interne.
            photo_buffer = create_circular_photo(member.photo.path, photo_size)
            if photo_buffer:
                # Bordure circulaire
                c.setFillColor(primary_color)
                c.circle(photo_x + photo_size / 2, photo_y + photo_size / 2,
                         photo_size / 2 + 3, fill=1, stroke=0)
                # Dessin à la taille d'affichage — ReportLab réduit la 2× image
                c.drawImage(ImageReader(photo_buffer), photo_x, photo_y,
                            width=photo_size, height=photo_size, mask='auto')
            else:
                include_photo = False
        except Exception:
            include_photo = False

    if not include_photo:
        c.setFillColor(HexColor('#f3f4f6'))
        c.circle(photo_x + photo_size / 2, photo_y + photo_size / 2,
                 photo_size / 2, fill=1, stroke=0)
        c.setStrokeColor(HexColor('#d1d5db'))
        c.setLineWidth(2)
        c.circle(photo_x + photo_size / 2, photo_y + photo_size / 2,
                 photo_size / 2, fill=0, stroke=1)

    # ── Zone infos (droite de la photo) ────────────────────────────────────
    info_x         = photo_x + photo_size + 12
    info_y_start   = photo_y + photo_size - 8
    max_info_width = card_width - info_x - 80   # réserve la place du QR

    # CORRECTIF CHEVAUCHEMENT : plancher absolu pour info_y
    # Le footer occupe les 25 premiers points → on s'arrête à 28 pour respirer.
    MIN_INFO_Y = 28



    def draw_field(label, value, y):
        """Dessine une paire label/valeur et retourne le y suivant,
        ou None si on est hors zone."""
        if y < MIN_INFO_Y:
            return None
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(HexColor('#374151'))
        c.drawString(info_x, y, label)
        c.setFont("Helvetica", 7.5)
        label_width = c.stringWidth(label, "Helvetica-Bold", 7.5)
        c.drawString(info_x + label_width + 5, y, value)
        return y - 11   

    # Nom complet
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(HexColor('#111827'))
    full_name = f"{member.first_name} {member.last_name}".upper()
    if len(full_name) > 25:
        full_name = full_name[:22] + ".."
    c.drawString(info_x, info_y_start, full_name)

    # ID Membre
    info_y = info_y_start - 14
    c.setFont("Helvetica", 8)
    c.setFillColor(HexColor('#6b7280'))
    c.drawString(info_x, info_y, f"ID: {member.member_id}")

    # Ligne séparatrice
    info_y -= 7
    c.setStrokeColor(HexColor('#e5e7eb'))
    c.setLineWidth(0.8)
    c.line(info_x, info_y, info_x + max_info_width, info_y)
    info_y -= 10

    # ── Champs détaillés — chacun vérifie la borne avant d'écrire ─────────

    # Famille
    if info_y and getattr(member, 'family', None):
        info_y = draw_field("Famille:", member.family.name[:20], info_y)

    # Situation matrimoniale
    if info_y and getattr(member, 'marital_status', None):
        info_y = draw_field("Situation:", member.get_marital_status_display()[:20], info_y)

    # Ministères (2 max)
    if info_y and hasattr(member, 'ministries'):
        ministries = member.ministries.all()
        if ministries.exists():
            names = ", ".join(m.name for m in ministries[:2])
            if len(names) > 25:
                names = names[:22] + ".."
            info_y = draw_field("Ministere:", names, info_y)

    # Groupes (2 max)
    if info_y and hasattr(member, 'groups'):
        groups = member.groups.all()
        if groups.exists():
            names = ", ".join(g.name for g in groups[:2])
            if len(names) > 25:
                names = names[:22] + ".."
            info_y = draw_field("Groupe:", names, info_y)

    # Baptême
    if info_y and getattr(member, 'baptism_date', None):
        info_y = draw_field("Bapteme:", member.baptism_date.strftime('%d/%m/%Y'), info_y)

    # Membre depuis
    if info_y and getattr(member, 'membership_date', None):
        info_y = draw_field("Membre depuis:", member.membership_date.strftime('%d/%m/%Y'), info_y)

    # Téléphone
    if info_y and getattr(member, 'phone', None):
        c.setFillColor(HexColor('#6b7280'))
        draw_field("Telephone:", member.phone, info_y)

    # ── QR Code ────────────────────────────────────────────────────────────
    if include_qr:
        qr_size = 65
        qr_x    = card_width - qr_size - 10
        qr_y    = photo_y + 8

        # Cadre
        c.setFillColor(HexColor('#f9fafb'))
        c.roundRect(qr_x - 4, qr_y - 4, qr_size + 8, qr_size + 8, 6, fill=1, stroke=0)
        c.setStrokeColor(HexColor('#e5e7eb'))
        c.setLineWidth(0.8)
        c.roundRect(qr_x - 4, qr_y - 4, qr_size + 8, qr_size + 8, 6, fill=0, stroke=1)

        qr_data   = f"https://votre-eglise.com/membre/{member.id}"
        qr_buffer = generate_qr_code(qr_data)
        c.drawImage(ImageReader(qr_buffer), qr_x, qr_y, width=qr_size, height=qr_size)

    # ── Footer ─────────────────────────────────────────────────────────────
    footer_y = 10

    c.setStrokeColor(HexColor('#e5e7eb'))
    c.setLineWidth(0.8)
    c.line(15, footer_y + 8, card_width - 15, footer_y + 8)

    c.setFont("Helvetica", 6.5)
    c.setFillColor(HexColor('#9ca3af'))
    c.drawString(15, footer_y, f"Emise le {timezone.now().strftime('%d/%m/%Y')}")
    c.drawRightString(card_width - 15, footer_y, "Valable 12 mois")

    c.save()
    buffer.seek(0)
    return buffer