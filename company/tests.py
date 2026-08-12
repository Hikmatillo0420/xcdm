import io
import json
import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.urls import reverse

from company.fields import SVGAndImageFormField
from company.models import Category, Project

SVG = b'<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"><rect width="10" height="10"/></svg>'
EVIL_SVG = b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>'
EVIL_SVG2 = b'<svg xmlns="http://www.w3.org/2000/svg"><rect onload="alert(1)"/></svg>'


def png_bytes():
    from PIL import Image
    buf = io.BytesIO()
    Image.new('RGB', (4, 4)).save(buf, format='PNG')
    return buf.getvalue()


class SVGFieldTest(TestCase):
    @classmethod
    def setUpClass(cls):
        # Testlar haqiqiy MEDIA_ROOT'ga fayl yozmasligi uchun.
        cls._media_root = tempfile.mkdtemp()
        cls._media_override = override_settings(MEDIA_ROOT=cls._media_root)
        cls._media_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls._media_override.disable()
        shutil.rmtree(cls._media_root, ignore_errors=True)

    def field(self):
        return SVGAndImageFormField(required=False)

    def test_accepts_svg(self):
        f = SimpleUploadedFile('logo.svg', SVG, content_type='image/svg+xml')
        cleaned = self.field().clean(f)
        self.assertEqual(cleaned.name, 'logo.svg')
        self.assertEqual(cleaned.content_type, 'image/svg+xml')

    def test_accepts_png(self):
        f = SimpleUploadedFile('logo.png', png_bytes(), content_type='image/png')
        self.assertEqual(self.field().clean(f).name, 'logo.png')

    def test_rejects_fake_svg(self):
        f = SimpleUploadedFile('fake.svg', b'not an svg at all', content_type='image/svg+xml')
        with self.assertRaises(ValidationError):
            self.field().clean(f)

    def test_rejects_script_svg(self):
        for payload in (EVIL_SVG, EVIL_SVG2):
            f = SimpleUploadedFile('evil.svg', payload, content_type='image/svg+xml')
            with self.assertRaises(ValidationError):
                self.field().clean(f)

    def test_rejects_other_extensions(self):
        f = SimpleUploadedFile('doc.pdf', b'%PDF-1.4', content_type='application/pdf')
        with self.assertRaises(ValidationError):
            self.field().clean(f)

    def test_model_save_with_svg(self):
        c = Category(title='x')
        c.image.save('cat.svg', SimpleUploadedFile('cat.svg', SVG), save=False)
        c.save()
        self.assertTrue(c.image.name.endswith('.svg'))


class ReorderTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('a', 'a@a.com', 'pw')
        self.client.force_login(self.admin)
        self.cat = Category.objects.create(title='c')
        self.projects = [
            Project.objects.create(
                category=self.cat, title='p%d' % i, type='t', description_short='s',
                project_type='pt', preview='http://x', description_long='l',
            )
            for i in range(4)
        ]

    def order(self):
        return list(Project.objects.order_by('order').values_list('title', flat=True))

    def test_initial_order(self):
        self.assertEqual(self.order(), ['p0', 'p1', 'p2', 'p3'])

    def test_reorder_endpoint(self):
        url = reverse('admin:company_project_reorder')
        pks = [str(p.pk) for p in [self.projects[3], self.projects[0], self.projects[1], self.projects[2]]]
        resp = self.client.post(url, data=json.dumps({'pks': pks}), content_type='application/json')
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(resp.json()['positions'], [0, 1, 2, 3])
        self.assertEqual(self.order(), ['p3', 'p0', 'p1', 'p2'])

    def test_get_not_allowed(self):
        resp = self.client.get(reverse('admin:company_project_reorder'))
        self.assertEqual(resp.status_code, 405)

    def test_bad_payload(self):
        resp = self.client.post(reverse('admin:company_project_reorder'),
                                data='[]', content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_unknown_pk(self):
        resp = self.client.post(reverse('admin:company_project_reorder'),
                                data=json.dumps({'pks': ['9999']}), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_non_staff_denied(self):
        self.client.logout()
        User.objects.create_user('u', 'u@u.com', 'pw')
        self.client.login(username='u', password='pw')
        resp = self.client.post(reverse('admin:company_project_reorder'),
                                data=json.dumps({'pks': ['1']}), content_type='application/json')
        self.assertIn(resp.status_code, (302, 403))

    def test_changelist_has_handles(self):
        resp = self.client.get(reverse('admin:company_project_changelist'))
        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode()
        self.assertEqual(html.count('class="drag-handle"'), 4)
        self.assertIn('drag-drop-order.js', html)

    def test_no_handles_when_sorted_by_other_column(self):
        resp = self.client.get(reverse('admin:company_project_changelist'), {'o': '2'})
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('drag-handle', resp.content.decode())
