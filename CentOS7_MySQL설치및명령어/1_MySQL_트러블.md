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
