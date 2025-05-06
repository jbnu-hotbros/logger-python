# Python MongoDB Logger

MongoDB를 사용하는 Python 로깅 시스템입니다. 로그 데이터를 MongoDB에 저장하여 관리할 수 있습니다.

## 기능

- Python의 기본 logging 모듈과 호환
- MongoDB에 로그 데이터 저장
- 동기/비동기 로깅 지원
- 타임존 설정 (기본값: Asia/Seoul, UTC+9) (현재 미작동, 이유 파악 못함함)
- 모듈별 로그 구분 가능
- 내부 라이브러리 로그 필터링

## 설치

1. 필요한 패키지 설치:
```bash
pip install python-dotenv pymongo motor pydantic-settings
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
# MongoDB 연결 정보
LOGGER_MONGO_HOST=localhost
LOGGER_MONGO_PORT=27017
LOGGER_MONGO_USER=root
LOGGER_MONGO_PASSWORD=password
LOGGER_LEVEL=INFO
```

## 모듈 구조

### config.py
- `kst_converter(*args)`: KST(한국 표준시)로 시간을 변환하는 함수
- `configure_logging(level: str = None, use_async: bool = False)`: 로깅 시스템을 설정하는 함수
  - level: 로그 레벨 설정 (기본값: INFO)
  - use_async: 비동기 로깅 사용 여부

### database.py
- `_get_uri() -> str`: MongoDB 연결 URI를 생성하는 내부 함수
- `get_sync_mongo_client() -> pymongo.MongoClient`: 동기 MongoDB 클라이언트 싱글턴
- `get_async_mongo_client() -> AsyncIOMotorClient`: 비동기 MongoDB 클라이언트 싱글턴
- `close_async_mongo_client()`: 비동기 MongoDB 클라이언트 연결 종료
- `close_sync_mongo_client()`: 동기 MongoDB 클라이언트 연결 종료
- `get_recent_log(message: str, module_name: str = None)`: 최근 로그를 조회하는 유틸리티 함수

### custom_handler.py
- `to_kst_datetime(timestamp: float) -> datetime`: 타임스탬프를 KST datetime으로 변환
- `ExcludeInternalLogsFilter`: 내부 라이브러리 로그를 필터링하는 클래스
- `MongoDBHandler`: 동기 MongoDB 로그 핸들러
  - `emit(record: logging.LogRecord)`: 로그 레코드를 MongoDB에 저장
  - `_format_log_entry(record: logging.LogRecord) -> dict`: 로그 레코드를 MongoDB 문서 형식으로 변환
- `AsyncMongoDBHandler`: 비동기 MongoDB 로그 핸들러
  - `emit(record: logging.LogRecord)`: 로그 레코드를 비동기 큐에 추가
  - `_format_log_entry(record: logging.LogRecord) -> dict`: 로그 레코드를 MongoDB 문서 형식으로 변환
- `mongo_log_worker(client: Optional[AsyncIOMotorClient] = None)`: 비동기 로그 삽입 워커

### settings.py
- `LoggerSettings`: 로깅 설정을 관리하는 Pydantic 설정 클래스
  - mongo_host: MongoDB 호스트
  - mongo_port: MongoDB 포트
  - mongo_user: MongoDB 사용자
  - mongo_password: MongoDB 비밀번호
  - level: 로그 레벨

## 사용 방법

### 기본 사용법

```python
import logging
from logger.config import configure_logging

# 로깅 시스템 설정
configure_logging(level="INFO", use_async=False)

# 로거 사용
logger = logging.getLogger(__name__)
logger.info("정보 메시지")
logger.error("에러 메시지")
```

### 비동기 로깅 사용

```python
import logging
from logger.config import configure_logging

# 비동기 로깅 설정
configure_logging(level="INFO", use_async=True)

# 로거 사용
logger = logging.getLogger(__name__)
logger.info("비동기로 저장되는 로그 메시지")
```

## 로그 데이터 구조

MongoDB에 저장되는 로그 데이터는 다음과 같은 구조를 가집니다:

```json
{
    "moduleName": "module_name",
    "functionLocation": "file_path:function_name:line_number",
    "timestamp": "2024-01-01T12:00:00+09:00",
    "logLevel": "INFO",
    "message": "로그 메시지"
}
```

## 주의사항

1. MongoDB 서버가 실행 중이어야 합니다.
2. 환경 변수가 올바르게 설정되어 있어야 합니다.
3. 비동기 로깅을 사용할 경우, 애플리케이션 종료 시 `close_async_mongo_client()`를 호출하여 연결을 정상적으로 종료해야 합니다.
4. 로그 레벨은 Python의 기본 로깅 레벨을 따릅니다 (DEBUG, INFO, WARNING, ERROR, CRITICAL).
