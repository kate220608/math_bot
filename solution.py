import requests


OPERATORS = ['=', '-', '%', '+', '/', '^', '*', '√']


def get_solution(text, reply_message):
    if reply_message == "Введите уравнение":
        if any(map(str.isdigit, text)) and any(map(lambda x: x.lower() == 'x', text)):
            if '//' in text:
                res = get_solution_wolfram(text.replace('//', '/'))
            elif '**' in text:
                res = get_solution_wolfram(text.replace('**', '^'))
            else:
                res = get_solution_wolfram(text)
            if res is not None:
                return res
            else:
               return "Решения нет."
        else:
           return "Это не уравнение"
    elif reply_message == "Введите пример":
        if any(map(str.isdigit, text)) and any(map(lambda x: x in OPERATORS, text)):
            if '√' in text:
                return float(text.replace('√', '')) ** 0.5
            else:
                return eval(text)
        else:
            return "Это не пример"


def get_solution_wolfram(question):
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