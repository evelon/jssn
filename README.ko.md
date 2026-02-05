# JSSN (JSON Schema Symbolized Notation)

**JSSN**은 사람이 읽기 쉽고 표현력이 높으며 결정론적인 방식으로 **canonical JSON Schema**를 생성하기 위해 설계된 schema‑first DSL입니다.

이 언어는 JSON Schema를 컴파일 타깃으로 사용하면서, **사람이 직접 작성하는 스키마 설계**에 초점을 맞춥니다.

> 상태: 실험적 언어 설계 (v0.1 draft)

---

## 왜 JSSN인가?

JSON Schema를 raw 형태로 직접 작성하면 다음과 같은 문제가 있습니다.

- 장황함 (verbose)
- 반복적 구조
- diff 추적이 어려움
- 구조적으로 이해하기 어려움

JSSN은 다음을 제공하기 위해 만들어졌습니다.

- 간결한 schema authoring 언어
- 강력한 canonicalization 규칙
- 결정론적 JSON Schema 생성
- 재사용 가능한 타입 정의
- 읽기 쉬운 constraint와 metadata 표현

JSSN은 JSON Schema를 대체하려는 언어가 아닙니다.  
대신 JSON Schema를 생성하는 **상위 작성 언어(authoring language)** 입니다.

---

## 설계 목표

JSSN은 다음 목표를 기반으로 설계되었습니다.

### 사람이 작성하기 쉬운 언어

읽기 쉽고, 쓰기 쉽고, 구조적으로 명확한 스키마 정의를 목표로 합니다.

### Canonical 출력

의미적으로 동일한 두 schema는 항상 동일한 JSON Schema를 생성해야 합니다.

### 결정론적 컴파일

JSSN 문서가 JSON Schema로 변환되는 과정에서 해석의 모호성이 없어야 합니다.

### 관심사의 분리

다음 요소들을 명확히 구분합니다.

- type
- constraint
- format
- metadata (annotation)

### JSON Schema 호환성

의미 있는 JSON Schema로 표현 가능한 모든 구조는 JSSN으로도 표현 가능해야 합니다.

---

## 예시

```jssn
meta {
  jssn_version: "0.1"
  entry: CaseSnapshot
}

type {
  SeatNo = int(0..7)
  uuid ^= str(uuid)
}

schema Player {
  id: uuid
  seat: SeatNo
}

schema CaseSnapshot {
  case_id: uuid
  players: [Player...]
}
```

이 코드는 다음 특징을 가진 canonical JSON Schema로 변환됩니다.

- 재사용 타입을 위한 `$defs`
- `$ref` 기반 참조
- 결정론적 구조
- 일관된 constraint 표현

---

## 핵심 개념

### Schema‑first DSL

JSSN 문서는 런타임 데이터가 아니라 **스키마 구조 자체**를 먼저 정의합니다.

### JSON Schema를 타깃으로 사용

JSSN은 JSON Schema로 emit/compile 됩니다.  
실제 validation 기준은 JSON Schema입니다.

### Canonical form

JSSN은 canonical 출력 규칙을 정의합니다.

이를 통해:

- 포맷 안정성 확보
- diff 가독성 향상
- emitter의 구조 정규화 가능

### 타입 시스템

JSSN은 다음을 지원합니다.

- primitive 타입
- 범위 및 길이 constraint
- enum
- const literal
- 재사용 타입
- inline vs `$defs` 타입
- 배열 및 tuple
- object property 규칙

### Annotation 시스템

validation에는 영향을 주지 않는 metadata를 지원합니다.

- description
- examples
- default
- deprecated

이 annotation들은 JSON Schema annotation으로 직접 매핑됩니다.

---

## 프로젝트 상태

이 저장소에는 현재 다음이 포함되어 있습니다.

- JSSN 언어 초안 (v0.1)
- 설계 탐색
- 내부 문서
- 개인 실험 코드

아직 production‑ready 언어는 아니며 공식 tooling은 없습니다.

---

## Repository 구조

```
/spec
  JSSN-Spec.md           # 영어 공식 spec (SSOT)
  spec.ko.summary.md     # 개인용 한국어 요약
```

추후 parser, emitter 등 tooling이 추가될 수 있습니다.

---

## 사용 목적

현재 JSSN은 다음 목적을 위해 설계되었습니다.

- 개인 schema 설계 실험
- JSON Schema authoring 실험
- 언어 설계 실험

향후 가능성:

- parser / emitter 구현
- formatter
- schema tooling
- 공개 언어로 발전

---

## License

TBD
