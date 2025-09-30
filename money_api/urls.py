from django.urls import path
from .views import UploadFinance, GetFinance, finance_dashboard

urlpatterns = [
    path('upload/<int:user_id>/<int:year>/', UploadFinance.as_view(), name='upload-finance'),
    path('records/<int:user_id>/<int:year>/', GetFinance.as_view(), name='get-finance'),
    path('finance/dashboard/', finance_dashboard, name='finance-dashboard'),
]
