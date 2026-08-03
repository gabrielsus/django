from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import generar_pdf_en_memoria
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