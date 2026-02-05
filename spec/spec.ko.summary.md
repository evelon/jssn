# JSSN Spec 요약 (개인 참고용)

이 문서는 JSSN(JSON Schema Symbolized Notation) v0.1 초안의 핵심 구조와 개념만 빠르게 참고하기 위한 개인용 요약이다.  
정식 기준 문서는 `JSSN-Spec.md`이며, 이 파일은 번역 + 요약 메모에 가깝다.

---

## 1. JSSN의 목적

JSSN은 **JSON Schema를 생성하기 위한 사람이 쓰는 DSL**이다.

핵심 철학:

- schema-first DSL
- JSON Schema로 완전히 변환 가능해야 함
- type / constraint / format / metadata 명확 분리
- 사람이 읽기 쉬운 작성 언어
- JSON Schema는 target (컴파일 결과)

---

## 2. 문서 구조

최상위 블록:

```
meta { ... }      // 필수
type { ... }      // 선택
schema Name { }   // 1개 이상 필수
```

canonical 순서:

1. meta
2. type
3. schema들

meta 필수:

- jssn_version
- schema 여러 개면 entry 필요

---

## 3. type 블록 (재사용 타입 정의)

type 블록 내부에서만 타입 선언.

두 가지 선언 방식:

### 3.1 defined type (`=`) → $defs 생성

```
type {
  SeatNo = int(0..7)
}
```

- JSON Schema `$defs` 생성
- 사용 시 `$ref`
- inline 금지

### 3.2 named inline type (`^=`) → inline 확장

```
type {
  Dice ^= int(1..6)
}
```

- $defs 생성 안함
- 사용 시 inline 삽입

사용 시 구분 없음:

```
roll: Dice
```

inline 여부는 선언에서만 결정됨.

---

## 4. format alias

```
type {
  uuid = str(uuid)
  email ^= str(email)
}
```

- = → $defs 생성
- ^= → inline
- annotation은 defined type만 가능

---

## 5. schema 블록

```
schema Player {
  id: uuid
}
```

- object 구조만 정의
- schema 이름도 전역 namespace 공유
- schema는 서로 타입처럼 참조 가능
- 여러 schema 있으면 meta.entry 필요

모든 schema는 JSON Schema `$defs`로 emit  
entry schema는 root `$ref`

---

## 6. 타입 시스템

primitive:

- int
- num
- str
- bool
- null
- obj
- arr

금지 identifier:
integer, number, string, boolean, object, array

---

## 7. object 규칙

기본: **closed object**

```
additionalProperties = forbid
```

열려면 반드시:

```
{
  ...
}
```

또는

```
{
  ...: int
}
```

### global rule

```
*: int
```

모든 value int

```
*(1..5): int
```

모든 key 길이 + value

### pattern rule

```
/^i-/: int
```

patternProperties

### spread key 제한

```
...(1..20): int
...(uuid): int
...(/regex/): int
```

---

## 8. array & tuple

### 일반 array

```
[int...]
```

### strict tuple

```
[int, str]
```

### open tuple

```
[int, str, ...]
```

### tail 반복 tuple

```
[int, str, int...]
```

### 길이 제한

```
[int...](1..3)
(1..3)[int...]
```

---

## 9. enum

type block enum:

```
type {
  Status = enum: str {
    RUNNING
    ENDED
  }
}
```

inline enum:

```
str(enum RUNNING|ENDED)
int(enum 1|2|3)
(enum A|2)
```

- bare identifier = string literal
- enum은 literal만 허용
- object/array enum은 ! 필요

---

## 10. const literal

```
enabled: !true
mode: !"RUNNING"
config: !{a:1}
```

typed const:

```
int(!3)
str(uuid, !"....")
```

- 항상 마지막 인자
- JSON Schema const로 변환
- union literal 허용

---

## 11. optional

기본 required

```
id?: int
```

null 허용과 다름.

---

## 12. annotation 시스템

validation 영향 없음  
metadata only

### example

```
@=1
@example(1)
```

### description

```
@:"text"
@desc("text")
```

### default

```
@~3
@default(3)
```

### deprecated

```
@deprecated
```

object/array literal은 항상 `!` 사용.

default는 validation 영향 없음.

---

## 13. canonical form 목적

canonical은:

- diff 안정성
- formatter 일관성
- deterministic emission
- semantic 동일성 비교

author가 반드시 canonical로 쓸 필요는 없음.

formatter/emitter용.

---

## 14. invalid 조건 주요

invalid 예:

- type 충돌
- global rule vs field 충돌
- enum vs const 충돌
- default constraint 위반
- 이름 중복
- format 2개 이상
- spread 2개 이상
- - 2개 이상

---

## 15. v0.1 범위

v0.1은 core language만 정의.

미포함:

- import/module
- multi-file
- tooling semantics
- strict format mode

---

## 개인 메모

이 DSL은 단순 JSON schema wrapper가 아니라  
"JSON Schema를 타겟으로 하는 새로운 schema 언어"에 가까움.

현재 상태:

- validation subset 중심
- human authoring 최적화
- emitter deterministic 설계
- canonical spec 존재
