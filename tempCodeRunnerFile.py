from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

def load_database(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

DATABASE = load_database('json/kkutu_all_words.json')
ENTRIES_BY_FIRST: dict[str, list[dict]] = {}
CHAR_COUNTS: dict[str, int] = {}
for entry in DATABASE:
    word = entry['word']
    first_char = word[0]
    ENTRIES_BY_FIRST.setdefault(first_char, []).append(entry)
    CHAR_COUNTS[first_char] = CHAR_COUNTS.get(first_char, 0) + 1
for lst in ENTRIES_BY_FIRST.values():
    lst.sort(key=lambda e: e['word'])

# 두음법칙 규칙을 (원본, 대체) 쌍으로 정의
RAW_DUEUM_RULES = [
    ('라', '나'), ('락', '낙'), ('란', '난'), ('랄', '날'),
    ('람', '남'), ('랍', '납'), ('랑', '낭'), ('래', '내'),
    ('랙', '낵'), ('랜', '낸'), ('랠', '낼'), ('램', '냄'),
    ('랩', '냅'), ('랭', '냉'), ('려', '여'), ('력', '역'),
    ('련', '연'), ('렬', '열'), ('렴', '염'), ('렵', '엽'),
    ('령', '영'), ('례', '예'), ('로', '노'), ('록', '녹'),
    ('론', '논'), ('롤', '놀'), ('롬', '놈'), ('롭', '놉'),
    ('롱', '농'), ('뢰', '뇌'), ('료', '요'), ('룡', '용'),
    ('루', '누'), ('룩', '눅'), ('룬', '눈'), ('룰', '눌'),
    ('룸', '눔'), ('룹', '눕'), ('룽', '눙'),
    ('르', '느'), ('륵', '늑'), ('른', '는'), ('를', '늘'),
    ('름', '늠'), ('릅', '늡'), ('릉', '능'),
    ('리', '이'), ('릭', '익'), ('린', '인'), ('릴', '일'),
    ('림', '임'), ('립', '입'), ('링', '잉'), ('녁', '역'),
    ('략', '약')
]
# 방향성 매핑: 원본을 key로 대체 리스트 생성
DUEUM_RULES: dict[str, list[str]] = {}
for orig, alt in RAW_DUEUM_RULES:
    DUEUM_RULES.setdefault(orig, []).append(alt)


def get_dueum_variants(query: str) -> list[str]:
    """
    입력된 query에 대해 두음법칙 변형을 적용.
    - '라'로 시작하면 '나'로 변환하지만,
      '나'로 시작할 때는 변환하지 않습니다.
    """
    if not query:
        return []
    variants = {query}
    first_char = query[0]
    rest = query[1:]
    # 원본 규칙에만 적용
    if first_char in DUEUM_RULES:
        for alt in DUEUM_RULES[first_char]:
            variants.add(alt + rest)
    return list(variants)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    sort_order = request.args.get('sort', 'desc')
    mode = request.args.get('mode', '끝말잇기')
    end_priority = request.args.get('endPriority', '').strip()

    # 두음 변형으로 검색 시작 문자 확장
    variants = get_dueum_variants(query)
    seen: set[str] = set()
    results: list[dict] = []

    for variant in variants:
        if not variant:
            continue
        first = variant[0]
        for entry in ENTRIES_BY_FIRST.get(first, []):
            word = entry['word']
            if word in seen or not word.startswith(variant):
                continue
            seen.add(word)
            item = entry.copy()
            item['length'] = len(word)
            results.append(item)

    if mode == '공격':
        for item in results:
            last_char = item['word'][-1]
            # 마지막 글자 변형을 같은 로직으로 적용
            last_variants = get_dueum_variants(last_char)
            item['follow_up_count'] = sum(CHAR_COUNTS.get(ch, 0) for ch in last_variants)
        results = [r for r in results if r['length'] > 1 and r['follow_up_count'] > 0]

    # 우선 정렬 (끝나는 단어 우선)
    if end_priority:
        results.sort(key=lambda x: (
            not x['word'].endswith(end_priority),
            -x.get('follow_up_count', 0) if mode == '공격' else -x['length']
        ))
    else:
        # 기본 정렬: 길이 또는 후속 단어 수 기준
        key_func = (lambda x: -x.get('follow_up_count', 0)) if mode == '공격' else (lambda x: -x['length'])
        results.sort(key=key_func)
        if sort_order == 'asc':
            results.reverse()

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)