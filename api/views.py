from django.http import HttpResponse, FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import generar_pdf_en_memoria
from .models import Comprobantes, Tareas,AdministradoresConsorcio, Bancos
from django.db import transaction,models
from django.db.models import F
import json
@csrf_exempt
def vista(request):
    if request.method == 'GET':
                return HttpResponse("<h1><font color='blue'>¡Hola desde la API de Django!</font></h1>") 
    elif request.method == 'POST':
                return HttpResponse("<h1><font color='green'>¡Hola desde la API de Django! (POST)</font></h1>") 
    else:   
                return HttpResponse("<h1><font color='red'>Método no permitido</font></h1>", status=405)
    
######clase para generar PDF
class DescargarReportePDFView(APIView):
    def post(self, request):
            # Recibís los 3 datos del JSON
            ticker = request.data.get('ticker')
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')

            if not all([ticker, start_date, end_date]):
                return Response({"error": "Faltan datos"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Instanciás / llamás a la utilidad para que te devuelva el PDF en memoria
                pdf_buffer = generar_pdf_en_memoria(ticker, start_date, end_date)

                # Devolvés el FileResponse desde la vista
                return FileResponse(
                    pdf_buffer, 
                    as_attachment=True, 
                    filename=f"reporte_{ticker}.pdf",
                    content_type='application/pdf'
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
##orm
def listar_tareas_view(request):
    # Consultamos todos los registros de la tabla tareas con el ORM
    datos = list(Tareas.objects.filter(titulo__icontains="OSDE").values())
    return JsonResponse(datos, safe=False)
###listar administradores por parte del nombre
def buscar_administradores_por_nombre(request, nombre):
    # Consultamos todos los registros de la tabla administradores_consorcio con el ORM
    datos = list(AdministradoresConsorcio.objects.filter(nombre__icontains=nombre).values())
    return JsonResponse(datos, safe=False)
###listar nombre administrador y nombre del banco
@csrf_exempt
def listar_administradores_con_banco(request):
    # Consultamos todos los registros de la tabla administradores_consorcio con el ORM
    datos = list(AdministradoresConsorcio.objects.select_related('banco_codigo').values(
            nombre_admin=F('nombre'),                  # Renombras 'nombre' a 'nombre_admin'
            banco=F('banco_codigo__nombre'),           # Renombras 'banco_codigo__nombre' a 'banco'
            direccion_banco=F('banco_codigo__direccion')
    ))
    return JsonResponse(datos, safe=False)
##########listado de cantidad de administradores por Banco
def cantidad_administradores_por_banco(request):
    # Consultamos todos los registros de la tabla administradores_consorcio con el ORM
    datos = list(AdministradoresConsorcio.objects.values('banco_codigo__nombre').annotate(cantidad=models.Count('id')).order_by('-cantidad'))
    return JsonResponse(datos, safe=False)
########obtengo mediante orm un administrador por matricula
def obtener_administrador_por_matricula(request, matricula):
    try:
        admin = AdministradoresConsorcio.objects.select_related('banco_codigo').get(matricula=matricula)
        datos = {
            "id": admin.id,
            "matricula": admin.matricula,
            "nombre": admin.nombre,
            "fecha_inscripcion": admin.fecha_inscripcion,
            "oneroso": admin.oneroso,
            "correo": admin.correo,
            "sanciones": admin.sanciones,
            "banco_id": admin.banco_codigo_id,
            "nombre_banco": admin.banco_codigo.nombre if admin.banco_codigo else None
        }
        return JsonResponse(datos, safe=False)
    except AdministradoresConsorcio.DoesNotExist:
        return JsonResponse({"error": "Administrador no encontrado"}, status=404)

#####hago un update de adminsitrador por id
@csrf_exempt
def actualizar_administrador(request, admin_id):
    if request.method == 'PUT' or request.method == 'POST':
        try:
            data = json.loads(request.body)
            admin = AdministradoresConsorcio.objects.get(id=admin_id)

            # Actualizamos los campos según los datos recibidos
            admin.matricula = data.get('matricula', admin.matricula)
            admin.nombre = data.get('nombre', admin.nombre)
            admin.fecha_inscripcion = data.get('fecha_inscripcion', admin.fecha_inscripcion)
            admin.oneroso = data.get('oneroso', admin.oneroso)
            admin.correo = data.get('correo', admin.correo)
            admin.sanciones = data.get('sanciones', admin.sanciones)
            admin.banco_codigo_id = data.get('banco_codigo', admin.banco_codigo_id)

            admin.save()
            return JsonResponse({"status": "success", "mensaje": "Administrador actualizado con éxito."})
        except AdministradoresConsorcio.DoesNotExist:
            return JsonResponse({"status": "error", "mensaje": "Administrador no encontrado."}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "mensaje": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error", "mensaje": "Método no permitido."}, status=405)
@csrf_exempt
###eliminar un administrador por id
def eliminar_administrador(request, admin_id):
    if request.method == 'DELETE':
        try:
            admin = AdministradoresConsorcio.objects.get(id=admin_id)
            admin.delete()
            return JsonResponse({"status": "success", "mensaje": "Administrador eliminado con éxito."})
        except AdministradoresConsorcio.DoesNotExist:
            return JsonResponse({"status": "error", "mensaje": "Administrador no encontrado."}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "mensaje": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error", "mensaje": "Método no permitido."}, status=405)

@csrf_exempt
###inserto por json un administrador
def insertar_administrador(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nuevo_admin = AdministradoresConsorcio(
                matricula=data['matricula'],
                nombre=data['nombre'],
                fecha_inscripcion=data['fecha_inscripcion'],
                oneroso=data['oneroso'],
                correo=data.get('correo', ''),
                sanciones=data.get('sanciones', ''),
                banco_codigo_id=data.get('banco_codigo')  # Asegurate de que el ID del banco esté presente
            )
            nuevo_admin.save()
            return JsonResponse({"status": "success", "mensaje": "Administrador insertado con éxito."})
        except Exception as e:
            return JsonResponse({"status": "error", "mensaje": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error", "mensaje": "Método no permitido."}, status=405)



##########importación de excel a neon
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt # Opcional si querés probar rápido con curl sin mandar token CSRF
def subir_excel_curl(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        excel_file = request.FILES['archivo']
        
        try:
            # Leemos el Excel directamente desde la memoria con Pandas
            df = pd.read_excel(excel_file)
            
            # Limpiamos columnas rápido
            df.columns = ['matricula', 'nombre', 'fecha_inscripcion', 'oneroso', 'correo', 'sanciones']
            
            # Acá harías la inserción o procesamiento que necesites
            total_registros = len(df)
            
            return JsonResponse({
                "status": "success",
                "mensaje": f"¡Archivo procesado con éxito!",
                "total_registros": total_registros,
                "primeros_3": df.head(3).to_dict(orient='records')
            }, safe=False)
            
        except Exception as e:
            return JsonResponse({"status": "error", "mensaje": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "mensaje": "Mandá un archivo válido con la key 'archivo'"}, status=400)

@csrf_exempt
def subir_excel_a_db(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        excel_file = request.FILES['archivo']
        
        try:
            # Leer el Excel con Pandas
            df = pd.read_excel(excel_file)
            df.columns = ['matricula', 'nombre', 'fecha_inscripcion', 'oneroso', 'correo', 'sanciones']
            df['correo'] = df['correo'].fillna('')
            
            # Usamos una transacción atómica para asegurar commit o rollback global
            with transaction.atomic():
                objetos_a_crear = []
                for _, row in df.iterrows():
                    # Evitamos duplicados o preparamos el objeto
                    objetos_a_crear.append(
                        AdministradoresConsorcio(
                            matricula=row['matricula'],
                            nombre=row['nombre'],
                            fecha_inscripcion=row['fecha_inscripcion'],
                            oneroso=str(row['oneroso']),
                            correo=str(row['correo']),
                            sanciones=str(row['sanciones'])
                        )
                    )
                
                # Bulk create ignorando duplicados o actualizando (según prefieras)
                # Django permite ignore_conflicts en Postgres
                AdministradoresConsorcio.objects.bulk_create(
                    objetos_a_crear, 
                    ignore_conflicts=True
                )
            
            return JsonResponse({
                "status": "success",
                "mensaje": f"¡Se procesaron e insertaron {len(objetos_a_crear)} registros en Neon con éxito!"
            })
            
        except Exception as e:
            # Si algo falla, la transacción hace rollback automático
            return JsonResponse({"status": "error", "mensaje": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "mensaje": "Enviá un archivo válido."}, status=400)