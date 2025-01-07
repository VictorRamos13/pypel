from django.shortcuts import render
from django.contrib.auth.decorators import login_required #as flag estao dentro de decorators

@login_required #isso aqui garante que a pessoa tem que estar logada
def main(request):
    return render(request, "main.html")