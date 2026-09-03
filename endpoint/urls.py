from django.contrib import admin
from django.urls import path
from api.views import cantidad_administradores_por_banco, listar_tareas_view, obtener_administrador_por_matricula, subir_excel_a_db, vista, DescargarReportePDFView,subir_excel_curl, buscar_administradores_por_nombre, listar_administradores_con_banco,insertar_administrador, actualizar_administrador,eliminar_administrador,obtener_administrador_por_matricula,obtener_productos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vista/', vista),
    path('descargar-reporte-pdf/', DescargarReportePDFView.as_view(), name='descargar-reporte-pdf'),
    path("api/tareas/",listar_tareas_view, name="listar_tareas"),
    path('api/subir-excel/', subir_excel_a_db, name='subir_excel_a_db'),
    path('api/buscar-administradores/<str:nombre>/', buscar_administradores_por_nombre, name='buscar_administradores_por_nombre'),
    path('api/listar-administradores-con-banco/', listar_administradores_con_banco, name='listar_administradores_con_banco'),
    path('api/cantidad-administradores-por-banco/', cantidad_administradores_por_banco, name='cantidad_administradores_por_banco'),
    path('api/insertar-administrador/', insertar_administrador, name='insertar_administrador'),
    path('api/actualizar-administrador/<int:admin_id>/', actualizar_administrador, name='actualizar_administrador'),
    path('api/eliminar-administrador/<int:admin_id>/', eliminar_administrador, name='eliminar_administrador'),
    path('api/administrador_matricula/<int:matricula>/',obtener_administrador_por_matricula, name='obtener_administrador_por_matricula'),
    path('api/traer-productos/', obtener_productos, name='obtener_productos'),
]