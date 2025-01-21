from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required #so executa a funcao se o cara estiver logado
def main(request):
    return render(request, "main.html")
