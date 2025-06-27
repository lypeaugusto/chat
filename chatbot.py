from openai import OpenAI

client = OpenAI(
    api_key="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"
)


def chat_with_gpt(mensagem, mensagens=None):
    if mensagens is None:
        mensagens = []
    mensagens.append({"role": "user", "content": mensagem})
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=mensagens,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro ao se comunicar com o modelo: {str(e)}"


if __name__ == "__main__":
    mensagens = []
    while True:
        user_input = input("Você: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("Saindo do chat.")
            break

        resposta = chat_with_gpt(user_input, mensagens)
        print(f"GPT: {resposta}")
 

