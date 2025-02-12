from django.urls import path
from . import views

app_name = 'cadastros'

urlpatterns = [

    #CADASTRO DE DEPARTAMENTO
    path('departamentos/', views.departamentos, name='departamentos'),
    path('obter_departamento_por_id/', views.obter_departamento_por_id, name='obter_departamento_por_id'),
    path('excluir_departamento/', views.excluir_departamento, name='excluir_departamento'),
    path('pesquisar_departamento_por_nome/', 
         views.pesquisar_departamento_por_nome, 
         name='pesquisar_departamento_por_nome'
         ),

    #-------------------------------------------------------------------------------------------------------------

]