# Apache Airflow 용어

### 1. 주요 용어

#### 1) Dag(대그) - Directred Acyclic Graph

- 실행 하려는 모든 Task의 모음 
- DAG를 작성한 파이썬 파일들은 "$AIRFLOW_HOME/dags" 디렉토리에 저장하는 것을 기본으로 하고 있다.

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

with DAG(
    dag_id="anly_sch",      # DAG를 구분하는 식별자
	description = "This is chlee DAG.", # DAG에 대한 설명을 적는 부분
    schedule_interval=timedelta(days=1), # DAG 실행 주기를 정함. 보통CRON EXPRESSION으로 정의
    start_date=datetime(2021, 10, 9), # DAG 실행 날짜
    default_args={
    	"retries":1,
        "retry_delay":timedelta(minutes=3),
    }, # setting
    catchup=False, # catch_up tutorial
) as dag:
```

#### 2) Task

```python
#python 함수 print_airflow()를 실행
t2 = PythonOperator(
	task_id = "print_airflow",
	python_callable = print_airflow,
	owner="Chlee",
	retries=3,
	retry_delay=timedelta(minutes=5),
    op_kwargs={'parameterName':'value','age':20}
)
```

##### 2-1) Xcom이용해서 return 값 넘기기( 작업간의 값 넘기기)

- xcom 의 최대 크기는 48KB 에 유의
  - pandas 데이터 프레임과 같은 큰 데이터는 xcom 사용 x

```python
def greet(age, ti): # xcom_pull 이용
    name = ti.xcom_pull(task_ids='get_Name')
    print(f"Hello World! My name is {name}, "
          f"and I am {age} years old!")

def get_name():
    return 'jeery'

with DAG(
    dag_id = 'chlee_1',
    default_args=default_args,
    description='My first tutorial bash DAG',
    schedule_interval= '@once',
    start_date=datetime.now()
)as dag:
    t1 = PythonOperator(
        task_id='get_Name',
        python_callable=get_name,
    )
    t2 = PythonOperator(
        task_id = "greet",
        python_callable = greet,
        op_kwargs={'age': 20},
    )
t1 >> t2
```

##### 2-2) 다중값 return

```python
def greets(age,ti):
	first_name = ti.xcom_pull(task_ids='get_Name',key='first_name')
    last_name = ti.xcom_pull(task_ids='get_Name',key='last_name')
    print(f"Hello World! My name is {first_name} {last_name}, "
          f"and I am {age} years old!")
    
def get_names(ti):
    ti.xcom_push(key='first_name', value='CheolHee')
    ti.xcom_push(key='last_name', value='Lee')
```

##### 2-3) 다중값, 다중 메소드 return 

```python
def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_Name',key='first_name')
    last_name = ti.xcom_pull(task_ids='get_Name',key='last_name')
    age = ti.xcom_pull(task_ids='get_age',key='age')
    print(f"Hello World! My name is {first_name} {last_name}, "
          f"and I am {age} years old!")

def get_name(ti):
    ti.xcom_push(key='first_name', value='CheolHee')
    ti.xcom_push(key='last_name', value='Lee')

def get_age(ti):
    ti.xcom_push(key='age',value=19)

with DAG(
    dag_id = 'chlee_4',
    default_args=default_args,
    description='My first tutorial bash DAG',
    schedule_interval= '@once',
    start_date=datetime.now()
)as dag:

    t1 = PythonOperator(
        task_id='get_Name',
        python_callable=get_name,
    )

    t2 = PythonOperator(
        task_id = "greet",
        python_callable = greet,
    )

    t3 = PythonOperator(
        task_id = 'get_age',
        python_callable = get_age,
    )
    
[t1,t3] >> t2
```

##### 2-4) 데코레이터 방식

```python
from datetime import datetime, timedelta
from airflow.decorators import dag, task

default_args = {
    'owner' : 'chlee',
    'retries':5,
    'retry_delay':timedelta(minutes=5)
}

@dag(dag_id='dag_with_taskflow_api_v01',
     default_args=default_args,
     start_date=datetime.now(),
     schedule_interval='@daily')

def hello_world_etl():
    @task()
    def get_name():
        return "chleeV"
    
    @task()
    def get_age():
        return 19

    @task()
    def greet(name, age):
        print(f"Hello World! My name is {name}"
              f"and I am {age} years old!")
        
    name = get_name()
    age = get_age()
    greet(name=name, age=age)
    
greet_dag = hello_world_etl()
```

##### 2-4-1) 데코레이션 방식 다중 값 넘기기 -  @task(multiple_outputs=True)

```python 
from datetime import datetime, timedelta

from airflow.decorators import dag, task

default_args = {
    'owner' : 'chlee',
    'retries':5,
    'retry_delay':timedelta(minutes=5)
}

@dag(dag_id='dag_with_taskflow_api_v02',
     default_args=default_args,
     start_date=datetime.now(),
     schedule_interval='@daily')

def hello_world_etl():
    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name' : 'jerry',
            'last_name' : 'tom'
                }
    
    @task()
    def get_age():
        return 19

    @task()
    def greet(first_name,last_name, age):
        print(f"Hello World! My name is {first_name} {last_name}"
              f"and I am {age} years old!")
        
    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'],
          last_name=name_dict['last_name'], age=age)
    
greet_dag = hello_world_etl()
```



#### 3) Operator



- 

#### 6) Sensor 

- 시간, 파일, 외부 이벤트를 기다리며 해당 조건을 충족해야만 이후의 작업을 진행할 수 있게 해주는 Airflow의 기능으로 Operator와 같이 하나의 task가 될 수 있으며 filesystem, hdfs, hive 등 다양한 형식을 제공한다.

##### 6-1) FileSensor

- https://dydwnsekd.tistory.com/76 예제
- ex) 해당 경로에 파일이 있는지 확인하는 역할을 하며, 1분마다 한번씩 체크를 진행해 파일이 있는 경우에만 다음 단계로 넘어갈 수 있게 된다.

#### 7) XCOMS

