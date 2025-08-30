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
# Perícias (checkboxes)
        "acrobacia_prof": "on" if request.form.get("acrobacia_prof") else "", "arcanismo_prof": "on" if request.form.get("arcanismo_prof") else "",
        "atletismo_prof": "on" if request.form.get("atletismo_prof") else "", "atuacao_prof": "on" if request.form.get("atuacao_prof") else "",
        "blefar_prof": "on" if request.form.get("blefar_prof") else "", "furtividade_prof": "on" if request.form.get("furtividade_prof") else "",
        "historia_prof": "on" if request.form.get("historia_prof") else "", "intimidacao_prof": "on" if request.form.get("intimidacao_prof") else "",
        "intuicao_prof": "on" if request.form.get("intuicao_prof") else "", "investigacao_prof": "on" if request.form.get("investigacao_prof") else "",
        "lidar_animais_prof": "on" if request.form.get("lidar_animais_prof") else "", "medicina_prof": "on" if request.form.get("medicina_prof") else "",
        "natureza_prof": "on" if request.form.get("natureza_prof") else "", "percepcao_prof": "on" if request.form.get("percepcao_prof") else "",
        "persuasao_prof": "on" if request.form.get("persuasao_prof") else "", "prestidigitacao_prof": "on" if request.form.get("prestidigitacao_prof") else "",
        "religiao_prof": "on" if request.form.get("religiao_prof") else "", "sobrevivencia_prof": "on" if request.form.get("sobrevivencia_prof") else "",
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
       
        # SUBSTITUINDO O CAMPO ANTIGO PELOS NOVOS DA TABELA
        "ataque_nome_1": request.form.get("ataque_nome_1"),
        "ataque_bonus_1": request.form.get("ataque_bonus_1"),
        "ataque_dano_1": request.form.get("ataque_dano_1"),
        "ataque_nome_2": request.form.get("ataque_nome_2"),
        "ataque_bonus_2": request.form.get("ataque_bonus_2"),
        "ataque_dano_2": request.form.get("ataque_dano_2"),
        "ataque_nome_3": request.form.get("ataque_nome_3"),
        "ataque_bonus_3": request.form.get("ataque_bonus_3"),
        "ataque_dano_3": request.form.get("ataque_dano_3"),
        
        # Equipamentos
        "equipamento": request.form.get("equipamento"),
        "moeda_pc": request.form.get("moeda_pc"),
        "moeda_pp": request.form.get("moeda_pp"),
        "moeda_pe": request.form.get("moeda_pe"),
        "moeda_po": request.form.get("moeda_po"),
        "moeda_pl": request.form.get("moeda_pl"),
        "quantidade_flechas": request.form.get("quantidade_flechas"),
        

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


        # Adicionar as novas chaves para especialização em Testes de Resistência
        "res_forca_exp": "on" if request.form.get("res_forca_exp") else "",
        "res_destreza_exp": "on" if request.form.get("res_destreza_exp") else "",
        "res_constituicao_exp": "on" if request.form.get("res_constituicao_exp") else "",
        "res_inteligencia_exp": "on" if request.form.get("res_inteligencia_exp") else "",
        "res_sabedoria_exp": "on" if request.form.get("res_sabedoria_exp") else "",
        "res_carisma_exp": "on" if request.form.get("res_carisma_exp") else "",

        # Adicionar as novas chaves para especialização em Perícias
        "acrobacia_exp": "on" if request.form.get("acrobacia_exp") else "",
        "arcanismo_exp": "on" if request.form.get("arcanismo_exp") else "",
        "atletismo_exp": "on" if request.form.get("atletismo_exp") else "",
        "atuacao_exp": "on" if request.form.get("atuacao_exp") else "",
        "blefar_exp": "on" if request.form.get("blefar_exp") else "",
        "furtividade_exp": "on" if request.form.get("furtividade_exp") else "",
        "historia_exp": "on" if request.form.get("historia_exp") else "",
        "intimidacao_exp": "on" if request.form.get("intimidacao_exp") else "",
        "intuicao_exp": "on" if request.form.get("intuicao_exp") else "",
        "investigacao_exp": "on" if request.form.get("investigacao_exp") else "",
        "lidar_animais_exp": "on" if request.form.get("lidar_animais_exp") else "",
        "medicina_exp": "on" if request.form.get("medicina_exp") else "",
        "natureza_exp": "on" if request.form.get("natureza_exp") else "",
        "percepcao_exp": "on" if request.form.get("percepcao_exp") else "",
        "persuasao_exp": "on" if request.form.get("persuasao_exp") else "",
        "prestidigitacao_exp": "on" if request.form.get("prestidigitacao_exp") else "",
        "religiao_exp": "on" if request.form.get("religiao_exp") else "",
        "sobrevivencia_exp": "on" if request.form.get("sobrevivencia_exp") else "",
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
