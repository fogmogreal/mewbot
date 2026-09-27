# 🔮 MewBot: Assistente Virtual Pokédex

> Agente conversacional inteligente especialista em Pokémon, desenvolvido para o desafio de projeto da **Digital Innovation One (DIO)**.

---

## 📌 Intuito do Projeto

O **MewBot** foi projetado para atuar como um assistente especialista sobre as adoráveis e poderosas criaturas do universo Pokémon. 

O objetivo principal é demonstrar a aplicação prática de uma arquitetura **RAG (Retrieval-Augmented Generation)** híbrida e simples:
1. **Base Local:** Consulta dados aprofundados sobre a história, biologia do Mew, fatos históricos de desenvolvimento (1996) e regras de Pokémon TCG através de um arquivo de texto local.
2. **Consultas em Tempo Real:** Conecta-se diretamente à **PokéAPI** via requisições HTTP para buscar estatísticas, tipos, peso e altura de qualquer um dos mais de 1.000 Pokémon existentes sem a necessidade de manter bancos de dados locais pesados.
3. **Segurança de Respostas:** Utiliza instruções de sistema para evitar alucinações de IA e responder estritamente dentro do contexto do universo Pokémon.

---

## 🛠️ Tecnologias e APIs Utilizadas

- **Linguagem:** Python 3.10+
- **Interface Gráfica:** Streamlit
- **Modelo de IA / LLM:** Google Gemini API (via SDK oficial `google-genai`)
- **API de Dados Externa:** PokéAPI (REST API)
- **Gerenciamento de Requisições:** `requests`

---

## ✨ Funcionalidades do Assistente

- 🔮 **Especialista em Mew:** Respostas detalhadas sobre a história, lore e estratégias de TCG do Mew baseadas na base de conhecimento local.
- 🌐 **Pokédex em Tempo Real:** Identificação automática de Pokémon citados na conversa para busca instantânea de estatísticas (BST, atributos, peso, altura e tipo) na PokéAPI.
- 📊 **Análises e Comparações:** Capacidade de comparar atributos entre diferentes Pokémon e gerar rankings táticos.
- 🛡️ **Filtro contra Tópicos Alheios:** Recusa amigável para perguntas fora do universo Pokémon, evitando respostas incorretas ou inventadas.
- 🔄 **Resiliência de API:** Alternância automática entre modelos Gemini em caso de instabilidade ou limite de taxa na API.

---

## 📁 Estrutura do Repositório (Tree)

```text
assistente-virtual-ia/
├── 📁 data/
│   └── 📄 base_conhecimento.txt   # Base estática com dados do Mew, TCG e regras
├── 📁 src/
│   └── 🐍 app.py                  # Código principal do assistente e interface
├── 📄 .gitignore                  # Arquivos ignorados pelo Git (chaves, cache, venv)
├── 📄 README.md                   # Documentação oficial do projeto
└── 📄 requirements.txt            # Dependências e bibliotecas do Python
```

---

## 📖 Passo a Passo de Como Usar o MewBot (Guia para Iniciantes)

Siga estas etapas simples para rodar o MewBot no seu computador, mesmo que você nunca tenha mexido com Python antes:

### 1. Obtenha sua Gemini API Key
Para usar a inteligência do robô, você precisa de uma chave gratuita do Google:
1. Acesse o site do [Google AI Studio](https://aistudio.google.com/).
2. Faça login com sua conta do Google.
3. Clique em **"Get API key"** (Obter Chave da API) e depois em **"Create API key"**.
4. Copie o código gerado e guarde-o em um local seguro.

---

### 2. Baixe o Projeto para o seu Computador
1. Abra o terminal (Prompt de Comando ou PowerShell no Windows).
2. Baixe o repositório executando o comando:
   ```bash
   git clone https://github.com/SEU_USUARIO/meus-desafios-criativos.git
   ```
3. Entre na pasta do projeto:
   ```bash
   cd meus-desafios-criativos
   ```

---

### 3. Instale as Bibliotecas Necessárias
Digite o comando abaixo no terminal para instalar automaticamente os programas necessários para o MewBot rodar:
```bash
pip install -r requirements.txt
```

---

### 4. Ligue o MewBot
Execute o comando de inicialização:
```bash
streamlit run src/app.py
```

Assim que você pressionar Enter, o navegador da sua máquina abrirá automaticamente na página do **MewBot** (no endereço `http://localhost:8501`).

---

### 5. Como Conversar no Chat
1. Na **barra lateral esquerda** que aparecerá na tela, cole a sua **Gemini API Key** que você copiou no Passo 1.
2. Pronto! Agora você já pode digitar suas dúvidas na caixa de texto do chat no centro da tela.

**Exemplos de perguntas para testar:**
- *"Me conte sobre a história de criação do Mew."*
- *"Quais são os atributos e o peso do Lucario?"*
- *"Qual Pokémon tem os maiores atributos na primeira geração?"*

---

## 🚀 Roadmap de Evolução Futurista (MewBot WhatsApp Edition)

Como próxima etapa de evolução do projeto, o MewBot deixará de ser apenas uma interface web para se tornar um **Bot de WhatsApp interativo** rodando via **FastAPI** e **Baileys/Twilio**, com o mini-game **"Safari Pokémon"**.

### 🎮 Mini-Game de Captura Aleatória no WhatsApp

- 📱 **Integração WhatsApp:** Comunicação bidirecional contínua com suporte a comandos e mensagens de voz.
- 🌿 **Encontros Aleatórios:** O bot gera encontros com Pokémon selvagens ao longo do dia em grupos ou no privado do usuário.
- 🎲 **Mecânica de Captura com Porcentagem de Sucesso:**
  - A taxa de captura é calculada com base nos dados reais do Pokémon na PokéAPI.
  - Pokémon Lendários e Míticos (ex: Mew, Rayquaza) possuem taxas de sucesso baixas (~3% a 5%), enquanto Pokémon comuns possuem taxas mais altas (~40% a 70%).
  - Bônus por uso de diferentes tipos de Pokébolas (Poké Ball, Great Ball, Ultra Ball, Master Ball).
- 💾 **Memória e Progressão por Usuário:**
  - Banco de dados SQLite/PostgreSQL vinculado ao número de telefone do usuário.
  - Registro de **Pokédex Pessoal** (quais Pokémon o usuário já capturou).
  - Sistema de Nível de Treinador, Inventário de Itens e Estatísticas de Capturas bem-sucedidas.

---

## 🙏 Agradecimentos

Agradeço à **Digital Innovation One (DIO)** e aos instrutores pelo conteúdo prático e pela oportunidade de desenvolver este projeto, unindo conceitos modernos de **IA Generativa**, **RAG** e integração de **APIs REST** em uma solução funcional e divertida.

---
*Desenvolvido por fogmogreal.*