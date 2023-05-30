# Apache Airflow 용어

#### 1) Catch Up

- python 코드로 DAG 작성할 때 Dag 속성 안에 "catchup" 인수를 둘 수 있다. default : True
- True : start_date 날 부터 작업 시작, False : 현재 날 부터 작업 시작

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

default_args={
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id = 'dag_with_catchup_bacfill_v02',
    default_args = default_args,
    start_date=datetime(2023,5,11),
    schedule_interval='@daily',
    catchup=False 
    ) as dag:
    task1 = BashOperator(
        task_id = 'task1',
        bash_command='echo This is a simple bash command!'  
    )
```

##### 1-1. Catchup 속성

- max_active_runs : DAG수준에서 설정 되며, catch up 중에 DAGrn이 얼마나 실행 될 수 있는지를 설정함.
- depends_on_past : 작업 수준에 설정 되며, 가장 최근에 DAG에서 동일한 작업이 수행 되었을 때 작업이 수행 될 수 있도록 제약을 걸 수 있음.
- wait_for_dwnstream : DAG 수준에서 설정되며 다음 DAG를 실행 하려면 전체 task들이 수행 되어야 실행 되도록 함.
- catchup_by_default : config파일에서 설정이 가능하며 DAG를 만들 때 기본 값 True, False를 정할 수 있음.

#### 2) Backfill

- Backfill은 DAG가 이미 배포되어 실행 중이며 해당 DAG를 사용하여 DAG의 시작 날짜 이전에 데이터를 처리하기 원할 때 사용한다. Backfill은 지정한 기간동안 DAG 다시 재시작, 지정한 기간동안 전체 재시작, 지정한 기간 지정한 상태 동안 전체 재시작을 지정 하여 사용이 가능하다. 또한 Start_date이전의 날짜를 명시하여 실행 할 수도 있다. CLI를 사용하여 Backfill을 사용할 수 있다.
- Backfill은 보통 전체 재시작을 하는데 사용하지 않고, 일정 기간동안 실패한 작업에 대해 재실행을 하는데 사용된다고 보면 된다.
- schedule_interval이 설정된 DAG만 실행 할 수 있음.

- CLI를 사용하여 Backfill을 사용

```shell
airflow dags backfill [-h] [-c CONF] [--delay-on-limit DELAY_ON_LIMIT] [-x]
                      [-n] [-e END_DATE] [-i] [-I] [-l] [-m] [--pool POOL]
                      [--rerun-failed-tasks] [--reset-dagruns] [-B]
                      [-s START_DATE] [-S SUBDIR] [-t TASK_REGEX] [-v] [-y]
                      dag_id

# 예시 
airflow dags backfill -s 2021-11-01 -e 2021-11-02 example_dag
```

- --continue-on-failure : 일부 작업이 실패해도 백필 계속 진행(ver 2.3 이상 지원)
- —delay-on-limit DELAY_ON_LIMIT : DagRun 재수행 시 max_active_runs 값에 막혀 실행되지 못한 경우, 재수행까지의 대기 시간을 설정한다.
- -l, --local : backfill 작업을 LocalExecutor에서 수행한다.다른 Executor가 아닌 현재 Backfill 작업을 시작한 위치에서 작업한다.
- -m, --mark-success : 실제로 backfill 작업을 수행하는 대신, 모든 Task를 SUCCESS 상태로 일괄 업데이트한다.
- --pool POOL : backfill Task가 실행될 pool을 지정한다.
- -B, --run-backwards : 가장 최근의 Data_Interval 부터 실행되며 END_DATE부터 START_DATE 순으로 실행된다.
- -t TASK_REGEX, --task-regex TASK_REGEX : DAG 내의 특정 Task만 backfill한다.
- --end-date : yyyy-mm-dd 형식
- -I : dependencies_on_past 속성 무시
- -s : start_date : yyyy-mm-dd 형식
- --reset-dagruns : 설정된 경우 백필은 기존 백필 관련 DAG실행을 삭제하고 DAG 새로 시작
- --rerun-failed-tasks : 설정된 경우 백필은 예외를 throw하는 대신 백필 날짜 범위에 대해 실패한 모든 작업을 자동으로 다시 실행

```shell
# 지정한 기간동안 backfill 수행하지 않을 날짜만 수행
airflow dags backfill --start-date {date} --end-date {date} dag_id
# 지정한 기간동안 backfill 모든 재실행
airflow dags backfill --start-date {date} --end-date {date} --reset-dagruns dag_id
# 지정한 기간동안 실패한 task들만 재실행
airflow dags backfill --start-date {date} --end-date {date} --rerun-failed-tasks
```

