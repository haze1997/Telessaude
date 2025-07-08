from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserRegisterForm, MensagemConsultaForm, ConsultaForm, PacienteDetalhesForm, UserDetalhesForm, UserSenhaForm, ReagendarConsultaForm, AgendarConsultaForm, UserBioForm # Import the form we just created
from .models import Consulta, MensagemConsulta, Paciente, ProfissionalSaude, User
from agora_token_builder import RtcTokenBuilder
from django.http import HttpResponse
import time

def register(request):
    print('Entrou aqui')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print('Entrou aqui no post')
            form.save() # Save user to Database
            username = form.cleaned_data.get('username') # Get the username that is submitted
            role = form.cleaned_data.get('role')
            messages.success(request, f'Conta criada para {username}!') # Show sucess message when account is created
            if role == 'paciente':
                novo_paciente = Paciente(user=User._default_manager.get(username = username))
                # Save the instance to the database
                novo_paciente.save()
            return redirect('home') # Redirect user to Homepage
    else:
        print('Entrou aqui no else')
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})
# Create your views here.

def home(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

@login_required
def consultas(request):
    data = {}
    if request.method == 'POST':
        form_id = request.POST.get('form_id')
        if form_id == 'form_agendar':
            nova_consulta = AgendarConsultaForm(request.POST)
            if nova_consulta.is_valid:
                nova_consulta.save()
                messages.success(request, 'Consulta Agendada com sucesso!')
        if form_id == 'form_reagendar':
            form_id_consulta = request.POST.get('form_id_consulta')
            instance_consulta = get_object_or_404(Consulta, pk=form_id_consulta)
            data['formReagendar'] = ReagendarConsultaForm(request.POST, instance=instance_consulta)
            if data['formReagendar'].is_valid:
                print('Entrou no reagendar')
                data['formReagendar'].save()
                messages.success(request, 'Consulta reagendada com sucesso!')
    if request.user.is_authenticated and ((request.user.role == 'paciente' and Paciente._default_manager.filter(user=request.user).exists()) or (request.user.role == 'profissional' and ProfissionalSaude._default_manager.filter(user=request.user).exists()) or (request.user.role == 'secretaria' and Funcionario._default_manager.filter(user=request.user, cargo='secretaria').exists())):
        if request.user.role == 'paciente':
            data['consultas'] = Consulta._default_manager.filter(paciente=Paciente._default_manager.get(user=request.user))
            data['consultasPg'] = Paginator(data['consultas'], 5)
        elif request.user.role == 'profissional':
            data['consultas'] = Consulta._default_manager.filter(profissional=ProfissionalSaude._default_manager.get(user=request.user))
            data['consultasPg'] = Paginator(data['consultas'], 5)
        elif request.user.role == 'secretaria':
            data['consultas'] = Consulta._default_manager.all()
            data['consultasPg'] = Paginator(data['consultas'], 5)
            data['formReagendar'] = ReagendarConsultaForm()
            data['formAgendar'] = AgendarConsultaForm()
            print(data['formReagendar'])
        page_number = request.GET.get('pg')
        try:
            data['consultasPgObj'] = data['consultasPg'].get_page(page_number)
        except PageNotAnInteger:
            data['consultasPgObj'] = data['consultasPg'].page(1)
        except EmptyPage:
            data['consultasPgObj'] = data['consultasPg'].page(data['consultasPg'].num_pages)
    return render(request, 'consultas.html', data)

def getToken(request):
    appId = '03d88d8127774ffa84eb99855ea22f0d'
    appCertificate = 'cc8eaf8869384b5da7b2fdcdb201b0e3'
    channelName = request.GET.get('id_consulta')
    uid = request.user.id
    #username = request.user.username
    #nome = request.user.nome
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1
    if request.user.is_authenticated and ((request.user.role == 'paciente' and Consulta._default_manager.filter(pk = channelName, paciente=Paciente._default_manager.get(user=request.user)).exists()) or (request.user.role == 'profissional' and Consulta._default_manager.filter(pk = channelName, profissional=ProfissionalSaude._default_manager.get(user=request.user)).exists())):
        token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    else:
        token = None
        uid = None

    return JsonResponse({'token': token, 'uid': uid}, safe=False)

def getUser(request):
    UID_user = request.GET.get('uid')
    username = User._default_manager.get(pk = UID_user).username
    nome = User._default_manager.get(pk = UID_user).nome
    if User._default_manager.get(pk = UID_user).role == 'profissional':
        role = ProfissionalSaude._default_manager.get(user = User._default_manager.get(pk = UID_user)).tipo
    else:
        role = 'paciente'
    return JsonResponse({'username': username, 'nome': nome, 'role': role}, safe=False)

@login_required
def sala(request, pk):
    data ={}
    if request.user.is_authenticated and ((request.user.role == 'paciente' and Consulta._default_manager.filter(pk = pk, paciente=Paciente._default_manager.get(user=request.user)).exists()) or (request.user.role == 'profissional' and Consulta._default_manager.filter(pk = pk, profissional=ProfissionalSaude._default_manager.get(user=request.user)).exists())):
        print('Entrou na sala')
        data['ver'] = Consulta._default_manager.get(pk=pk)
        data['paciente'] = data['ver'].paciente
        #consulta = get_object_or_404(Consulta, id=pk)
        #data['consultaSala'] = get_object_or_404(Consulta, pk=pk)
        data['mensagensChat'] = MensagemConsulta._default_manager.filter(consulta=data['ver']).order_by('-data_envio')[:30]
        data['messageForm'] = MensagemConsultaForm()
        if request.method == 'POST':
            form_id = request.POST.get('form_id')
            #if data['messageForm'].is_valid():
            username = request.user
            print(username)
            #print(conteudo)
            if form_id == 'form_consulta':
                data['consultaForm'] = ConsultaForm(request.POST,  instance = data['ver'])
                if data['consultaForm'].is_valid():
                    #data['consultaForm'].cleaned_data['pk'] = pk
                    data['consultaForm'].save()
                    messages.success(request, 'Consulta salva com sucesso!')

            if form_id == 'form_paciente':
                data['pacienteDetalhes'] = PacienteDetalhesForm(request.POST, instance = data['paciente'])
                if data['pacienteDetalhes'].is_valid():
                    data['pacienteDetalhes'].save()
                    messages.success(request, 'Paciente atualizado com sucesso!')

            """if data['messageForm'].is_valid():
                conteudo = request.POST.get('conteudo') #data['messageForm'].cleaned_data.get('conteudo')
                anexo = request.POST.get('anexo')
                if conteudo is not None:
                    MensagemConsulta._default_manager.create(consulta = data['ver'], autor=username, conteudo=conteudo, anexo=anexo)
                data['consultaForm'] = ConsultaForm(instance = data['ver'])"""
            """if request.user.role == 'paciente':
                data['consultaForm'].fields['motivo'].disabled = True
                data['consultaForm'].fields['preco'].disabled = True
                data['consultaForm'].fields['anamnese'].disabled = True
                data['consultaForm'].fields['presente'].disabled = True"""
        else:
            pass
            #data['messageForm'] = MensagemConsultaForm()

        data['consultaForm'] = ConsultaForm(instance = data['ver'])
        data['pacienteDetalhes'] = PacienteDetalhesForm(instance = data['paciente'])

        if request.user.role == 'paciente':
            data['consultaForm'].fields['motivo'].disabled = True
            data['consultaForm'].fields['preco'].disabled = True
            data['consultaForm'].fields['anamnese'].disabled = True
            data['consultaForm'].fields['presente'].disabled = True
            data['pacienteDetalhes'].fields['peso'].disabled = True
            data['pacienteDetalhes'].fields['altura'].disabled = True
            data['pacienteDetalhes'].fields['tipo_sanguineo'].disabled = True
            data['pacienteDetalhes'].fields['doencas_cronicas'].disabled = True
            data['pacienteDetalhes'].fields['alergias'].disabled = True
    else:
        print('Entrou no else da sala')
        return redirect('consultas')
    return render(request, 'sala_consulta.html', data)

def cadastro(request):
    return render(request, 'register.html')

@login_required
def perfil(request):
    data = {}
    form_id = request.POST.get('form_id')
    if request.method == 'POST' and form_id == 'formUser':
        data['formUsuario'] = UserDetalhesForm(request.POST, instance = request.user)
        if data['formUsuario'].is_valid():
            data['formUsuario'].save()
            messages.success(request, 'Informações de usuário atualizadas com sucesso!')
    if request.method == 'POST' and form_id == 'formPassword':
        data['formSenha'] = UserSenhaForm(request.user, request.POST)
        if data['formSenha'].is_valid():
            data['formSenha'].save()
            messages.success(request, 'Senha alterada com sucesso. Faça o login novamente!')
            return redirect('login')
    if request.method == 'POST' and form_id == 'formBio':
        data['formBio'] = UserBioForm(request.POST, instance = request.user)
        if data['formBio'].is_valid():
            data['formBio'].save()
            messages.success(request, 'Informação da Bio salva com sucesso!')
    data['formUsuario'] = UserDetalhesForm(instance = request.user)
    data['formSenha'] = UserSenhaForm(request.user)
    data['formBio'] = UserBioForm(instance = request.user)
    return render(request, 'profile.html', data)

def recuperarsenha(request):
    return render(request, 'recover_password.html')

def chat(request):
    pass

@csrf_exempt
def enviarmensagem(request, pk):
    if request.method == 'POST':
        msgform = MensagemConsultaForm(request.POST, request.FILES)
        if msgform.is_valid():
            id_consulta = pk
            conteudo = request.POST.get('conteudo') #data['messageForm'].cleaned_data.get('conteudo')
            anexo = request.FILES.get('anexo')
            MSG = MensagemConsulta(consulta = Consulta._default_manager.get(pk=id_consulta), autor=request.user, conteudo=conteudo, anexo=anexo)
            MSG.save()
    return HttpResponse(status = 201);

@login_required
def deleteConsulta(request, id):
    if request.method == 'GET' and (request.user.role == 'secretaria' and Funcionario._default_manager.filter(user=request.user, cargo='secretaria').exists()):
        item = get_object_or_404(Consulta, pk=id)
        item.delete()
        messages.success(request, 'Consulta deletada com sucesso!')
        return redirect('consultas')

"""
def editarusuario(request):
    data = {}
    form_id = request.POST.get('form_id')
    if request.method == 'POST' and form_id == 'formUser':
        data['formUsuario'] = UserDetalhesForm(request.POST, instance = request.user)
        if data['formUsuario'].is_valid():
            data['formUsuario'].save()
            messages.success(request, 'Informações de usuário atualizadas com sucesso!')
    if request.method == 'POST' and form_id == 'formPassword':
        data['formSenha'] = UserSenhaForm(request.POST, instance = request.user)
        if data['formSenha'].is_valid():
            data['formSenha'].save()
            messages.success(request, 'Informações de usuário atualizadas com sucesso!')
    data['formUsuario'] = UserDetalhesForm(instance = request.user)
    data['formSenha'] = UserSenhaForm
    return render(request, 'profile.html', data)
"""
"""
def salvapaciente(request, pk):
    if request.method == 'POST':
        pacienteForm = PacienteDetalhesForm(request.POST)
        if pacienteForm.is_valid():
            id_paciente = pk
            peso = request.POST.get('peso') #data['messageForm'].cleaned_data.get('conteudo')
            altura = request.POST.get('altura')
            tipo_sanguineo = request.POST.get('tipo_sanguineo')
            print(tipo_sanguineo)
            doencas_cronicas = request.POST.get('doencas_cronicas')
            alergias = request.POST.get('alergias')
            paciente_obj = Paciente._default_manager.filter(pk = id_paciente).update(peso = peso, altura = altura, tipo_sanguineo = tipo_sanguineo, doencas_cronicas = doencas_cronicas, alergias = alergias)
            paciente_obj.save()
            messages.success(request, 'Paciente atualizado com sucesso!')
    return HttpResponse(status = 201);
"""
def sair(request):
    logout(request)
    return redirect('login')


from rest_framework import viewsets
from .models import Funcionario
from .serializers import ProfissionalSaudeSerializer, FuncionarioSerializer, PacienteSerializer, ConsultaSerializer

class ProfissionalSaudeViewSet(viewsets.ModelViewSet):
    queryset = ProfissionalSaude._default_manager.all()
    serializer_class = ProfissionalSaudeSerializer

class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario._default_manager.all()
    serializer_class = FuncionarioSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente._default_manager.all()
    serializer_class = PacienteSerializer

class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta._default_manager.all()
    serializer_class = ConsultaSerializer
