import pytest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from pharmacy.patient_view import patient_home, patient_profile, my_prescription
from pharmacy.models import CustomUser, Patients, Prescription
from django.shortcuts import render


@pytest.mark.django_db
@patch('pharmacy.patient_view.Patients')  # Asegúrate que esto coincida con el import en patient_view.py
def test_patient_home_view(mock_patients):
    # Crear request
    factory = RequestFactory()
    request = factory.get('/patient/home')

    # Mock usuario
    mock_user = MagicMock()
    mock_user.id = 1
    request.user = mock_user

    # Mock de paciente y de objects.get
    mock_dispense = MagicMock()
    mock_dispense.count.return_value = 2

    mock_patient = MagicMock()
    mock_patient.dispense_set.all.return_value = mock_dispense

    mock_patients.objects.get.return_value = mock_patient

    # Ejecutar la vista
    response = patient_home(request)

    # Aserciones
    assert response.status_code == 200
    assert b'Dashboard' in response.content or b'dashboard' in response.content.lower()


@pytest.mark.django_db
@patch("pharmacy.patient_view.messages")
@patch("pharmacy.patient_view.PatientPicForm1")
@patch("pharmacy.patient_view.CustomUser")
@patch("pharmacy.patient_view.Patients")
def test_patient_profile_get_method(mock_patients, mock_custom_user, mock_form_class, mock_messages):
    factory = RequestFactory()
    request = factory.get('/patient/profile')
    request.user = MagicMock(id=1)

    mock_custom_user.objects.get.return_value = MagicMock(id=1)

    mock_patients.objects.get.return_value = MagicMock()

    mock_form_class.return_value = MagicMock()

    response = patient_profile(request)

    assert response.status_code == 200
    assert b"<html" in response.content.lower() or b"<!doctype" in response.content.lower()


@pytest.mark.django_db
@patch("pharmacy.patient_view.messages")
@patch("pharmacy.patient_view.PatientPicForm1")
@patch("pharmacy.patient_view.CustomUser")
@patch("pharmacy.patient_view.Patients")
def test_patient_profile_post_valid_form(mock_patients, mock_custom_user, mock_form_class, mock_messages):
    factory = RequestFactory()
    request = factory.post('/patient/profile', {
        'first_name': 'Juan',
        'last_name': 'Perez',
        'email': 'juan@test.com',
        'address': 'Calle Falsa 123'
    }, FILES={})  

    request.user = MagicMock(id=1)

    mock_user = MagicMock()
    mock_custom_user.objects.get.return_value = mock_user

    mock_patient = MagicMock()
    mock_patients.objects.get.return_value = mock_patient

    mock_form = MagicMock()
    mock_form.is_valid.return_value = True
    mock_form.save.return_value = None
    mock_form_class.return_value = mock_form

    response = patient_profile(request)

    assert response.status_code == 302
    assert response.url == "/patient_profile/"
    mock_messages.success.assert_called_once()


@pytest.mark.django_db
@patch("pharmacy.patient_view.messages")
@patch("pharmacy.patient_view.PatientPicForm1")
@patch("pharmacy.patient_view.CustomUser")
@patch("pharmacy.patient_view.Patients")
def test_patient_profile_post_invalid_form(mock_patients, mock_custom_user, mock_form_class, mock_messages):
    factory = RequestFactory()
    request = factory.post('/patient/profile', {
        'first_name': 'Juan',
        'last_name': 'Perez',
        'email': 'juan@test.com',
        'address': 'Calle Falsa 123'
    }, FILES={}) 

    request.user = MagicMock(id=1)

    mock_user = MagicMock()
    mock_custom_user.objects.get.return_value = mock_user

    mock_patient = MagicMock()
    mock_patients.objects.get.return_value = mock_patient

    mock_form = MagicMock()
    mock_form.is_valid.return_value = False  
    mock_form_class.return_value = mock_form

    response = patient_profile(request)

    assert response.status_code == 302

    assert response.url == "/patient_profile/"

    mock_messages.error.assert_not_called()



@pytest.mark.django_db
@patch('pharmacy.patient_view.render')
def test_my_prescription_returns_valid_data(mock_render):
    user = CustomUser.objects.create_user(username="test_user", user_type=5)
    patient = Patients.objects.get(admin=user)
    prescription = Prescription.objects.create(patient_id=patient, description="Test")

    mock_render.return_value = MagicMock(status_code=200)
    
    request = RequestFactory().get("/")
    request.user = user
    response = my_prescription(request)
    
    assert response.status_code == 200
    
    args, kwargs = mock_render.call_args
    
    assert args[0] == request  
    assert args[1] == 'doctor_templates/myprescription.html'  
    
    context = args[2] if len(args) > 2 else kwargs.get('context', {})
    
    assert 'prescrips' in context
    assert 'patient' in context
    assert prescription in context['prescrips']
    assert patient in context['patient']