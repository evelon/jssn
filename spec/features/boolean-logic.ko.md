# 불리언 로직

> **JSON Schema 대응:** `allOf`, `anyOf`, `oneOf`, `not`

JSON Schema의 불리언 로직 키워드는 값이 여러 하위 스키마를 동시에 만족하거나(`allOf`), 여러 스키마 중 최소 하나를 만족하거나(`anyOf`), 여러 스키마 중 정확히 하나를 만족하거나(`oneOf`), 특정 스키마를 만족하지 않을 것(`not`)을 요구합니다. JSSN은 이를 키워드가 아닌 전용 연산자로 표현합니다.

## `&` — 교집합 (allOf)

> **JSON Schema 대응:** `allOf`

```jssn
address & {
  label?: str
}

defs <
  address = { street?: str }
>
```

다음과 동등합니다:

```json
{
  "type": "object",
  "allOf": [{ "$ref": "#/$defs/address" }],
  "properties": {
    "label": { "type": "string" }
  },
  "$defs": {
    "address": {
      "type": "object",
      "properties": {
        "street": { "type": "string" }
      }
    }
  }
}
```

`&`는 스키마 개수에 상관없이 이어 쓸 수 있습니다: `a & b & c`는 `allOf: [a, b, c]`와 동등합니다.

### 닫힌 컬렉션과 `&`

#### unevaluatedProperties

> **JSON Schema 대응:** `unevaluatedProperties`

`obj`는 기본적으로 닫혀 있으므로([object.ko.md](object.ko.md) 참고), `&`로 두 개의 닫힌 형태를 교집합하면 결과도 합리적으로 닫혀야 합니다 — 양쪽 속성의 합집합 밖에 있는 속성은 허용되지 않아야 합니다. JSON Schema에서는 이를 `additionalProperties`로 표현할 수 없습니다. 스키마 자신의 `additionalProperties`는 `allOf`로 도입된 속성을 보지 못하기 때문입니다; 이를 처리하는 키워드가 바로 `unevaluatedProperties`입니다.

- `address & { label?: str }` → `unevaluatedProperties: false`
- `address & { label?: str } & {...}` → `unevaluatedProperties: true` (마지막의 단독 `{...}`가 이를 다시 엽니다. 일반 `obj`에서와 동일합니다)

#### unevaluatedItems

> **JSON Schema 대응:** `unevaluatedItems`

`unevaluatedItems`는 위의 `unevaluatedProperties`와 조금 다르게 동작합니다: 이 키워드는 `false`일 때만 의미가 있습니다. `arr`은 후행 `...` 요소가 없으면 기본적으로 닫혀 있으므로([array.ko.md](array.ko.md) 참고), 여기서도 같은 논리가 적용됩니다 — `&`로 두 개의 닫힌 배열을 교집합하면 결과에 `unevaluatedItems: false`가 암시됩니다. 이를 명시적으로 다시 열려면 후행에 `& [...]`를 추가하세요.

`tuple = [str]`이 주어졌을 때:

- `tuple & [str, num]` → `unevaluatedItems: false`
- `tuple & [str, num] & [...]` → `unevaluatedItems: true` (마지막의 단독 `[...]`가 이를 다시 엽니다. 일반 `arr`에서와 동일합니다)

**중첩된 `unevaluatedItems: true`는 바깥쪽 `false`로 감싸지면 그대로 유지되지 않습니다.** 다음과 같은 형태의 스키마를 주의하세요:

```json
{
  "type": "array",
  "prefixItems": [{ "type": "string" }],
  "allOf": [
    {
      "prefixItems": [{ "type": "string" }, { "type": "number" }],
      "unevaluatedItems": true
    }
  ],
  "unevaluatedItems": false
}
```

이는 다음과 같이 변환되어야 할 것처럼 보이지만:

```jssn
[str, num, ...] & [str]
```

실제로는 다음과 같이 변환됩니다:

```jssn
[str, num] & [str]
```

바깥쪽 `unevaluatedItems: false`가 이런 식으로 안쪽 `unevaluatedItems: true`(또는 `items: true`)를 덮어쓰고 나면, 안쪽의 열림 상태는 더 이상 의미가 없습니다 — 결과로 나오는 `arr`은 바깥쪽 `false`가 닫는 지점에서 닫히며, 그 열림 상태가 덮어써진 분기의 jssn 변환 결과에는 `...`가 나타나서는 안 됩니다. 각 분기를 독립적으로 변환하면서 어떤 바깥쪽 `false`가 이를 덮어쓰는지 추적하지 않는 독자는 이 부분을 매우 쉽게 잘못 판단해 `...`를 그대로 남기게 됩니다 — 바로 이런 이유로 JSON Schema → JSSN 컨버터는 이 판단을 독자에게 맡길 수 없습니다: 컨버터 스스로 이 경우를 감지해서 `...`를 그대로 옮기지 않고 제거해야 합니다.

## `|` — 합집합 (anyOf)

> **JSON Schema 대응:** `anyOf`

```jssn
circle | rectangle

defs <
  circle = { shape: "circle", radius: num }
  rectangle = { shape: "rectangle", width: num, height: num }
>
```

다음과 동등합니다:

```json
{
  "anyOf": [{ "$ref": "#/$defs/circle" }, { "$ref": "#/$defs/rectangle" }],
  "$defs": {
    "circle": {
      "type": "object",
      "properties": {
        "shape": { "const": "circle" },
        "radius": { "type": "number" }
      },
      "required": ["shape", "radius"]
    },
    "rectangle": {
      "type": "object",
      "properties": {
        "shape": { "const": "rectangle" },
        "width": { "type": "number" },
        "height": { "type": "number" }
      },
      "required": ["shape", "width", "height"]
    }
  }
}
```

`&`와 마찬가지로 `|`도 스키마 개수에 상관없이 이어 쓸 수 있습니다: `a | b | c | ...`는 `anyOf: [a, b, c, ...]`입니다.

## `~` — 부정 (not)

> **JSON Schema 대응:** `not`

```jssn
{
  username: str
  role: str & ~deprecatedRole
  team?: team
}

defs <
  deprecatedRole = enum("superadmin", "root", "godmode")
  team = { id: str, name?: str }
>
```

다음과 동등합니다:

```json
{
  "type": "object",
  "properties": {
    "username": { "type": "string" },
    "role": {
      "allOf": [
        { "type": "string" },
        { "not": { "$ref": "#/$defs/deprecatedRole" } }
      ]
    },
    "team": { "$ref": "#/$defs/team" }
  },
  "required": ["username", "role"],
  "$defs": {
    "deprecatedRole": {
      "enum": ["superadmin", "root", "godmode"]
    },
    "team": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" }
      },
      "required": ["id"]
    }
  }
}
```

`~`는 단항 접두 연산자입니다 — 정확히 하나의 스키마만 받으므로 그 자체로는 괄호가 필요 없습니다.

## `^(...)` — 정확히 하나 (oneOf)

> **JSON Schema 대응:** `oneOf`

이 연산자는 나머지 셋보다 다듬어지지 않았습니다 — 아직 여러 사례로 검증되지 않았고, 단일 예제로부터 도출된 형태입니다.

```jssn
{
  value?: num
  next?: ^(#, null)
}
```

다음과 동등합니다:

```json
{
  "type": "object",
  "properties": {
    "value": { "type": "number" },
    "next": {
      "oneOf": [{ "$ref": "#" }, { "type": "null" }]
    }
  }
}
```

`&`/`|`/`~`와 달리, `oneOf`는 중위 연산자가 아니라 함수 호출 형태로 작성됩니다 — `oneOf: [a, b, c]`에 대해 `^(a, b, c)`처럼 씁니다.

## 연산자 조합하기

같은 표현식 안에서 `&`와 `|`를 섞어 쓸 때는 항상 괄호가 필요합니다 — 둘 사이에는 정의된 우선순위가 없습니다. `~`는 단항 접두 연산자로서 바로 뒤에 오는 단일 스키마에만 명확하게 결합되므로 이 규칙에서 예외입니다 (위 참고).

```jssn
baseVariant & ~discontinuedVariant & (colorVariant | sizeVariant)
```

여기서 `(colorVariant | sizeVariant)`는 반드시 괄호로 묶어야 합니다 — `baseVariant & ~discontinuedVariant & colorVariant | sizeVariant`는 정의된 의미가 없습니다.
