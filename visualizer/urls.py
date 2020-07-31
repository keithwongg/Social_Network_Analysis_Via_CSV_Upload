from django.urls import path, include
from . import views 

# app_name = "articles"

urlpatterns = [
    path('', views.upload_csv, name = 'upload'),
    path('analytics/', views.analytics, name = "analytics"),
    path('analytics/clickDataQuery/', views.clickDataQuery, name = "clickDataQuery"),
    path('analytics/resetCSV/', views.resetCSV, name = "resetCSV"),
    
]
