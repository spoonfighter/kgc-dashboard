/**
 * Gemini AI에게 질문을 던지는 커스텀 함수
 * @param {string} prompt 질문 내용
 * @return Gemini의 답변
 * @customfunction
 */
function mygemini(prompt) {
  // 1. 스크립트 속성에서 API 키 불러오기
  // [주의] 프로젝트 설정 -> 스크립트 속성에 'GOOGLE_API_KEY'가 등록되어 있어야 합니다.
  const apiKey = PropertiesService.getScriptProperties().getProperty('GOOGLE_API_KEY');
  
  if (!apiKey) return "에러: 스크립트 속성에 GOOGLE_API_KEY를 설정해주세요.";
  if (!prompt) return "질문을 입력해주세요.";

  // 2. 모델 엔드포인트 설정 (현재 안정적인 1.5-flash 모델 권장)
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;

  // 3. 요청 데이터 구성
  const payload = {
    "contents": [{
      "parts": [{
        "text": prompt
      }]
    }]
  };

  const options = {
    "method": "post",
    "contentType": "application/json",
    "payload": JSON.stringify(payload),
    "muteHttpExceptions": true // 에러 발생 시 상세 내용을 확인하기 위함
  };

  try {
    // 4. API 호출 (스크린샷에서 누락된 부분)
    const response = UrlFetchApp.fetch(url, options);
    const json = JSON.parse(response.getContentText());

    // 5. 응답 결과 처리
    if (json.candidates && json.candidates[0].content && json.candidates[0].content.parts) {
      return json.candidates[0].content.parts[0].text;
    } else {
      return "에러 발생: " + response.getContentText();
    }
  } catch (e) {
    return "연결 에러: " + e.toString();
  }
}
