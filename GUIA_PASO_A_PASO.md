# Guía Paso a Paso — Formularios con Django

> **Actividad N°4:** Creación y Manejo de Formularios con Django  
> **App:** `contacto` | **Proyecto:** `config`

---

## 1. Requisitos previos

- Python 3.8+ instalado
- `pip` disponible
- Git (opcional)

Verifica con:
```bash
python --version
pip --version
```

---

## 2. Crear entorno virtual e instalar Django

Dentro de la carpeta del repositorio:

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# Instalar Django
pip install django
```

---

## 3. Crear el proyecto Django

```bash
django-admin startproject config .
```

El `.` al final evita que se cree una subcarpeta extra. La estructura queda:

```
config/
  __init__.py
  asgi.py
  settings.py
  urls.py
  wsgi.py
manage.py
venv/
```

---

## 4. Crear la app `contacto`

```bash
python manage.py startapp contacto
```

Ahora aparece la carpeta `contacto/`:

```
contacto/
  __init__.py
  admin.py
  apps.py
  migrations/
  models.py
  tests.py
  views.py
```

### 4.1 Registrar la app en `settings.py`

Abre `config/settings.py` y agrega `'contacto'` en `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'contacto',  # <-- Agregar aquí
]
```

---

## 5. Configurar templates

### 5.1 Crear carpeta `templates/`

En la raíz del proyecto (junto a `manage.py`):

```bash
mkdir templates
```

### 5.2 Indicarle a Django dónde buscar templates

En `config/settings.py`, busca `TEMPLATES` y modifica el `DIRS`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # <-- Agregar esta línea
        'APP_DIRS': True,
        ...
    },
]
```

---

## 6. Crear la plantilla base `base.html`

Crea el archivo `templates/base.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mi Sitio{% endblock %}</title>
</head>
<body>
    <header>
        <h1>Mi Aplicación Django</h1>
        <nav>
            <a href="{% url 'contacto' %}">Contacto</a>
        </nav>
        <hr>
    </header>

    <main>
        {% block content %}
        {% endblock %}
    </main>

    <footer>
        <hr>
        <p>&copy; 2026 - Mi Proyecto Django</p>
    </footer>
</body>
</html>
```

---

## 7. Crear el formulario `ContactoForm`

Crea o edita `contacto/forms.py`:

```python
from django import forms


class ContactoForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Tu nombre'})
    )
    correo = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'tu@correo.com'})
    )
    mensaje = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea(attrs={'placeholder': 'Escribe tu mensaje aquí...', 'rows': 5})
    )

    def clean_mensaje(self):
        """Valida que el mensaje tenga al menos 10 caracteres."""
        mensaje = self.cleaned_data.get('mensaje', '')
        if len(mensaje) < 10:
            raise forms.ValidationError('El mensaje debe tener al menos 10 caracteres.')
        return mensaje
```

---

## 8. Crear la vista

Edita `contacto/views.py`:

```python
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
```

---

## 9. Crear el template `contacto.html`

Crea `templates/contacto.html`:

```html
{% extends "base.html" %}

{% block title %}Contacto{% endblock %}

{% block content %}
    <h2>Formulario de Contacto</h2>

    <form method="post" action="{% url 'contacto' %}">
        {% csrf_token %}

        <p>
            {{ form.nombre.label_tag }}<br>
            {{ form.nombre }}
            {% if form.nombre.errors %}
                <span style="color: red;">{{ form.nombre.errors }}</span>
            {% endif %}
        </p>

        <p>
            {{ form.correo.label_tag }}<br>
            {{ form.correo }}
            {% if form.correo.errors %}
                <span style="color: red;">{{ form.correo.errors }}</span>
            {% endif %}
        </p>

        <p>
            {{ form.mensaje.label_tag }}<br>
            {{ form.mensaje }}
            {% if form.mensaje.errors %}
                <span style="color: red;">{{ form.mensaje.errors }}</span>
            {% endif %}
        </p>

        <button type="submit">Enviar</button>
    </form>
{% endblock %}
```

### 9.1 Template de éxito

Crea `templates/contacto_exito.html`:

```html
{% extends "base.html" %}

{% block title %}Mensaje Enviado{% endblock %}

{% block content %}
    <h2>¡Gracias por contactarnos!</h2>
    <p>Hola <strong>{{ nombre }}</strong>, hemos recibido tu mensaje. Te responderemos pronto.</p>
    <a href="{% url 'contacto' %}">Enviar otro mensaje</a>
{% endblock %}
```

---

## 10. Configurar las URLs

### 10.1 Crear `contacto/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.contacto, name='contacto'),
]
```

### 10.2 Incluir las URLs en el proyecto

Edita `config/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include  # <-- Agregar include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contacto/', include('contacto.urls')),  # <-- Agregar esta línea
]
```

Ahora la URL completa será: `http://127.0.0.1:8000/contacto/`

---

## 11. Probar la aplicación

### 11.1 Migraciones

```bash
python manage.py migrate
```

### 11.2 Ejecutar el servidor

```bash
python manage.py runserver
```

### 11.3 Navegar al formulario

Abre en tu navegador: [http://127.0.0.1:8000/contacto/](http://127.0.0.1:8000/contacto/)

### 11.4 Probar validaciones

1. Deja el campo **mensaje** con menos de 10 caracteres y envía.
2. Deberías ver el error en rojo debajo del campo.
3. Completa todos los campos correctamente y envía.
4. Deberías ver la página de éxito.

---

## 12. Resumen de la estructura final

```
/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py          # Incluye contacto.urls
│   ├── asgi.py
│   └── wsgi.py
├── contacto/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py          # ContactoForm
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py           # Ruta → contacto/
│   └── views.py          # Vista contacto()
├── templates/
│   ├── base.html         # Plantilla base
│   ├── contacto.html     # Formulario
│   └── contacto_exito.html  # Confirmación
├── manage.py
├── GUIA_PASO_A_PASO.md
└── venv/
```

---

## Bonus: usar `form.as_p` en lugar de renderizado manual

Si quieres ahorrar líneas, puedes reemplazar el contenido de `contacto.html` con:

```html
{% extends "base.html" %}

{% block title %}Contacto{% endblock %}

{% block content %}
    <h2>Formulario de Contacto</h2>

    <form method="post" action="{% url 'contacto' %}">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Enviar</button>
    </form>
{% endblock %}
```

`form.as_p` envuelve cada campo en un `<p>` y ya incluye labels, inputs y errores. Es más rápido pero da menos control sobre el HTML.

---

## Posibles errores y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'contacto'` | App no registrada | Agrega `'contacto'` en `INSTALLED_APPS` |
| `TemplateDoesNotExist` | Ruta de templates mal configurada | Verifica `DIRS` en `TEMPLATES` |
| `Reverse for 'contacto' not found` | URL name incorrecto | Verifica `name='contacto'` en `urls.py` |
| `CSRF token missing` | Falta `{% csrf_token %}` en el form | Agrega el tag dentro del `<form>` |

---

> **¡Listo!** Has creado un formulario Django con validación personalizada, herencia de plantillas, y manejo de errores en el frontend.
