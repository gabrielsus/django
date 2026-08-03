from django.contrib import admin
from django.urls import path
from api.views import vista, DescargarReportePDFView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vista/', vista),
    path('descargar-reporte-pdf/', DescargarReportePDFView.as_view(), name='descargar-reporte-pdf'),
]