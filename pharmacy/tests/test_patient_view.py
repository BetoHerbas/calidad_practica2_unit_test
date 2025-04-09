import pytest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from pharmacy.patient_view import patient_home

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
