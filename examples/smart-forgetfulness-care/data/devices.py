
# 가상의 IoT 기기 상태 데이터
HOME_DEVICES = {
    "device_01": {
        "id": "smart_plug_dressing_room",
        "name": ["고데기", "헤어드라이어", "화장대 플러그", "드라이기"],
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
    },
    "device_03": {
        "id": "gas_valve_kitchen",
        "name": ["가스", "가스밸브", "가스렌지"],
        "type": "valve",
        "status": "OFF",
        "location": "Kitchen"
    },
    "device_04": {
        "id": "smart_light_bedroom",
        "name": ["침실 불", "안방 조명", "침실 조명"],
        "type": "light",
        "status": "ON",
        "location": "Bedroom"
    }
}
