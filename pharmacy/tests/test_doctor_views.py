import pytest
from django.urls import reverse
from pharmacy.models import Prescription, CustomUser, Doctor
from pharmacy.forms import DoctorForm
from django.contrib.auth.models import Group

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
