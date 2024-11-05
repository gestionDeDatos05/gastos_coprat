from django.shortcuts import render, redirect
from Aplicacion.models import *
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum

def actualizarProyecto(request):
    id = request.POST['id'] # CAMPO id
    categoria = request.POST['categoria'].upper() # CAMPO Folio
    pago = request.POST['pago'] # CAMPO cliente
    factura = request.POST['factura'] # CAMPO estatus
    monto = request.POST['monto'].upper() # CAMPO proyecto
    descripcion = request.POST['descripcion'] # CAMPO descripcion
    proveedor = request.POST['proveedor'] # CAMPO fechaInicio
    fecha = request.POST['fecha'] # CAMPO fechaFinal
    
    actualizarDetalleProyecto = tblProyecto.objects.get(ID=id)
    categoria_instancia = tblCategoriaGasto.objects.get(ID=categoria)
    formaPago_instancia = tblFormaPago.objects.get(ID=pago)
    # actualizarDetalleProyecto.IDProyecto = categoria_instancia
    actualizarDetalleProyecto.IDFormaDePago = formaPago_instancia
    actualizarDetalleProyecto.IDCategoria = categoria_instancia
    actualizarDetalleProyecto.Monto = monto
    actualizarDetalleProyecto.Factura = factura
    actualizarDetalleProyecto.Proveedor = proveedor
    actualizarDetalleProyecto.Descripcion = descripcion
    actualizarDetalleProyecto.Fecha = fecha
    actualizarDetalleProyecto.save()
    messages.success(request, f'El proyecto con el folio "{factura}" se ha actualizado exitosamente.')

    #  DATOS PARA REGRESAR AL TEMPLATE DE PROYECTOS
    id_Proyecto = request.POST['idProyecto'] # CAMPO id
    cliente = request.POST['cliente'] # CAMPO cliente
    proyecto = request.POST['proyecto'].upper() # CAMPO proyecto
    folio = request.POST['folio'] # CAMPO folio
    descripcion = request.POST['descripcion'] # CAMPO descripcion
    
    fecha_actual = datetime.now().date()
    fecha_formateada = fecha_actual.strftime('%Y-%m-%d') 
    selectPago = tblFormaPago.objects.all()
    selectCategoria = tblCategoriaGasto.objects.all()
    context = {'id':id_Proyecto, 'cliente': cliente, 'folio': folio, 'proyecto': proyecto, 'descripcion':descripcion}

    detalleProyecto = tblProyecto.objects.filter(IDProyecto = id_Proyecto).values("ID", "IDProyecto_id__Folio", "IDFormaDePago_id__Descripcion", 
                                "IDCategoria_id__Descripcion", "Monto", "Factura", "Descripcion", "Proveedor", "Fecha")
    
    proveedor = tblProyecto.objects.values("Proveedor").distinct()

    montoXCategoria = tblProyecto.objects.values('IDProyecto_id', 'IDCategoria_id__Descripcion').annotate(total_monto=Sum('Monto'))
    montoXPago = tblProyecto.objects.values('IDProyecto_id', 'IDFormaDePago_id__Descripcion').annotate(total_monto=Sum('Monto'))

        
    return render(request, 'Proceso/Gastos/index.html', {"context": context, 'selectPago':selectPago, 'selectCategoria':selectCategoria, 
    'fecha_actual':fecha_formateada, 'detalleProyecto':detalleProyecto, 'montoXCategoria':montoXCategoria,'montoXPago':montoXPago,
    'proveedor':proveedor})
    
# def datos_seleccionado_proyecto(request):
#     #  DATOS PARA REGRESAR AL TEMPLATE DE PROYECTOS
#     id_Proyecto = request.POST['idProyecto'] # CAMPO id
#     cliente = request.POST['cliente'] # CAMPO cliente
#     proyecto = request.POST['proyecto'].upper() # CAMPO proyecto
#     folio = request.POST['folio'] # CAMPO folio
#     descripcion = request.POST['descripcion'] # CAMPO descripcion
    
#     fecha_actual = datetime.now().date()
#     fecha_formateada = fecha_actual.strftime('%Y-%m-%d') 
#     selectPago = tblFormaPago.objects.all()
#     selectCategoria = tblCategoriaGasto.objects.all()
#     context = {'id':id_Proyecto, 'cliente': cliente, 'folio': folio, 'proyecto': proyecto, 'descripcion':descripcion}
#     print(context)
#     detalleProyecto = tblProyecto.objects.filter(IDProyecto = id_Proyecto).values("ID", "IDProyecto_id__Folio", "IDFormaDePago_id__Descripcion", 
#                                 "IDCategoria_id__Descripcion", "Monto", "Factura", "Descripcion", "Proveedor", "Fecha")
    
#     proveedor = tblProyecto.objects.values("Proveedor").distinct()

#     montoXCategoria = tblProyecto.objects.values('IDProyecto_id', 'IDCategoria_id__Descripcion').annotate(total_monto=Sum('Monto'))
#     montoXPago = tblProyecto.objects.values('IDProyecto_id', 'IDFormaDePago_id__Descripcion').annotate(total_monto=Sum('Monto'))