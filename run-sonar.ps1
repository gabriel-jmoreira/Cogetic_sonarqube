# Instala dependências de desenvolvimento
pip install -r playwright-python/requirements-dev.txt

# Gera relatório de cobertura de testes
cd playwright-python
python -m pytest --cov=./ --cov-report=xml:coverage.xml --junitxml=test-results.xml -v

# Volta para o diretório raiz
cd ..

# Executa o scanner do SonarQube
docker run --rm \
    -e SONAR_HOST_URL="http://localhost:9000" \
    -e SONAR_LOGIN="your-sonar-token" \
    -v "${PWD}:/usr/src" \
    sonarsource/sonar-scanner-cli
