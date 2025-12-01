from django.contrib import admin

# Register your models here.

from .models import User, ProfissionalSaude, Funcionario, Paciente, Consulta, RelatorioGerencial, MensagemConsulta

admin.site.register(User)
admin.site.register(ProfissionalSaude)
admin.site.register(Funcionario)
admin.site.register(Paciente)
admin.site.register(Consulta)
admin.site.register(RelatorioGerencial)
admin.site.register(MensagemConsulta)
