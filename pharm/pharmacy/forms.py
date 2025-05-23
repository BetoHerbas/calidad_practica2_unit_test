from django.forms import ModelForm
from .models import Patients, Stock, Category, Prescription, Pharmacist, Doctor, PharmacyClerk, AdminHOD, Dispense, CustomUser
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import Form
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import RegexValidator

import json
class PatientPicForm1(forms.ModelForm):
    class Meta:
        model = Patients
        fields = ['first_name', 'last_name', 'profile_pic', 'age', 'address', 'date_admitted', 'last_updated']  

      


class DateInput(forms.DateInput):
    input_type = "date"

from phonenumber_field.formfields import PhoneNumberField
class ClientForm(forms.Form):
    mobile = PhoneNumberField()

class PatientForm(forms.Form):

    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    reg_no = forms.CharField(label="Reg No", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    phone_number = forms.CharField(label="Mobile", max_length=50)
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    dob= forms.DateField(label="dob", widget=DateInput(attrs={"class":"form-control"}))

    FIELD_REQUIRED_MSG = "This field is required"

    # Validations for patient
    def clean_reg_no(self):
        reg_no = self.cleaned_data['reg_no']
        if  not  reg_no:
            raise ValidationError(self.FIELD_REQUIRED_MSG)
        for instance in Patients.objects.all():
            if instance.reg_no==reg_no:
                raise ValidationError( "Registration number aready exist")
      
        return reg_no


    def clean_phone_number(self):
        phone_number=self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('This field is requied')
        elif len(phone_number) < 10:
            raise forms.ValidationError('Invalid Number')
        for instance in Patients.objects.all():
            if instance.phone_number==phone_number:
                raise ValidationError( "PhoneNumber aready exist")
        
        return phone_number
        
            
   
    def clean_username(self):
        username = self.cleaned_data['username']
        if  not  username:
            raise ValidationError(self.FIELD_REQUIRED_MSG)
        for instance in CustomUser.objects.all():
            if instance.username==username:
                raise ValidationError( "Username aready exist")
      
        return username

    def clean_firstName(self):
        first_name = self.cleaned_data['first_name']
        if  not  first_name:
            raise ValidationError(self.FIELD_REQUIRED_MSG)
        return first_name

    def clean_secondName(self):
        last_name = self.cleaned_data['last_name']
        if  not  last_name:
            raise ValidationError(self.FIELD_REQUIRED_MSG)
        return last_name

class EditPatientForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    phone_number = forms.CharField(label="Mobile", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    dob= forms.DateField(label="dob", widget=DateInput(attrs={"class":"form-control"}))
   
    
    

class StockForm(forms.ModelForm):
    valid_to= forms.DateField(label="Expiry Date", widget=DateInput(attrs={"class":"form-control"}))

    class Meta:
        model=Stock
        fields = [
            'category', 'drug_imprint', 'drug_name', 'drug_color', 'drug_shape',
            'quantity', 'manufacture', 'drug_strength', 'valid_to',
            'drug_description', 'drug_pic'
        ]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["patient_id", "description", "prescribe", "date_precribed"]


class CustomerForm(ModelForm):
    class Meta:
        model = Pharmacist
        fields = ["emp_no", "age", "profile_pic", "created_at", "updated_at"]


class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ["emp_no", "age", "profile_pic", "created_at", "updated_at"]

    def clean_firstName(self):
        first_name = self.cleaned_data["first_name"]
        if not first_name:
            raise ValidationError(self.FIELD_REQUIRED_MSG)
        return first_name

    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        if not mobile:
            raise forms.ValidationError(self.FIELD_REQUIRED_MSG)
        return mobile

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not username:
            raise ValidationError(self.FIELD_REQUIRED_MSG)
        for instance in CustomUser.objects.all():
            if instance.username == username:
                raise ValidationError("Username already exists")


class ClerkForm(ModelForm):
    class Meta:
        model = PharmacyClerk
        fields = ["emp_no", "profile_pic", "created_at", "updated_at"]


class HodForm(ModelForm):
    class Meta:
        model = AdminHOD
        fields = ["emp_no", "profile_pic", "created_at", "updated_at"]


class PatientSearchForm1(ModelForm):
    class Meta:
        model = Patients
        fields = ["reg_no", "first_name", "last_name", "age", "date_admitted", "last_updated"]


class PatientForm7(ModelForm):
    class Meta:
        model = Patients
        fields = [
            "reg_no",
            "first_name",
            "last_name",
            "dob",
            "phone_number",
            "age",
            "address",
            "date_admitted",
            "last_updated",
        ]



class DispenseForm(ModelForm):
    class Meta:
        model = Dispense
        fields = [
            "patient_id",
            "drug_id",
            "drug_name",
            "dispense_quantity",
            "dispense_date",
            "pharmacist",
            "comments",
        ]


class ReceiveStockForm(ModelForm):
    valid_to = forms.DateField(label="Expiry Date", widget=DateInput(attrs={"class": "form-control"}))

    class Meta:
        model = Stock
        fields = [
            "supplier",
            "batch_no",
            "cost_per_unit",
            "total_cost",
            "unit_price",
            "received_date",
            "valid_to",
        ]



class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['reorder_level']

