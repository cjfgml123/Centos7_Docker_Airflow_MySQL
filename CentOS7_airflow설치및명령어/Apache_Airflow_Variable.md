# Apache Airflow Variables

- 참고 : https://dydwnsekd.tistory.com/65

### 1. Airflow Variables

- Airflow 전역에서 사용할 수 있는 값을 미리 저장해두고 DAG에서 공통적으로 사용할 수 있는 변수를 말함.

- WebServer UI에서 쉽게 설정 가능

- key-value 형식으로 구성됨.

- JSON으로 여러개의 Variable 등록 가능 (Import Variables)


#### 2. Depends_on_past , wait_for_downstream

##### 2-1. Depends_on_past

- default 값은 False
- 이전 날짜의 task instance 들 중 하나라도 fail일 경우 다음 DagRun에서 해당 task가 완료 될 때 까지 기다림.
- DAGRun 중에서 이전 작업에 대해 의존성을 부여하여야 하는 경우 사용. ex) ETL 작업을 할 때 그 전 기록된 내용을 가지고 계산을 하여 오늘 내용을 기록하는 경우.

##### 2-2. wait_for_downstream

- 이전 날짜의 task instance 들 중 fail인 것 까지 작동하고 나머지 DAGRun의 task들은 실행하지 않고 no status로 대기한다.

```python
default_args={
    'owner' : 'eddie',
    'retries' : 1,
    'retry_delay' : timedelta(minutes=1),
    'depends_on_past':False,  <---- 이 부분
    'wait_for_downstream':True,
}
```

