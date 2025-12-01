#from django.db import models

# Create your models here.
#from pathlib import Path
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Usuário com papéis (RBAC)
class User(AbstractUser):
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=250)
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('secretaria', 'Secretária'),
        ('profissional', 'Profissional de Saúde'),
        ('paciente', 'Paciente'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    endereco = models.CharField(max_length=500)
    telefone = models.CharField(max_length=20)
    bio = models.TextField(max_length=500, null=True, blank=True)
    GENERO_CHOICES = [
        ('m', 'Masculino'),
        ('f', 'Feminino'),
    ]
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nome', 'sobrenome', 'email', 'role', 'cpf', 'data_nascimento', 'endereco', 'telefone', 'genero']

class ProfissionalSaude(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    TIPO_CHOICES = [
        ('Médico', 'Médico'),
        ('Nutricionista', 'Nutricionista'),
        ('Psicólogo', 'Psicólogo'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    numero_conselho = models.CharField(max_length=50)
    def __str__(self):
            return self.user.username

class Funcionario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=50)
    def __str__(self):
            return self.user.username

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    peso = models.FloatField(null=True, blank=True)
    altura = models.FloatField(null=True, blank=True)
    tipo_sanguineo = models.CharField(max_length=3, null=True, blank=True)
    doencas_cronicas = models.TextField(null=True, blank=True)
    alergias = models.TextField(null=True, blank=True)
    def __str__(self):
            return self.user.username


class Consulta(models.Model):
    profissional = models.ForeignKey(ProfissionalSaude, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.TextField(null=True, blank=True)
    anamnese = models.TextField(null=True, blank=True)
    presente = models.BooleanField(default=False)

    class Meta:
        unique_together = ('profissional', 'data_hora')

    def __str__(self):
        return f"Consulta de {self.paciente.user.nome} com {self.profissional.user.nome} no dia {self.data_hora}"

class MensagemConsulta(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='mensagens')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    conteudo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    # Anexos opcionais (receitas, exames, etc.)
    anexo = models.FileField(upload_to='consultas/anexos/' + datetime.now().strftime("%Y-%m-%d") + '/', null=True, blank=True)

    class Meta:
        ordering = ['data_envio']
        verbose_name = 'Mensagem da Consulta'
        verbose_name_plural = 'Mensagens das Consultas'


    def __str__(self):
        return f"Mensagem de {self.autor} para consulta #{self.consulta.id}"

class RelatorioGerencial(models.Model):
    mes = models.IntegerField()
    ano = models.IntegerField()
    numero_consultas = models.IntegerField()
    percentual_presenca = models.FloatField()
    numero_pacientes = models.IntegerField()
    faturamento_bruto_mensal = models.DecimalField(max_digits=10, decimal_places=2)
    faturamento_bruto_anual = models.DecimalField(max_digits=12, decimal_places=2)
