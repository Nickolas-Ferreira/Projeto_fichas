from flask import Flask, render_template, request, redirect, url_for
import json
import os
import uuid

app = Flask(__name__)

ARQUIVO_JSON = "ficha.json"

def carregar_dados():
    if not os.path.exists(ARQUIVO_JSON):
        return []
    with open(ARQUIVO_JSON, "r", encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def salvar_dados(dados):
    with open(ARQUIVO_JSON, "w", encoding='utf-8') as f:
        json.dump(dados, f, indent=4)

@app.route("/")
def pagina_inicial():
    fichas = carregar_dados()
    return render_template("index.html", fichas=fichas)

@app.route("/ficha/<ficha_id>")
def ver_ficha(ficha_id):
    if ficha_id == 'nova':
        return render_template("ficha.html", ficha={})
    else:
        fichas = carregar_dados()
        ficha = next((f for f in fichas if f.get('id') == ficha_id), None)
        if ficha:
            return render_template("ficha.html", ficha=ficha)
        else:
            return "Ficha não encontrada!", 404

@app.route("/salvar/<ficha_id>", methods=["POST"])
def salvar_ficha(ficha_id):
    fichas = carregar_dados()
    
    dados_formulario = {
        # Header
        "nome_personagem": request.form.get("nome_personagem"), "classe_nivel": request.form.get("classe_nivel"),
        "antecedente": request.form.get("antecedente"), "nome_jogador": request.form.get("nome_jogador"),
        "raca": request.form.get("raca"), "tendencia": request.form.get("tendencia"),
        "pontos_experiencia": request.form.get("pontos_experiencia"),
        "tamanho": request.form.get("tamanho"),
        
        # Coluna Esquerda
        "forca": request.form.get("forca"), "destreza": request.form.get("destreza"),
        "constituicao": request.form.get("constituicao"), "inteligencia": request.form.get("inteligencia"),
        "sabedoria": request.form.get("sabedoria"), "carisma": request.form.get("carisma"),
        "inspiracao": request.form.get("inspiracao"), "bonus_proficiencia": request.form.get("bonus_proficiencia"),
        "res_forca_prof": "on" if request.form.get("res_forca_prof") else "",
        "res_destreza_prof": "on" if request.form.get("res_destreza_prof") else "",
        "res_constituicao_prof": "on" if request.form.get("res_constituicao_prof") else "",
        "res_inteligencia_prof": "on" if request.form.get("res_inteligencia_prof") else "",
        "res_sabedoria_prof": "on" if request.form.get("res_sabedoria_prof") else "",
        "res_carisma_prof": "on" if request.form.get("res_carisma_prof") else "",
        "acrobacia_prof": "on" if request.form.get("acrobacia_prof") else "", "arcanismo_prof": "on" if request.form.get("arcanismo_prof") else "",
        "atletismo_prof": "on" if request.form.get("atletismo_prof") else "", "atuacao_prof": "on" if request.form.get("atuacao_prof") else "",
        "blefar_prof": "on" if request.form.get("blefar_prof") else "", "furtividade_prof": "on" if request.form.get("furtividade_prof") else "",
        "historia_prof": "on" if request.form.get("historia_prof") else "", "intimidacao_prof": "on" if request.form.get("intimidacao_prof") else "",
        "intuicao_prof": "on" if request.form.get("intuicao_prof") else "", "investigacao_prof": "on" if request.form.get("investigacao_prof") else "",
        "lidar_animais_prof": "on" if request.form.get("lidar_animais_prof") else "", "medicina_prof": "on" if request.form.get("medicina_prof") else "",
        "natureza_prof": "on" if request.form.get("natureza_prof") else "", "percepcao_prof": "on" if request.form.get("percepcao_prof") else "",
        "persuasao_prof": "on" if request.form.get("persuasao_prof") else "", "prestidigitacao_prof": "on" if request.form.get("prestidigitacao_prof") else "",
        "religiao_prof": "on" if request.form.get("religiao_prof") else "", "sobrevivencia_prof": "on" if request.form.get("sobrevivencia_prof") else "",
        "sabedoria_passiva": request.form.get("sabedoria_passiva"), "idiomas_proficiencias": request.form.get("idiomas_proficiencias"),
        
        # Coluna Central
        "classe_armadura": request.form.get("classe_armadura"), "iniciativa": request.form.get("iniciativa"), "deslocamento": request.form.get("deslocamento"),
        "pontos_vida_maximos": request.form.get("pontos_vida_maximos"), "pontos_vida_atuais": request.form.get("pontos_vida_atuais"),
        "pontos_vida_temporarios": request.form.get("pontos_vida_temporarios"), "dados_vida_total": request.form.get("dados_vida_total"),
        "dados_vida": request.form.get("dados_vida"),
        "sucesso1": "on" if request.form.get("sucesso1") else "", "sucesso2": "on" if request.form.get("sucesso2") else "", "sucesso3": "on" if request.form.get("sucesso3") else "",
        "fracasso1": "on" if request.form.get("fracasso1") else "", "fracasso2": "on" if request.form.get("fracasso2") else "", "fracasso3": "on" if request.form.get("fracasso3") else "",
        "ataques_magias": request.form.get("ataques_magias"), "equipamento": request.form.get("equipamento"),
        
        # Coluna Direita
        "tracos_personalidade": request.form.get("tracos_personalidade"), "ideais": request.form.get("ideais"),
        "vinculos": request.form.get("vinculos"), "fraquezas": request.form.get("fraquezas"),
        "caracteristicas_talentos": request.form.get("caracteristicas_talentos"),
    }

    if ficha_id == 'nova':
        dados_formulario['id'] = str(uuid.uuid4())
        fichas.append(dados_formulario)
    else:
        for i, ficha in enumerate(fichas):
            if ficha.get('id') == ficha_id:
                dados_formulario['id'] = ficha_id
                fichas[i] = dados_formulario
                break
    
    salvar_dados(fichas)
    return redirect(url_for("ver_ficha", ficha_id=dados_formulario['id']))

if __name__ == "__main__":
    app.run(debug=True)
