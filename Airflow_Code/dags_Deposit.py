from datetime import timedelta
import pendulum
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from chlee.DataQuery import DataQuery as query
from chlee.Collector_1 import Controller as contr
from io import StringIO
import pandas as pd 
import boto3 #S3 연결 객체
import os 
import asyncio

'''
- S3 연결 및 Key 변수
- _endpoint : S3 연결 url
- _access_key : S3 accessKey
- _secret_key : S3 secretKey
- _s3_bucket_name : S3 버킷이름
- _s3_root_folder : S3에 저장된 csv파일 Key값에 활용 ex) bank_folder/Deposit/2023/예금_2023_05_13.csv
'''
_endpoint = Variable.get('s3_endpoint')
_access_key = Variable.get('s3_access_key')
_secret_key = Variable.get('s3_secret_key')
_s3_bucket_name = 'chlee-test'
_s3_root_folder = 'bank_folder/Deposit'

'''
- db 연결 변수
'''
_db_ip = Variable.get('db_host')
_db_name = Variable.get('db_name')
_db_port = Variable.get('db_port')
_db_pw = Variable.get('db_pw')
_db_user = Variable.get('db_user')
_tableName = "DepositBankTable"

'''
- Collector_1.py 의 적금 데이터 수집 실행 메소드
- 파라미터
    - _run : Collector_1.py 의 DepositRun() 
- Return
    - True 시 Dag 정상 동작
    - False 시 Dag 재실행
'''
def Run(_run):
    if asyncio.run(_run):
        return True
    else:
        return False 

'''
- 예금 데이터 S3에 저장 , S3는 폴더 개념 X , Key(key가 폴더형태로 보일뿐)로 관리
- Task 성공 시 S3에 CSV 저장 후, 로컬의 CSV 삭제
- Task 실패 시 예외 발생 시켜 Task 재 실행
- 파라미터
    - context : airflow context 변수 사용
- Xcom push value 
    - s3에 저장된 csv파일 key 값
'''
def DepositDataToS3(**context):
    _year = str(context['logical_date'].date().year)
    _month = context['logical_date'].date().month
    _month = str(_month) if _month > 9 else "0" + str(_month)
    _day = context['logical_date'].date().day
    _day = str(_day) if _day > 9 else "0" + str(_day)
    
    _s3_folder = f'{_s3_root_folder}/{_year}'
    _s3 = boto3.client('s3', endpoint_url=_endpoint, aws_access_key_id=_access_key, aws_secret_access_key=_secret_key)
    
    _fileName = f"예금_{_year}_{_month}_{_day}.csv"
    
    _contr = contr()

    if Run(_contr.DepositRun(_fileName,_year,_month,_day)):
        _s3_key = f'{_s3_folder}/{_fileName}'
        _s3.upload_file(_fileName, _s3_bucket_name, _s3_key)
        print("예금 데이터 업로드 완료")
        if os.path.isfile(_fileName):
            os.remove(_fileName)
    else:
        raise Exception(f"Failed to fetch DepositRun {_fileName} Data.")
    print("Deposit S3 Key : ",_s3_key)
    context['ti'].xcom_push(key='s3key', value = _s3_key)

'''
- 예금 데이터 .csv를 S3에서 로딩 후 MySQL DB에 저장 , DB 연결 해제
- DF 에서 결측값 '-' => None로 변환(DB적재를 위해)
- 테이블 생성 함수는 DB에서 직접 Create하기(DBA 역할)
- 파라미터
    - context : airflow context 변수 사용
- Xcom pull value 
    - s3에 저장된 csv파일 key 값
'''
def DepositDataS3ToDB(**context):
    _s3_key = context['ti'].xcom_pull(task_ids='DepositData_To_S3',key='s3key')
    
    print("s3_key : ",_s3_key)
    _s3 = boto3.client('s3', endpoint_url=_endpoint, aws_access_key_id=_access_key, aws_secret_access_key=_secret_key)
    _response = _s3.get_object(Bucket=_s3_bucket_name, Key=_s3_key)
    _csv_data = _response['Body'].read().decode('utf-8')
    
    _df = pd.read_csv(StringIO(_csv_data))
    _df[_df.columns[:10]] = _df[_df.columns[:10]].replace({'-':None})
    print(_df.head())

    _query = query(_db_ip,int(_db_port),_db_name,_db_user,_db_pw,_tableName)
    #_query.CreateTable_DepositData()
    _query.InsertDepositDFToTable(_df)
    _query.DisConnect()
    
default_args = {
    'owner': 'chlee',
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
    'depends_on_past': False
}

with DAG(
    dag_id = 'chlee_dag_deposit',
    start_date=pendulum.datetime(2023, 6, 10, tz="Asia/Seoul"),
    default_args=default_args,
    schedule_interval='@daily',
    catchup=True
) as dag:
    
    _task_start = DummyOperator(
        task_id = 'Task_Start',
    )
    
    _task1 = PythonOperator(
        task_id = 'DepositData_To_S3',
        python_callable=DepositDataToS3,
        provide_context=True # airflow 2.x 부터는 안써도 됨.
    ) 

    _task2 = PythonOperator(
        task_id="DepositData_To_DB",
        python_callable= DepositDataS3ToDB,
        provide_context=True
    )
    
    _task_end = DummyOperator(
        task_id = 'Task_End',
    )
    
    _task_start >> _task1 >> _task2 >> _task_end
    
