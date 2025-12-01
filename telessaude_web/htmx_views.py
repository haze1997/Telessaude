from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Consulta, MensagemConsulta, Paciente, ProfissionalSaude

@login_required
def getMensagem(request, pk):
    consulta_id = pk
    if request.user.is_authenticated  and ((request.user.role == 'paciente' and Consulta._default_manager.filter(pk = pk, paciente=Paciente._default_manager.get(user=request.user)).exists()) or (request.user.role == 'profissional' and Consulta._default_manager.filter(pk = pk, profissional=ProfissionalSaude._default_manager.get(user=request.user)).exists())):
        consultas = Consulta._default_manager.get(pk = consulta_id)
        consulta_msg = MensagemConsulta._default_manager.filter(consulta = consultas).order_by('-data_envio')
    else:
        return redirect('consultas')
    return render(request, 'recursos/getMessage.html', {'mensagensChat': consulta_msg})
