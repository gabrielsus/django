from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def vista(request):
    if request.method == 'GET':
                return HttpResponse("<h1><font color='blue'>¡Hola desde la API de Django!</font></h1>") 
    elif request.method == 'POST':
                return HttpResponse("<h1><font color='green'>¡Hola desde la API de Django! (POST)</font></h1>") 
    else:   
                return HttpResponse("<h1><font color='red'>Método no permitido</font></h1>", status=405)
    