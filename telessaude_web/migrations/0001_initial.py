# Generated by Django 3.2.25 on 2025-06-20 00:22

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nome', models.CharField(max_length=50)),
                ('sobrenome', models.CharField(max_length=250)),
                ('role', models.CharField(choices=[('admin', 'Administrador'), ('secretaria', 'Secretária'), ('profissional', 'Profissional de Saúde'), ('paciente', 'Paciente')], max_length=20)),
                ('data_nascimento', models.DateField()),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('endereco', models.CharField(max_length=500)),
                ('telefone', models.CharField(max_length=20)),
                ('genero', models.CharField(choices=[('m', 'Masculino'), ('f', 'Feminino')], max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora', models.DateTimeField()),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('motivo', models.TextField(blank=True, null=True)),
                ('anamnese', models.TextField(blank=True, null=True)),
                ('presente', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RelatorioGerencial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.IntegerField()),
                ('ano', models.IntegerField()),
                ('numero_consultas', models.IntegerField()),
                ('percentual_presenca', models.FloatField()),
                ('numero_pacientes', models.IntegerField()),
                ('faturamento_bruto_mensal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('faturamento_bruto_anual', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='ProfissionalSaude',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('Médico', 'Médico'), ('Nutricionista', 'Nutricionista'), ('Psicólogo', 'Psicólogo')], max_length=20)),
                ('numero_conselho', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.FloatField(blank=True, null=True)),
                ('altura', models.FloatField(blank=True, null=True)),
                ('tipo_sanguineo', models.CharField(blank=True, max_length=3, null=True)),
                ('doencas_cronicas', models.TextField(blank=True, null=True)),
                ('alergias', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MensagemConsulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.TextField()),
                ('data_envio', models.DateTimeField(auto_now_add=True)),
                ('lida', models.BooleanField(default=False)),
                ('anexo', models.FileField(blank=True, null=True, upload_to='consultas/anexos/')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensagens_enviadas', to=settings.AUTH_USER_MODEL)),
                ('consulta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensagens', to='telessaude_web.consulta')),
            ],
            options={
                'verbose_name': 'Mensagem da Consulta',
                'verbose_name_plural': 'Mensagens das Consultas',
                'ordering': ['data_envio'],
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='consulta',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telessaude_web.paciente'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='profissional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telessaude_web.profissionalsaude'),
        ),
        migrations.AlterUniqueTogether(
            name='consulta',
            unique_together={('profissional', 'data_hora')},
        ),
    ]
