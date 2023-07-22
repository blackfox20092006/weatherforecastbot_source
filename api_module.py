from requests import post, get
import re
import difflib
from predict_keras import response
from unidecode import unidecode
api = "4ae0cc0d44434fa786113412231007"
base_url = "http://api.weatherapi.com/v1"
current = '/current.json'
search = '/search.json'
future = '/future.json'
def _current_(location):
    #lấy thông tin dự báo thời tiết hiện tại
    data = get(f'{base_url}{current}?key={api}&q={location}&lang=vi')
    try:
        return {
            "name": str(data.json()['location']['name']) + ', ' + str(data.json()['location']['country']),
            "temperature": data.json()['current']['temp_c'],
            "condition": data.json()['current']['condition']['text'],
            "feel_like": data.json()['current']['feelslike_c'],
        }
    except:
        return {}

def _future_(location, time):
    #lấy dự báo thời tiết của 1 ngày bất kì (phải nằm trong khoảng 14 ngày sau đến 300 ngày sau tính tới tương lai)
    extract_numbers = lambda s: re.findall(r'\d+', s)
    numbers = extract_numbers(time)
    d, m, y = map(int, numbers)
    if len(str(d)) not in [1, 2] or len(str(m)) not in [1, 2] or len(str(y)) != 4:
        return 'TimeNotVaild'
    data = get(f'{base_url}{future}?key={api}&q={location}&dt={y}-{m}-{d}&lang=vi')
    data = data.json()
    try:
        return {
            "name": str(data['location']['name']) + ', ' + str(data['location']['country']),
            "date": data['forecast']['forecastday'][0]['date'],
            "max_temp": data['forecast']['forecastday'][0]['day']['maxtemp_c'],
            "min_temp": data['forecast']['forecastday'][0]['day']['maxtemp_c'],
            "condition": data['forecast']['forecastday'][0]['day']['condition']['text']
        }
    except:
        #do ngày tháng không hợp lệ hoặc không nằm trong khoảng 14 ngày sau đến 300 ngày sau tính tới tương lai
        return {}

def _search_(location):
    #lấy thông tin vị trí địa lý cụ thể của 1 địa điểm hoặc lấy tên thành phố với đầu vào chỉ 1 vài kí tự đầu của tên
    data = get(f'{base_url}{search}?key={api}&q={location}')
    try:
        return [
            {
                "name": i['name'] + ', ' + i['region'] + ', ' + i['country'],
                "lat": i['lat'],
                'long': i['lon']
            } for i in data.json()
        ]
    except:
        return []


'''
def get_answer(question):
    check_pattern = lambda input_string: re.match(r'^[a-zA-Z\s]+ \d+\S+\d+\S+\d*\s*$', input_string) is not None
    extract_latin_chars = lambda input_string: re.sub(r'[^a-zA-Z\s]', '', unidecode(input_string))
    if not check_pattern(question):
        question = extract_latin_chars(question)
        return _current_(question)
    elif check_pattern(question):
        question = extract_latin_chars(question)
        return _future_(''.join(question.split(' ')[:len(question.split(' '))]), question.split(' ')[len(question.split(' '))-1])
    elif _search_(extract_latin_chars(question)) == []:
        return response(question)
    elif _search_(''.join(extract_latin_chars(question).split(' ')[:len(question.split(' '))-1])) == []:
        return response(question)
    else:
        return 'Xin lỗi, tôi không hiểu bạn lắm, bạn có thể hỏi lại với cách khác không ạ ?'
'''
def get_answer(question):
    check_pattern = lambda input_string: re.match(r'^[a-zA-Z\s]+ \d+\S+\d+\S+\d*\s*$', input_string) is not None
    extract_latin_chars = lambda input_string: re.sub(r'[^a-zA-Z\s]', '', unidecode(input_string))
    #is_variant = lambda input_string: difflib.SequenceMatcher(None, input_string, "dubaothoitiet").ratio() > 0.5
    if question.split(' ')[0] == 'dubaothoitiet':
        ques = extract_latin_chars(' '.join(question.split(' ')[1:len(question.split(' '))-1])) + ' ' + (question.split(' '))[len(question.split(' '))-1]
        if check_pattern(ques):
            #dự báo thời tiết ngày cụ thể
            return _future_(' '.join(ques.split(' ')[:len(ques.split(' '))-1]), ques.split(' ')[len(ques.split(' '))-1])
        else:
            return _current_(ques)
    else:
        return response(question)