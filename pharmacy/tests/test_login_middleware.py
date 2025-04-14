from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from pharmacy.LoginCheckMiddleWare import LoginCheckMiddleWare
from pharmacy.models import CustomUser


class LoginMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = LoginCheckMiddleWare(get_response=lambda request: None)


    def test_tc1_user_not_authenticated_at_login(self):
        request = self.factory.get(reverse("login"))
        request.user = AnonymousUser()
        response = self.middleware.process_view(request, lambda x: x, [], {})
        self.assertIsNone(response)

    def test_tc2_user_not_authenticated_other_page(self):
        request = self.factory.get("/some-page/")
        request.user = AnonymousUser()
        response = self.middleware.process_view(request, lambda x: x, [], {})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_tc3_user_authenticated_module_allowed(self):
        # Crear un usuario simulado de tipo "3" (Doctor)
        user = CustomUser.objects.create_user(username="doctor", password="test", user_type="3")

        # Simular una vista en un módulo permitido
        class MockView:
            __module__ = "pharmacy.DoctorViews"

        request = self.factory.get("/some-path/")
        request.user = user

        # Ejecutar middleware
        response = self.middleware.process_view(request, MockView, [], {})

        # Debe permitir el acceso (no redirige)
        self.assertIsNone(response)

    def test_tc4_user_authenticated_module_not_allowed(self):
        user = CustomUser.objects.create_user(username="clerk", password="1234", user_type="4")
        request = self.factory.get("/some-page/")
        request.user = user

        def fake_view(request): pass
        fake_view.__module__ = "some.other.module"

        response = self.middleware.process_view(request, fake_view, [], {})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/receptionist_home/", response.url)

    def test_tc5_user_type_not_defined(self):
        user = CustomUser.objects.create_user(username="no_type", password="1234", user_type="99")
        request = self.factory.get("/any/")
        request.user = user
        response = self.middleware.process_view(request, lambda x: x, [], {})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_tc6_no_redirect_defined_allows_any_module(self):
        user = CustomUser.objects.create_user(username="hod", password="1234", user_type="1")
        request = self.factory.get("/other/")
        request.user = user

        def fake_view(request): pass
        fake_view.__module__ = "otro.modulo"

        response = self.middleware.process_view(request, fake_view, [], {})
        self.assertIsNone(response)
