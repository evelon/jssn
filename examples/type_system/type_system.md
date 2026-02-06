# Type System Showcase

이 예시는 **JSSN v0.2 타입 시스템의 핵심 표현력**을 간단히 보여주기 위한 예시다.

목표:

- primitive constraint
- enum / literal
- array / tuple / typed tail
- optional field
- reusable type
- open object (`...`)

실제 서비스 도메인에 종속되지 않은 **순수 타입 예시**다.

---

## Highlights

### Primitive constraints

```jssn
SmallInt = int(0..9)
UserId = str(uuid)
```

이러한 alias는 사용 시 inline 으로 확장되며 JSON Schema에는 별도의 이름으로 남지 않는다.

---

### Enum, literal, and union

```jssn
Status = enum: str {
  ACTIVE
  DISABLED
  BANNED
}

YesNo = "YES" | "NO"
```

- `enum block form`은 JSON Schema의 `enum`으로 변환된다.
- 문자열 literal의 union (`"YES" | "NO"`)은 일반 union이며 enum으로 canonicalize되지 않는다.

---

### Arrays

```jssn
tags: []str
scores: [](1..5)int
matrix: [](3)[](2..4)int
```

- 배열은 **prefix 형태 `[]Type`** 로 표현한다.
- 길이 제약은 `[]` 바로 뒤에 `(min..max)` 형태로 붙는다.
- prefix 표기는 중첩 배열에서도 읽기 쉬운 구조를 유지한다.

---

### Tuples

```jssn
pair: [str, int]
open_any_tail: [str, int, ...]
typed_tail: [str, int, ...SmallInt]
typed_tail_len: [str, int, ...(1..3)SmallInt]
```

- 고정 길이 tuple
- 열린 tuple (tail이 any)
- 타입이 지정된 tail tuple
- tail 반복 개수에 대한 길이 제약

---

### Object shape

```jssn
profile: obj {
  name: str(1..20)
  age?: int(0..150)
  email?: str(email)
  ...
}
```

- object는 `obj {}` 형태 사용을 권장한다 (`{}` 도 허용).
- 필드는 기본적으로 required.
- `?` 는 optional field를 의미한다.
- `...` 는 additional properties 허용을 의미한다.

---

이 예시는 JSSN의 모든 문법을 나열하기 위한 것이 아니라,

> JSON Schema를 사람이 읽기 좋은 형태로 작성할 수 있다

는 감각을 전달하기 위한 예시다.
