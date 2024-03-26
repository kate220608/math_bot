import requests


def get_solution(question):
    app_id = 'PKP57J-LKJRVT8HHV'
    if '+' in question:
        question = question.replace('+', '%2B')
    elif '*' in question:
        question = question.replace('*', '×')

    api_url = f'http://api.wolframalpha.com/v2/query?input={question}&appid={app_id}'

    try:
        response = requests.get(api_url)
        data = response.text
        print(data)
        solution = ''
        while True:
            # Извлекаем решение из ответа
            start_index = data.find('<plaintext>') + len('<plaintext>')
            if data.find('<plaintext>') != -1:
                end_index = data.find('</plaintext>')
                solution += data[start_index:end_index].strip() + '\n'
                data = data.replace('<plaintext>', '', 1)
                data = data.replace('</plaintext>', '', 1)
            else:
                break

        return solution
    except requests.exceptions.RequestException:
        print('Произошла ошибка при отправке запроса.')
        return None