from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('medicines/', views.MedicinesList.as_view(), name='medicines-list'),
    path('medicine/<int:pk>', views.MedicinesDetailView.as_view(), name='medicine-detail'),
    path('medicines_filter/<str:category>', views.MedicinesList.as_view(), name='medicines-filt'),
    path('medicines_order/<str:ordering>', views.MedicinesList.as_view(), name='medicines-ord')
]
