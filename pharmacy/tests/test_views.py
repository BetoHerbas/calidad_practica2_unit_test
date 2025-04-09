import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_login_get_request(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assert b'login' in response.content.lower()

@pytest.mark.django_db
@pytest.mark.parametrize("user_type,expected_redirect", [
    ('1', '/'),
    ('2', reverse('pharmacist_home')),
    ('3', reverse('doctor_home')),
    ('4', reverse('clerk_home')),
    ('5', reverse('patient_home')),
])
def test_login_success_by_user_type(client, user_type, expected_redirect):
    user = User.objects.create_user(username='testuser', password='pass1234', user_type=user_type)
    response = client.post(reverse('login'), {'username': 'testuser', 'password': 'pass1234'})
    assert response.status_code == 302
    assert response.url == expected_redirect

@pytest.mark.django_db
def test_login_invalid_user_type(client):
    user = User.objects.create_user(username='weirduser', password='pass1234', user_type='9')
    response = client.post(reverse('login'), {'username': 'weirduser', 'password': 'pass1234'}, follow=True)

    assert response.status_code == 200
    assert b'Invalid Login' in response.content

@pytest.mark.django_db
def test_login_invalid_credentials(client):
    response = client.post(reverse('login'), {'username': 'nouser', 'password': 'nopass'}, follow=True)
    assert response.status_code == 200
    assert b'Invalid Login Credentials' in response.content
