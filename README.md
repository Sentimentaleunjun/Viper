# Viper-Lite

Viper-Lite는 **C 스타일의 문법**과 **파이썬처럼 쉬운 사용성**을 결합한 범용 프로그래밍 언어입니다.  
네트워크, 보안, DNS, URL, 프록시, 호스팅 등 다양한 분야에서 실험적으로 사용 가능하도록 설계되었습니다.

---

## 주요 기능

- 변수 선언 및 할당
- 사칙연산 및 비교 연산
- 문자열 처리
- 조건문 (`if`) 및 반복문 (`while`)
- 함수 정의 및 호출 (`func`)
- 모듈 내장:
  - `network.get_ip(host)` – 호스트의 IP 반환
  - `dns.lookup(domain)` – 도메인 정보 반환
  - `security.sha256(string)` – SHA-256 해시 반환
- REPL 지원 (`exit` 입력 시 종료)

---

## 설치 및 실행

1. 프로젝트 폴더로 이동:

```powershell
cd C:\Users\<사용자명>\Desktop\Viper-Language
