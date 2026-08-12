import os
import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, get_available_image_extensions
from django.db import models
from django.utils.translation import gettext_lazy as _

# SVG ichida skript ishlashiga yo'l qo'ymaydigan tekshiruv: yuklangan fayl
# MEDIA_URL orqali to'g'ridan-to'g'ri ochilganda XSS bo'lib ketmasligi uchun.
DANGEROUS_SVG_CONTENT = re.compile(
    rb'<\s*script'          # <script>
    rb'|<\s*foreignObject'  # ichiga HTML joylash
    rb'|javascript\s*:'     # href="javascript:..."
    rb'|\son\w+\s*=',       # onload=, onclick=, ...
    re.IGNORECASE,
)

SVG_READ_LIMIT = 5 * 1024 * 1024


def validate_image_and_svg_file_extension(value):
    allowed = list(get_available_image_extensions()) + ['svg']
    return FileExtensionValidator(allowed_extensions=allowed)(value)


def is_svg_upload(data):
    name = getattr(data, 'name', '') or ''
    return os.path.splitext(name)[1].lower() == '.svg'


def validate_svg(data):
    """SVG faylning haqiqiy SVG ekanini va xavfsizligini tekshiradi."""
    if data.size and data.size > SVG_READ_LIMIT:
        raise ValidationError(_('SVG file is too large (max 5 MB).'), code='invalid_svg')

    data.seek(0)
    content = data.read()
    data.seek(0)

    if b'<svg' not in content.lower():
        raise ValidationError(
            _('Upload a valid SVG file. The file you uploaded was either not an SVG or a corrupted one.'),
            code='invalid_svg',
        )
    if DANGEROUS_SVG_CONTENT.search(content):
        raise ValidationError(
            _('This SVG contains scripts or event handlers and cannot be uploaded.'),
            code='unsafe_svg',
        )


class SVGAndImageFormField(forms.ImageField):
    """SVG'ni ham, oddiy rasm formatlarini ham qabul qiladigan form maydoni."""

    default_validators = [validate_image_and_svg_file_extension]

    def to_python(self, data):
        if not data or not is_svg_upload(data):
            # Odatdagi rasm: Pillow tekshiruvi o'z holicha ishlaydi.
            return super().to_python(data)

        f = forms.FileField.to_python(self, data)
        if f is None:
            return None
        validate_svg(f)
        f.content_type = 'image/svg+xml'
        return f


class SVGAndImageField(models.ImageField):
    """ImageField, lekin .svg fayllarni ham qabul qiladi.

    width_field/height_field ishlatilmaydi — SVG o'lchamini Pillow o'qiy olmaydi.
    """

    def formfield(self, **kwargs):
        return super().formfield(**{'form_class': SVGAndImageFormField, **kwargs})
