from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from cadastros.models import Departamento, Perfil, Usuario

class Command(BaseCommand):
    help = 'Inicializa o sistema com os dados padrão' #python manage.py -h inicializa_sistema = aparece esse help

    def handle(self, *args, **kwargs): #retorna ele mesmo, uma lista de argumentos
        
        #cria um departamento geral
        departamento, created = Departamento.objects.get_or_create(nome='Geral', sigla='GERAL')
        if created:
            self.success.write(self.style.SUCCESS(f'Departamento criado: {departamento.nome}'))
            #aparece no console departamento criado, esse SUCCESS é o layout verde bonitinho que criou

        #cria os perfis de usuario
        perfil_administrador, created = Perfil.objects.get_or_create(id=1, nome='Administrador')
        if created:
            self.success.write(self.style.SUCCESS(f'Perfil criado: {perfil_administrador.nome}'))

        pefil_estoquista, created = Perfil.objects.get_or_create(id=2, nome='Estoquista')
        if created:
            self.success.write(self.style.SUCCESS(f'Perfil criado: {pefil_estoquista.nome}'))

        pefil_vendedor, created = Perfil.objects.get_or_create(id=3, nome='Vendedor')
        if created:
            self.success.write(self.style.SUCCESS(f'Perfil criado: {pefil_vendedor.nome}'))

        #cria o usuario administrador principal do sistema
        User = get_user_model()
        if not User.objects.filter(email='adm@gmail.com').exists():
            usuario = User(
                email = 'adm@gmail.com',
                nome = 'Administrador',
                is_admin = True,
                departamento = departamento #passa um objeto que foi criado agora
            )
            usuario.set_password('123456')
            usuario.save()

            usuario.perfis.add(perfil_administrador)
            usuario.save()
            
            self.stdout.write(self.style.SUCCESS('Usuário administrador criado com sucesso'))
        else:
            self.stdout.write(self.style.WARNING('Usuário administrador já existe'))

