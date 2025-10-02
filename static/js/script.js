let currentSortOrder = 'desc';
let currentMode = '끝말잇기';

// 검색 입력 여부 확인
function checkSearchInput() {
  const query = document.getElementById('search-bar').value;
  const searchButton = document.getElementById('search-btn');
  searchButton.disabled = query.trim() === '';
}

// 설정 팝업
function openSettings() {
  document.getElementById('settings-popup').classList.remove('hidden');
}

function closeSettings() {
  document.getElementById('settings-popup').classList.add('hidden');
}

// 끝나는 단어 입력창 표시 여부 제어
function toggleEndWordInput() {
  const enabled = document.getElementById('enable-endword-setting').checked;
  const endInput = document.getElementById('end-search-bar');
  endInput.style.display = enabled ? 'inline-block' : 'none';
}

// 미션단어 입력창 표시 여부 제어
function toggleMissionInput() {
  const enabled = document.getElementById('enable-mission-setting').checked;
  const missionInput = document.getElementById('mission-search-bar');
  missionInput.style.display = enabled ? 'inline-block' : 'none';
}

// 검색 실행
function searchWord() {
  const query = document.getElementById('search-bar').value;
  const endEnabled = document.getElementById('enable-endword-setting').checked;
  const endQuery = endEnabled ? document.getElementById('end-search-bar').value.trim() : '';
  const missionEnabled = document.getElementById('enable-mission-setting').checked;
  const missionQuery = missionEnabled ? document.getElementById('mission-search-bar').value.trim() : '';
  if (query.trim() === '') return;

  const params = new URLSearchParams({
    query: query,
    sort: currentSortOrder,
    mode: currentMode,
    endPriority: endQuery,
    missionChar: missionQuery
  });

  fetch(`/search?${params.toString()}`)
    .then(response => response.json())
    .then(data => {
      const resultsDiv = document.getElementById('results');
      resultsDiv.innerHTML = '';
      if (data.length === 0) {
        resultsDiv.innerHTML = '<p>결과가 없습니다.</p>';
      } else {
        data.forEach(item => {
          const wordDiv = document.createElement('div');
          wordDiv.style.marginBottom = '10px';

          const wordText = document.createElement('p');
          wordText.textContent = item.word;
          wordText.style.fontSize = '1.2rem';
          wordText.style.margin = '0';

          const detailsText = document.createElement('span');
          const length = item.length;
          let followUpCount = 0;

          if (currentMode === '공격' && item.follow_up_count !== undefined) {
            followUpCount = item.follow_up_count;
          }

          let detailsContent = currentMode === '끝말잇기'
            ? `단어 길이: ${length}자`
            : `단어 길이: ${length}자 | 후속 단어 수: ${followUpCount}`;

          // 미션단어 정보 추가
          if (missionEnabled && missionQuery && item.mission_count !== undefined) {
            detailsContent += ` | 🎯${missionQuery} 개수: ${item.mission_count}`;
          }

          detailsText.textContent = detailsContent;
          detailsText.style.color = '#777';
          detailsText.style.fontSize = '0.9rem';
          detailsText.style.display = 'block';

          wordDiv.appendChild(wordText);
          wordDiv.appendChild(detailsText);
          resultsDiv.appendChild(wordDiv);
        });
      }
    })
    .catch(error => console.error('Error:', error));
}

function changeSortOrder(order) {
  currentSortOrder = order;
  document.getElementById('sort-order-display').textContent = order === 'asc' ? '오름차순' : '내림차순';
  searchWord();
}

function toggleMode() {
  if (currentMode === '끝말잇기') {
    currentMode = '공격';
    currentSortOrder = 'asc';
  } else {
    currentMode = '끝말잇기';
    currentSortOrder = 'desc';
  }

  document.getElementById('mode-btn').textContent = currentMode;
  document.getElementById('sort-order-display').textContent = currentSortOrder === 'asc' ? '오름차순' : '내림차순';
  searchWord();
}

// 엔터 키로 검색
document.getElementById('search-bar').addEventListener('keyup', e => {
  if (e.key === 'Enter') searchWord();
});

document.getElementById('end-search-bar').addEventListener('keyup', e => {
  if (e.key === 'Enter') searchWord();
});

document.getElementById('mission-search-bar').addEventListener('keyup', e => {
  if (e.key === 'Enter') searchWord();
});
