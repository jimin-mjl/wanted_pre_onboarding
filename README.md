# 원티드 프리온보딩 백엔드 코스 지원 과제

## 기능 요구 사항
- 채용공고 읽기 / 등록 / 수정 / 삭제 API
  - 채용공고 리스트 API
  - 채용공고 디테일 API
    - 해당 회사가 올린 다른 채용공고 ID 리스트 포함
  - 채용공고 등록 API
    - 회사 ID, 포지션, 상세설명, 보상금, 사용기술, 마감일 정보 포함
  - 채용공고 수정 API
    - 회사 ID 제외 전체 정보 수정 가능
  - 채용공고 삭제 API
    - DB에서 완전 삭제
- 키워드로 채용공고 검색 API
  - 텍스트 정보에 한해 검색 가능
- 채용공고 지원 API
  - 중복 지원 제한 기능

## 구현 사항 및 구현 과정
- 기능 요구 사항 전체 구현
  - Django Rest Framework 활용해 API View 작성
- 각 API에 대한 테스트 코드 구현
  - unittest 기반의 Django Rest Framework의 APITestCase 활용

## 테스트 및 실행 방법
1. `.env` 파일 작성
```
SECRET_KEY=secretkey
```
2. 가상환경 설치 및 의존 패키지 설치
```shell
python3 -m venv ENV
source ENV/bin/activate
pip install -r requirements.txt
```
3. DB 세팅
```shell
python manage.py migrate
```
4. 테스트 코드 실행
```shell
python manage.py test
```
5. API 동작 확인을 위한 서버 실행
```shell
python manage.py runserver
```
