# 사용법

## 디렉토리 구성
* confile : config 파일 
* logfile : log 파일

## 소스 코드 구성
* main.py
* func.py : 각 functions 정의
* metrics.py : metrics의 list 요소로 external_metrics_list, internal_metrics_list_rdb, internal_metrics_list_aof 로 구성
* params.py : 각 parameter 정의

## 기타 구성 
* init_config.conf : 기존 redis.conf 파일에서 주석과 랜덤적용할 파라미터 부분 제거
* memtier.py : memtier_benchmark 실행 cmd command
* gen_config.py : redis config 생성
* connection.py : GA config에 benchmark 적용
---

## 실행 방법
params.py 의 count_file 변수에 생성할 confile 수 지정한 후 main.py 실행

## 실행 결과
metrics 값들은 csv 파일형태로 저장되었습니다! 서로 다른 confile로 실행된 각 결과들이 행으로 구분되었습니다. 
* result_external.csv : memtier_bechmark 결과값
* result_internal.csv : redis info 내용
* confingkkk : configfile 폴더 내부에 conf 파일 생성
* logfilekkk : logfile 폴더 내부에 logfile 파일 생성
