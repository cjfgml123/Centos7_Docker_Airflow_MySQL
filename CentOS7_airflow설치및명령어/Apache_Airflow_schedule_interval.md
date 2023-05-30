# Apache Airflow Schedule_interval

```python
with DAG(
    dag_id = 'dag_with_catchup_bacfill_v02',
    default_args = default_args,
    start_date=datetime(2023,5,11),
    # crontab.guru 에서 cron 표현식 사용자 시간에 맞는 것 알려줌. ex) 매주 화요일 3시
    schedule_interval='@daily', # '0 0 * * *'
    catchup=False
    ) as dag: 
    task1 = BashOperator(
        task_id = 'task1',
        bash_command='echo This is a simple bash command!'    
    )
```



### 1. Cron Expression Preset

| preset   | meaning                                                     | cron        | timedelta          |
| -------- | ----------------------------------------------------------- | ----------- | ------------------ |
| None     | 예약하지 않고 외부에서 트리거된 DAG에만 사용                |             |                    |
| @once    | Schedule once and only once                                 |             |                    |
| @hourly  | Run once an hour at the beginning of the hour               | ‘0 * * * *’ | timedelta(hours=1) |
| @daily   | Run once a day at midnight                                  | ‘0 0 * * *’ | timedelta(days=1)  |
| @weekly  | Run once a week at midnight on Sunday morning               | ‘0 0 * * 0’ | timedelta(weeks=1) |
| @monthly | Run once a month at midnight of the first day of the month. | ‘0 0 1 * *’ |                    |
| @yearly  | Run once a year at midnight of January 1                    | ‘0 0 1 1 *’ |                    |

