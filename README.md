# Python MongoDB Logger

MongoDB를 사용하는 Python 로깅 시스템입니다. 로그 데이터를 MongoDB에 저장하여 관리할 수 있습니다.

## 기능

- Python의 기본 logging 모듈과 호환
- MongoDB에 로그 데이터 저장
- 타임존 설정 가능 (기본값: Asia/Seoul, UTC+9) --(설정 기능 미구현)--
- 모듈별 로그 구분 가능

## 설치

1. 필요한 패키지 설치:
```bash
pip install python-dotenv pymongo
```

2. MongoDB 설치 및 실행:
```bash
# Docker를 사용하는 경우
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

## 설정

### 환경 변수 (.env)

`.env` 파일을 프로젝트 루트에 생성하고 다음 변수들을 설정하세요:

```env
# 모듈 이름 (로그 구분용)
MODULE_NAME=your_module_name

# 최소 로그 레벨 (해당 로그 레벨 이상만 로깅됨. 실 사용시 INFO 레벨 추천)
MINIMUM_LOG_LEVEL = DEBUG

# MongoDB 연결 정보
LOGGER_MONGO_DATABASE_HOST=127.0.0.1
LOGGER_MONGO_DATABASE_PORT=27017
LOGGER_MONGO_DATABASE_ID=root
LOGGER_MONGO_DATABASE_PASSWORD=rootpw
```

## 사용 방법

### 기본 사용법

```python
import logging
from app.logger.database_handler import MongoDBHandler

# 로거 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# MongoDB 핸들러 추가
mongo_handler = MongoDBHandler()
logger.addHandler(mongo_handler)

# 로그 기록
logger.info("정보 메시지")
logger.error("에러 메시지")
```

### 타임존 설정

```python
from app.utils.time import get_current_time

# 기본값 (Asia/Seoul, UTC+9)
current_time = get_current_time()

# 다른 타임존 설정
new_york_time = get_current_time(-5)  # 뉴욕 (UTC-5)
london_time = get_current_time(0)     # 런던 (UTC+0)
beijing_time = get_current_time(8)    # 베이징 (UTC+8)
```

## 로그 데이터 구조

MongoDB에 저장되는 로그 데이터는 다음과 같은 구조를 가집니다:

```json
{
    "moduleName": "your_module_name",
    "functionLocation": "file_path:function_name:line_number",
    "timestamp": "2024-01-01T12:00:00+09:00",
    "logLevel": "INFO",
    "message": "로그 메시지"
}
```

## 주의사항

1. MongoDB 서버가 실행 중이어야 합니다.
2. 환경 변수가 올바르게 설정되어 있어야 합니다.
3. 로그 레벨은 Python의 기본 로깅 레벨을 따릅니다 (DEBUG, INFO, WARNING, ERROR, CRITICAL).
