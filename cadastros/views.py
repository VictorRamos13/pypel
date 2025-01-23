from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q, F, Count, Subquery, OuterRef, FloatField, Sum, ExpressionWrapper
from .models import Usuario, Perfil, Departamento
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

#CADASTRO DE DEPARTAMENTOS
@login_required #tem que estar logada para carregar a view
def departamentos(request):

    #pega a sessao atual do cara e ve se entrou com o perfil errado
    if request.session.get('perfil_atual') not in {'Administrador'}:
        messages.error(request, 'Você não é administrador!')
        return redirect('core:main') #main é uma view que ta dentro de core
    
    if request.method == 'POST':
        messages.success(request, 'Implementar depois!')
        #Alguma coisa
    
    #traz todos os departamentos cadastrados do sistema menos o "geral" e ordena pelo nome
    departamento_lista = Departamento.objects.all().exclude(nome__iexact="Geral").order_by('nome')

    paginator = Paginator(departamento_lista, settings.NUMBER_GRID_PAGES) #cria o numero de paginas com esse tamanho
    numero_pagina = request.GET.get('page')#pega em qual pagina esta, porque a cada pagina a 'sessao muda'
    page_obj = paginator.get_page(numero_pagina)

    return render(request, 'departamentos.html', {'page_obj': page_obj})
    