from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# ========================= FUNÇÕES =========================

def anonimizar_nome(nome):
    """Substitui o nome por 'Usuario' + número aleatório"""
    return "Usuario" + str(random.randint(1000, 9999))

def anonimizar_email(email):
    """Substitui o email por email genérico"""
    dominio = email.split("@")[-1] if "@" in email else "exemplo.com"
    return f"user{random.randint(1000,9999)}@{dominio}"

def pseudonimizar_valor(valor):
    """
    Substitui cada caractere do valor por outro caractere ASCII simples.
    Mantém tamanho similar.
    """
    resultado = ""
    for char in str(valor):
        if char.isalpha():
            # shift simples nas letras (rot13)
            if char.islower():
                resultado += chr((ord(char) - 97 + 13) % 26 + 97)
            else:
                resultado += chr((ord(char) - 65 + 13) % 26 + 65)
        elif char.isdigit():
            # muda os números para outro dígito
            resultado += str((int(char) + 5) % 10)
        else:
            resultado += char
    return resultado

def despseudonimizar_valor(valor):
    """
    Reverte a pseudonimização aplicada pelo pseudonimizar_valor.
    """
    resultado = ""
    for char in str(valor):
        if char.islower():
            resultado += chr((ord(char) - 97 - 13) % 26 + 97)
        elif char.isupper():
            resultado += chr((ord(char) - 65 - 13) % 26 + 65)
        elif char.isdigit():
            resultado += str((int(char) - 5) % 10)
        else:
            resultado += char
    return resultado

# ========================= ROTAS =========================

@app.route("/anonimizar", methods=["POST"])
def anonimizar():
    """
    Recebe JSON com dados e retorna versão anonimizada.
    """
    dados = request.get_json()
    dados_anonimizados = {}

    if "nome" in dados:
        dados_anonimizados["nome"] = anonimizar_nome(dados["nome"])
    if "email" in dados:
        dados_anonimizados["email"] = anonimizar_email(dados["email"])

    return jsonify(dados_anonimizados)

@app.route("/pseudonimizar", methods=["POST"])
def pseudonimizar():
    """
    Recebe JSON com dados e retorna versão pseudonimizada.
    """
    dados = request.get_json()
    dados_pseudo = {}

    for chave, valor in dados.items():
        dados_pseudo[chave] = pseudonimizar_valor(valor)

    return jsonify(dados_pseudo)

@app.route("/verificar_pseudonimo", methods=["POST"])
def verificar_pseudonimo():
    """
    Recebe JSON com valores pseudonimizados e retorna os valores originais.
    """
    dados = request.get_json()
    dados_originais = {}

    for chave, valor in dados.items():
        dados_originais[chave] = despseudonimizar_valor(valor)

    return jsonify(dados_originais)