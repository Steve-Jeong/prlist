# prlist - 파일 병합 유틸리티

## 프로그램 설명

`prlist`는 지정된 디렉토리 내의 모든 파일 내용을 하나로 병합하는 파이썬 기반 유틸리티입니다. 각 파일 내용 앞에 파일 경로를 주석으로 추가해주어 출처를 쉽게 확인할 수 있습니다.

주요 기능:
- 디렉토리 트리 탐색
- `.prlistignore`를 통한 파일/디렉토리 제외 기능
- 병합 결과를 표준 출력 또는 파일로 저장

## .prlistignore 사용법

`.prlistignore` 파일을 사용하여 병합에서 제외할 파일/디렉토리를 지정할 수 있습니다. Git의 `.gitignore`와 유사한 방식으로 작동합니다.

### 기본 사용 패턴
- 주석은 #으로 시작
- .log # 모든 .log 파일 제외
- /temp # 루트의 temp 디렉토리 제외
- build/ # 모든 build 디렉토리 제외
- secret. # secret.으로 시작하는 모든 파일 제외

### 무시 규칙 우선순위
1. 프로젝트 루트의 `.prlistignore` 파일
2. 하위 디렉토리의 `.prlistignore` 파일 (상위 규칙을 덮어씀)

## 설치 및 실행 가이드

### 1. 저장소 복제
```bash
git clone https://github.com/Steve-Jeong/prlist.git
cd prlist
```
### 2. 가상 환경 설정 (선택 사항)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```
### 3. 실행 권한 부여
```bash
chmod +x prlist.py
```
### 4. 사용 방법
기본 사용법:

```bash
./prlist.py <대상-디렉토리> > <결과 파일 이름>
결과를 <결과 파일 이름>으로 저장:
```
```bash
./prlist.py <대상-디렉토리> > output.txt
```
### 5. 테스트 실행
```bash
./prlist.py ./test_samples
```

## 의존성
Python 3.6 이상

추가 패키지 요구사항 없음

## 라이센스
MIT License