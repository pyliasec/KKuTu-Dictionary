from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# JSON 파일에서 단어 데이터 로드
def load_database(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    sort_order = request.args.get('sort', 'desc')  # 'des   c' or 'asc'
    mode = request.args.get('mode', '끝말잇기')  # '끝말잇기' or '공격'

    # database.json 파일을 로드
    database = load_database('database.json')

    # 쿼리로 단어를 필터링 (시작 단어로 필터링)
    results = [entry for entry in database if entry['word'].startswith(query)]
    
    # 공격 모드일 때 후속 단어 수를 계산
    if mode == '공격':
        for entry in results:
            last_char = entry['word'][-1]  # 단어의 마지막 글자
            # 후속 단어를 찾아서 개수를 셈
            entry['follow_up_count'] = sum(1 for e in database if e['word'].startswith(last_char))

    # 길이를 계산해서 포함시킴
    for entry in results:
        entry['length'] = len(entry['word'])

    # 공격 모드일 때 후속 단어 수 기준으로 정렬 (후속 단어 수가 같으면 길이 순으로 정렬)
    if mode == '공격':
        if sort_order == 'asc':
            results = sorted(results, key=lambda x: (x['follow_up_count'], x['length']))
        else:
            results = sorted(results, key=lambda x: (x['follow_up_count'], x['length']), reverse=True)
    else:
        # 끝말잇기 모드일 때는 단어 길이 기준으로 정렬
        results = sorted(results, key=lambda x: x['length'], reverse=(sort_order == 'desc'))

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=5001)