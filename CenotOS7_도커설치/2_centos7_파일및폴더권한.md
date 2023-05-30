# CentOS7 파일 및 폴더 권한

### 1. 파일 권한 확인 법

- 각각의 파일, 폴더에는 권한 있음.
- 각각의 맨 앞부분에 있는 문장(drwxr-xr-x)이 해당 파일 및 폴더의 권한을 나타냄.

```shell
ls -al
```

### 2. 파일 권한 보기

 -|rw-|rw-|r--
1  2  3  4

1) Indicates type - 해당 파일의 종류를 나타낸다. (Directory, Regular file, Symbolic link 등)

2) 해당 파일(폴더)을 생성하거나 소유하고 있는 유저의 권한을 나타낸다.

3) 해당 파일(폴더)에 부여된 그룹에 속한 유저의 권한을 나타낸다.

4) 해당 파일(폴더)에 대한 모든 유저들의 권한을 나타낸다.

*참고 r : read(읽기), w : write(쓰기), x : execute(실행)을 나타낸다.

| Permissions |          |          |            |
| ----------- | -------- | -------- | ---------- |
| user        | r - read | w -write | x -execute |
| group       | r - read | w -write | x -execute |
| others      | r - read | w -write | x -execute |

#### 2-1. 예시

- 문자 사용하여 변경 ( 권한 부여)

```shell
chmod g+rw testfile               //해당 그룹에 속하는 유저에게 읽기와 쓰기 권한을 준다.
chmod u+r testfile                 //해당 파일을 소유한 사람에게 읽기 권한을 준다.
chmod ugo+rwx testfile             //소유자, 그룹, 모든 유저에게 읽기 쓰기 실행 권한을 준다 > *매우 안좋음
```

- 권한 삭제

```shell
chmod g-rw testfile              //해당 그룹에 속하는 유저에게 읽기와 쓰기 권한을 삭제한다.
chmod u-r testfile                 //해당 파일을 소유한 사람에게 읽기 권한을 삭제한다.
chmod ugo-rwx testfile             //소유자, 그룹, 모든 유저에게 읽기 쓰기 실행 권한을 삭제한다.
```

