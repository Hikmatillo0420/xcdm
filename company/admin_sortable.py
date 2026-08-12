import json

from django.db import transaction
from django.http import JsonResponse
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from ordered_model.admin import OrderedModelAdmin


class DragDropOrderedModelAdmin(OrderedModelAdmin):
    """OrderedModelAdmin, ustiga changelist qatorlarini sichqoncha bilan
    tortib tartibni o'zgartirish imkoniyati qo'shilgan.

    Qatorning istalgan bo'sh joyidan ushlab tortiladi; havola, tugma va
    checkbox'lar odatdagidek ishlayveradi. Tortish faqat ro'yxat o'z tartib
    maydoni bo'yicha turganda yoqiladi (boshqa ustun bo'yicha saralash yoki
    qidiruvda o'chadi).

    Eslatma: modelda `order_with_respect_to` ishlatilsa bu mixin to'g'ri
    ishlamaydi — u butun jadvalni yagona ketma-ketlik deb hisoblaydi.
    """

    class Media:
        css = {'all': ('company/admin/drag-drop-order.css',)}
        js = ('company/admin/drag-drop-order.js',)

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

    @property
    def order_field_name(self):
        return getattr(self.model, 'order_field_name', 'order')

    @method_decorator(require_POST)
    def reorder_view(self, request):
        if not self.has_change_permission(request):
            return JsonResponse({'error': 'permission denied'}, status=403)

        try:
            payload = json.loads(request.body.decode('utf-8'))['pks']
        except (ValueError, TypeError, KeyError, UnicodeDecodeError):
            return JsonResponse({'error': 'invalid payload'}, status=400)

        if not isinstance(payload, list) or not payload:
            return JsonResponse({'error': 'invalid payload'}, status=400)

        pks = [str(pk) for pk in payload]
        if len(set(pks)) != len(pks):
            return JsonResponse({'error': 'duplicate pks'}, status=400)

        order_field = self.order_field_name

        with transaction.atomic():
            rows = list(
                self.model.objects.order_by(order_field, 'pk')
                .values_list('pk', order_field)
            )
            current = {str(pk): value for pk, value in rows}
            arranged = [str(pk) for pk, _ in rows]
            slot_of = {pk: index for index, pk in enumerate(arranged)}

            if any(pk not in slot_of for pk in pks):
                return JsonResponse({'error': 'unknown objects in payload'}, status=400)

            # Faqat ko'rinib turgan qatorlar egallagan o'rinlar qayta
            # taqsimlanadi — qolgan sahifalardagi yozuvlar joyida qoladi.
            for slot, pk in zip(sorted(slot_of[pk] for pk in pks), pks):
                arranged[slot] = pk

            # Butun ro'yxat 0..N-1 qilib qayta raqamlanadi. Bu eski
            # yozuvlardagi takrorlangan (masalan, hammasi 0 bo'lgan)
            # qiymatlarni ham bir yo'la to'g'rilaydi.
            for position, pk in enumerate(arranged):
                if current[pk] != position:
                    self.model.objects.filter(pk=pk).update(**{order_field: position})

        return JsonResponse({'pks': pks})
