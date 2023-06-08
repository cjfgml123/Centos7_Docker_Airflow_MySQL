# CentOS7 MySQL 트러블 모음

### 1. airflow.cfg 파일에서 executor

```shell
#airflow.cfg 에서 
executor = LocalExecutor #로 변경 후
airflow db init # 진행
airflow db check # db Connection 상태 확인
```

![error_0](.\image\error_0.PNG)

- Airflow 예제에서 발생한 에러



#### 2. Airflow pymysql module이 없다는 에러 발생 (import 부분) 

- dockerfile에 "RUN pip install pymysql"이 있음에도 import가 안될 시 "docker-compose build" 실행 후 "docker-compose up -d" 으로 다시 시작
- 원인 : docker compose 파일 실행하기 전에 이미지를 빌드하는 단계에서 문제가 발생할 수 있어 도커 이미지를 다시 빌드하는 명령어 (docker-compose build)
