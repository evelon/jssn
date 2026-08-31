# 참조

> **JSON Schema 대응:** `$ref` 키워드와, 이름 있는 재사용 가능한 하위 스키마를 위한 `$defs`.

`$defs`는 이름 있는 하위 스키마를 담고, `$ref`는 스키마가 필요한 어디에서든 그중 하나를 가리킵니다. JSSN은 JSON Pointer 문법(`"#/$defs/name"`) 대신 더 짧은 형식을 사용하며, 재사용 가능한 스키마에 별도의 최상위 블록을 부여합니다.

## Defs 선언하기

재사용 가능한 스키마는 스키마 본문과 분리된 `defs < ... >` 블록에서 선언합니다. 각 항목은 `name = type` 형태입니다. JSON Schema에서 `$defs`는 자신과 같은 레벨의 다른 요소들과 상호작용하지 않습니다 — 이는 `properties`/`required` 등의 형제 요소가 아니라 하나의 네임스페이스입니다 — 그래서 스키마 내 어디에 위치하든 일반 속성처럼 쓰지 않고 항상 이렇게 별도 블록으로 분리해 씁니다.

```jssn
{
  billing_address: $address
}

defs <
  address = { street: str, city: str }
>
```

또는 `defs`와 스키마 사이의 연결을 강조하고 싶다면,

```jssn
{
  billing_address: $address
} defs <
  address = { street: str, city: str }
>
```

다음과 동등합니다:

```json
{
  "type": "object",
  "properties": {
    "billing_address": { "$ref": "#/$defs/address" }
  },
  "required": ["billing_address"],
  "$defs": {
    "address": {
      "type": "object",
      "properties": {
        "street": { "type": "string" },
        "city": { "type": "string" }
      },
      "required": ["street", "city"]
    }
  }
}
```

## Def 참조하기

세 가지 형식이 있으며, 흔히 쓰이는 순서대로 나열합니다.

### 가장 가까운 참조

> **JSON Schema 대응:** 가장 가까운 `$defs` 항목으로 수동으로 해석한 `$ref` JSON Pointer

def의 이름 앞에 `$`를 붙여 씁니다: `$address`. 이는 현재 위치에서 바깥쪽으로 검색하며 해당 이름을 담고 있는 가장 가까운 `defs` 블록을 찾습니다 — 몇 단계 위에 있는지 셀 필요가 없습니다. 같은 이름이 여러 레벨에 존재한다면(섀도잉), 가장 가까운 것이 우선합니다.

```jssn
{
  billing_address: $address
  shipping_address: $address
}

defs <
  address = { street: str }
>
```

### 절대 경로

> **JSON Schema 대응:** `$ref: "#/$defs/..."`를 축약한 형태

`#`를 쓰고, 스키마 루트로부터의 경로를 쓴 다음, 마지막 `$defs` 조회를 위한 `$name`을 씁니다:

- `#$address` — 루트 레벨의 def로, `#/$defs/address`와 동등합니다
- `#order.customer$name` — `order.customer` 아래에 스코프된 def([루트 바깥의 Defs](#루트-바깥의-defs) 참고); 경로 세그먼트 사이의 `/`는 `.`가 되며, 마지막 `$defs/name` 세그먼트만 `$` 축약형을 유지합니다

가장 가까운 참조가 잘못된 def를 가릴 수 있는 상황이거나, def가 어디에 있는지 명시하는 것이 간결함보다 더 중요할 때 이 형식을 사용하세요.

### 원본 JSON Pointer

> **JSON Schema 대응:** `$ref`를 그대로 풀어 쓴 형태

축약되지 않은 전체 JSON Pointer도 따옴표 없이 그대로 사용할 수 있습니다: `#/$defs/address`. 이는 주로 JSSN에 전용 축약형이 없는 대상을 참조할 때 유용합니다 — [`$defs` 바깥 참조하기](#defs-바깥-참조하기) 참고.

## 공통 패턴

### `items`, `additionalProperties`, `patternProperties`에서 참조하기

def 참조는 타입이 올 수 있는 어디에나 등장할 수 있습니다 — [array.ko.md](array.ko.md)와 [object.ko.md](object.ko.md)의 구성 요소 안에서도 별도의 문법 없이 그대로 사용할 수 있습니다.

```jssn
[...$product]

defs <
  product = { sku: str }
>
```

```jssn
{
  ...: $score
}

defs <
  score = num
>
```

```jssn
{
  /^env_/: $envValue
}

defs <
  envValue = str
>
```

이는 각각 `items`, `additionalProperties`, `patternProperties`가 `{ "$ref": "#/$defs/..." }`를 담고 있는 것과 동등합니다.

### 다른 Def를 참조하는 Def

```jssn
{
  order: $order
}

defs <
  order = { customer: $person }
  person = { name: str }
>
```

다음과 동등합니다:

```json
{
  "type": "object",
  "properties": {
    "order": { "$ref": "#/$defs/order" }
  },
  "required": ["order"],
  "$defs": {
    "order": {
      "type": "object",
      "properties": {
        "customer": { "$ref": "#/$defs/person" }
      },
      "required": ["customer"]
    },
    "person": {
      "type": "object",
      "properties": {
        "name": { "type": "string" }
      },
      "required": ["name"]
    }
  }
}
```

간접 참조 체인(`a = b`, `b = c`, `c = { ... }`)도 같은 방식으로 동작합니다 — 각 `$name`이 독립적으로 해석되므로, 이를 작성하는 데 위의 형식 이상은 필요하지 않습니다.

### 자기 참조 (재귀 구조)

def는 무한히 중첩될 수 있는 구조를 위해 자기 자신을 참조할 수 있습니다:

```jssn
$node

defs <
  node = {
    value: str
    children: [...$node]
  }
>
```

다음과 동등합니다:

```json
{
  "$ref": "#/$defs/node",
  "$defs": {
    "node": {
      "type": "object",
      "properties": {
        "value": { "type": "string" },
        "children": {
          "type": "array",
          "items": { "$ref": "#/$defs/node" }
        }
      },
      "required": ["value", "children"]
    }
  }
}
```

### 루트 참조 (`#`)

단독 `#`는 문서 전체를 가리킵니다 — 재귀적인 형태가 별도의 `$defs` 항목 없이 _바로_ 루트 스키마일 때 유용합니다. 실제 예제는 [boolean-logic.ko.md](boolean-logic.ko.md)의 `oneOf` 섹션을 참고하세요 (`next`가 다른 노드이거나 `null`인 연결 리스트 노드를, `next: ^(#, null)`로 표현하는 예제입니다).

### 상호 재귀적인 Defs

```jssn
$expr

defs <
  expr = num | $binaryOp
  binaryOp = {
    op: enum("+", "-", "*", "/")
    left: $expr
    right: $expr
  }
>
```

다음과 동등합니다:

```json
{
  "$ref": "#/$defs/expr",
  "$defs": {
    "expr": {
      "oneOf": [{ "type": "number" }, { "$ref": "#/$defs/binaryOp" }]
    },
    "binaryOp": {
      "type": "object",
      "properties": {
        "op": { "enum": ["+", "-", "*", "/"] },
        "left": { "$ref": "#/$defs/expr" },
        "right": { "$ref": "#/$defs/expr" }
      },
      "required": ["op", "left", "right"]
    }
  }
}
```

절대 경로 형식(`left: #$expr`)도 여기서 동작하며, `binaryOp`가 얼마나 깊이 중첩되어 있든 동일하게 읽힙니다 — 가장 가까운 참조 형식은 정확한 깊이를 세어야만 하는 상황에서만 이점이 있는데, 여기서는 그런 상황이 발생하지 않습니다.

### 재귀적인 범용 값 타입

`$defs`/`$ref` 패턴이 실무에서 가장 많이 쓰이는 용도입니다: "JSON으로 표현 가능한 모든 값."

```jssn
$json

defs <
  json = str | num | bool | null | [...$json] | { ...: $json }
>
```

다음과 동등합니다:

```json
{
  "$ref": "#/$defs/json",
  "$defs": {
    "json": {
      "oneOf": [
        { "type": "string" },
        { "type": "number" },
        { "type": "boolean" },
        { "type": "null" },
        { "type": "array", "items": { "$ref": "#/$defs/json" } },
        {
          "type": "object",
          "additionalProperties": { "$ref": "#/$defs/json" }
        }
      ]
    }
  }
}
```

여기서는 새로운 것이 필요하지 않습니다 — array.md의 `[...type]`, object.md의 `{...: type}`, boolean-logic.md의 `|` 모두 다른 타입과 마찬가지로 자기 참조와 그대로 결합됩니다.

## 흔치 않은 형태

아래 형식들은 유효하지만 거의 필요하지 않습니다. 대부분의 독자는 이 섹션을 건너뛰어도 됩니다.

### `$anchor`

> **JSON Schema 대응:** `$anchor`, `$ref: "#name"`으로 참조됩니다

경로 대신 단순한 이름으로 참조합니다 — 주로 다른 문서에서 참조될 것을 염두에 둔 스키마에서 유용합니다.

```jssn
{
  billing_address: #address
}

defs <
  address as #address = { street: str }
>
```

### `$defs` 바깥 참조하기

> **JSON Schema 대응:** `$defs`가 아닌 위치를 가리키는 `$ref`

`$ref`는 `$defs` 아래뿐 아니라 문서 내 모든 스키마를 대상으로 삼을 수 있습니다. JSSN에는 이를 위한 전용 표기법이 없습니다 — 이는 안티패턴으로 취급되며, 원본 JSON Pointer로 대체됩니다:

```jssn
{
  primary_email: str(email)
  backup_email: #/properties/primary_email
}
```

### 루트 바깥의 Defs

> **JSON Schema 대응:** 문서 루트가 아니라 속성 자신의 스키마 안에 중첩된 `$defs`

[Defs 선언하기](#defs-선언하기)에서의 논리가 여기에도 그대로 적용됩니다 — `$defs`는 어디에 있든 하나의 네임스페이스이므로, 여전히 별도 블록으로 분리해 작성하되 어느 속성에 속하는지 경로로 한정합니다:

```jssn
{
  order: { item: $lineItem }
}

order.defs <
  lineItem = { sku: str }
>
```

다음과 동등합니다:

```json
{
  "type": "object",
  "properties": {
    "order": {
      "type": "object",
      "properties": {
        "item": { "$ref": "#/properties/order/$defs/lineItem" }
      },
      "required": ["item"],
      "$defs": {
        "lineItem": {
          "type": "object",
          "properties": {
            "sku": { "type": "string" }
          },
          "required": ["sku"]
        }
      }
    }
  },
  "required": ["order"]
}
```

### 불리언 스키마인 Def

> **JSON Schema 대응:** 값이 `true`나 `false`인 `$defs` 항목

```jssn
{
  metadata: $unconstrained
  locked_field: $nothingAllowed
}

defs <
  unconstrained = true
  nothingAllowed = false
>
```

이 간접 참조는 여기서 아무런 이득이 없습니다 — `metadata: true`와 `locked_field: false`는 def를 거치지 않아도 정확히 같은 의미입니다. 이 섹션은 유용해서가 아니라, 이 표기법이 유효하다는 것을 보여주기 위해 존재합니다.

## 설계 노트

- **상대 경로보다 가장 가까운 참조를 택했습니다.** 이전의 두 가지 설계는 상대 파일 경로처럼 레벨 수를 명시적으로 세었습니다: 0, 1, 2단계 위를 나타내는 증가하는 점(`.`, `..`, `...`), 그리고 별도로 Unix 스타일로 세그먼트를 반복하는 방식(`../..`). 둘 다 폐기되었습니다: 매번 주변 구조로부터 개수를 다시 유추해야 했고, 이는 더 짧은 표기가 절약해주는 것보다 실제로 더 큰 비용이었습니다. 가장 가까운 참조는 이 세는 과정을 완전히 없애는 대신, 섀도잉이 참조 지점에서 눈에 보이지 않고 암묵적이게 되는 대가를 치릅니다 — 서로 다른 레벨에서 같은 이름을 가진 두 def가 드물고, 항상 절대 경로로 해결 가능하다는 점에서 받아들일 만한 트레이드오프로 간주됩니다.

## 범위 밖 (당분간)

- `$dynamicRef`/`$dynamicAnchor` — *참조하는* 스키마가 오버라이드할 수 있는 def를 위한 메커니즘으로, 확장 가능한 기반 스키마 설계(스키마 라이브러리, 어휘집)를 위한 것입니다. 설계가 완료되면 이 문서에 포함되어야 하지만, 아직 확정된 표기법이 없어 여기에는 작성하지 않습니다.
