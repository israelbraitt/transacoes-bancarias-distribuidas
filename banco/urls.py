from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('conta', views.conta, name="conta"),
    path('transferencia', views.form_transferencia, name="transferencia"),
    path('efetuar_transferencia', views.efetuar_transferencia, name="efetuar"),
    path('notificar', views.notificar, name="notificar")
]