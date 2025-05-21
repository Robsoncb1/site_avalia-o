# Documentação do Site de Avaliação do Buffet - Coco Bambu Alphaville

## Visão Geral

Este documento contém a documentação completa do site de avaliação do buffet para o restaurante Coco Bambu Alphaville. O site foi desenvolvido para permitir que os clientes avaliem a qualidade do buffet e forneçam sugestões, em um ambiente interativo, dinâmico e comercialmente atraente.

## Estrutura do Projeto

```
coco_bambu_app/
├── src/
│   ├── models/         # Modelos de banco de dados
│   ├── routes/         # Rotas e controladores
│   ├── static/         # Arquivos estáticos (CSS, JS, imagens)
│   │   ├── css/        # Folhas de estilo
│   │   ├── js/         # Scripts JavaScript
│   │   └── img/        # Imagens e ícones
│   ├── templates/      # Templates HTML
│   ├── utils/          # Utilitários e funções auxiliares
│   └── main.py         # Ponto de entrada da aplicação
├── tests/              # Testes automatizados
├── venv/               # Ambiente virtual Python
└── requirements.txt    # Dependências do projeto
```

## Tecnologias Utilizadas

- **Backend**: Flask (Python 3.11)
- **Banco de Dados**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Bibliotecas**: SQLAlchemy, Bleach, Flask-Testing
- **Ferramentas de Teste**: unittest, coverage

## Funcionalidades Principais

### 1. Avaliação do Buffet
- Sistema de avaliação com estrelas (1-5) para diferentes aspectos do buffet
- Formulário para comentários e sugestões textuais
- Seleção de pratos favoritos
- Sugestões de novos pratos

### 2. Visualização de Feedback
- Exibição de avaliações aprovadas
- Filtros por classificação, data e categoria
- Paginação de resultados

### 3. Menu do Buffet
- Apresentação visual dos pratos disponíveis
- Categorização por tipo de prato
- Destaques e pratos especiais

### 4. Contato e Informações
- Formulário de contato
- Mapa de localização
- Informações sobre horários e preços
- Política de privacidade e termos de uso

## Modelos de Dados

### Avaliacao
Armazena as avaliações dos clientes sobre o buffet.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Identificador único |
| nome | String | Nome do cliente |
| email | String | Email do cliente |
| data_avaliacao | DateTime | Data e hora da avaliação |
| qualidade | Integer | Avaliação da qualidade (1-5) |
| variedade | Integer | Avaliação da variedade (1-5) |
| apresentacao | Integer | Avaliação da apresentação (1-5) |
| reposicao | Integer | Avaliação da reposição (1-5) |
| atendimento | Integer | Avaliação do atendimento (1-5) |
| media_geral | Float | Média das avaliações |
| comentario | Text | Comentário textual |
| pratos_favoritos | String | Lista de pratos favoritos |
| sugestao_pratos | String | Sugestão de novos pratos |
| frequencia | String | Frequência de visita |
| permissao_contato | Boolean | Permissão para contato |
| aprovada | Boolean | Status de aprovação |

### Contato
Armazena mensagens enviadas através do formulário de contato.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Identificador único |
| nome | String | Nome do remetente |
| email | String | Email do remetente |
| telefone | String | Telefone do remetente |
| assunto | String | Assunto da mensagem |
| mensagem | Text | Conteúdo da mensagem |
| data_envio | DateTime | Data e hora do envio |
| newsletter | Boolean | Inscrição na newsletter |
| lida | Boolean | Status de leitura |
| respondida | Boolean | Status de resposta |

## Rotas da Aplicação

### Rotas Principais
- **/** - Página inicial
- **/avaliar** - Formulário de avaliação
- **/feedback** - Visualização de avaliações
- **/menu** - Menu do buffet
- **/sobre** - Informações sobre o restaurante
- **/contato** - Formulário de contato

### Rotas de API
- **/api/avaliacoes** - API para obter avaliações em formato JSON
- **/submit_avaliacao** - Endpoint para envio de avaliações
- **/submit_contato** - Endpoint para envio de mensagens de contato

## Segurança e Privacidade

### Medidas de Segurança
- Sanitização de entradas para prevenir XSS
- Validação de dados em formulários
- Proteção contra injeção SQL via SQLAlchemy
- Detecção e prevenção de spam
- Limitação de taxa para prevenir ataques de força bruta

### Privacidade
- Política de privacidade clara e acessível
- Consentimento explícito para uso de dados
- Anonimização de dados pessoais quando necessário
- Política de retenção de dados definida
- Conformidade com regulamentações de proteção de dados

## Acessibilidade

O site foi desenvolvido seguindo as diretrizes de acessibilidade WCAG, incluindo:

- Navegação por teclado
- Contraste adequado para texto e elementos visuais
- Textos alternativos para imagens
- Estrutura semântica HTML
- Suporte a leitores de tela
- Responsividade para diferentes dispositivos
- Preferências de movimento reduzido

## Testes

### Testes Automatizados
- Testes unitários para modelos de dados
- Testes para funções de segurança e privacidade
- Testes de rotas e templates
- Cobertura de código

### Testes Manuais
- Verificação de compatibilidade cross-browser
- Testes de usabilidade
- Validação de formulários
- Testes de responsividade

## Instruções de Implantação

### Requisitos do Sistema
- Python 3.11 ou superior
- MySQL 5.7 ou superior
- Servidor web compatível com WSGI (recomendado: Nginx + Gunicorn)
- 1GB de RAM mínimo
- 10GB de espaço em disco

### Passos para Implantação

1. **Preparação do Ambiente**
   ```bash
   # Clonar o repositório
   git clone [URL_DO_REPOSITORIO]
   cd coco_bambu_app
   
   # Criar e ativar ambiente virtual
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   
   # Instalar dependências
   pip install -r requirements.txt
   ```

2. **Configuração do Banco de Dados**
   ```bash
   # Criar banco de dados MySQL
   mysql -u root -p
   CREATE DATABASE coco_bambu;
   CREATE USER 'coco_user'@'localhost' IDENTIFIED BY 'senha_segura';
   GRANT ALL PRIVILEGES ON coco_bambu.* TO 'coco_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

3. **Configuração da Aplicação**
   - Editar variáveis de ambiente:
     ```
     export DB_USERNAME=coco_user
     export DB_PASSWORD=senha_segura
     export DB_NAME=coco_bambu
     export SECRET_KEY=chave_secreta_muito_segura
     ```

4. **Inicialização do Banco de Dados**
   ```bash
   # Dentro do diretório do projeto, com ambiente virtual ativado
   python -c "from src.main import app, db; app.app_context().push(); db.create_all()"
   ```

5. **Configuração do Servidor Web (Nginx + Gunicorn)**
   ```bash
   # Instalar Gunicorn
   pip install gunicorn
   
   # Criar arquivo de configuração do Nginx
   sudo nano /etc/nginx/sites-available/coco_bambu
   ```
   
   Conteúdo do arquivo:
   ```
   server {
       listen 80;
       server_name seu_dominio.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
   
   ```bash
   # Ativar configuração
   sudo ln -s /etc/nginx/sites-available/coco_bambu /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

6. **Iniciar a Aplicação**
   ```bash
   # Iniciar com Gunicorn
   gunicorn -w 4 -b 127.0.0.1:8000 "src.main:app"
   ```

7. **Configuração de Serviço (opcional)**
   ```bash
   # Criar arquivo de serviço systemd
   sudo nano /etc/systemd/system/coco_bambu.service
   ```
   
   Conteúdo do arquivo:
   ```
   [Unit]
   Description=Coco Bambu Alphaville Buffet Evaluation Site
   After=network.target
   
   [Service]
   User=www-data
   WorkingDirectory=/caminho/para/coco_bambu_app
   Environment="PATH=/caminho/para/coco_bambu_app/venv/bin"
   Environment="DB_USERNAME=coco_user"
   Environment="DB_PASSWORD=senha_segura"
   Environment="DB_NAME=coco_bambu"
   Environment="SECRET_KEY=chave_secreta_muito_segura"
   ExecStart=/caminho/para/coco_bambu_app/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 "src.main:app"
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   ```bash
   # Ativar e iniciar o serviço
   sudo systemctl enable coco_bambu
   sudo systemctl start coco_bambu
   ```

## Manutenção e Atualizações

### Backup do Banco de Dados
```bash
# Backup diário
mysqldump -u coco_user -p coco_bambu > backup_$(date +%Y%m%d).sql
```

### Monitoramento de Logs
```bash
# Verificar logs da aplicação
sudo journalctl -u coco_bambu
```

### Atualizações de Segurança
- Manter todas as dependências atualizadas:
  ```bash
  pip install --upgrade -r requirements.txt
  ```
- Verificar regularmente por vulnerabilidades conhecidas

## Conclusão

Este site foi desenvolvido seguindo as melhores práticas de desenvolvimento web, com foco em experiência do usuário, acessibilidade, segurança e privacidade. A arquitetura modular permite fácil manutenção e expansão futura.

Para suporte técnico ou dúvidas, entre em contato com a equipe de desenvolvimento.

---

© 2025 Coco Bambu Alphaville - Todos os direitos reservados
