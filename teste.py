import os
from flask import Flask, request, jsonify
from dicttoxml import dicttoxml
from fpdf import FPDF
import json
from datetime import datetime
import random
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

produtos = []
numero_nota = random.randint(1000, 9999)

def get_produtos_info():
    return [{"nome": p["nome"], "ativo": p["ativo"]} for p in produtos]

@app.route('/produtos', methods=['GET'])
def listar_produtos_api():
    if not produtos:
        return jsonify({"message": "Nenhum produto cadastrado."}), 200
    return jsonify(get_produtos_info()), 200

@app.route('/produtos', methods=['POST'])
def cadastrar_produto_api():
    data = request.get_json()
    nome_do_produto = data.get('nome')

    if not nome_do_produto:
        return jsonify({"error": "Nome do produto é obrigatório."}), 400

    if any(p['nome'].lower() == nome_do_produto.lower() for p in produtos):
        return jsonify({"error": f"Produto '{nome_do_produto}' já está cadastrado."}), 409

    produto = {'nome': nome_do_produto, 'ativo': False}
    produtos.append(produto)
    return jsonify({"message": f"O produto '{nome_do_produto}' foi cadastrado com sucesso!", "produto": produto}), 201

@app.route('/produtos/<string:nome_do_produto>/ativar', methods=['PUT'])
def ativar_produto_api(nome_do_produto):
    for produto in produtos:
        if produto['nome'].lower() == nome_do_produto.lower():
            if produto['ativo']:
                return jsonify({"message": f"O produto '{produto['nome']}' já está ativado."}), 200
            else:
                produto['ativo'] = True
                return jsonify({"message": f"Produto '{produto['nome']}' ativado com sucesso!", "produto": produto}), 200
    return jsonify({"error": f"Produto '{nome_do_produto}' não encontrado."}), 404

@app.route('/produtos/<string:nome_do_produto>/desativar', methods=['PUT'])
def desativar_produto_api(nome_do_produto):
    for produto in produtos:
        if produto['nome'].lower() == nome_do_produto.lower():
            if not produto['ativo']:
                return jsonify({"message": f"O produto '{produto['nome']}' já está desativado."}), 200
            else:
                produto['ativo'] = False
                return jsonify({"message": f"Produto '{produto['nome']}' desativado com sucesso!", "produto": produto}), 200
    return jsonify({"error": f"Produto '{nome_do_produto}' não encontrado."}), 404

@app.route('/produtos/<string:nome_do_produto>', methods=['DELETE'])
def remover_produto_api(nome_do_produto):
    initial_len = len(produtos)
    global produtos
    produtos = [p for p in produtos if p['nome'].lower() != nome_do_produto.lower()]

    if len(produtos) < initial_len:
        return jsonify({"message": f"Produto '{nome_do_produto}' removido com sucesso!"}), 200
    return jsonify({"error": f"Produto '{nome_do_produto}' não encontrado."}), 404

def salvar_nota_em_arquivos(dados_nota):
    numero = dados_nota["numero"]
    nome_base = f"nota_fiscal_{numero}"

    if not os.path.exists('notas_fiscais'):
        os.makedirs('notas_fiscais')

    json_path = os.path.join('notas_fiscais', f"{nome_base}.json")
    with open(json_path, "w", encoding="utf-8") as f_json:
        json.dump(dados_nota, f_json, ensure_ascii=False, indent=4)

    xml_data = dicttoxml(dados_nota, custom_root="NotaFiscal", attr_type=False)
    xml_path = os.path.join('notas_fiscais', f"{nome_base}.xml")
    with open(xml_path, "wb") as f_xml:
        f_xml.write(xml_data)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Nota Fiscal - Café Express", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Número: {numero}", ln=True)
    pdf.cell(200, 10, txt=f"Data: {dados_nota['data']}", ln=True)
    pdf.cell(200, 10, txt=f"Cliente: {dados_nota['cliente']}", ln=True)
    pdf.cell(200, 10, txt=f"Produto: {dados_nota['produto']}", ln=True)
    pdf.cell(200, 10, txt=f"Valor: R$ {dados_nota['valor']:.2f}", ln=True)
    pdf_path = os.path.join('notas_fiscais', f"{nome_base}.pdf")
    pdf.output(pdf_path)

def enviar_email(dados_nota, destino_email):
    numero = dados_nota["numero"]
    nome_base = f"nota_fiscal_{numero}"
    
    remetente = "seu_email@gmail.com"
    senha = "sua_senha_aqui"

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destino_email
    msg["Subject"] = f"Nota Fiscal {numero}"

    for ext in [".pdf", ".json", ".xml"]:
        caminho = os.path.join('notas_fiscais', f"{nome_base}{ext}")
        try:
            with open(caminho, "rb") as f:
                parte = MIMEBase("application", "octet-stream")
                parte.set_payload(f.read())
                encoders.encode_base64(parte)
                parte.add_header("Content-Disposition", f"attachment; filename={os.path.basename(caminho)}")
                msg.attach(parte)
        except FileNotFoundError:
            print(f"Arquivo de anexo não encontrado: {caminho}")
            continue

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha)
            servidor.send_message(msg)
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

def validar_email(email):
    padrao_email = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    return re.fullmatch(padrao_email, email)

@app.route('/nota_fiscal', methods=['POST'])
def emitir_nota_fiscal_api():
    global numero_nota
    data = request.get_json()
    nome_produto_vendido = data.get('produto')
    cliente = data.get('cliente', 'Não informado')
    email_destino = data.get('email_destino')

    if not nome_produto_vendido:
        return jsonify({"error": "Nome do produto é obrigatório para emitir a nota."}), 400

    ativos = [p for p in produtos if p.get('ativo')]

    produto_encontrado = None
    for p in ativos:
        if p['nome'].lower() == nome_produto_vendido.lower():
            produto_encontrado = p
            break

    if not produto_encontrado:
        if not ativos:
            return jsonify({"error": "Nenhum produto ativado. Ative um produto antes de emitir uma nota."}), 400
        return jsonify({"error": f"Produto '{nome_produto_vendido}' não encontrado na lista de produtos ativos."}), 404

    valor = round(random.uniform(3.5, 20.0), 2)
    data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    dados_nota = {
        "numero": numero_nota,
        "data": data_hora,
        "cliente": cliente,
        "produto": produto_encontrado['nome'],
        "valor": valor
    }

    try:
        salvar_nota_em_arquivos(dados_nota)
        
        numero_nota = random.randint(1000, 9999) 

        response_message = f"Nota fiscal {dados_nota['numero']} emitida com sucesso e salva em 'notas_fiscais/'."
        
        if email_destino:
            if validar_email(email_destino):
                if enviar_email(dados_nota, email_destino):
                    response_message += f" E-mail enviado com sucesso para {email_destino}."
                else:
                    response_message += f" Falha ao enviar e-mail para {email_destino}. Verifique as configurações do servidor e as credenciais."
            else:
                response_message += f" O e-mail '{email_destino}' fornecido é inválido. E-mail não enviado."

        return jsonify({"message": response_message, "nota_fiscal": dados_nota}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao emitir nota fiscal: {str(e)}"}), 500

from flask_cors import CORS
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
