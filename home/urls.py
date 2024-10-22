from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.index, name='Index'),
    path('autores/', views.autores, name='autores'),
    path('contenido/',views.contenido, name='contenido'),
    path('contenido/<int:id>', views.visualizar, name='visualizar'),
    path('contenido/agregar', views.agregar, name="agregar"),
    path('validacion/', views.validacion, name='validacion'),
    path('clear-session/', views.clear_session, name='clear_session')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)