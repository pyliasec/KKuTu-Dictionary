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
REVERSE_DUEUM_RULES: dict[str, list[str]] = {}
for orig, alt in RAW_DUEUM_RULES:
    DUEUM_RULES.setdefault(orig, []).append(alt)
    DUEUM_RULES.setdefault(alt, []).append(orig)  # 양방향 적용
    REVERSE_DUEUM_RULES.setdefault(alt, []).append(orig)
    REVERSE_DUEUM_RULES.setdefault(orig, []).append(alt)

def get_dueum_variants(query: str, reverse: bool = False) -> list[str]:
    """
    입력된 query에 대해 두음법칙 변형을 적용.
    - reverse=False: 시작 글자에 적용 (라→나, 나→라)
    - reverse=True: 마지막 글자에 적용 (력→역, 역→력)
    """
    if not query:
        return []
    variants = {query}
    char = query[-1] if reverse else query[0]
    rest = query[:-1] if reverse else query[1:]
    rule_set = REVERSE_DUEUM_RULES if reverse else DUEUM_RULES

    if char in rule_set:
        for alt in rule_set[char]:
            variant = (rest + alt) if reverse else (alt + rest)
            variants.add(variant)
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

    # 시작 글자 두음법칙 적용
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
            # 마지막 글자 두음법칙 적용 (양방향)
            last_variants = get_dueum_variants(last_char, reverse=True)
            item['follow_up_count'] = sum(CHAR_COUNTS.get(ch, 0) for ch in last_variants)
        results = [r for r in results if r['length'] > 1 and r['follow_up_count'] > 0]

    # 우선 정렬 (끝나는 단어 우선)
    if end_priority:
        # 끝 글자 두음법칙 적용 (양방향)
        end_variants = get_dueum_variants(end_priority, reverse=True)
        results.sort(key=lambda x: (
            not any(x['word'].endswith(ev) for ev in end_variants),
            -x.get('follow_up_count', 0) if mode == '공격' else -x['length']
        ))
    else:
        key_func = (lambda x: -x.get('follow_up_count', 0)) if mode == '공격' else (lambda x: -x['length'])
        results.sort(key=key_func)
        if sort_order == 'asc':
            results.reverse()

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)





# from flask import Flask, render_template, request, jsonify
# import json
# import hgtk

# app = Flask(__name__)

# def load_database(filename):
#     with open(filename, 'r', encoding='utf-8') as file:
#         return json.load(file)

# DATABASE = load_database('json/kkutu_all_words.json')
# ENTRIES_BY_FIRST: dict[str, list[dict]] = {}
# CHAR_COUNTS: dict[str, int] = {}
# for entry in DATABASE:
#     word = entry['word']
#     first_char = word[0]
#     ENTRIES_BY_FIRST.setdefault(first_char, []).append(entry)
#     CHAR_COUNTS[first_char] = CHAR_COUNTS.get(first_char, 0) + 1
# for lst in ENTRIES_BY_FIRST.values():
#     lst.sort(key=lambda e: e['word'])

# # 두음법칙 적용을 위한 초성 리스트와 모음 집합
# CHOSEONG_LIST = [
#     'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ',
#     'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ',
#     'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
# ]
# VOWEL_YI = {'ㅣ', 'ㅑ', 'ㅕ', 'ㅛ', 'ㅠ', 'ㅒ', 'ㅖ'}



# def apply_dueum(orig: str, cand: str) -> bool:
#     """
#     두음법칙 조건 검사:
#     1) ㄹ -> ㄴ
#     2) (ㄹ 또는 ㄴ) -> ㅇ + 'ㅣ','ㅑ',... 계열
#     """
#     try:
#         o_ch, o_jung, o_jong = hgtk.letter.decompose(orig)
#         c_ch, c_jung, c_jong = hgtk.letter.decompose(cand)
#     except hgtk.exception.NotHangulException:
#         return False

#     # ㄹ -> ㄴ
#     if o_ch == 'ㄹ' and c_ch == 'ㄴ':
#         return True
#     # ㄹ or ㄴ -> ㅇ + 특정 모음
#     if o_ch in ('ㄹ', 'ㄴ') and c_ch == 'ㅇ' and c_jung in VOWEL_YI:
#         return True
#     return False


# def get_dueum_variants(query: str) -> list[str]:
#     """
#     형태소 분해 기반으로 두음법칙 변형 생성
#     """
#     if not query:
#         return []
#     variants = {query}
#     first = query[0]
#     rest = query[1:]

#     # 모든 초성 후보에 대해 두음법칙 검사
#     for cho in CHOSEONG_LIST:
#         try:
#             candidate = hgtk.letter.compose(cho,
#                                            hgtk.letter.decompose(first)[1],
#                                            hgtk.letter.decompose(first)[2])
#         except hgtk.exception.NotHangulException:
#             continue
#         if apply_dueum(first, candidate):
#             variants.add(candidate + rest)
#     return list(variants)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/search', methods=['GET'])
# def search():
#     query = request.args.get('query', '')
#     sort_order = request.args.get('sort', 'desc')
#     mode = request.args.get('mode', '끝말잇기')
#     end_priority = request.args.get('endPriority', '').strip()

#     variants = get_dueum_variants(query)
#     seen: set[str] = set()
#     results: list[dict] = []

#     for variant in variants:
#         if not variant:
#             continue
#         first = variant[0]
#         for entry in ENTRIES_BY_FIRST.get(first, []):
#             word = entry['word']
#             if word in seen or not word.startswith(variant):
#                 continue
#             seen.add(word)
#             item = entry.copy()
#             item['length'] = len(word)
#             results.append(item)

#     if mode == '공격':
#         for item in results:
#             last_char = item['word'][-1]
#             last_variants = get_dueum_variants(last_char)
#             item['follow_up_count'] = sum(CHAR_COUNTS.get(ch, 0) for ch in last_variants)
#         results = [r for r in results if r['length'] > 1 and r['follow_up_count'] > 0]

#     if end_priority:
#         results.sort(key=lambda x: (
#             not x['word'].endswith(end_priority),
#             -x.get('follow_up_count', 0) if mode == '공격' else -x['length']
#         ))
#     else:
#         key_func = (lambda x: -x.get('follow_up_count', 0)) if mode == '공격' else (lambda x: -x['length'])
#         results.sort(key=key_func)
#         if sort_order == 'asc':
#             results.reverse()

#     return jsonify(results)

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5001)
