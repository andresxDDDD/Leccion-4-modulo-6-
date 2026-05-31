
from django.shortcuts import render
from .forms import ContactoForm


def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Aquí procesarías los datos (ej: enviar email, guardar en BD, etc.)
            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['correo']
            mensaje = form.cleaned_data['mensaje']

            # Por ahora solo mostramos un mensaje de éxito
            return render(request, 'contacto_exito.html', {
                'nombre': nombre,
            })
    else:
        form = ContactoForm()

    return render(request, 'contacto.html', {
        'form': form,
    })
