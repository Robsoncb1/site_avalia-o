"""
Módulo de testes para o site Coco Bambu Alphaville
Implementa funções para testar funcionalidades e validar o site
"""

import unittest
from flask import Flask
from flask_testing import TestCase
from src.main import app
from src.models.avaliacao import db, Avaliacao, Contato
from src.utils.security import sanitize_input, validate_email, validate_rating
from src.utils.privacy import PrivacyManager

class TestAvaliacaoModel(unittest.TestCase):
    """Testes para o modelo de Avaliação"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        """Limpeza após os testes"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_nova_avaliacao(self):
        """Testa a criação de uma nova avaliação"""
        avaliacao = Avaliacao(
            nome="Teste",
            email="teste@exemplo.com",
            qualidade=5,
            variedade=4,
            apresentacao=5,
            reposicao=4,
            atendimento=5,
            comentario="Teste de comentário"
        )
        
        db.session.add(avaliacao)
        db.session.commit()
        
        avaliacao_db = Avaliacao.query.filter_by(email="teste@exemplo.com").first()
        
        self.assertIsNotNone(avaliacao_db)
        self.assertEqual(avaliacao_db.nome, "Teste")
        self.assertEqual(avaliacao_db.qualidade, 5)
        self.assertEqual(avaliacao_db.media_geral, 4.6)  # (5+4+5+4+5)/5 = 4.6
    
    def test_to_dict(self):
        """Testa a conversão do modelo para dicionário"""
        avaliacao = Avaliacao(
            nome="Teste",
            email="teste@exemplo.com",
            qualidade=5,
            variedade=4,
            apresentacao=5,
            reposicao=4,
            atendimento=5,
            comentario="Teste de comentário",
            pratos_favoritos="Camarão,Lagosta"
        )
        
        avaliacao_dict = avaliacao.to_dict()
        
        self.assertEqual(avaliacao_dict['nome'], "Teste")
        self.assertEqual(avaliacao_dict['qualidade'], 5)
        self.assertEqual(avaliacao_dict['media_geral'], 4.6)
        self.assertEqual(avaliacao_dict['pratos_favoritos'], ["Camarão", "Lagosta"])

class TestContatoModel(unittest.TestCase):
    """Testes para o modelo de Contato"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        """Limpeza após os testes"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_novo_contato(self):
        """Testa a criação de um novo contato"""
        contato = Contato(
            nome="Teste",
            email="teste@exemplo.com",
            telefone="11999999999",
            assunto="Teste",
            mensagem="Teste de mensagem"
        )
        
        db.session.add(contato)
        db.session.commit()
        
        contato_db = Contato.query.filter_by(email="teste@exemplo.com").first()
        
        self.assertIsNotNone(contato_db)
        self.assertEqual(contato_db.nome, "Teste")
        self.assertEqual(contato_db.assunto, "Teste")
        self.assertEqual(contato_db.lida, False)

class TestSeguranca(unittest.TestCase):
    """Testes para as funções de segurança"""
    
    def test_sanitize_input(self):
        """Testa a sanitização de entrada"""
        # Teste com HTML
        html_input = "<script>alert('XSS')</script>Texto normal"
        sanitized = sanitize_input(html_input)
        self.assertEqual(sanitized, "Texto normal")
        
        # Teste com texto normal
        normal_input = "Texto normal sem HTML"
        sanitized = sanitize_input(normal_input)
        self.assertEqual(sanitized, normal_input)
        
        # Teste com None
        sanitized = sanitize_input(None)
        self.assertEqual(sanitized, "")
    
    def test_validate_email(self):
        """Testa a validação de e-mail"""
        # E-mail válido
        self.assertTrue(validate_email("teste@exemplo.com"))
        
        # E-mails inválidos
        self.assertFalse(validate_email("teste@"))
        self.assertFalse(validate_email("teste"))
        self.assertFalse(validate_email("teste@exemplo"))
        self.assertFalse(validate_email(""))
        self.assertFalse(validate_email(None))
    
    def test_validate_rating(self):
        """Testa a validação de avaliação"""
        # Avaliações válidas
        self.assertTrue(validate_rating(1))
        self.assertTrue(validate_rating(3))
        self.assertTrue(validate_rating(5))
        self.assertTrue(validate_rating("3"))
        
        # Avaliações inválidas
        self.assertFalse(validate_rating(0))
        self.assertFalse(validate_rating(6))
        self.assertFalse(validate_rating("abc"))
        self.assertFalse(validate_rating(None))

class TestPrivacidade(unittest.TestCase):
    """Testes para as funções de privacidade"""
    
    def test_anonymize_data(self):
        """Testa a anonimização de dados"""
        data = {
            'nome': 'João Silva',
            'email': 'joao@exemplo.com',
            'telefone': '11999999999',
            'comentario': 'Teste de comentário'
        }
        
        # Anonimizar nome e email
        anonymized = PrivacyManager.anonymize_data(data, ['nome', 'email'])
        self.assertEqual(anonymized['nome'], 'J****')
        self.assertEqual(anonymized['email'], '****@exemplo.com')
        self.assertEqual(anonymized['telefone'], '11999999999')  # Não anonimizado
        
        # Anonimizar telefone
        anonymized = PrivacyManager.anonymize_data(data, ['telefone'])
        self.assertEqual(anonymized['telefone'], '****9999')
        
        # Anonimizar todos os campos
        anonymized = PrivacyManager.anonymize_data(data, ['nome', 'email', 'telefone', 'comentario'])
        self.assertEqual(anonymized['nome'], 'J****')
        self.assertEqual(anonymized['email'], '****@exemplo.com')
        self.assertEqual(anonymized['telefone'], '****9999')
        self.assertEqual(anonymized['comentario'], '****')

class TestRoutes(TestCase):
    """Testes para as rotas da aplicação"""
    
    def create_app(self):
        """Cria a aplicação para testes"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app
    
    def setUp(self):
        """Configuração inicial para os testes"""
        db.create_all()
        
    def tearDown(self):
        """Limpeza após os testes"""
        db.session.remove()
        db.drop_all()
    
    def test_index_route(self):
        """Testa a rota principal"""
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('index.html')
    
    def test_avaliar_route(self):
        """Testa a rota de avaliação"""
        response = self.client.get('/avaliar')
        self.assert200(response)
        self.assert_template_used('avaliar.html')
    
    def test_feedback_route(self):
        """Testa a rota de feedback"""
        response = self.client.get('/feedback')
        self.assert200(response)
        self.assert_template_used('feedback.html')
    
    def test_contato_route(self):
        """Testa a rota de contato"""
        response = self.client.get('/contato')
        self.assert200(response)
        self.assert_template_used('contato.html')
    
    def test_sobre_route(self):
        """Testa a rota sobre"""
        response = self.client.get('/sobre')
        self.assert200(response)
        self.assert_template_used('sobre.html')
    
    def test_menu_route(self):
        """Testa a rota de menu"""
        response = self.client.get('/menu')
        self.assert200(response)
        self.assert_template_used('menu.html')
    
    def test_404_route(self):
        """Testa a página 404"""
        response = self.client.get('/pagina-inexistente')
        self.assert404(response)
        self.assert_template_used('404.html')

if __name__ == '__main__':
    unittest.main()
