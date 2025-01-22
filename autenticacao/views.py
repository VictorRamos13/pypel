from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from cadastros.models import Usuario
from django.http import HttpResponse

def login(request):
    if request.method == 'POST':
        email = request.POST.get('txtEmail')
        senha = request.POST.get('txtSenha')
        perfil_id = request.POST.get('slcPerfil')

        usuario = authenticate(request, username=email, password=senha) #checagem de autenticacao
        
        if usuario is not None and perfil_id:
            perfis_usuario = usuario.perfis.filter(id=perfil_id)
            if perfis_usuario.exists():
                #limpa as sessoes do usuario
                request.session.flush()
                #cria a sessao do usuario
                auth_login(request, usuario)
                
                #armazenando na sessão
                request.session['id_atual'] = usuario.id
                request.session['email_atual'] = usuario.email
                request.session['departamento_id_atual'] = usuario.departamento.id
                request.session['departamento_nome_atual'] = usuario.departamento.nome
                request.session['departamento_sigla_atual'] = usuario.departamento.sigla                      
                request.session['perfil_atual'] = perfis_usuario.first().nome                
                request.session['perfis'] = list(usuario.perfis.values_list('nome', flat=True))
                
                #configura sessao para expirar em 4 horas
                request.session.set_expiry(14400)
                
                messages.success(request, 'Login realizado com sucesso!')
                
                #no futuro iremos separar em diferentes paginas
                if request.session.get('perfil_atual') in {'Administrador', 'Estoquista', 'Vendedor'}:
                    return redirect('core:main')
                
            else:
                messages.error(request, 'Perfil inválido para este usuário.')
        else:
            if usuario is None:
                messages.error(request, 'Senha incorreta.')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
            
    return render(request, 'login.html')

def get_perfis(request):
    email = request.GET.get('email', '')
    perfis = []
    if Usuario.objects.filter(email=email).exists():
        usuario = Usuario.objects.get(email=email)
        perfis = usuario.perfis.all().values('id', 'nome')
        data = {'perfis': list(perfis), 'usuario_existe': True}
    else:
        data = {'usuario_existe': False}
    return JsonResponse(data)

def logout(request):
    #limpa a sessao ao deslogar
    request.session.flush()
    auth_logout(request)
    
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('autenticacao:login')

def esqueci_senha(request):

    if request.method == 'POST':
        
        email = request.POST.get('txtEmail')
        senha = request.POST.get('txtNovaSenha')

        try:
            #busca o email no banco, "select por email"
            usuario = Usuario.objects.get(email=email)
            
            #se encontrar redefine a senha
            usuario.set_password(senha)
            usuario.save()

            messages.success(request, "Senha alterada com sucesso!")
            return redirect('autenticacao:login')
        
        #pega o erro e trata ele exibindo na tela isso ai
        except Usuario().DoesNotExist: 
            messages.error(request, "Esse e-mail não está registrado.")
            
        
    return render(request, 'esqueci_senha.html')