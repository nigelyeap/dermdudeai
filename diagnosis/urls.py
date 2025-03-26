from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_case, name='submit_case'),
    path('result/<int:case_id>/', views.case_result, name='case_result'),
    path('delete_image/<int:case_id>/', views.delete_image, name='delete_image'),
]