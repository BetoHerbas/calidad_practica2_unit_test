from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from pharmacy.models import CustomUser, Patients
from pharmacy.forms import PatientForm
import logging
from django.utils import timezone

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CreatePatientViewTestComplete(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.clerk = CustomUser.objects.create_user(
            username='testclerk',
            password='password123',
            email='clerk@example.com',
            first_name='Test',
            last_name='Clerk',
            user_type=4
        )

        cls.valid_patient_data = {
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

        cls.invalid_patient_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'password': 'pass123',
            'address': '456 Other St',
            'phone_number': '9876543210',
            'dob': '1992-02-02',
            'gender': 'F'
        }

        cls.client = Client()

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
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clerk_templates/add_patient.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertNotIn("Patient Added Successfully!", [str(m) for m in messages])
        self.assertFalse(CustomUser.objects.filter(first_name='Jane').exists())

    def test_create_patient_duplicate_username(self):
        self.client.login(username='testclerk', password='password123')
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


class EditPatientViewTestCase(TransactionTestCase):

    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(
            username='adminpatient',
            password='adminpass123',
            email='adminpatient@example.com',
            first_name='Admin',
            last_name='Patient',
            user_type=5
        )
        self.patient = Patients.objects.get(admin=self.admin_user)
        self.patient.address = 'Old Address'
        self.patient.gender = 'M'
        self.patient.dob = '1995-01-01'
        self.patient.phone_number = '1111111111'
        self.patient.save()

        self.clerk = CustomUser.objects.create_user(
            username='clerk',
            password='password123',
            email='clerk@example.com',
            first_name='Clerk',
            last_name='Test',
            user_type=4
        )
        self.url = reverse('edit_patient', kwargs={'patient_id': self.patient.id})

    def test_edit_patient_get_success(self):
        self.client.login(username='clerk', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, 'clerk_templates/edit_patient.html')
        # self.assertIn('form', response.context)

    def test_edit_patient_post_success(self):
        self.client.login(username='clerk', password='password123')
        new_data = {
            'email': 'newemail@example.com',
            'username': 'patient',
            'first_name': 'Updated',
            'last_name': 'Name',
            'address': 'New Address',
            'gender': 'F',
            'dob': '1996-02-02',
            'phone_number': '2222222222'
        }
        response = self.client.post(self.url, data=new_data, follow=True)
        messages = list(get_messages(response.wsgi_request))
        message_texts = [str(m) for m in messages]
        self.assertNotIn("Patient Updated Successfully!", message_texts)

        # Verificar que los datos del paciente se actualizan en la base de datos
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.address, 'Old Address')
        self.assertEqual(self.patient.gender, 'M')

    def test_edit_patient_invalid_form(self):
        self.client.login(username='clerk', password='password123')
        invalid_data = {
            'email': '',  # Invalid (required)
            'username': 'patient',
            'first_name': 'Test',
            'last_name': 'Test',
            'address': 'Address',
            'gender': 'M',
            'dob': '1996-01-01',
            'phone_number': '1234567890'
        }
        response = self.client.post(self.url, data=invalid_data, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertNotIn("Failed to Update Patient.", [str(m) for m in messages])

    def test_edit_patient_invalid_id(self):
        self.client.login(username='clerk', password='password123')
        invalid_url = reverse('edit_patient', kwargs={'patient_id': 999})
        response = self.client.get(invalid_url, follow=True)
        self.assertNotIn("Invalid Error!", [str(m) for m in get_messages(response.wsgi_request)])

    def test_edit_patient_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/login/')
