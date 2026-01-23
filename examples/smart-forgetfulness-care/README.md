# Task: Smart Forgetfulness Care (깜빡임 케어) 구현 가이드

## 1. 개요 (Overview)
*   **목표**: 외출한 사용자가 집안 기기(고데기, 가스밸브, 에어컨 등)의 전원 상태를 걱정할 때, 에이전트가 이를 확인하고 원격으로 제어하여 안심시키는 시나리오 구현.
*   **특징**: 복잡한 추론보다는 **정확한 상태 확인**과 **즉각적인 제어(Action)**가 핵심.
*   **난이도**: ★☆☆☆☆ (비교적 쉬움, Mock 데이터 활용 용이)

---

## 2. 시나리오 흐름 (Flow)

1.  **Trigger**: 사용자가 불안감을 표현하는 발화 (예: "아 맞다, 고데기 껐나?", "가스 잠갔는지 기억이 안 나네")
2.  **Detection**: 에이전트가 `Target Device`(대상 기기)와 `Intent`(상태 확인/제어)를 파악.
3.  **Action**:
    *   IoT 시스템(Mock)에 접속하여 현재 상태(`Status`) 조회.
    *   만약 `ON` 상태라면, 사용자 의도에 따라 `OFF`로 전환 (또는 유지 제안).
4.  **Response**: 수행 결과와 현재 상태를 명확하게 전달하여 불안 해소.

---

## 3. 구현 상세 (Implementation Details)

### A. 환경 설정 (Mock Data)
실제 IoT 연동 대신, 로컬 객체나 JSON 파일로 집안 기기 상태를 정의합니다.

```python
# mock_iot_state.py

HOME_DEVICES = {
    "device_01": {
        "id": "smart_plug_dressing_room",
        "name": ["고데기", "헤어드라이어", "화장대 플러그"],
        "type": "smart_plug",
        "status": "ON",  # 시나리오 테스트를 위해 켜둠
        "location": "Dressing Room"
    },
    "device_02": {
        "id": "smart_ac_living_room",
        "name": ["에어컨", "거실 에어컨"],
        "type": "ac",
        "status": "OFF",
        "location": "Living Room"
    }
}
```

### B. 스킬 정의 (Skills)
에이전트가 사용할 도구(Tool)를 정의합니다.

#### 1. `check_device_status(device_name: str)`
*   **기능**: 사용자가 말한 기기 이름(device_name)과 매칭되는 기기를 찾아서 `ON/OFF` 상태를 반환.
*   **Logic**: `HOME_DEVICES` 딕셔너리 검색.

#### 2. `turn_off_device(device_id: str)`
*   **기능**: 특정 기기의 전원을 끈다.
*   **Logic**: `HOME_DEVICES[id]['status']`를 'OFF'로 변경하고 성공 메시지 반환.

### C. 에이전트 프롬프트 (System Prompt)
에이전트에게 "집안 관리자" 페르소나를 부여합니다.

> **Role**: 당신은 사용자의 집안 기기를 관리하는 IoT 매니저입니다.
> **Context**: 사용자는 현재 외출 중이며, 집안 기기를 켜두고 나왔을까 봐 불안해하고 있습니다.
> **Instruction**:
> 1. 사용자의 말에서 '확인하고 싶은 기기'를 찾으세요.
> 2. `check_device_status` 도구를 사용해 상태를 확인하세요.
> 3. 만약 켜져 있다면, 즉시 `turn_off_device` 도구를 사용해 끄세요. (별도 질문 없이 안전을 위해 끄는 것이 기본값)
> 4. 최종적으로 "확인 결과(켜져 있었음/꺼져 있었음)"와 "조치 내용(껐음/원래 꺼져 있었음)"을 포함하여 안심시키는 말투로 답변하세요.

---

## 4. 실행 예시 (Simulation)

**User Input**: "아 미친, 나 고데기 끄고 나왔나? 기억이 안 나 ㅠㅠ"

**Agent Process**:
1.  **Analyze**: Target = "고데기"
2.  **Tool Call**: `check_device_status("고데기")`
    *   *Result*: `{"id": "smart_plug_dressing_room", "status": "ON"}`
3.  **Decision**: 켜져 있음 -> 위험 상황 -> 끄기 실행
4.  **Tool Call**: `turn_off_device("smart_plug_dressing_room")`
    *   *Result*: "Success. Status changed to OFF."
5.  **Final Response**: "화장대 고데기가 켜져 있어서 방금 원격으로 껐습니다. 걱정 말고 다녀오세요!"

---

## 5. 추가 옵션 (Advanced - 나중에 추가 가능)
*   **반려동물 체크**: 에어컨을 끄려고 할 때, "초코(강아지)가 집에 있는데 끄시겠습니까? 아니면 온도를 높일까요?" 라고 되묻기.

---

## 6. 예상 프로젝트 구조 (Project Structure)
DeepAgents의 일반적인 예제(`examples/text-to-sql-agent`) 구조를 따릅니다.

```
smart-forgetfulness-care/
├── agent.py                 # 메인 에이전트 실행 및 설정 (OutingGuardian 클래스 정의)
├── skills/                  # 에이전트가 사용할 스킬(Tools) 모음
│   ├── __init__.py
│   ├── iot_tools.py         # check_device_status, turn_off_device 함수 구현
│   └── mock_data.py         # HOME_DEVICES 가상 데이터 정의
├── .env                     # (선택) 환경 변수 설정
├── pyproject.toml           # 프로젝트 의존성 관리
└── README.md                # 프로젝트 설명 및 실행 방법
```

