from django.shortcuts import render, redirect, get_object_or_404
from .models import Campania, Rol, Contacto, Mensaje, Conversacion
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q
# ¡Importa los formularios que acabamos de crear!
from .forms import CampaniaForm, RoleForm, ContactoForm, MensajeForm


# ---------- ROLES ----------
@login_required
@never_cache
def roles_list(request):
    roles = Rol.objects.all()
    # Esta vista funciona bien, renderiza la plantilla de la lista
    return render(request, 'roles_list.html', {'roles': roles})

@login_required
@never_cache
def roles_create(request):
    if request.method == 'POST':
        # Procesamos el formulario enviado
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save() # Guarda el nuevo rol
            return redirect('roles_list')
        # Si el formulario NO es válido, se volverá a renderizar abajo con los errores
    else:
        # Petición GET: creamos un formulario vacío
        form = RoleForm()
    
    # Mostramos la plantilla del formulario (roles_form.html)
    # y le pasamos el formulario (vacío o con errores)
    return render(request, 'roles_form.html', {'form': form})

@login_required
@never_cache
def roles_update(request, id):
    # Obtenemos el objeto que queremos editar
    rol = get_object_or_404(Rol, id=id)
    
    if request.method == 'POST':
        # Procesamos el formulario enviado, pasándole la 'instance'
        # para que sepa qué objeto actualizar
        form = RoleForm(request.POST, instance=rol)
        if form.is_valid():
            form.save() # Guarda los cambios
            return redirect('roles_list')
        # Si no es válido, se renderizará de nuevo con errores
    else:
        # Petición GET: creamos un formulario pre-llenado
        # con los datos de la 'instance'
        form = RoleForm(instance=rol)
    
    # Mostramos la plantilla del formulario (roles_form.html)
    # y le pasamos el formulario (pre-llenado o con errores)
    return render(request, 'roles_form.html', {'form': form})

@login_required
@never_cache
def roles_delete(request, id):
    # Esta vista está bien, solo acepta POST (desde el formulario de la lista)
    rol = get_object_or_404(Rol, id=id)
    if request.method == 'POST': # Buena práctica añadir esta comprobación
        rol.delete()
    return redirect('roles_list')


# ---------- CONTACTOS ----------
@login_required
@never_cache
def contactos_list(request):
    query = request.GET.get('q')
    if query:
        contactos = Contacto.objects.filter(
            Q(nombre__icontains=query) |  # busca coincidencias en el nombre
            Q(correo__icontains=query) |  # opcional: busca también por correo
            Q(telefono__icontains=query)  # opcional: busca también por teléfono
        ).order_by('-fecha_modificacion')
    else:
        contactos = Contacto.objects.all().order_by('-fecha_modificacion')

    context = {
        'contactos': contactos,
        'query': query,  # para mantener el texto en el input
    }
    return render(request, 'contactos_list.html', context)

@login_required
@never_cache
def contactos_create(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contactos_list')
    else:
        # GET: Creamos un formulario vacío
        form = ContactoForm()
    
    # Renderizamos la plantilla del formulario de contacto
    return render(request, 'contactos_form.html', {'form': form})

@login_required
@never_cache
def contactos_update(request, id):
    contacto = get_object_or_404(Contacto, id=id)
    
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect('contactos_list')
    else:
        # GET: Creamos el formulario pre-llenado
        form = ContactoForm(instance=contacto)
    
    # Renderizamos la plantilla del formulario de contacto
    return render(request, 'contactos_form.html', {'form': form})

@login_required
@never_cache
def contactos_delete(request, id):
    contacto = get_object_or_404(Contacto, id=id)
    if request.method == 'POST':
        contacto.delete()
    return redirect('contactos_list')

from .models import Conversacion
from .forms import ConversacionForm
from django.utils import timezone

@login_required
@never_cache
def conversaciones_list(request):
    conversaciones = Conversacion.objects.select_related('contacto', 'conversacion_anterior').all()
    return render(request, 'conversaciones_list.html', {'conversaciones': conversaciones})

@login_required
@never_cache
def conversaciones_update(request, id):
    conversacion = get_object_or_404(Conversacion, id=id)
    if request.method == 'POST':
        form = ConversacionForm(request.POST, instance=conversacion)
        if form.is_valid():
            form.save()
            return redirect('conversaciones_list')
    else:
        form = ConversacionForm(instance=conversacion)
    return render(request, 'conversaciones_form.html', {'form': form})

@login_required
@never_cache
def conversaciones_delete(request, id):
    conversacion = get_object_or_404(Conversacion, id=id)
    if request.method == 'POST':
        conversacion.delete()
    return redirect('conversaciones_list')


@login_required
@never_cache
def mensajes_view(request, conversacion_id):
    conversacion = get_object_or_404(Conversacion, id=conversacion_id)
    mensajes = conversacion.mensajes.all()

    # Formulario para enviar mensajes
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.conversacion = conversacion
            mensaje.remitente = 'bot'
            mensaje.save()


            # Actualizamos último mensaje y contador
            conversacion.ultimo_mensaje = timezone.now()
            conversacion.mensajes_enviados = conversacion.mensajes.filter(remitente='usuario').count()
            conversacion.save()

            return redirect('mensajes_view', conversacion_id=conversacion.id)
    else:
        form = MensajeForm()

    return render(request, 'mensajes.html', {
        'conversacion': conversacion,
        'mensajes': mensajes,
        'form': form
    })


@login_required
@never_cache
def campanias_list(request):
    campanias = Campania.objects.all().order_by('-fechaCreacion')
    return render(request, 'campanias_list.html', {'campanias': campanias})

@login_required
@never_cache
def campanias_create(request):
    if request.method == 'POST':
        form = CampaniaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('campanias_list')
    else:
        form = CampaniaForm()
    return render(request, 'campanias_form.html', {'form': form})

@login_required
@never_cache
def campanias_update(request, id):
    campania = get_object_or_404(Campania, id=id)
    if request.method == 'POST':
        form = CampaniaForm(request.POST, request.FILES, instance=campania)
        if form.is_valid():
            form.save()
            return redirect('campanias_list')
    else:
        form = CampaniaForm(instance=campania)
    return render(request, 'campanias_form.html', {'form': form})

@login_required
@never_cache
def campanias_delete(request, id):
    campania = get_object_or_404(Campania, id=id)
    if request.method == 'POST':
        campania.delete()
        return redirect('campanias_list')

@login_required
@never_cache
def campanias_preview(request, id):
    campania = get_object_or_404(Campania, id=id)
    return render(request, 'campanias_preview.html', {'campania': campania})
