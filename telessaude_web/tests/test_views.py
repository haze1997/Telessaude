import unittest
from django.test import TestCase, Client
from django.urls import reverse
import json
from ..models import Paciente, User
class TestarRespostaJSONgetToken(TestCase):
    def setUp(self):
        user = User._default_manager.create_user(username = 'temporario', nome = 'Temp', sobrenome = 'Temp', email = 'temp@gmail.com', role = 'paciente', cpf = '5555222255', data_nascimento = '1996-10-10', endereco = 'Rua das Flores', telefone = '999999', genero = 'm', password = 'teste123')
        paciente = Paciente._default_manager.create(user = user)
        self.client = Client()
    def test_my_view_getToken(self):
        logado = self.client.login(username='temporario', password='teste123')
        self.assertTrue(logado)
        # Usa o nome da URL (como definido em urls.py) em vez do caminho
        urlgetToken = reverse('get_token')  # Substitua pelo nome real da sua URL

        resposta = self.client.get(urlgetToken,  data={'id_consulta': '1'})
        self.assertEqual(resposta.status_code, 200)

        data = json.loads(resposta.content)
        tokenResposta = data['token']
        uidResposta = data['uid']
        # Verifica se a resposta é um JSON válido (ajuste conforme o esperado da sua view)
        #self.assertIsInstance(data, dict)
        # Verifica se há um token na resposta (ajuste conforme sua API)
        self.assertIn('token', data)  # Ou outra verificação mais específica
        self.assertIsNone(tokenResposta)
        self.assertIsNone(uidResposta)
