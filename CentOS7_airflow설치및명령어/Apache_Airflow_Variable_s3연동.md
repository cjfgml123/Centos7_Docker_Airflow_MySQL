# Apache Airflow Variables S3 연동

### 1. Airflow Variables 을 이용한 S3 연동

- AWS S3(Amazon Simple Storage Service) : 인터넷용 스토리지 서비스
- 버킷(Bucket) : 객체들이 모여있는 컨테이너를 버킷이라 부르며 가장 높은 수준의 네임스페이스 역할을 함. 액세스 제어나 사용량 보고에 대한 집계 단위 등 여러 목적으로 사용가능
- 객체(Object) : 데이터가 저장되는 단위, 객체는 데이터와 키, 메타데이터로 구성. 객체 키는 버킷 내 객체를 고유하게 식별함.
- 객체 키(Object Key): 객체를 만들 때 버킷 내 각 객체의 고유한 식별자로 키 이름을 지정.
  - ex) test.jpg 파일이 image 폴더 안에 들어가 있다면 test.jpg 파일의 키는 image/test.jpg 임.

```python
import boto3
# airflow 기본 import 추가해야함. 코드 편리상 여기서는 뺌.
from airflow.models import Variable, TaskInstance

_endpoint = Variable.get('s3_endpoint') # s3 url 주소
_access_key = Variable.get('s3_access_key') 
_secret_key = Variable.get('s3_secret_key')
_s3_bucket_name = 'chlee-test'

def S3ToDB():
    _s3 = boto3.client('s3', endpoint_url=_endpoint, aws_access_key_id=_access_key, 		        aws_secret_access_key=_secret_key)
    # 버킷 생성 : 한번만 실행 , 중복 실행 시 
    # botocore.errorfactory.BucketAlreadyOwnedByYou: An error occurred (BucketAlreadyOwnedByYou) 발생
    _s3.create_bucket(Bucket=_s3_bucket_name) 
    
    response = _s3.list_buckets()
    # 버킷 리스트 조회
    for bucket in response.get('Buckets', []):
      print(bucket.get('Name'))
```

#### 1-1) 버킷 이름 규칙

- "botocore.exceptions.ClientError: An error occurred (InvalidBucketName) when calling the CreateBucket operation: The specified bucket is not valid." 에러 발생 시

- 3~63자의 길이여야 합니다.
- 소문자, 숫자, 하이픈(-) 및 마침표(.)만 포함할 수 있습니다.  "_" 안됨.
- 하이픈(-)으로 시작하거나 끝나면 안 됩니다.
- 마침표(.)는 버킷 이름의 어떤 부분에도 연속으로 사용되면 안 됩니다.

#### 1-2) File Upload 

- file_name = 업로드할 파일, 상대 경로는 실행하는 코드를 기준으로 함.
- bucket = 업로드될 버킷의 이름을 지정
- key = 업로드되어 버킷 내에서 해당 파일이 가질 키를 지정. image/test.jpg라고 하면 버킷의 image 폴더 안에 test.jpg라는 파일명으로 저장.
- S3에 파일을 업로드할 때 폴더가 존재하지 않음. s3는 폴더 구조를 가지지 않고, 객체의 키(Key)로 표현되는 경로를 사용하여 데이터를 저장, ex) :  "folder/subfolder/data.csv"와 같은 키를 사용하여 폴더 구조를 표현 가능.

```python
import boto3

# AWS 계정의 액세스 키와 비밀 키 설정
_access_key = "YOUR_ACCESS_KEY"
_secret_key = "YOUR_SECRET_KEY"

# S3 서비스에 연결
_endpoint = "https://s3.amazonaws.com"  # 엔드포인트 URL
_s3 = boto3.client('s3', endpoint_url=_endpoint, aws_access_key_id=_access_key, aws_secret_access_key=_secret_key)

# 업로드할 파일 정보
local_file_path = 'data.csv'  # 로컬 파일 경로
s3_bucket_name = 'YOUR_BUCKET_NAME'  # S3 버킷 이름
s3_key = 'folder/subfolder/data.csv'  # S3에 저장될 파일 경로 및 이름

# 파일 업로드
_s3.upload_file(local_file_path, s3_bucket_name, s3_key)
```

