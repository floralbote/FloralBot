## 🌸 FloralBot AI — Sistema de Atendimento com Essências Florais de Bach

**FloralBot AI** é um sistema completo desenvolvido em **Flask**, projetado para gestão de usuários, administração de florais e um **chatbot inteligente** integrado com **IA (Gemini API)** para auxiliar usuários com sugestões baseadas nas Essências Florais de Bach.

---

## 🚀 Funcionalidades Principais

### 🔐 Autenticação e Controle de Usuários

* **Cadastro Completo**:
    * Nome, E-mail, Senha.
    * Data de nascimento (com cálculo automático de idade).
    * Gênero (Feminino / Masculino / Outro + campo personalizado / Prefiro não dizer).
    * Login e `logout` seguro.
* **Painel Administrativo**:
    * Listar usuários.
    * Criar, editar e excluir contas.
    * Definir permissões de administrador.

### 🌼 Administração de Florais

* **CRUD** (Create, Read, Update, Delete) para gestão de florais.
* Página pública listando florais disponíveis.

### 🤖 Chatbot Inteligente

* Integração com a **Gemini API** para fornecer sugestões de Essências Florais de Bach baseadas na interação do usuário.

---

## 🗄 Banco de Dados

* **Tecnologia**: SQLite.
* **Migrações**: Gerenciamento de schema com **Alembic**.
* **Relacionamentos**: `User 1 → N ChatHistory`.
* **Exclusão em cascata**: Se um usuário for deletado, todo o histórico de conversas associado é removido automaticamente.

---

## 🎨 Frontend

* **Framework**: **TailwindCSS** para estilização rápida e moderna.
* **Design**: Layout **responsivo**.
* **Interatividade (JavaScript)**:
    * Cálculo automático de idade no formulário de cadastro.
    * Exibição condicional do campo "Outro gênero".
    * Interações dinâmicas do chatbot.
* **Templates**: Utiliza **HTML** com **Jinja2**.

---

## 🧩 Estrutura do Projeto

```

floralbot_ai/
│
├── Documentação/
│   └── ML_DL-Métricas/
│       ├── FLORALBOT_de_Template_Projeto_ML_DL.ipynb
│       ├── Relatorio Final ML_DL - FloralBot.pdf
│       └── floralbot_de_template_projeto_ml_dl.py
│        ├── Documentação do Sistema.pdf
│
├── .vscode/
├── __pycache__/
│
├── app/
│   ├── auth/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/ (se existir)
│   ├── templates/
│   ├── models.py
│   ├── routes.py
│   ├── chatbot.py
│   ├── utils.py
│   └── ml_pipeline.py
│
├── database/
│
├── migrations/
│
├── seeds/
│
├── tests/
│
├── run.py
├── config.py
├── config_gemini.py
├── create_db.py
│
├── requirements.txt
├── package.json
├── package-lock.json
├── tailwind.config.js
├── .gitignore
├── .gitattributes
└── README.md

```

---

## ⚙️ Como Rodar o Projeto Localmente

Certifique-se de ter o **Python 3.12** instalado.

1.  **Ativar o ambiente virtual**
    ```bash
    .\venv\Scripts\Activate
    ```

2.  **Instalar dependências**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurar Variáveis de Ambiente**
    Crie o arquivo `.env` e adicione sua chave da API do Gemini.
    ```
    GEMINI_API_KEY=SUA_CHAVE_AQUI
    ```

4.  **Executar o servidor**
    ```bash
    python run.py
    ```

Acesse o projeto no seu navegador:

👉 **http://127.0.0.1:5000**

---

## 🔥 Tecnologias Utilizadas

| Categoria | Tecnologia | Uso Principal |
| :--- | :--- | :--- |
| **Backend** | **Python 3.12** | Linguagem principal |
| **Web Framework** | **Flask** | Micro-framework web |
| **Banco de Dados** | **SQLAlchemy** | ORM para SQLite |
| **Migrações** | **Alembic** | Gerenciamento de schema |
| **Inteligência Artificial** | **Gemini API** | Motor do Chatbot |
| **Frontend** | **TailwindCSS** | Estilização CSS utility-first |
| **Templates** | **HTML + Jinja2** | Estrutura e renderização de páginas |
| **Interatividade** | **JavaScript** | Lógica de frontend e manipulação de DOM |

---

## 🧪 Testes

Estrutura reservada para implementação futura de testes unitários:

tests/

---

## ⭐ Autoria

* **Apoio de Inteligência Artificial:** Desenvolvido com o suporte essencial do **ChatGPT**.
* **Mentoria e Orientação:** Conduzido sob a mentoria especializada da **Dra. Fernanda Oliveira**.
* **Customização Final:** Detalhadamente customizado e finalizado pelos **criadores do FloralBot AI:**

* Fabia Santos
* Gisele Santos
* Giulia Santos
* Gustavo Marinho
* Rhafael Marques

_3º e 4º semestre de Gestão da Tecnologia da Informação - UniFECAF_.

---

## 💖 Aviso Importante

Este sistema é de natureza **educacional** e **não substitui o acompanhamento profissional de saúde ou terapias com florais**.
O chatbot fornece sugestões baseadas nos dados e regras definidas.
