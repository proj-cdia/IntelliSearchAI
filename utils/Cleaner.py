def answer_cleaner(answer):
    try:
        start = answer.index('Resposta:') + len('Resposta:')
        end = answer[start:]
        items = end.split('\n')[0].split(',')
        items = [item.strip() for item in items]

        result = []
        # Usa um loop for para pegar até três itens
        for i in range(min(3, len(items))):
            result.append(items[i])
        return result
    except ValueError:
        print("Não foi possível encontrar a resposta no texto de saída.")
        return []