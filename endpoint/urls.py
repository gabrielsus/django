from django.contrib import admin
from django.urls import path
from api.views import listar_tareas_view, vista, DescargarReportePDFView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vista/', vista),
    path('descargar-reporte-pdf/', DescargarReportePDFView.as_view(), name='descargar-reporte-pdf'),
    path("api/tareas/",listar_tareas_view, name="listar_tareas"),
]