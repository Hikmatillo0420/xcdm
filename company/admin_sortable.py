import json

from django.contrib.admin.views.main import ORDER_VAR, SEARCH_VAR
from django.db import transaction
from django.http import JsonResponse
from django.urls import path, reverse
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from ordered_model.admin import OrderedModelAdmin


class DragDropOrderedModelAdmin(OrderedModelAdmin):
    """OrderedModelAdmin, ustiga changelist'da sichqoncha bilan tortib
    tartibni o'zgartirish (drag & drop) imkoniyati qo'shilgan.

    Tortish faqat ro'yxat o'z tartib maydoni bo'yicha saralanganda ishlaydi
    (boshqa ustun bo'yicha saralash yoki qidiruv yoqilganda tutqich chiqmaydi).
    """

    class Media:
        css = {'all': ('company/admin/drag-drop-order.css',)}
        js = ('company/admin/drag-drop-order.js',)

    # --- URL'lar -----------------------------------------------------------

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        # Standart URL'lardan oldin turishi shart, aks holda `<path:object_id>`
        # ushlab qoladi.
        return [
            path(
                'reorder/',
                self.admin_site.admin_view(self.reorder_view),
                name='%s_%s_reorder' % info,
            ),
        ] + super().get_urls()

    def reorder_url(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        return reverse('admin:%s_%s_reorder' % info, current_app=self.admin_site.name)

    # --- Changelist --------------------------------------------------------

    def is_reorderable(self, request):
        return not request.GET.get(ORDER_VAR) and not request.GET.get(SEARCH_VAR)

    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        if self.is_reorderable(request) and 'drag_handle' not in list_display:
            list_display.insert(0, 'drag_handle')
        return list_display

    @property
    def order_field_name(self):
        return getattr(self.model, 'order_field_name', 'order')

    def drag_handle(self, obj):
        return format_html(
            '<span class="drag-handle" data-pk="{}" data-order="{}"'
            ' data-reorder-url="{}" title="{}">&#x2807;</span>',
            obj.pk,
            getattr(obj, self.order_field_name),
            self.reorder_url(),
            _('Drag to change the position'),
        )

    drag_handle.short_description = ''

    # --- Saqlash -----------------------------------------------------------

    @method_decorator(require_POST)
    def reorder_view(self, request):
        if not self.has_change_permission(request):
            return JsonResponse({'error': 'permission denied'}, status=403)

        try:
            pks = json.loads(request.body.decode('utf-8'))['pks']
        except (ValueError, TypeError, KeyError, UnicodeDecodeError):
            return JsonResponse({'error': 'invalid payload'}, status=400)

        if not isinstance(pks, list) or not pks:
            return JsonResponse({'error': 'invalid payload'}, status=400)

        order_field = self.order_field_name
        objects = self.model.objects.filter(pk__in=pks).only('pk', order_field)
        by_pk = {str(obj.pk): obj for obj in objects}

        if len(by_pk) != len(set(str(pk) for pk in pks)):
            return JsonResponse({'error': 'unknown objects in payload'}, status=400)

        # Ko'rinib turgan qatorlarning mavjud tartib raqamlari qayta
        # taqsimlanadi — shu sababli sahifalash buzilmaydi.
        positions = sorted(getattr(obj, order_field) for obj in by_pk.values())

        with transaction.atomic():
            for pk, position in zip((str(pk) for pk in pks), positions):
                if getattr(by_pk[pk], order_field) != position:
                    self.model.objects.filter(pk=pk).update(**{order_field: position})

        return JsonResponse({
            'pks': [str(pk) for pk in pks],
            'positions': positions,
        })
