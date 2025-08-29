from flask import Flask, render_template, request, redirect, url_for
import json
import os
import uuid

# --- CONFIGURAÇÃO DA APLICAÇÃO ---
app = Flask(__name__)

# Arquivo JSON que servirá como "banco de dados"
ARQUIVO_JSON = "ficha.json"


# --- FUNÇÕES DE AJUDA PARA MANIPULAR DADOS ---

def carregar_dados():
    """
    Carrega os dados do arquivo JSON.
    Se o arquivo não existir ou estiver vazio/corrompido, retorna uma lista vazia.
    """
    if not os.path.exists(ARQUIVO_JSON):
        return []
    with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def salvar_dados(dados):
    """
    Salva os dados (lista de fichas) no arquivo JSON.
    """
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


# --- ROTAS ---

@app.route("/")
def pagina_inicial():
    """
    Página inicial - mostra todas as fichas.
    """
    fichas = carregar_dados()
    return render_template("index.html", fichas=fichas)


@app.route("/ficha/<ficha_id>")
def ver_ficha(ficha_id):
    """
    Visualizar ou criar uma ficha.
    """
    if ficha_id == "nova":
        return render_template("ficha.html", ficha={})
    else:
        fichas = carregar_dados()
        ficha = next((f for f in fichas if f.get("id") == ficha_id), None)
        if ficha:
            return render_template("ficha.html", ficha=ficha)
        else:
            return "Ficha não encontrada!", 404


@app.route("/salvar/<ficha_id>", methods=["POST"])
def salvar_ficha(ficha_id):
    """
    Salvar ou atualizar uma ficha a partir do formulário.
    """
    fichas = carregar_dados()

    # Coleta todos os dados enviados no formulário
    dados_formulario = {
        # Cabeçalho
        "nome_personagem": request.form.get("nome_personagem"),
        "classe": request.form.get("classe"),
        "nivel": request.form.get("nivel"),
        "antecedente": request.form.get("antecedente"),
        "nome_jogador": request.form.get("nome_jogador"),
        "raca": request.form.get("raca"),
        "tendencia": request.form.get("tendencia"),
        "pontos_experiencia": request.form.get("pontos_experiencia"),
        "tamanho": request.form.get("tamanho"),

        # Atributos
        "forca": request.form.get("forca"),
        "destreza": request.form.get("destreza"),
        "constituicao": request.form.get("constituicao"),
        "inteligencia": request.form.get("inteligencia"),
        "sabedoria": request.form.get("sabedoria"),
        "carisma": request.form.get("carisma"),
        "inspiracao": request.form.get("inspiracao"),
        "bonus_proficiencia": request.form.get("bonus_proficiencia"),
        "sabedoria_passiva": request.form.get("sabedoria_passiva"),

        # Resistências (checkboxes)
        "res_forca_prof": "on" if request.form.get("res_forca_prof") else "",
        "res_forca_exp": "on" if request.form.get("res_forca_exp") else "",
        "res_destreza_prof": "on" if request.form.get("res_destreza_prof") else "",
        "res_destreza_exp": "on" if request.form.get("res_destreza_exp") else "",
        "res_constituicao_prof": "on" if request.form.get("res_constituicao_prof") else "",
        "res_constituicao_exp": "on" if request.form.get("res_constituicao_exp") else "",
        "res_inteligencia_prof": "on" if request.form.get("res_inteligencia_prof") else "",
        "res_inteligencia_exp": "on" if request.form.get("res_inteligencia_exp") else "",
        "res_sabedoria_prof": "on" if request.form.get("res_sabedoria_prof") else "",
        "res_sabedoria_exp": "on" if request.form.get("res_sabedoria_exp") else "",
        "res_carisma_prof": "on" if request.form.get("res_carisma_prof") else "",
        "res_carisma_exp": "on" if request.form.get("res_carisma_exp") else "",

        # Perícias (exemplo - continue para todas as outras no seu HTML)
        "acrobacia_prof": "on" if request.form.get("acrobacia_prof") else "",
        "acrobacia_exp": "on" if request.form.get("acrobacia_exp") else "",
        "arcanismo_prof": "on" if request.form.get("arcanismo_prof") else "",
        "arcanismo_exp": "on" if request.form.get("arcanismo_exp") else "",

        # Combate
        "classe_armadura": request.form.get("classe_armadura"),
        "iniciativa": request.form.get("iniciativa"),
        "deslocamento": request.form.get("deslocamento"),
        "pontos_vida_maximos": request.form.get("pontos_vida_maximos"),
        "pontos_vida_atuais": request.form.get("pontos_vida_atuais"),
        "pontos_vida_temporarios": request.form.get("pontos_vida_temporarios"),
        "dados_vida_total": request.form.get("dados_vida_total"),
        "dados_vida": request.form.get("dados_vida"),
        "sucesso1": "on" if request.form.get("sucesso1") else "",
        "sucesso2": "on" if request.form.get("sucesso2") else "",
        "sucesso3": "on" if request.form.get("sucesso3") else "",
        "fracasso1": "on" if request.form.get("fracasso1") else "",
        "fracasso2": "on" if request.form.get("fracasso2") else "",
        "fracasso3": "on" if request.form.get("fracasso3") else "",
        "ataques_magias": request.form.get("ataques_magias"),

        # Equipamentos
        "equipamento": request.form.get("equipamento"),
        "moeda_pc": request.form.get("moeda_pc"),
        "moeda_pp": request.form.get("moeda_pp"),
        "moeda_pe": request.form.get("moeda_pe"),
        "moeda_po": request.form.get("moeda_po"),
        "moeda_pl": request.form.get("moeda_pl"),

        # Personalidade
        "tracos_personalidade": request.form.get("tracos_personalidade"),
        "ideais": request.form.get("ideais"),
        "vinculos": request.form.get("vinculos"),
        "defeitos": request.form.get("defeitos"),
        "caracteristicas_talentos": request.form.get("caracteristicas_talentos"),

        # Grimório
        "classe_conjuradora": request.form.get("classe_conjuradora"),
        "habilidade_chave": request.form.get("habilidade_chave"),
        "cd_magia": request.form.get("cd_magia"),
        "bonus_ataque_magia": request.form.get("bonus_ataque_magia"),
        "truques": request.form.get("truques"),

        # Magias por nível (exemplo até 3 - expanda até 9 se precisar)
        "espacos_total_1": request.form.get("espacos_total_1"),
        "espacos_usados_1": request.form.get("espacos_usados_1"),
        "magias_nivel_1": request.form.get("magias_nivel_1"),

        "espacos_total_2": request.form.get("espacos_total_2"),
        "espacos_usados_2": request.form.get("espacos_usados_2"),
        "magias_nivel_2": request.form.get("magias_nivel_2"),

        "espacos_total_3": request.form.get("espacos_total_3"),
        "espacos_usados_3": request.form.get("espacos_usados_3"),
        "magias_nivel_3": request.form.get("magias_nivel_3"),
    }

    # Criar nova ficha ou atualizar existente
    if ficha_id == "nova":
        dados_formulario["id"] = str(uuid.uuid4())
        fichas.append(dados_formulario)
    else:
        for i, ficha in enumerate(fichas):
            if ficha.get("id") == ficha_id:
                dados_formulario["id"] = ficha_id
                fichas[i] = dados_formulario
                break

    salvar_dados(fichas)
    return redirect(url_for("ver_ficha", ficha_id=dados_formulario["id"]))


# --- MAIN ---
if __name__ == "__main__":
    app.run(debug=True)
