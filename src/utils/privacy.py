"""
Módulo de privacidade para o site Coco Bambu Alphaville
Implementa funções para gerenciamento de dados pessoais e políticas de privacidade
"""

import json
import datetime
from flask import session, request

class PrivacyManager:
    """Classe para gerenciamento de privacidade e dados pessoais"""
    
    @staticmethod
    def anonymize_data(data, fields_to_anonymize):
        """
        Anonimiza dados pessoais
        
        Args:
            data (dict): Dicionário com dados a serem anonimizados
            fields_to_anonymize (list): Lista de campos a serem anonimizados
            
        Returns:
            dict: Dados anonimizados
        """
        anonymized_data = data.copy()
        
        for field in fields_to_anonymize:
            if field in anonymized_data:
                if field == 'email':
                    # Anonimiza email mantendo domínio
                    parts = anonymized_data[field].split('@')
                    if len(parts) == 2:
                        anonymized_data[field] = f"****@{parts[1]}"
                    else:
                        anonymized_data[field] = "****@****.com"
                elif field == 'nome':
                    # Anonimiza nome mantendo inicial
                    if anonymized_data[field]:
                        anonymized_data[field] = f"{anonymized_data[field][0]}****"
                    else:
                        anonymized_data[field] = "****"
                elif field == 'telefone':
                    # Anonimiza telefone mantendo últimos 4 dígitos
                    if anonymized_data[field] and len(anonymized_data[field]) >= 4:
                        anonymized_data[field] = f"****{anonymized_data[field][-4:]}"
                    else:
                        anonymized_data[field] = "********"
                else:
                    # Anonimiza outros campos
                    anonymized_data[field] = "****"
        
        return anonymized_data
    
    @staticmethod
    def log_consent(user_id, consent_type, granted):
        """
        Registra consentimento do usuário
        
        Args:
            user_id (str): Identificador do usuário
            consent_type (str): Tipo de consentimento (ex: 'marketing', 'cookies', 'termos')
            granted (bool): Se o consentimento foi concedido ou não
            
        Returns:
            bool: True se o registro foi bem-sucedido, False caso contrário
        """
        try:
            consent_log = {
                'user_id': user_id,
                'consent_type': consent_type,
                'granted': granted,
                'timestamp': datetime.datetime.utcnow().isoformat(),
                'ip_address': request.remote_addr,
                'user_agent': request.user_agent.string
            }
            
            # Em produção, salvar em banco de dados
            # Aqui apenas retornamos o log para demonstração
            return True
        except Exception as e:
            print(f"Erro ao registrar consentimento: {str(e)}")
            return False
    
    @staticmethod
    def get_privacy_policy():
        """
        Retorna a política de privacidade atual
        
        Returns:
            dict: Política de privacidade
        """
        privacy_policy = {
            'version': '1.0',
            'last_updated': '2025-05-16',
            'sections': [
                {
                    'title': 'Coleta de Dados',
                    'content': 'O Coco Bambu Alphaville coleta informações que você nos fornece diretamente, como nome, e-mail, telefone e mensagens enviadas através de nossos formulários de contato e avaliação.'
                },
                {
                    'title': 'Uso de Dados',
                    'content': 'Utilizamos seus dados para responder às suas solicitações e mensagens, processar reservas e pedidos, enviar comunicações sobre promoções e eventos (apenas se você optar por recebê-las), e melhorar nossos serviços e experiência do cliente.'
                },
                {
                    'title': 'Proteção de Dados',
                    'content': 'Implementamos medidas de segurança para proteger suas informações contra acesso não autorizado, alteração, divulgação ou destruição.'
                },
                {
                    'title': 'Seus Direitos',
                    'content': 'Você tem o direito de acessar, corrigir ou excluir seus dados pessoais a qualquer momento. Para exercer esses direitos, entre em contato conosco através dos canais informados em nossa página de contato.'
                },
                {
                    'title': 'Cookies',
                    'content': 'Nosso site utiliza cookies para melhorar sua experiência de navegação. Você pode configurar seu navegador para recusar todos os cookies ou para indicar quando um cookie está sendo enviado.'
                },
                {
                    'title': 'Compartilhamento de Dados',
                    'content': 'Não compartilhamos seus dados pessoais com terceiros, exceto quando necessário para a prestação de serviços solicitados por você ou quando exigido por lei.'
                }
            ]
        }
        
        return privacy_policy
    
    @staticmethod
    def get_terms_of_service():
        """
        Retorna os termos de serviço atuais
        
        Returns:
            dict: Termos de serviço
        """
        terms_of_service = {
            'version': '1.0',
            'last_updated': '2025-05-16',
            'sections': [
                {
                    'title': 'Aceitação dos Termos',
                    'content': 'Ao utilizar nosso site e serviços, você concorda com estes Termos de Serviço. Se você não concordar com algum dos termos, não poderá acessar o site ou utilizar nossos serviços.'
                },
                {
                    'title': 'Uso do Site',
                    'content': 'Você concorda em utilizar o site apenas para fins legais e de acordo com estes Termos. Você não deve utilizar o site de maneira que possa danificar, desabilitar, sobrecarregar ou prejudicar o site ou interferir no uso do site por terceiros.'
                },
                {
                    'title': 'Conteúdo do Usuário',
                    'content': 'Ao enviar avaliações, comentários ou sugestões através do site, você concede ao Coco Bambu Alphaville o direito não exclusivo de utilizar, reproduzir, adaptar, publicar, traduzir e distribuir seu conteúdo em qualquer mídia. Você é responsável pelo conteúdo que envia e garante que ele não viola direitos de terceiros.'
                },
                {
                    'title': 'Propriedade Intelectual',
                    'content': 'O conteúdo do site, incluindo textos, gráficos, logotipos, ícones, imagens, clipes de áudio, downloads digitais e compilações de dados, é propriedade do Coco Bambu Alphaville e está protegido por leis de direitos autorais.'
                },
                {
                    'title': 'Limitação de Responsabilidade',
                    'content': 'O Coco Bambu Alphaville não será responsável por quaisquer danos diretos, indiretos, incidentais, consequenciais ou punitivos resultantes do uso ou incapacidade de usar o site ou serviços.'
                },
                {
                    'title': 'Alterações nos Termos',
                    'content': 'O Coco Bambu Alphaville reserva-se o direito de modificar estes Termos a qualquer momento. As alterações entrarão em vigor imediatamente após a publicação dos Termos revisados no site.'
                }
            ]
        }
        
        return terms_of_service
    
    @staticmethod
    def set_cookie_consent(consent_granted):
        """
        Define o consentimento de cookies na sessão
        
        Args:
            consent_granted (bool): Se o consentimento foi concedido ou não
            
        Returns:
            bool: True se a operação foi bem-sucedida, False caso contrário
        """
        try:
            session['cookie_consent'] = consent_granted
            session['cookie_consent_timestamp'] = datetime.datetime.utcnow().isoformat()
            return True
        except Exception as e:
            print(f"Erro ao definir consentimento de cookies: {str(e)}")
            return False
    
    @staticmethod
    def has_cookie_consent():
        """
        Verifica se o usuário concedeu consentimento para cookies
        
        Returns:
            bool: True se o consentimento foi concedido, False caso contrário
        """
        return session.get('cookie_consent', False)
    
    @staticmethod
    def get_data_retention_policy():
        """
        Retorna a política de retenção de dados
        
        Returns:
            dict: Política de retenção de dados
        """
        retention_policy = {
            'avaliações': '2 anos',
            'mensagens_contato': '1 ano',
            'dados_pessoais': '1 ano após último acesso',
            'logs_acesso': '90 dias'
        }
        
        return retention_policy
