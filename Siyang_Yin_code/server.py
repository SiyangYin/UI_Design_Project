from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import re
import copy

app = Flask(__name__)
   
current_id = 1
   
word_learned_lists = []

# non_ppc_people = [
# "Phyllis",
# "Dwight",
# "Oscar",
# "Creed",
# "Pam",
# "Jim",
# "Stanley",
# "Michael",
# "Kevin",
# "Kelly"
# ]
# ppc_people = [
# "Angela"
# ]


dataset = [
{
    'Id': 1,
    'List_name': "Word List1: People",
    'Poster': "https://www.goethe-verlag.com/book2/_bilder/001.jpg",
    'Words': [
        {
            'Index': 0,
            'Korean': "저",
            'English': "I",
            'Pronunciation': "jeo",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0003.mp3"
        },
        {
            'Index': 1,
            'Korean': "저와 당신",
            'English': "I and you",
            'Pronunciation': "jeowa dangsin",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0004.mp3"
        },
        {
            'Index': 2,
            'Korean': "우리 둘 다",
            'English': "both of us",
            'Pronunciation': "uli dul da",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0005.mp3"
        },
        {
            'Index': 3,
            'Korean': "그",
            'English': "he",
            'Pronunciation': "geu",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0006.mp3"
        },
        {
            'Index': 4,
            'Korean': "그와 그녀",
            'English': "he and she",
            'Pronunciation': "geuwa geunyeo",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0007.mp3"
        },
        {
            'Index': 5,
            'Korean': "그들 둘 다",
            'English': "they both",
            'Pronunciation': "geudeul dul da",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0008.mp3"
        },
        {
            'Index': 6,
            'Korean': "남자",
            'English': "the man",
            'Pronunciation': "namja",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0009.mp3"
        },
        {
            'Index': 7,
            'Korean': "여자",
            'English': "the woman",
            'Pronunciation': "yeoja",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0010.mp3"
        },
        {
            'Index': 8,
            'Korean': "아이",
            'English': "the child",
            'Pronunciation': "ai",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0011.mp3"
        },
        {
            'Index': 9,
            'Korean': "가족",
            'English': "a family",
            'Pronunciation': "gajog",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0012.mp3"
        },
        {
            'Index': 10,
            'Korean': "저의 가족",
            'English': "my family",
            'Pronunciation': "jeoui gajog",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0013.mp3"
        },
        {
            'Index': 11,
            'Korean': "저는 여기 있어요",
            'English': "I am here.",
            'Pronunciation': "jeoneun yeogi iss-eoyo",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0015.mp3"
        }
    ]
}, 
{
    'Id': 2,
    'List_name': "Word List2: Family Members",
    'Poster': "https://www.goethe-verlag.com/book2/_bilder/002.jpg",
    'Words': [
        {
            'Index': 0,
            'Korean': "할아버지",
            'English': "the grandfather",
            'Pronunciation': "hal-abeoji",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0023.mp3"
        },
        {
            'Index': 1,
            'Korean': "할머니",
            'English': "the grandmother",
            'Pronunciation': "halmeoni",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0024.mp3"
        },
        {
            'Index': 2,
            'Korean': "아버지",
            'English': "the father",
            'Pronunciation': "abeoji",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0026.mp3"
        },
        {
            'Index': 3,
            'Korean': "어머니",
            'English': "the mother",
            'Pronunciation': "eomeoni",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0027.mp3"
        },
        {
            'Index': 4,
            'Korean': "아들",
            'English': "the son",
            'Pronunciation': "adeul",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0029.mp3"
        },
        {
            'Index': 5,
            'Korean': "딸",
            'English': "the daughter",
            'Pronunciation': "ttal",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0030.mp3"
        },
        {
            'Index': 6,
            'Korean': "형 / 오빠 / 남동생",
            'English': "the brother",
            'Pronunciation': "hyeong / oppa / namdongsaeng",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0032.mp3"
        },
        {
            'Index': 7,
            'Korean': "누나 / 언니 / 여동생",
            'English': "the sister",
            'Pronunciation': "nuna / eonni / yeodongsaeng",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0033.mp3"
        },
        {
            'Index': 8,
            'Korean': "삼촌",
            'English': "the uncle",
            'Pronunciation': "samchon",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0035.mp3"
        },
        {
            'Index': 9,
            'Korean': "이모 / 고모",
            'English': "the aunt",
            'Pronunciation': "imo / gomo",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0036.mp3"
        },
        {
            'Index': 10,
            'Korean': "우리는 가족이에요.",
            'English': "We are a family.",
            'Pronunciation': "ulineun gajog-ieyo.",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0038.mp3"
        },
        {
            'Index': 11,
            'Korean': "가족이 작지 않아요.",
            'English': "The family is not small.",
            'Pronunciation': "gajog-i jagji anh-ayo.",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0039.mp3"
        }
    ]
}, 
{
    'Id': 3,
    'List_name': "Word List3: Getting to know others",
    'Poster': "https://www.goethe-verlag.com/book2/_bilder/003.jpg",
    'Words': [
        {
            'Index': 0,
            'Korean': "안녕!",
            'English': "Hi!",
            'Pronunciation': "annyeong!",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0043.mp3"
        },
        {
            'Index': 1,
            'Korean': "안녕하세요!",
            'English': "Hello!",
            'Pronunciation': "annyeonghaseyo!",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0044.mp3"
        },
        {
            'Index': 2,
            'Korean': "잘 지내세요?",
            'English': "How are you?",
            'Pronunciation': "jal jinaeseyo?",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0045.mp3"
        },
        {
            'Index': 3,
            'Korean': "당신은 유럽에서 오셨어요?",
            'English': "Do you come from Europe?",
            'Pronunciation': "dangsin-eun yuleob-eseo osyeoss-eoyo?",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0046.mp3"
        },
        {
            'Index': 4,
            'Korean': "당신은 미국에서 오셨어요?",
            'English': "Do you come from America?",
            'Pronunciation': "dangsin-eun migug-eseo osyeoss-eoyo?",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0047.mp3"
        },
        {
            'Index': 5,
            'Korean': "당신은 아시아에서 오셨어요?",
            'English': "Do you come from Asia?",
            'Pronunciation': "dangsin-eun asia-eseo osyeoss-eoyo?",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0048.mp3"
        },
        {
            'Index': 6,
            'Korean': "당신은 어떤 호텔에서 머물러요?",
            'English': "In which hotel are you staying?",
            'Pronunciation': "dangsin-eun eotteon hotel-eseo meomulleoyo?",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0049.mp3"
        },
        {
            'Index': 7,
            'Korean': "당신은 여기 온 지 얼마나 됐어요?",
            'English': "How long have you been here for?",
            'Pronunciation': "angsin-eun yeogi on ji eolmana dwaess-eoyo?",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0050.mp3"
        },
        {
            'Index': 8,
            'Korean': "이곳이 마음에 들어요?",
            'English': "Do you like it here?",
            'Pronunciation': "igos-i ma-eum-e deul-eoyo?",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0052.mp3"
        },
        {
            'Index': 9,
            'Korean': "이곳에 휴가를 오셨어요?",
            'English': "Are you here on vacation?",
            'Pronunciation': "igos-e hyugaleul osyeoss-eoyo?",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0053.mp3"
        },
        {
            'Index': 10,
            'Korean': "언제 저를 한 번 방문하세요!",
            'English': "Please do visit me sometime!",
            'Pronunciation': "eonje jeoleul han beon bangmunhaseyo!",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0054.mp3"
        },
        {
            'Index': 11,
            'Korean': "이것이 제 주소예요.",
            'English': "Here is my address.",
            'Pronunciation': "igeos-i je jusoyeyo.",
            'Audio': "https://www.book2.nl/book2/KO/SOUND/0055.mp3"
        }
    ]
}, 

]
# quiz1_answer = ['A', 'A', 'A', 'A', 'A', 'A']
# score = 0


ppc_people = [
#     {
#         'Index': 0,
#         'Korean': "저",
#         'English': "I",
#         'Pronunciation': "jeo",
#         'Audio': "https://www.book2.nl/book2/KO/SOUND/0003.mp3"
#     }
]
# ppc_people = [
# "저, I",
# "저와 당신, I and you",
# "우리 둘 다, both of us",
# "그, he",
# "그와 그녀, he and she",
# "그들 둘 다, they both",
# "남자, the man",
# "여자, the woman",
# "아이, the child"
# ]
non_ppc_people = [

]
  
@app.route('/')
def index(name=None):
    return render_template('layout.html', name=name)

# @app.route('/init', methods=['GET', 'POST'])
# def init():  
#     global dataset
#     
# #     json_data = request.get_json()
# #     print("json_data : " + str(json_data))
#     return jsonify(dataset = dataset)

@app.route('/init_quiz', methods=['GET', 'POST'])
def init_quiz():   
    global non_ppc_people 
    global dataset
    global current_id
    return jsonify(non_ppc_people = non_ppc_people, dataset = dataset, current_id = current_id)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():   
    return render_template('add_item.html')

@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    global current_id
    global dataset
    
    data_entry = {}
    form_data = request.get_json()
#     print(form_data)
    current_id+=1
    data_entry["Id"] = current_id
    for value in form_data:
        data_entry[value["name"]] = value["value"];    
#     print(data_entry)

    dataset.append(data_entry)
    print(dataset)
#     render_template('view_item.html')
    return jsonify(Id = current_id)
#     return render_template('view_item.html')
    
@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')

@app.route('/search_input', methods=['GET', 'POST'])
def search_input():
    global current_id
    global dataset
    
#     data_entry = {}
    result = []
    input = request.get_json()
    print("input: "+str(input))
    pattern = re.compile(input, re.I)
    for i in dataset:
        for j in i.values():
#             print("j:"+str(j))
            if re.search(pattern, str(j)):
                result.append(i)
                break
#     print("result: ")
#     print(result)
    return jsonify(result = result)

@app.route('/view_item', methods=['GET', 'POST'])
def view_item():
    return render_template('view_item.html')

@app.route('/take_quiz', methods=['GET', 'POST'])
def take_quiz():
    return render_template('quiz.html')

@app.route('/return', methods=['GET', 'POST'])
def return_to():
    return render_template('search.html')

@app.route('/view_item/<item_id>', methods=['GET', 'POST'])
def view_item_id(item_id=None):
    global dataset
    
    item = dataset[int(item_id)-1]
#     print(item["Poster"])
    return render_template('item.html', item = item)



@app.route('/init', methods=['GET', 'POST'])
def init():
    global non_ppc_people 
    global ppc_people
    global dataset
    global word_learned_lists
    ppc_people = copy.deepcopy(dataset[0]["Words"])
    return jsonify(ppc_people = ppc_people, non_ppc_people = non_ppc_people, dataset = dataset, word_learned_lists = word_learned_lists) 

@app.route('/clear_to_learn', methods=['GET', 'POST'])
def clear_to_learn():
    global non_ppc_people 
    global ppc_people
    global dataset
    ppc_people = []
    return jsonify(ppc_people = ppc_people, non_ppc_people = non_ppc_people) 
    
@app.route('/clear_learned', methods=['GET', 'POST'])
def clear_learned():
    global non_ppc_people
    global ppc_people
    global dataset
    non_ppc_people = []
    return jsonify(ppc_people = ppc_people, non_ppc_people = non_ppc_people) 


@app.route('/move_to_ppc', methods=['GET', 'POST'])
def move_to_ppc(name=None):
    global non_ppc_people 
    global ppc_people
    json_data = request.get_json()   
#     print(str(json_data))
#     print("non_ppc_people: " + str(non_ppc_people))
#     print("ppc_people: " + str(ppc_people))        
    ppc_people.append(json_data["name"])
    non_ppc_people.remove(json_data["name"])
#     print("non_ppc_people: " + str(non_ppc_people))
#     print("ppc_people: " + str(ppc_people))        
    return jsonify(ppc_people = ppc_people, non_ppc_people = non_ppc_people) 

@app.route('/import_word_list', methods=['GET', 'POST'])
def import_word_list(name=None):
    global non_ppc_people 
    global ppc_people
    global current_id
    json_data = request.get_json()   
#     print(str(json_data))
#     print("non_ppc_people: " + str(non_ppc_people))
#     print("ppc_people: " + str(ppc_people))        
    ppc_people = copy.deepcopy(dataset[json_data["name"]-1]["Words"])
    current_id = json_data["name"]
#     non_ppc_people.remove(json_data["name"])
#     print("non_ppc_people: " + str(non_ppc_people))
#     print("ppc_people: " + str(ppc_people))        
    return jsonify(ppc_people = ppc_people, non_ppc_people = non_ppc_people) 

@app.route('/move_to_non_ppc', methods=['GET', 'POST'])
def move_to_non_ppc(name=None):
    global non_ppc_people 
    global ppc_people
    json_data = request.get_json()   
#     print(str(json_data))
    non_ppc_people.append(json_data["name"])
    ppc_people.remove(json_data["name"])
#     print("non_ppc_people: " + str(non_ppc_people))
#     print("ppc_people: " + str(ppc_people))    
    return jsonify(ppc_people = ppc_people, non_ppc_people = non_ppc_people)

@app.route('/check_answer', methods=['GET', 'POST'])
def check_answer():
    global quiz1_answer
    global current_id
    score = 0
    
#     data_entry = {}
    form_data = request.get_json()
#     print(form_data)
#     current_id+=1
#     data_entry["Id"] = current_id
    for i, value in enumerate(form_data):
        if quiz1_answer[i] == value["value"]:
            score+=1
#         data_entry[value["name"]] = value["value"]    
#     print(data_entry)

#     dataset.append(data_entry)
#     print(dataset)
#     render_template('view_item.html')
    return jsonify(score = score)
#     return render_template('view_item.html')

@app.route('/update_achievement', methods=['GET', 'POST'])
def update_achievement():
    global word_learned_lists
    global current_id
    json_data = request.get_json()    
#     if dataset[json_data["current_id"]-1] not in word_learned_lists:
#     print(json_data)
    word_learned_lists.append(dataset[json_data["name"]-1])
    print(word_learned_lists)
    return jsonify(word_learned_lists = word_learned_lists)


if __name__ == '__main__':
   app.run(debug = True)
   
  