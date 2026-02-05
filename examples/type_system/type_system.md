# Type System Showcase

이 예시는 **JSSN 타입 표현력**을 간단히 보여주기 위한 예시다.

목표:

- primitive constraint
- enum / literal
- array vs tuple
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

숫자 범위와 format 제약을 간단히 표현할 수 있다.

---

### Enum and literal

```jssn
Status = enum: str { ACTIVE DISABLED BANNED }
YesNo = “YES” | “NO”
```

- `enum:` → JSON Schema enum으로 emit
- literal union → 일반 union (enum으로 자동 canonicalize되지 않음)

---

### Arrays

```jssn
tags: [str...]
scores: (1..5)[int...]
```

- `[T...]` → homogeneous array
- `(1..5)[T...]` → length constraint

---

### Tuples

```jssn
pair: [str, int]
open_pair: [str, int, ...]
typed_tail: [str, int, SmallInt...]
```

- fixed tuple
- open tuple
- typed tail tuple

---

### Object shape

```jssn
profile: {
    name: str(1..20)
    age?: int(0..150)
    email?: str(email)
    ...
}
```

- 기본 required
- `?` → optional
- `...` → additionalProperties 허용

---

이 예시는 JSSN의 모든 기능을 보여주기 위한 것이 아니라,

> JSON Schema를 사람이 읽기 좋은 형태로 작성할 수 있다

는 감각을 전달하기 위한 예시다.
