#!/bin/bash

# Script para executar testes e validar o site Coco Bambu Alphaville
# Autor: Manus AI
# Data: 17/05/2025

echo "=== Iniciando testes do site Coco Bambu Alphaville ==="

# Criar diretório para relatórios de teste se não existir
mkdir -p /home/ubuntu/site_coco_bambu/test_reports

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source /home/ubuntu/site_coco_bambu/coco_bambu_app/venv/bin/activate

# Instalar dependências de teste
echo "Instalando dependências de teste..."
pip install pytest flask-testing coverage pytest-html

# Executar testes unitários
echo "Executando testes unitários..."
cd /home/ubuntu/site_coco_bambu/coco_bambu_app
python -m unittest discover -s tests

# Executar testes com cobertura
echo "Executando testes com cobertura..."
coverage run -m unittest discover -s tests
coverage report -m
coverage html -d /home/ubuntu/site_coco_bambu/test_reports/coverage

# Verificar sintaxe Python
echo "Verificando sintaxe Python..."
find . -name "*.py" -exec python -m py_compile {} \;

# Verificar sintaxe HTML
echo "Verificando sintaxe HTML..."
find ./src/templates -name "*.html" -exec echo "Verificando {}" \; -exec python -c "import re; f=open('{}', 'r'); content=f.read(); f.close(); print('OK' if re.search(r'<html.*>.*</html>', content, re.DOTALL) else 'Erro')" \;

# Verificar sintaxe CSS
echo "Verificando sintaxe CSS..."
find ./src/static/css -name "*.css" -exec echo "Verificando {}" \; -exec python -c "import re; f=open('{}', 'r'); content=f.read(); f.close(); print('OK' if content and not re.search(r'[^{}]+{[^}]*[^;{]}\s', content) else 'Possível erro')" \;

# Verificar sintaxe JavaScript
echo "Verificando sintaxe JavaScript..."
find ./src/static/js -name "*.js" -exec echo "Verificando {}" \; -exec python -c "import re; f=open('{}', 'r'); content=f.read(); f.close(); print('OK' if content and not re.search(r'[^;{}]\s*$', content, re.MULTILINE) else 'Possível erro')" \;

# Iniciar servidor para testes manuais
echo "Iniciando servidor para testes manuais..."
echo "Acesse http://localhost:5000 para testar manualmente"
echo "Pressione Ctrl+C para encerrar o servidor quando terminar os testes"
cd /home/ubuntu/site_coco_bambu/coco_bambu_app
python -m src.main

echo "=== Testes concluídos ==="
