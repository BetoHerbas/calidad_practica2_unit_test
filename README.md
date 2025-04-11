# PharmacyManagementSystem
<h2>🔥Pharmacy Dispensing Management System || Python Django</h2>
  
  
   <p>This is a simple Pharmacy Management System programmed using Python Django. The system has 5 types of users are the Administrator, Pharmacist, Doctor, and Receptionist(pharmacyClerk) and Patient.This project has user-friendly functionalities.</p>
   
   

## Run these Commads
### Step 1
     pip install -r requirements.txt
### Step 2
     python manage.py migrate
        
### Step 3
     python manage.py runserver

### Step 4
     create .env
     add SECRET_KEY = 'django-insecure-ui1u$88tg97g-()a(^hcv5mn#jzcu^3yb1n=!s7kn-!t25932n'
-----------------------------------------------------------------------------------

### Admin User Login: 
- Username: admin
- password: 1234  
  
          Administrator Main Features
     - Manage Admissions/Patients
     - Manage System Users
     - Manage Patient's Prescription
     - Manage Medicinal Drugs Categories
     - Manage Medicinal Drugs
     - Manage Stocks
     - Dispense Medicinal Drug
     - Manage Personal Accounti

------------------------------------------------------------------------------------
### Patient Login:
- Username: patient1
- password: 1234

           Patient Main Featues
     -  Manage his/her medications
     - Feedback Pharmacist incase of dispensing issue
     -  manage Personal Account
      
 
-----------------------------------------------------------------------------------
### Pharmacist Login:
- Username: pharmacist1
- password: 1234

        Pharmacist  Main Features
     - Manage Medicinal Drugs
     - Manage Stocks
     - Dispense Medicinal Drug
     - Manage Patient Feedback messeges
     - Manage Personal Account
     
        

-------------------------------------------------------------------------------------
### PharmacyClerk Login:
- Username: pharmacyclerk1
- password: 1234

            Receptionist Main Features
     - Manage Admissions/Patients
     - Manage Personal Account

------------------------------------------------------------------------------------
### Doctor Login:
- Username: doctor1
- password: 1234
        
        Doctor Main Featues
     - Manage Patient's Prescription
     - Manage Personal Account
   
-----------------------------------------------------------------------------------
## How to run the Unit Tests
run the next command in the root of the project
pytest --cov=pharmacy --cov-config=.coveragerc --cov-report=html
-----------------------------------------------------------------------------------

N/B: When adding New patient there are some validations in filling the forms 
     For easy filling of forms use fake filler extension in chrome 
     Fake Filler Extension Chrome link:https://chrome.google.com/webstore/detail/fake-filler/bnjjngeaknajbdcgpfkgnonkmififhfo

--------------------------------------------------------------------------------------










