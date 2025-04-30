# Python MongoDB Logger

Python의 기본 로깅 시스템을 MongoDB와 연동하여 로그를 저장하는 프로젝트입니다.

## 기능

- Python의 기본 `logging` 모듈과 호환
- MongoDB에 로그 자동 저장
- 타임존 설정 가능 (기본값: Asia/Seoul, UTC+9)
- 로그 레벨, 모듈명, 함수 위치, 메시지 등 상세 정보 저장

## 설치

```bash
pip install -r requirements.txt
```

## 환경 설정 (.env)

```env
# MongoDB 설정
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=log
MONGODB_COLLECTION=log

# 로깅 설정
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
MODULE_NAME=default_module  # 로그에 표시될 모듈명
TIMEZONE_OFFSET=9  # 기본값: 9 (Asia/Seoul)
```

## 사용 방법

1. 기본 사용 예시:
```python
import logging
from app.logger.database_handler import MongoDBHandler

# 로거 설정
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)

# MongoDB 핸들러 추가
mongo_handler = MongoDBHandler()
logger.addHandler(mongo_handler)

# 로그 기록
logger.info('테스트 로그 메시지')
```

2. 다른 타임존 사용:
```python
from app.utils.time import get_current_time

# 뉴욕 시간대 (UTC-5)
ny_time = get_current_time(-5)

# 런던 시간대 (UTC+0)
london_time = get_current_time(0)

# 베이징 시간대 (UTC+8)
beijing_time = get_current_time(8)
```

## 로그 형식

MongoDB에 저장되는 로그 형식:
```json
{
    "moduleName": "모듈명",
    "functionLocation": "파일경로:함수명:라인번호",
    "timestamp": "2024-01-01T12:00:00+09:00",
    "logLevel": "INFO",
    "message": "로그 메시지"
}
```

## 주의사항

- MongoDB 서버가 실행 중이어야 합니다.
- `.env` 파일이 프로젝트 루트 디렉토리에 있어야 합니다.
