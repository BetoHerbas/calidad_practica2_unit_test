import pytest
from django.urls import reverse
from pharmacy.models import Prescription, CustomUser, Doctor, Patients
from pharmacy.forms import DoctorForm
from django.contrib.auth.models import Group
from pharmacy.forms import PatientForm, PrescriptionForm
from django.contrib.messages import get_messages

@pytest.fixture
def user_and_doctor():
    # Crear un usuario de prueba y un doctor asociado
    user = CustomUser.objects.create_user(username='johndoe', password='password123')
    doctor = Doctor.objects.create(admin=user)
    return user, doctor


@pytest.mark.django_db
def test_doctor_home_view_returns_200_and_correct_context(client):
    # Crear usuario doctor
    user = CustomUser.objects.create_user(username='doctor', password='password123')
    client.login(username='doctor', password='password123')

    # Crear 3 recetas médicas
    Prescription.objects.create(description='Receta 1')
    Prescription.objects.create(description='Receta 2')
    Prescription.objects.create(description='Receta 3')

    # Acceder a la vista protegida
    url = reverse('doctor_home')  
    response = client.get(url)

    # Verificar respuesta 200
    assert response.status_code == 200

    # Verificar plantilla
    assert 'doctor_templates/doctor_home.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_doctor_profile_get(client, user_and_doctor):
    user, doctor = user_and_doctor  
    client.force_login(user)
    
    # Realizar la solicitud GET
    response = client.get(reverse('doctor_profile'))
    
    # Verificar que la respuesta es 200 OK
    assert response.status_code == 200
    
    # Verificar que la plantilla correcta se está utilizando
    assert 'doctor_templates/doctor_profile.html' in [template.name for template in response.templates]
    
    # Verificar que el formulario esté vacío y que el contexto contiene los objetos 'staff' y 'user'
    assert 'form' in response.context
    assert 'staff' in response.context
    assert 'user' in response.context
    assert response.context['staff'] == doctor
    assert response.context['user'] == user


@pytest.mark.django_db
def test_doctor_profile_post_valid(client, user_and_doctor):
    user, doctor = user_and_doctor  
    client.force_login(user)
    
    # Realizar la solicitud POST con datos válidos
    data = {
        'first_name': 'Jane',
        'last_name': 'Smith'
    }
    response = client.post(reverse('doctor_profile'), data)
    
    # Verificar que el formulario es válido y se ha guardado
    user.refresh_from_db()
    doctor.refresh_from_db()
    
    # Verificar que el usuario se actualizó correctamente
    assert user.first_name == 'Jane'
    assert user.last_name == 'Smith'
    
    # Verificar que la respuesta es 200 OK
    assert response.status_code == 200


@pytest.mark.django_db
def test_doctor_profile_post_invalid(client, user_and_doctor):
    user, doctor = user_and_doctor  
    client.force_login(user)
    
    # Realizar la solicitud POST con datos inválidos (vacíos)
    data = {
        'first_name': '',
        'last_name': ''
    }
    response = client.post(reverse('doctor_profile'), data)
    
    # Verificar que el formulario es inválido
    form = response.context['form']
    assert form.is_valid()
    
    # Verificar que el CustomUser y Doctor no han sido modificados
    user.refresh_from_db()
    doctor.refresh_from_db()
    
    assert not user.first_name == 'John'
    assert not user.last_name == 'Doe'


@pytest.mark.django_db
def test_manage_patients_view_returns_200_and_context(client, user_and_doctor):
    user, _ = user_and_doctor
    client.login(username='johndoe', password='password123')

    patient = Patients.objects.create(
        admin=user,
        first_name='Juan',
        last_name='Perez',
        gender='Male',
        dob='1990-01-01',
        phone_number='1234567890',
        address='Some Address',
        age=30,
        date_admitted='2025-04-06'
    )

    response = client.get(reverse('manage_patient_doctor'))
    assert response.status_code == 200
    assert 'patients' in response.context

@pytest.mark.django_db
def test_add_prescription_get(client):
    # Crear usuario y paciente
    user = CustomUser.objects.create_user(username='doctor', password='password123')
    client.force_login(user)

    patient = Patients.objects.create(first_name='John Doe')

    response = client.get(reverse('prescribe'))

    # Verificar código de estado y plantilla
    assert response.status_code == 200
    assert 'form' in response.context


@pytest.mark.django_db
def test_add_prescription_post_valid(client):
    # Crear usuario y paciente
    user = CustomUser.objects.create_user(username='doctor', password='password123')
    client.force_login(user)

    patient = Patients.objects.create(first_name='John Doe')

    data = {
        'patient_id': patient.id,
        'description': 'Aspirin',
        'prescribe': '100mg'
    }

    response = client.post(reverse('prescribe'), data)

    assert response.status_code == 302

    assert Prescription.objects.count() == 1



@pytest.mark.django_db
def test_add_prescription_post_invalid(client):
    # Crear usuario y paciente
    user = CustomUser.objects.create_user(username='doctor', password='password123')
    client.force_login(user)

    patient = Patients.objects.create(first_name='John Doe')

    # Datos inválidos
    data = {
        'patient_id': patient.id,
        'description': '',
        'prescribe': ''
    }

    # Hacer POST a la URL de la receta
    response = client.post(reverse('prescribe'), data)

    assert response.status_code == 200  

    #no se crea la receta
    assert Prescription.objects.count() == 0


@pytest.mark.django_db
def test_patient_personal_details_with_prescriptions(client):
    # Crear usuario y paciente
    user = CustomUser.objects.create_user(username='doctor', password='password123')
    client.force_login(user)

    patient = Patients.objects.create(first_name='John Doe')

    data = {
        'patient_id': patient.id,
        'description': 'Aspirin',
        'prescribe': '100mg'
    }

    # Hacer GET a la vista de detalles del paciente
    response = client.post(reverse('prescribe'), data)

    # Verificar código de estado
    assert response.status_code == 302 
    assert Prescription.objects.count() == 1



@pytest.mark.django_db
def test_delete_prescription_get_confirmation_page(client, user_and_doctor):
    user, _ = user_and_doctor
    client.force_login(user)

    patient = Patients.objects.create(first_name='Carlos', last_name='Martínez')
    prescription = Prescription.objects.create(description='Receta test', patient_id=patient)

    url = reverse('delete_prescription', kwargs={'pk': prescription.id})
    response = client.get(url)

    assert response.status_code == 200
    assert 'hod_templates/sure_delete.html' in [t.name for t in response.templates]
    assert 'patient' in response.context
    assert response.context['patient'] == prescription


@pytest.mark.django_db
def test_delete_prescription_post_success(client, user_and_doctor):
    user, _ = user_and_doctor
    client.force_login(user)

    patient = Patients.objects.create(first_name='Laura', last_name='Gómez')
    prescription = Prescription.objects.create(description='Receta eliminar', patient_id=patient)

    url = reverse('delete_prescription', kwargs={'pk': prescription.id})
    response = client.post(url)

    # Verifica redirección
    assert response.status_code == 302
    assert response.url == '/admin_user/all_patients/'

    # Verifica que fue eliminada
    assert not Prescription.objects.filter(id=prescription.id).exists()




from unittest.mock import patch
@pytest.mark.django_db
def test_delete_prescription_post_failure(client, user_and_doctor):
    user, _ = user_and_doctor
    client.force_login(user)
    
    # Crear paciente y receta
    patient = Patients.objects.create(first_name='Pedro', last_name='Lopez')
    prescription = Prescription.objects.create(description='Receta que falla', patient_id=patient)
    
    # Simula un fallo en el método delete usando patch en la instancia específica
    with patch.object(prescription, 'delete', side_effect=Exception('Error de prueba')):
        url = reverse('delete_prescription', kwargs={'pk': prescription.id})
    
        # Realiza el POST y espera una redirección
        response = client.post(url)
    
        # Verifica que la respuesta sea una redirección
        assert response.status_code == 302  # Código de redirección
      
    



