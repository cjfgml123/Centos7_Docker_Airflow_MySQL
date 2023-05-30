# CentOS7 Docker 설치 및 명령어

### 1. Docker 설치

- 참고 링크 : https://docs.docker.com/engine/install/centos/

```shell
 sudo yum install -y yum-utils # yum-utils 유틸리티 제공 패키지 설치
 sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo # Docker Engine 설치 저장소 추가
```

```shell
# 도커 엔진 최신버전 설치
 yum install docker-ce docker-ce-cli containerd.io -y
 
 # 도커 시작
 sudo systemctl start docker 
```

```shell
# 도커 상태 확인
systemctl status docker
```

![1_docker_status](.\image\1_docker_status.png)

```shell
# docker 실행중인 container확인
docker ps

# 모든 container 확인
docker ps -a
```

```shell
# docker-compose up 시 명령어 찾을 수 없는 에러
pip install docker-compose # 실행
```

```shell
docker-compose up airflow-init # 처음 한번 실행

# 실행 중인 컨테이너들 한번에 종료
docker stop $(docker ps -aq)

# 다시 시작 및 매번 실행할 때(compose 파일 있는 곳에서)
docker-compose up
```

### 2. 컨테이너 기반 : airflow , python, playwright 설치

- 컨테이너 기반 airflow 포트 8080이여서 기존의 설치된 airflow 종료 => 포트 충돌 발생
- airflow 메타 데이터 저장 -> MySQL로 하는 것 해봐야함. (compose 파일에서 설정하는 건지 확인 필요)

- mysql 컨테이너 추가 원할 시 : docker-compose.yaml 의 service 부분에 밑의 내용 추가 후 "docker-compose up" 다시 실행

```yaml
mysql:
    image: mysql:8.0.28-debian
    networks:
      airflow_net:
        aliases:
          - mysql
    ports:
      - "10000:3306"
    volumes:
      - ./mysql:/var/lib/mysql
    environment: 
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: ssisb
      MYSQL_USER: ssisb
      MYSQL_PASSWORD: ssisb
      TZ: Asia/Seoul
    command:
      - --character-set-server=utf8mb4
      - --collation-server=utf8mb4_unicode_ci
```



