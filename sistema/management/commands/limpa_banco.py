from django.core.management.base import BaseCommand
from django.db import connection, transaction
from cadastros.models import Departamento, Perfil, Usuario

class Command(BaseCommand):
    help = 'Redefine o sistema apagando tudo do banco'

    #flags do django @ = o usuario tem que ta logado para chamar a flag
    @transaction.atomic
    def handle(self, *args, **kwargs):
        cursor = connection.cursor()

        app_labels = ['cadastros']
        tables = [table for table in connection.introspection.table_names()
                  if any(app in table for app in app_labels)] #retorna todas as tables de cadastros
        
        if connection.vendor == 'postgresql':
            for table in tables:
                cursor.execute(f'ALTER TABLE "{table}" DISABLE TRIGGER ALL;')#desabilitando as chaves de seguranca
                #chave estrangeira esta desabilitando, por exemplo
        
        for table in tables:
            cursor.execute(f'TRUNCATE TABLE "{table}" CASCADE;')#para as mudancas propagarem no banco

        if connection.vendor == 'postgresql':
            for table in tables:
                cursor.execute(f"""
                    SELECT setval(pg_get_serial_sequence('"{table}"', 'id'), 1, false)
                    WHERE EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = '{table}' AND column_name ='id'
                        AND column_default LIKE 'nextval%'    
                    );
                """)
        
        if connection.vendor == 'postgresql':
            for table in tables:
                cursor.execute(f'ALTER TABLE "{table}" ENABLE TRIGGER ALL;')
        self.stdout.write(self.style.SUCCESS('Banco limpo com sucesso!'))