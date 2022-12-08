import xlwt
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.shortcuts import render, redirect
from registration.models import *
from django.http import HttpResponseRedirect, HttpResponse
import reportlab


# problem corverting datefield in string
def export_orders(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="buyurtmalar.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Buyurtmalar')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = [ 
                'FISH',
                'Manzili', 
                'Telefon raqami',
                'Simkarta turi',
                "Sovg'a turi",
                'Simkarta narxi',
                'Sana'
                ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 
    font_style = xlwt.XFStyle()
    orders = SimOrder.objects.all()
    for o in orders:
        sim_types = o.sim_type.sim_option
        gifts = o.gift.name
        added_dates = str(o.added_date)
    rows = SimOrder.objects.all().values_list(
        'full_name',
        'address', 
        'tel_number', 
        'sim_type__sim_option', 
        'gift__name',
        'sim_cost',
        'added_date',
          )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def generatePDF(request):
    buffer = io.BytesIO()
    orders = SimOrder.objects.all()
    x = canvas.Canvas(buffer)
    x.drawString(100, 100, "some text")
    x.showPage()
    x.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='orders.pdf')