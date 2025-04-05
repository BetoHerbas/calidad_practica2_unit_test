from django.urls import path
from .import HODViews
from .import pharmacistViews,DoctorViews,views,patient_view,clerkViews
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('',HODViews.admin_dashboard,name='admin_dashboard'),
    path('admin_user/patient_form/',HODViews.create_patient,name='patient_form'),
    path('admin_user/all_patients/',HODViews.all_patients,name='all_patients'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_user,name='logout'), 
    # path('get_user_details/', views.get_user_details, name="get_user_details"),

    path('admin_user/add_pharmacist/',HODViews.create_pharmacist,name='add_pharmacist'),
    path('admin_user/manage_pharmacist/',HODViews.manage_pharmacist,name='manage_pharmacist'),
    path('admin_user/add_doctor/',HODViews.create_doctor,name='add_doctor'),
    path('admin_user/manage_doctor/',HODViews.manage_doctor,name='manage_doctor'),
    path('admin_user/add_pharmacyClerk/',HODViews.create_pharmacy_clerk,name='add_pharmacyClerk'),
    path('admin_user/admin_user/manage_pharmacyClerk/',HODViews.manage_pharmacy_clerk,name='manage_pharmacyClerk'),
    path('admin_user/add_stock/',HODViews.add_stock,name='add_stock'),
    path('admin_user/add_category/',HODViews.add_category,name='add_category'),
    path('admin_user/manage_stock/',HODViews.manage_stock,name='manage_stock'),    
    path('admin_user/prescribe_drug/',HODViews.add_prescription,name='prescribe'),
    path('admin_user/edit_patient/<patient_id>/',HODViews.edit_patient,name='edit_patient'),
    # path('add_patient_save/',HODViews.editPatientSave,name='edit_patient_save'),

    path('admin_user/delete_patient/<str:pk>/',HODViews.confirm_delete,name='delete_patient'),
    path('admin_user/patient_personal_records/<pk>/',HODViews.patient_personal_records,name='patient_record'),
    path('admin_user/delete_prescription/<str:pk>/',HODViews.delete_prescription,name='delete_prescription'),
    path('admin_user/doctor_profile/',DoctorViews.doctor_profile,name='doctor_profile'),
    path('admin_user/hod_profile/',HODViews.hod_profile,name='hod_profile'),
    path('admin_user/delete_doctor/<str:pk>/',HODViews.delete_doctor,name='delete_doctor'),
    path('admin_user/delete_pharmacist/<str:pk>/',HODViews.delete_pharmacist,name='delete_pharmacist'),
    path('admin_user/delete_receptionist/<str:pk>/',HODViews.delete_pharmacy_clerk,name='delete_clerk'),
    path('admin_user/hod_profile/editAdmin_profile/',HODViews.edit_admin,name='edit-admin'),
    path('admin_user/delete_drug/<str:pk>/',HODViews.delete_drug,name='delete_drug'),


    path('admin_user/edit_pharmacist/<staff_id>/', HODViews.edit_pharmacist, name="edit_pharmacist"),
    path('admin_user/edit_doctor/<doctor_id>/', HODViews.edit_doctor, name="edit_doctor"),
    path('admin_user/edit_receptionist/<clerk_id>/', HODViews.edit_pharmacy_clerk, name="edit_clerk"),
    path('admin_user/edit_drug/<pk>/', HODViews.edit_stock, name="edit_drug"),
    path('admin_user/receive_drug/<pk>/', HODViews.receive_drug, name="receive_drug"),
    path('admin_user/reorder_level/<str:pk>/', HODViews.reorder_level, name="reorder_level"),
    path('admin_user/drug_details/<str:pk>/', HODViews.drug_details, name="drug_detail"),
    path('patient_feedback_message/', pharmacistViews.patient_feedback_message, name="patient_feedback_message"),
    path('patient_feedback_message_reply/', pharmacistViews.patient_feedback_message_reply, name="patient_feedback_message_reply"),
    path('admin_user/delete_patient_feedback/<str:pk>/', pharmacistViews.delete_feedback, name="delete_fed"),

        path('delete_details/<str:pk>/', pharmacistViews.delete_dispense4, name="del_disp"),



    #Pharmacist
    path('pharmacist_home/',pharmacistViews.pharmacist_home,name='pharmacist_home'),
    path('pharmacist_manage_patients/',pharmacistViews.manage_patients_pharmacist,name='manage_patient_pharmacist'),
    path('manage_disp/<pk>/',pharmacistViews.manage_dispense,name='pharmacist_disp'),
#    path('manage_dispe/<str:pk>/',pharmacistViews.dispenseDrug,name='pharm_disp'),
    # path('manage_stock_form/<str:pk>/',pharmacistViews.dispense,name='pharm_disp2'),
    path('staff_profile/',pharmacistViews.user_profile,name='pharmacist_profile'),

    path('manage_stock2/',pharmacistViews.manage_stock,name='manage_stock2'),    
    path('manage_prescrip/',pharmacistViews.manage_prescription,name='pharmacist_prescription'),
    path('pharmacist_user/drug_details/<str:pk>/', pharmacistViews.drug_details, name="drug_detail2"),



    #Doctor
    path('doctor_home/',DoctorViews.doctor_home,name='doctor_home'),
    path('manage_patients/',DoctorViews.manage_patients,name='manage_patient_doctor'),
    path('doctor_prescribe_drug/<str:pk>/',DoctorViews.add_prescription,name='doctor_prescribe2'),
    path('patient_personal_details/<str:pk>/',DoctorViews.patient_personal_details,name='patient_record_doctor'),
    path('manage_prescription_doctor/',DoctorViews.manage_prescription,name='manage_precrip_doctor'),
    path('doctor_prescribe_delete/<str:pk>/',DoctorViews.delete_prescription,name='doctor_prescrip_delete'),
    path('doctor_prescribe_edit/<str:pk>/',DoctorViews.edit_prescription,name='doctor_prescrip_edit'),

    #Patients
    path('patient_profile/',patient_view.patient_profile,name='patient_profile'),
    path('patient_home/',patient_view.patient_home,name='patient_home'),
    path('patient_feedback/',patient_view.patient_feedback,name='patient_feedback'),
    path('staff_feedback_save/', patient_view.patient_feedback_save, name="patient_feedback_save"),
    path('taken_home/',patient_view.patient_dispense3,name='taken_home'),
    path('delete_patient_feedback2/<str:pk>/',patient_view.patient_delete_feedback, name="delete_fed2"),
    path('delete_dispen/',patient_view.my_prescription_delete,name='taken_delete'),

    #Receptionist
    path('receptionist_profile/',clerkViews.receptionist_profile,name='clerk_profile'),
    path('receptionist_home/',clerkViews.clerk_home,name='clerk_home'),
    path('receptionist/patient_form/',clerkViews.create_patient,name='patient_form2'),
    path('receptionist/all_patients/',clerkViews.all_patients,name='all_patients2'),
    path('receptionist/edit_patient/<patient_id>/',clerkViews.edit_patient,name='edit_patient_clerk'),
    path('receptionist/patient_personal_records/<str:pk>/',clerkViews.patient_personal_records,name='patient_record_clerk'),
    path('receptionist/delete_patient/<str:pk>/',clerkViews.confirm_delete,name='delete_patient_clerk'),
    # path('receptionist/dispense_drug/<str:pk>/',pharmacistViews.dispenseDrug,name='dispense_drug'),


  
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name="reset_password"),

    path('reset_password_sent/',auth_views.PasswordResetDoneView
    .as_view(template_name="password_reset_sent.html"),name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView
    .as_view(template_name="password_reset_form.html"),name="password_reset_confirm"),



    

   path('reset_password_complete/',auth_views.PasswordResetCompleteView
    .as_view(template_name="password_reset_done.html"),name="password_reset_complete"),
]
