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
        acao = request.POST.get('btnAcao')

        if acao == 'novo_departamento':
            nome = request.POST.get('txtName')

            if (nome == 'Geral'):
                messages.error(request, 'Cadastre outro nome, seu Animal!')
                return redirect('cadastros:departamentos')

            sigla = request.POST.get('txtSigla')

            if Departamento.objects.filter(nome=nome).exists(): #se existir algum departamento com o nome que o usuario digitou
                messages.error(request, 'Já existe um departamento com esse nome!')
                return redirect('cadastros:departamentos')
            
            departamento = Departamento(
                nome=nome,
                sigla=sigla
            )
            departamento.save()

            messages.success(request, 'Departamento cadastrado com sucesso!')
            return redirect('cadastros:departamentos')
        
        elif acao == 'alterar_departamento':
            departamento_id = request.POST.get('txtId')

            #pega tudo do banco sobre o departamento com base no id
            departamento = Departamento.objects.get(id=departamento_id)

            nome = request.POST.get('txtName')
            
            if (nome == 'Geral' or Departamento.objects.filter(nome=nome).exists()):
                    messages.error(request, 'Cadastre outro nome, seu Animal!')
                    return redirect('cadastros:departamentos')
            
            sigla = request.POST.get('txtSigla')

            departamento.nome = nome
            departamento.sigla = sigla
            departamento.save()

            messages.success(request, 'Departamento alterado com sucesso!')
            return redirect('cadastros:departamentos')

    
    #traz todos os departamentos cadastrados do sistema menos o "geral" e ordena pelo nome
    departamento_lista = Departamento.objects.all().exclude(nome__iexact="Geral").order_by('nome')

    paginator = Paginator(departamento_lista, settings.NUMBER_GRID_PAGES) #cria o numero de paginas com esse tamanho
    numero_pagina = request.GET.get('page')#pega em qual pagina esta, porque a cada pagina a 'sessao muda'
    page_obj = paginator.get_page(numero_pagina)

    return render(request, 'departamentos.html', {'page_obj': page_obj})

@login_required
def obter_departamento_por_id(request):
    departamento_id = request.GET.get('departamento_id', None)

    #selecione todos os campos do departamento onde o id for igual id_departamento
    #SELECT * from Departamento WHERE id = id_departamento :)
    departamento = Departamento.objects.get(id=departamento_id)

    departamento_dados = {
        'id': departamento.id,
        'nome': departamento.nome,
        'sigla': departamento.sigla
    }
    return JsonResponse(departamento_dados)

@login_required
def excluir_departamento(request):
    if request.method == 'POST':
        departamento_id = request.POST.get('departamento_id')
        departamento = Departamento.objects.filter(id=departamento_id).first()
        departamento.delete()

        if (departamento.usuario_set.exists()):
            return JsonResponse({'success': False,
                                 'messages': 'Usuários vinculados!'})

        return JsonResponse({'success': True,
                            'messages': 'Departamento excluido com sucesso!'})
    
@login_required
def pesquisar_departamento_por_nome(request):
    departamento_nome = request.GET.get('departamento_nome', '')
    numero_pagina = request.GET.get('page')#do proprio objeto paginator

    #icontains = LIKE no sql
    departamento_lista = Departamento.objects.filter(nome__icontains=departamento_nome).exclude(nome__iexact="Geral").order_by('nome')

    paginator = Paginator(departamento_lista, settings.NUMBER_GRID_PAGES)
    page_obj = paginator.get_page(numero_pagina)

    return JsonResponse({
        #vai renderizar a departamentos_table.html com esses novos parametros
        'html': render_to_string('departamentos_table.html',
                                 {'page_obj': page_obj,
                                  'query': departamento_nome,
                                  'request': request})
    })