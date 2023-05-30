# Apache Airflow Jinja Templates

- 참조 : https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html
- 추가 사용자 지정 매크로는 플러그인을 통해 전체적으로 추가 하거나 인수를 통해 DAG 수준에서 추가할 수 있다. 



### 1. 변수

- Airflow는 기본적으로 모든 템플릿에서 액세스할 수 있는 몇 가지 변수를 전달함.

| Variable | Type | Description                                 |
| -------- | ---- | ------------------------------------------- |
| {{ds}}   | str  | The DAG run’s logical date as `YYYY-MM-DD`. |



