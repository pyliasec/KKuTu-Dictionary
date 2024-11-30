let currentSortOrder = 'desc';  // 기본값은 내림차순
let currentMode = '끝말잇기';   // 기본 모드는 끝말잇기

// 검색어 입력 시 버튼 상태 변경
function checkSearchInput() {
    const query = document.getElementById('search-bar').value;
    const searchButton = document.getElementById('search-btn');
    searchButton.disabled = query.trim() === '';  // 검색어가 없으면 버튼 비활성화
}

// 검색 함수
function searchWord() {
    const query = document.getElementById('search-bar').value;
    if (query.trim() === '') {
        return; // 검색어가 비어 있으면 아무 작업도 하지 않음
    }

    // 현재 모드에 맞는 JSON 파일을 선택
    const jsonFile = currentMode === '끝말잇기' ? '끝말잇기' : '공격';

    fetch(`/search?query=${query}&sort=${currentSortOrder}&mode=${jsonFile}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = ''; // 기존 내용 초기화
            if (data.length === 0) {
                resultsDiv.innerHTML = '<p>결과가 없습니다.</p>';
            } else {
                data.forEach(item => {
                    const wordDiv = document.createElement('div');
                    wordDiv.style.marginBottom = '10px'; // 단어 간격 추가

                    const wordText = document.createElement('p');
                    wordText.textContent = item.word;
                    wordText.style.fontSize = '1.2rem'; // 기본 폰트 크기
                    wordText.style.margin = '0';

                    // 단어 길이와 후속 단어 수를 같은 줄에 표시
                    const detailsText = document.createElement('span');
                    const length = item.length;
                    let followUpCount = 0;

                    // 공격 모드일 때만 후속 단어 수를 표시
                    if (currentMode === '공격' && item.follow_up_count !== undefined) {
                        followUpCount = item.follow_up_count;
                    }

                    // 끝말잇기 모드일 때는 후속 단어 수를 포함하지 않음
                    detailsText.textContent = currentMode === '끝말잇기' 
                        ? `단어 길이: ${length}자` 
                        : `단어 길이: ${length}자 | 후속 단어 수: ${followUpCount}`;

                    detailsText.style.color = '#777'; // 회색
                    detailsText.style.fontSize = '0.9rem'; // 작은 글씨
                    detailsText.style.display = 'block'; // 다음 줄로 표시

                    wordDiv.appendChild(wordText);
                    wordDiv.appendChild(detailsText);
                    resultsDiv.appendChild(wordDiv);
                });
            }
        })
        .catch(error => console.error('Error:', error));
}

// 정렬 순서 변경
function changeSortOrder(order) {
    currentSortOrder = order;
    const sortOrderText = order === 'asc' ? '오름차순' : '내림차순';
    document.getElementById('sort-order-display').textContent = sortOrderText;  // 현재 정렬 표시
    searchWord();  // 정렬을 변경한 후 다시 검색
}

// 끝말잇기/공격 모드 전환
function toggleMode() {
    if (currentMode === '끝말잇기') {
        currentMode = '공격';
        currentSortOrder = 'asc'; // 공격 모드로 전환되면 정렬을 오름차순으로 설정
    } else {
        currentMode = '끝말잇기';
        currentSortOrder = 'desc'; // 끝말잇기 모드로 전환되면 정렬을 내림차순으로 설정
    }

    document.getElementById('mode-btn').textContent = currentMode; // 버튼 텍스트 변경
    document.getElementById('sort-order-display').textContent = currentSortOrder === 'asc' ? '오름차순' : '내림차순'; // 정렬 표시
    searchWord();  // 모드를 변경한 후 다시 검색
}

// 엔터 키 감지 추가
document.getElementById('search-bar').addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        const query = document.getElementById('search-bar').value;
        if (query.trim() !== '') {
            searchWord();  // 검색어가 있을 때만 실행
        }
    }
});
