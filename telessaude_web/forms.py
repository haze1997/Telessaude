from django import forms
from .models import Consulta, User, MensagemConsulta, Paciente
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.forms import ModelForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.CharField(widget=forms.HiddenInput, initial="paciente")
    # Configuration
    class Meta:
        model = User
        fields = ['username', 'nome', 'sobrenome', 'email', 'role', 'cpf', 'data_nascimento', 'endereco', 'telefone', 'genero', 'password1', 'password2']

class UserDetalhesForm(ModelForm):
    email = forms.EmailField()
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    role = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    cpf = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # Configuration
    class Meta:
        model = User
        fields = ['username', 'nome', 'sobrenome', 'email', 'role', 'cpf', 'data_nascimento', 'endereco', 'telefone', 'genero']


class UserSenhaForm(PasswordChangeForm):
    # Configuration
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Desativa o autofocus para o campo 'old_password'
            self.fields['old_password'].widget.attrs.update({'autofocus': False})
            # Desativa o autofocus para o campo 'new_password1'
            self.fields['new_password1'].widget.attrs.update({'autofocus': False})
            # Desativa o autofocus para o campo 'new_password2'
            self.fields['new_password2'].widget.attrs.update({'autofocus': False})
    #pass

class UserBioForm(ModelForm):
    class Meta:
        model = User
        fields = ['bio']
        widgets = {
            'bio' : forms.Textarea(attrs={'placeholder': 'Fale um pouco sobre você...', 'class': 'p4', 'maxlength': '500', 'rows': '4'}),
        }

class ReagendarConsultaForm(ModelForm):
    data_hora = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
            date_attrs={'type': 'date'},
            time_attrs={'type': 'time', 'step': '60'}  # 60-second steps
        )
    )
    class Meta:
        model = Consulta
        fields = ['data_hora']

class AgendarConsultaForm(ModelForm):
    data_hora = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
            date_attrs={'type': 'date'},
            time_attrs={'type': 'time', 'step': '60'}  # 60-second steps
        )
    )
    class Meta:
        model = Consulta
        fields = ['motivo', 'paciente', 'profissional', 'data_hora', 'preco']
        widgets = {
            'motivo' : forms.TextInput(attrs={'placeholder': 'Motivo...', 'class': 'p4 text-black', 'maxlength': '300'}),
        }

class ConsultaForm(ModelForm):
    class Meta:
        model = Consulta
        fields = ['motivo','anamnese', 'preco', 'presente']
        widgets = {
            'motivo' : forms.TextInput(attrs={'placeholder': 'Motivo...', 'class': 'p4 text-black', 'maxlength': '300'}),
            'anamnese' : forms.Textarea(attrs={'placeholder': 'Anamnese...', 'class': 'p4 text-black', 'maxlength': '3000', 'rows': '4'}),
        }

class MensagemConsultaForm(ModelForm):
    class Meta:
        model = MensagemConsulta
        fields = ['conteudo', 'anexo']
        widgets = {
            'conteudo' : forms.Textarea(attrs={'placeholder': 'Escreva uma mensagem...', 'class': 'p4 text-black', 'maxlength': '3000', 'rows': '4', 'autofocus': True}),

        }

class PacienteDetalhesForm(ModelForm):
    class Meta:
        model = Paciente
        fields = ['peso', 'altura', 'tipo_sanguineo', 'doencas_cronicas', 'alergias']
