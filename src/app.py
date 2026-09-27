import os
import re
import time
import requests
from pathlib import Path

import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# Configuração da página
st.set_page_config(
    page_title="MewBot - Assistente Virtual Pokédex",
    page_icon="🔮",
    layout="centered"
)

st.title("🔮 MewBot: Assistente Virtual Pokédex")
st.caption("Agente Inteligente com Integração Direta à PokéAPI e Base de Conhecimento Própria")

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DATA = RAIZ_PROJETO / "data"

# -----------------------------------------------------------------------------
# 1. Busca de dados em tempo real na PokéAPI com Cache
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def buscar_dados_pokeapi(nome_ou_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{str(nome_ou_id).lower().strip()}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            dados = res.json()
            nome = dados['name'].capitalize()
            pokedex_id = dados['id']
            tipos = ", ".join([t['type']['name'].capitalize() for t in dados['types']])
            altura = dados['height'] / 10
            peso = dados['weight'] / 10
            stats_dict = {s['stat']['name']: s['base_stat'] for s in dados['stats']}
            total_stats = sum(stats_dict.values())
            stats_formatted = "\n".join([f"- **{k.upper()}**: {v}" for k, v in stats_dict.items()])
            habilidades = ", ".join([h['ability']['name'].capitalize() for h in dados['abilities']])

            return f"""=== DADOS OFICIAIS DA POKÉAPI EM TEMPO REAL ===
Nome: {nome} (#{pokedex_id:04d})
Tipo(s): {tipos}
Altura: {altura} m | Peso: {peso} kg
Habilidades: {habilidades}
Total de Atributos Base (BST): {total_stats}

Atributos Base (Stats):
{stats_formatted}
==============================================="""
    except Exception:
        pass
    return None


def identificar_pokemon_no_prompt(prompt):
    palavras = re.findall(r'\b[a-zA-Z0-9-]+\b', prompt.lower())
    stop_words = {
        "qual", "quais", "como", "sobre", "mais", "forte", "pokemon", "pokémon", 
        "mew", "stats", "tipo", "queros", "quero", "top", "lista", "com", "para"
    }
    
    for palavra in palavras:
        if palavra not in stop_words and len(palavra) > 2:
            contexto_api = buscar_dados_pokeapi(palavra)
            if contexto_api:
                return contexto_api, palavra
    return None, None


def carregar_base_conhecimento():
    caminho = PASTA_DATA / "base_conhecimento.txt"
    if caminho.exists():
        return caminho.read_text(encoding="utf-8")
    return "Base de conhecimento não encontrada."


def obter_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            pass
    return api_key.strip() if api_key else None


api_key = obter_api_key()

if not api_key:
    api_key = st.sidebar.text_input("Insira sua Gemini API Key:", type="password").strip()

base_conhecimento_mew = carregar_base_conhecimento()


def criar_instrucao(contexto_dinamico):
    return f"""
Você é o MewBot, um assistente virtual especialista no universo Pokémon.

=== BASE DE CONHECIMENTO PRINCIPAL (LORE E MEW) ===
{base_conhecimento_mew}

=== DADOS ADICIONAIS OBTIDOS EM TEMPO REAL ===
{contexto_dinamico if contexto_dinamico else "Nenhum Pokémon específico consultado na API para esta pergunta."}

REGRAS DE COMPORTAMENTO:
1. Sempre priorize as informações exatas presentes nas bases acima.
2. Para perguntas comparativas, listas, rankings ou análises gerais (ex: "quais os mais fortes", "top 10", "evoluções"), você ESTÁ AUTORIZADO a usar seu conhecimento sobre Pokémon para responder de forma rica e detalhada, comparando com os dados fornecidos.
3. Se o assunto for TOTALMENTE ALHEIO ao universo Pokémon (ex: culinária, política, geografia do mundo real), responda exatamente:
"Desculpe, não tenho essa informação na minha base de conhecimento atual."
4. Mantenha um tom amigável, direto, claro e especialista.
"""


if not api_key:
    st.info("👈 Insira sua Gemini API Key na barra lateral para ativar o assistente.")
else:
    client = genai.Client(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Pergunte sobre o Mew ou qualquer um dos 1025+ Pokémon..."):

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("O MewBot está consultando a PokéAPI e analisando os dados..."):
                
                contexto_api, pokemon_encontrado = identificar_pokemon_no_prompt(prompt)
                system_instruction = criar_instrucao(contexto_api)

                modelos_para_tentar = [
                    "gemini-3.8-flash",
                    "gemini-2.0-flash",
                    "gemini-1.5-flash"
                ]
                
                resposta_sucesso = False
                ultimo_erro = None

                for modelo in modelos_para_tentar:
                    for tentativa in range(2):
                        try:
                            response = client.models.generate_content(
                                model=modelo,
                                contents=prompt,
                                config=types.GenerateContentConfig(
                                    system_instruction=system_instruction,
                                    temperature=0.3
                                )
                            )

                            resposta_texto = response.text

                            if resposta_texto:
                                st.write(resposta_texto)
                                if pokemon_encontrado:
                                    st.caption(f"🌐 *Dados obtidos em tempo real via PokéAPI para: `{pokemon_encontrado.capitalize()}`*")
                                else:
                                    st.caption("📚 *Consulta realizada na Base de Conhecimento do MewBot*")
                                
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": resposta_texto
                                })
                                resposta_sucesso = True
                                break

                        except APIError as e:
                            ultimo_erro = e
                            time.sleep(1)
                        except Exception as e:
                            ultimo_erro = e
                            time.sleep(1)

                    if resposta_sucesso:
                        break

                if not resposta_sucesso and ultimo_erro:
                    st.error(f"Erro ao comunicar com a API: {ultimo_erro}")