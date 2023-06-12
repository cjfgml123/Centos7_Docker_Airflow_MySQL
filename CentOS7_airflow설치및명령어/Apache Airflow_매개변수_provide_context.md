## 1. Airflow 자체변수, 매개변수, return 사용

- 참고 : https://airflow.apache.org/docs/apache-airflow/2.5.1/release_notes.html#airflow-operators-python-pythonoperator

### 1-1. provide_context

- Airflow 2.x 더 이상 "provide_context=True"로 설정 필요 없이 context 변수 바로 사용됨.

```python
def myfunc(**context):
    print(context)  # all variables will be provided to context


python_operator = PythonOperator(task_id="mytask", python_callable=myfunc)

```

### 1-2. context 변수

- 참고 : https://blog.bsk.im/2021/03/21/apache-airflow-aip-39/
- logical_date

  - 데이터 처리 작업에서 사용되는 데이터의 논리적인 시간을 나타냄.
  - ex) 데이터 웨어하우스에서 매일 적재되는 데이터를 처리하는 DAG 작업이 있다면 , 각 실행에 대해, 해당 실행이 처리하는 데이터의 날짜를 나타낼 수 있음.
  - logical_date =  data_interval_start
- execution_date

  - airflow 2.2 에서 deprecated 시킴. 사용은 가능. -> logical_date(실행시점), data_interval_start,로 나뉨.
  - 해당 Task가 실행하고자 하는 Time Window의 시작지점.
  - ex) : 쇼핑몰에서 1월3일의 매출을 계산하려면 3일이 끝나고 하루가 넘어가는 1월 4일에 매출을 계산해야함. 여기서 작업 대상이 되는 데이터는 (1월3일 == execution_date)가 되고 , 실제 작업이 실행되는 시간은 1월4일이 됨.
  - 1월3~4일 사이를 Time Window라고 함.
- data_interval

  - data_interval_start : 타임 윈도우의 시작
  - data_interval_end : 타임 윈도우의 끝
- ti
- dag_run : 수행 중인 dag 인스턴스
- conf : 사용중인 ConfigParser 객체
- task_instance : 현재 task 인스턴스
