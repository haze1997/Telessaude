# Generated by Django 3.2.25 on 2025-07-07 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telessaude_web', '0006_alter_mensagemconsulta_anexo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensagemconsulta',
            name='anexo',
            field=models.FileField(blank=True, null=True, upload_to='consultas/anexos/2025-07-07/'),
        ),
    ]
