# **ParkingManager**

O **ParkingManager** é uma API REST desenvolvida para gerenciar um sistema de estacionamento. Ela permite o controle de entrada e saída de veículos, cálculo de valores a serem pagos com base no tempo de permanência, e também disponibiliza relatórios sobre as movimentações realizadas.

### **Tecnologias Utilizadas**

-   **Django**: Framework web robusto e escalável.
-   **Django REST Framework (DRF)**: Extensão do Django para construção de APIs RESTful.
-   **SQLite**: Banco de dados utilizado para armazenamento dos dados.
-   **JWT (JSON Web Token)**: Para autenticação segura dos endpoints protegidos.
-   **drf-spectacular**: Ferramenta para geração de documentação interativa no formato OpenAPI.
  
<div style="display: inline_block; background-color: white"><br>
  <img align="center" alt="Python" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" />
  <img align="center" alt="Git" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" />
  <img style="background: white" align="center" alt="Django" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg" />         
  <img style="background: white" align="center" alt="DRF" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/djangorest/djangorest-original.svg" /> 
  <img style="background: white" align="center" alt="SQLite" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/sqlite/sqlite-original.svg" /> 
</div>

---

### **Funcionalidades**

-   **Entrada de Veículo**: Registra a entrada de um veículo no estacionamento.
-   **Saída de Veículo**: Registra a saída de um veículo, verificando pagamento e tempo de tolerância.
-   **Cálculo do Valor a Pagar**: Calcula o valor devido com base no tempo de permanência (R$ 5,00 por hora, considerando frações como hora completa).
-   **Pagamento**: Registra o pagamento para um veículo específico.
-   **Relatório**: Lista todas as movimentações de entrada e saída realizadas.
-   **Autenticação JWT**: Protege os endpoints para que apenas usuários autenticados possam acessá-los.

---

## **Pré-requisitos**

Antes de iniciar, você precisará ter instalado na sua máquina:

-   Python 3.8 ou superior
-   Pip (gerenciador de pacotes do Python)

---

## **Passo a Passo para Configuração**

### **1. Clonar o Repositório**

```bash
git clone https://github.com/fabiano-filho/parking_govOne.git
cd parking_govOne
```

### **2. Criar e Ativar o Ambiente Virtual**

```bash
python -m venv env
# Ativar o ambiente virtual:
# Windows:
env\Scripts\activate
# Linux/Mac:
source env/bin/activate
```

### **3. Instalar as Dependências**

```bash
pip install -r requirements.txt
```

### **4. Configurar Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
ESTACIONAMENTO_VALOR_HORA=5.0
TOLERANCIA_TEMPO_SAIDA=10
```

Essas variáveis configuram o valor por hora do estacionamento e o tempo de tolerância após o pagamento, respectivamente.
Obs.: por padrão, o sistema irá considerar os valores 5.0 e 10, respectivamente.

### **5. Configurar o Banco de Dados**

Execute as migrações para criar as tabelas no banco de dados:

```bash
python manage.py makemigrations
python manage.py migrate
```

### **6. Criar um Superusuário**

Crie um superusuário para acessar o painel administrativo e realizar operações:

```bash
python manage.py createsuperuser
```

### **7. Iniciar o Servidor**

Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

Acesse a aplicação no navegador: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## **Documentação da API**

A documentação interativa da API está disponível nos seguintes endpoints (usando `drf-spectacular`):

-   **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)

---

## **Como Usar a API**

### **Autenticação**

Antes de acessar os endpoints protegidos, obtenha um token JWT no endpoint `/api/token/`:

**POST `/api/token/`**

```json
{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```

Resposta de sucesso:

```json
{
    "refresh": "TOKEN_DE_ATUALIZACAO",
    "access": "TOKEN_DE_ACESSO"
}
```

Inclua o token `access` no cabeçalho das requisições:

```
Authorization: Bearer <TOKEN_DE_ACESSO>
```

---

### **Endpoints Disponíveis**

1. **Registrar Entrada de Veículo**

    - **POST `/api/entrada/`**
    - **Corpo da Requisição:**
        ```json
        {
            "placa": "ABC1234"
        }
        ```

2. **Registrar Saída de Veículo**

    - **POST `/api/saida/`**
    - **Corpo da Requisição:**
        ```json
        {
            "placa": "ABC1234",
            "pago": true
        }
        ```

3. **Consultar Valor a Pagar**

    - **GET `/api/valor/?placa=ABC1234`**

4. **Registrar Pagamento**

    - **POST `/api/pagar/`**
    - **Corpo da Requisição:**
        ```json
        {
            "placa": "ABC1234"
        }
        ```

5. **Relatório de Movimentações**
    - **GET `/api/relatorio/`**

---

## **Testes Automatizados**

### **Como Executar os Testes**

1. Certifique-se de que o banco de dados de testes está configurado.
2. Execute os testes com o comando:

```bash
python manage.py test
```

### **O que é Testado?**

-   Registro de entrada de veículos (incluindo validação de placas).
-   Registro de saída de veículos, com validação de pagamento e tolerância.
-   Cálculo de valores a pagar.
-   Registro de pagamento.
-   Relatórios.
-   Proteção com autenticação JWT (verificação de acesso não autenticado).

---
