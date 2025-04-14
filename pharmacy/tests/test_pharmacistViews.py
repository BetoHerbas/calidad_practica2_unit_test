import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.messages import get_messages
from pharmacy.models import CustomUser, Pharmacist


@pytest.mark.django_db
def test_user_profile_get():
    """TC1: GET muestra formulario"""
    user = CustomUser.objects.create_user(
        username="pharma_test", 
        password="testpass",
        user_type=2  
    )

    client = Client()
    client.force_login(user)
    response = client.get(reverse('pharmacist_profile'))  

    assert response.status_code == 200
    assert 'pharmacist_templates/staff_profile.html' in [t.name for t in response.templates]
    assert 'form' in response.context

@pytest.mark.django_db
def test_user_profile_post_valid():
    """TC2: POST con datos válidos actualiza perfil"""
    # Configuración
    user = CustomUser.objects.create_user(
        username="pharma_test",
        password="testpass",
        user_type=2,
        first_name="NombreAntiguo",  
        last_name="ApellidoAntiguo"
    )
    pharmacist = Pharmacist.objects.get(admin=user)  
    pharmacist.address = "DirecciónAntigua"
    pharmacist.save()

    data = {
        'first_name': 'NombreNuevo',
        'last_name': 'ApellidoNuevo',
        'address': 'DirecciónNueva'
    }

    client = Client()
    client.force_login(user)
    response = client.post(reverse('pharmacist_profile'), data)

    assert response.status_code == 302
    assert response.url == reverse('pharmacist_profile')
    
    user.refresh_from_db()
    pharmacist.refresh_from_db()
    assert user.first_name == "NombreNuevo"
    assert pharmacist.address == "DirecciónNueva"
    
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Profile Updated Successfully"
    
    
@pytest.mark.django_db
def test_user_profile_post_invalid():
    """TC3 (adaptado): POST con campo vacío actualiza con ese valor"""
    user = CustomUser.objects.create_user(
        username="pharma_test",
        password="testpass",
        user_type=2,
        first_name="NombreOriginal",
        last_name="ApellidoOriginal"
    )
    pharmacist = Pharmacist.objects.get(admin=user)
    pharmacist.address = "DirecciónOriginal"
    pharmacist.save()

    data = {
        'first_name': '',
        'last_name': 'ApellidoNuevo',
        'address': 'DirecciónNueva'
    }

    client = Client()
    client.force_login(user)
    response = client.post(reverse('pharmacist_profile'), data)

    assert response.status_code == 302
    assert response.url == reverse('pharmacist_profile')

    user.refresh_from_db()
    pharmacist.refresh_from_db()
    assert user.first_name == ""  
    assert user.last_name == "ApellidoNuevo"
    assert pharmacist.address == "DirecciónNueva"
