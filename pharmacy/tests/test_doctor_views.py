import pytest
from django.urls import reverse
from pharmacy.models import Prescription, CustomUser
from django.contrib.auth.models import Group

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

    # Verificar contexto
    assert response.context['Prescription_total'] == 3
