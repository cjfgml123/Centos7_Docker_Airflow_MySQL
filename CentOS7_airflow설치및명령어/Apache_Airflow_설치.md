# Apache Airflow 설치

- OS : Centos7

### 1. 설치

```shell
sudo mkdir ~/airflow # 시작경로 : root
export AIRFLOW_HOME=~/airflow
AIRFLOW_VERSION=2.5.0  # airflow와 python version 호환 미리 확인 필요
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

#### 1-1) Airflow 실행 전 셋팅

- Airflow DB 초기화  (DB는 Airflow와 DAG와 Task 등을 관리하기 때문에 셋팅이 필요)

```shell
airflow db init 
```

![error_0](.\image\error_0.png)

- splite3 버전 호환 문제나 "No module named '_sqlite3' " 발생 시 => 'sqlite3 를 설치하거나 버전을 올리는 방법'으로 해결 
- 나는 MySQL 진행 예정이므로 

```shell
pip3 install 'apache-airflow[mysql]' 
```

![error_1](.\image\error_1.png)


- 이런 에러 발생 시

```shell
sudo yum install mysql-devel
pip3 install 'apache-airflow[mysql]' #진행
```

#### 1-2) Airflow User 확인 명령어

```shell
[root@leecheolhee ~]# airflow users list
```



### 1-3) Airflow 실행 프로세스 확인 명령어

```sh
ps -ef | grep airflow
