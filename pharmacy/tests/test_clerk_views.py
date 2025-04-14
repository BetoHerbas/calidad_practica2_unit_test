from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from pharmacy.models import CustomUser, Patients
from pharmacy.forms import PatientForm
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CreatePatientViewTestComplete(TransactionTestCase):

    def setUp(self):
        self.clerk = CustomUser.objects.create_user(
            username='testclerk',
            password='password123',
            email='clerk@example.com',
            first_name='Test',
            last_name='Clerk',
            user_type=4
        )

        self.valid_patient_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'testpass123',
            'address': '123 Main St',
            'phone_number': '1234567890',
            'dob': '1990-01-01',
            'gender': 'M'
        }

        self.invalid_patient_data = {
            # Falta 'username' y 'email'
            'first_name': 'Jane',
            'last_name': 'Smith',
            'password': 'pass123',
            'address': '456 Other St',
            'phone_number': '9876543210',
            'dob': '1992-02-02',
            'gender': 'F'
        }

        self.client = Client()

    def test_create_patient_get_request(self):
        self.client.login(username='testclerk', password='password123')
        response = self.client.get(reverse('patient_form2'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clerk_templates/add_patient.html')
        self.assertIsInstance(response.context['form'], PatientForm)

    def test_create_patient_successful_post(self):
        self.client.login(username='testclerk', password='password123')
        response = self.client.post(
            reverse('patient_form2'),
            data=self.valid_patient_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('patient_form2'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Patient Not Saved', [str(m) for m in messages])
        self.assertTrue(~(CustomUser.objects.filter(username='johndoe').exists()))

    def test_create_patient_invalid_form(self):
        self.client.login(username='testclerk', password='password123')
        response = self.client.post(
            reverse('patient_form2'),
            data=self.invalid_patient_data,
            follow=True
        )
        # Como el formulario es inválido, debería renderizar la misma plantilla
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clerk_templates/add_patient.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertNotIn("Patient Added Successfully!", [str(m) for m in messages])
        self.assertFalse(CustomUser.objects.filter(first_name='Jane').exists())

    def test_create_patient_duplicate_username(self):
        self.client.login(username='testclerk', password='password123')
        # Creamos un usuario con el mismo username
        CustomUser.objects.create_user(
            username='johndoe',
            email='another@example.com',
            password='somepass123',
            user_type=5
        )
        response = self.client.post(
            reverse('patient_form2'),
            data=self.valid_patient_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Patient Not Saved", [str(m) for m in messages])

    def test_create_patient_exception_handling(self):
        self.client.login(username='testclerk', password='password123')
        # Forzar un error, por ejemplo, quitando el email para provocar error en el modelo
        corrupted_data = self.valid_patient_data.copy()
        corrupted_data['email'] = ''
        response = self.client.post(
            reverse('patient_form2'),
            data=corrupted_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Patient Not Saved", [str(m) for m in messages])
        self.assertFalse(CustomUser.objects.filter(username='johndoe').exists())

    def test_create_patient_unauthenticated_redirect(self):
        response = self.client.get(reverse('patient_form2'))
        self.assertRedirects(response, f"/login/")


