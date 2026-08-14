from google import genai
import re
import os
import io
import matplotlib
matplotlib.use('Agg')  # Usar un backend sin GUI para generar gráficos en memoria
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import traceback
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from yfinance import download
###LIMPIEZA DE TEXTO PARA REPORTLAB
def limpiar_markdown_para_reportlab(texto):
  # Reemplaza **texto** por <b>texto</b>
  texto = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texto)

  # Limpia los encabezados tipo ### o --- si los trae el texto de la IA
  texto = re.sub(r'---', '', texto)
  texto = re.sub(r'#{1,6}\s?', '', texto)

  return texto

#####importo analisis AI google genai
def generarReporte(data):
  client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

  # Prompt estructurado pidiendo saltos de línea y análisis web
  prompt = (
      f"Haceme un análisis técnico y financiero completo de la evolución de"
      f" este ticker basándote en este dataframe: {data}. "
      "Busca también en la web información reciente sobre el contexto actual"
      " de este activo y su mercado. "
      "IMPORTANTE: Redactá la respuesta estructurada en párrafos claros."
      " Utilizá saltos de línea dobles (\\n\\n) para separar cada párrafo o"
      " sección y evitar bloques de texto largos."
  )


  try:
      response = client.models.generate_content(
      model="gemini-3.5-flash-lite",  # Ajustado al modelo estándar actual de la SDK
      contents=prompt,
  )
  except Exception as e:
    print(f"Error al generar el reporte: {e}")
    traceback.print_exc()
    return "Error al generar el reporte."
  return response.text
####PLOTEO DE DATAFRAME
def generar_plot_en_memoria(data, ticker_symbol):
  if data.empty:
    return None

  plt.figure(figsize=(7, 3.5), dpi=200)
  plt.plot(
      data.index,
      data['Close'],
      color="#0a83fd",
      linewidth=2,
      label='Cierre',
  )

  # Título y etiquetas con tamaño controlado
  plt.title(
      f'Precio de Cierre de {ticker_symbol}',
      fontsize=12,
      fontweight='bold',
      pad=10,
  )
  plt.xlabel('Fecha', fontsize=10)
  plt.ylabel('Cierre', fontsize=10)

  # --- AJUSTES DE FECHA Y LETRA EN LOS EJES ---
  ax = plt.gca()

  # Frecuencia de las marcas (ej: cada 1 o 2 semanas según el rango, o mensual con MonthLocator)
  ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)
  )  # O MonthLocator()

  # Formato reducido a MM/YY como querías
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))

  # Achicar la letra de los números de los ejes X e Y
  ax.tick_params(axis='x', labelsize=8)
  ax.tick_params(axis='y', labelsize=8)

  # Rotar levemente por las dudas
  plt.xticks(rotation=0, ha='center')
  # --------------------------------------------

  plt.grid(True, linestyle='--', alpha=0.5)
  plt.legend(loc='upper left', fontsize=9)
  plt.tight_layout()

  buffer = io.BytesIO()
  plt.savefig(buffer, format='png')
  plt.close()
  buffer.seek(0)
  return buffer

#######generación de PDF con ReportLab
def generar_pdf_en_memoria(ticker, start_date, end_date):
    # 1. Obtenemos los datos de Yahoo Finance
    data = download(ticker, start=start_date, end=end_date)
    
    if data is None or data.empty:
        raise ValueError(f"No se pudieron obtener datos para el ticker {ticker}")

    # 2. Generamos el análisis con Gemini en base al texto de los datos
    analisis = generarReporte(data.to_string()) if data is not None else "No se pudo generar el análisis."

    # 3. Creamos un búfer de bytes en memoria (RAM)
    buffer = io.BytesIO()

    # 4. Configuramos el SimpleDocTemplate para que escriba en el búfer
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Título principal
    story.append(Paragraph(f"Reporte de Precios de Acciones: {ticker}", styles['Title']))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph(f"Datos procesados desde {start_date} hasta {end_date}.", styles['Normal']))
    story.append(Spacer(1, 12))

    # Generamos el gráfico en memoria
    buffer_plot = generar_plot_en_memoria(data, ticker)
    if buffer_plot is not None:
        imagen_plot = Image(buffer_plot, width=150*mm, height=100*mm, kind='proportional', hAlign='CENTER')
        story.append(Paragraph(f"Gráfico de Cierre de {ticker}", styles['Heading2']))
        story.append(Spacer(1, 12))
        story.append(imagen_plot)
        story.append(Spacer(1, 12))

    # Agregamos el análisis de la IA formateado para ReportLab (cambiando saltos de línea por <br/>)
    if analisis:
        texto_limpio = limpiar_markdown_para_reportlab(analisis)
        texto_formateado = texto_limpio.replace('\n', '<br/>')
        story.append(Paragraph(texto_formateado, styles['Normal']))

    # Definimos la función para el pie de página
    def datosfijos(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont('Helvetica', 10)
        canvas.drawString(10 * mm, 10 * mm, "Página %d" % (doc_obj.page))
        canvas.restoreState()

    # 5. Construimos el PDF dentro del búfer
    doc.build(story, onFirstPage=datosfijos, onLaterPages=datosfijos)

    # 6. Devolvemos el puntero del búfer al inicio para que Django pueda leerlo
    buffer.seek(0)
    
    return buffer