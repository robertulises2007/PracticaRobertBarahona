from django.urls import path
from . import views, auth_views

urlpatterns = [
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    # CRUD Roles
    path('roles/', views.roles_list, name='roles_list'),
    path('roles/create/', views.roles_create, name='roles_create'),
    path('roles/update/<int:id>/', views.roles_update, name='roles_update'),
    path('roles/delete/<int:id>/', views.roles_delete, name='roles_delete'),

    # CRUD Contactos
    path('contactos/', views.contactos_list, name='contactos_list'),
    path('contactos/create/', views.contactos_create, name='contactos_create'),
    path('contactos/update/<int:id>/', views.contactos_update, name='contactos_update'),
    path('contactos/delete/<int:id>/', views.contactos_delete, name='contactos_delete'),


    path('conversaciones/', views.conversaciones_list, name='conversaciones_list'),
    path('conversaciones/editar/<int:id>/', views.conversaciones_update, name='conversaciones_update'),
    path('conversaciones/eliminar/<int:id>/', views.conversaciones_delete, name='conversaciones_delete'),
    path('conversaciones/<int:conversacion_id>/mensajes/', views.mensajes_view, name='mensajes_view'),

    # CRUD Campañas
    path('campanias/', views.campanias_list, name='campanias_list'),
    path('campanias/create/', views.campanias_create, name='campanias_create'),
    path('campanias/update/<int:id>/', views.campanias_update, name='campanias_update'),
    path('campanias/delete/<int:id>/', views.campanias_delete, name='campanias_delete'),
    path('campanias/preview/<int:id>/', views.campanias_preview, name='campanias_preview'),

]
