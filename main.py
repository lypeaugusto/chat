from openai import OpenAI
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

print("API KEY:", os.environ.get("OPENAI_API_KEY")) 

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    mensagem = data.get("mensagem", "")
    mensagens = data.get("mensagens", [])
    mensagens.append({"role": "user", "content": mensagem})
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=mensagens
        )
        resposta = completion.choices[0].message.content
        return jsonify({"resposta": resposta, "mensagens": mensagens})
    except Exception as e:
        erro_str = str(e)
        if "401" in erro_str or "invalid_api_key" in erro_str:
            resposta = "Erro: Esta API deu o limite de gratuidade. Por favor, utilize uma chave de API válida."
        else:
            resposta = f"Erro: {erro_str}"
        return jsonify({"resposta": resposta, "mensagens": mensagens})


@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chatbot GPT</title>
        <style>
            body { font-family: Arial, sans-serif; background: #111; color: #eee; }
            #chatbox {
                width: 90%; max-width: 500px; margin: 40px auto; background: #222;
                border-radius: 8px; box-shadow: 0 0 10px #000; padding: 20px;
            }
            #messages { height: 300px; overflow-y: auto; border: 1px solid #333; padding: 10px; background: #181818; }
            .msg { margin: 10px 0; }
            .user { color: #42a5f5; }
            .gpt { color: #66bb6a; }
            #input { width: 80%; padding: 8px; background: #222; color: #eee; border: 1px solid #333; }
            #send { padding: 4px 10px; font-size: 14px; background: #333; color: #eee; border: none; border-radius: 4px; }
            #send:hover { background: #444; }
            .erro { color: #ff5252; font-weight: bold; }
        </style>
    </head>
    <body>
        <div id="chatbox">
            <h2>Chatbot GPT</h2>
            <div id="messages"></div>
            <input id="input" type="text" placeholder="Digite sua mensagem..." autocomplete="off"/>
            <button id="send" onclick="enviar()">Enviar</button>
        </div>
        <script>
            let mensagens = [];
            function adicionarMsg(texto, classe) {
                let div = document.createElement('div');
                div.className = 'msg ' + classe;
                div.innerText = texto;
                document.getElementById('messages').appendChild(div);
                document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;
            }
            function enviar() {
                let input = document.getElementById('input');
                let texto = input.value.trim();
                if (!texto) return;
                adicionarMsg("Você: " + texto, "user");
                fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({mensagem: texto, mensagens: mensagens})
                })
                .then(r => r.json())
                .then(data => {
                    if (data.resposta.startsWith("Erro: Esta API é paga")) {
                        adicionarMsg(data.resposta, "erro");
                    } else {
                        adicionarMsg("GPT: " + data.resposta, "gpt");
                    }
                    mensagens = data.mensagens;
                });
                input.value = "";
                input.focus();
            }
            document.getElementById('input').addEventListener('keydown', function(e) {
                if (e.key === 'Enter') enviar();
            });
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
