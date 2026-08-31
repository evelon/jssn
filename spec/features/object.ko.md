# 객체

> **JSON Schema 대응:** `object` 타입과 `properties`, `required`, `additionalProperties`, `patternProperties`, `minProperties`, `maxProperties`

[types.ko.md](types.ko.md)에서 설명했듯이, JSSN `obj`의 기본 문법은 다음과 같습니다.

```jssn
{
  name: str
  email: str
  age: int
}
```

다음과 동등합니다:

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "email": { "type": "string" },
    "age": { "type": "integer" }
  },
  "required": ["name", "email", "age"],
  "additionalProperties": false
}
```

## 필수 속성과 선택 속성

> **JSON Schema 대응:** `properties`와 결합된 `required` 배열

속성은 기본적으로 필수입니다. 속성을 선택으로 표시하려면 키 이름 바로 뒤, 콜론 앞에 `?`를 붙입니다.

```jssn
{
  name: str
  email: str
  age?: int
}
```

여기서 `name`과 `email`은 반드시 있어야 합니다. `age`는 생략할 수 있습니다.

다음과 동등합니다:

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "email": { "type": "string" },
    "age": { "type": "integer" }
  },
  "required": ["name", "email"]
}
```

`?`는 항상 키 이름 바로 뒤에 옵니다 — 키 이름 앞이나 타입 뒤가 아닙니다.

```jssn
age?: int
```

다음이 아니라:

```jssn
?age: int
```

이것도 아닙니다:

```jssn
age: int?
```

## 중첩된 객체

모든 `obj`는 깊이에 상관없이 자신만의 독립적인 필수/선택 속성 집합을 가집니다. `?`로 속성을 표시하는 것은 오직 그 속성이 바로 상위 객체 안에서 선택인지 여부에만 영향을 줍니다.

```jssn
{
  title: str
  meta?: {
    tags: arr
    notes?: str
  }
}
```

`meta` 자체는 선택이지만, 존재한다면 그 안의 `tags`는 필수입니다.

다음과 동등합니다:

```json
{
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "meta": {
      "type": "object",
      "properties": {
        "tags": { "type": "array" },
        "notes": { "type": "string" }
      },
      "required": ["tags"]
    }
  },
  "required": ["title"]
}
```

## 타입 제약 없이 필수인 경우

JSON Schema는 `properties`에 전혀 나타나지 않는 키를 `required`에 나열하는 것을 허용합니다 — 그 키는 반드시 존재해야 하지만, 값은 특정한 형태로 제약되지 않습니다. JSSN에서는 단독 키(콜론도 타입도 없는)가 이미 "필수이며 타입은 `any`"를 의미하므로 — 단독 키의 `any` 축약형에 대해서는 [types.ko.md](types.ko.md)를 참고하세요 — 이 경우에는 추가 표시가 전혀 필요 없습니다.

```jssn
{
  id
  name: str
}
```

여기서 `id`는 반드시 존재해야 하지만 어떤 JSON 값이든 가질 수 있습니다; `name`은 반드시 존재해야 하며 문자열이어야 합니다.

다음과 동등합니다:

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" }
  },
  "required": ["id", "name"]
}
```

`id`가 `required`에는 나타나지만 `properties`에는 나타나지 않는다는 점에 주목하세요 — 정확히 위에서 설명한 형태입니다.

같은 조합은 반대 방향으로도 동작합니다: `id?`(단독 키에 `?` 접미사)는 선택이면서 타입은 `any`입니다.

## 설계 노트

- **기본적으로 필수이며, JSON Schema 자체의 기본값을 뒤집습니다.** JSON Schema는 `required`에 나열되지 않는 한 속성을 선택으로 취급합니다. JSSN은 이를 뒤집어 표시가 없으면 필수를 의미하도록 합니다. 이렇게 하면 필수/선택 표기가 JSSN이 이미 JSON Schema의 기본값을 열림에서 닫힘으로 뒤집은 나머지 두 곳 — 배열 요소([array.ko.md](array.ko.md) 참고)와 `additionalProperties`(아래 참고) — 와 일관성을 갖게 됩니다. 이 둘은 모두 JSON Schema에서는 기본적으로 제약이 없거나 열려 있지만 JSSN에서는 기본적으로 닫혀 있습니다. `required`만 예외로 남겨 JSON Schema의 "기본적으로 선택" 관례를 그대로 따르게 두었다면, "표시 없음"이 의미하는 바에 대해 JSSN이 내부적으로 일관성을 잃었을 것입니다.
- **필수를 뜻하는 `!`가 아니라 선택을 뜻하는 `?`입니다.** 이 명세의 이전 버전은 속성을 필수로 표시하는 데 `!`를 사용했고, 기본값은 선택이었습니다(JSON Schema 자체의 기본값과 일치, 위 참고). 실제로는 속성을 필수로 표시하는 것을 잊는 것(`!` 누락)이 선택이어야 할 속성을 잘못 표시하는 것보다 훨씬 저지르기 쉬운 실수입니다 — 그리고 표시가 없는 속성이 다른 모든 선택 속성과 똑같아 보이기 때문에 훨씬 놓치기도 쉽습니다. 대신 선택 속성을 `?`로 표시하면, 흔한 실수(선택으로 표시하는 것을 잊는 것)는 다른 모든 필수 속성과 똑같아 보이는 속성을 만들어내고, 더 드물지만 더 치명적인 실수(의도치 않게 선택이 되어버린 속성)는 눈에 띄는 `?`로 즉시 드러납니다. 이는 또한 TypeScript 등 유사 언어에서 `?`가 필수성이 아니라 선택성을 표시하는 것과 더 가까운 용도로 `?`를 사용하는 것이기도 합니다.
- **이전 설계가 nullable을 위해 남겨두었던 `?` 기호를 사용합니다.** `!` 기반 설계는 나중에 nullable 값 축약형(예: "문자열 또는 null"을 의미하는 `str?`)을 위해 `?`를 비워두려고, 선택성을 위한 `?` 사용을 검토했다가 기각했습니다. 하나의 기호가 같은 방식으로 두 곳에 쓰이면 두 의미를 깔끔하게 담을 수 없기 때문입니다. 이번 버전은 이 트레이드오프를 받아들입니다: 이제 *키* 뒤의 `?`는 선택을 의미하므로, 향후 nullable 축약형은 다른 기호가 필요하거나, *타입* 뒤에서 `?`를 재사용하고 위치(키 대 타입)로 의미를 구분해야 할 것입니다. 필수/선택 실수가 nullable 축약형의 필요성(아직 일정이 없습니다 — [README.ko.md](../README.ko.md)의 로드맵 참고)보다 얼마나 더 흔한지를 고려하면, 이는 감수할 가치가 있다고 판단됩니다.

## 추가 속성

> **JSON Schema 대응:** `additionalProperties`

JSSN의 기본 형태는 `additionalProperties`가 `false`로 설정된 것입니다. `additionalProperties`가 없거나 `true`라면, 다음과 같이 작성합니다.

```jssn
{
  name: str
  email: str
  age: int
  ...
}
```

여기서 `...`는 `any`의 생략된 형태입니다. 다음과 같습니다:

```jssn
{
  name: str
  email: str
  age: int
  ...: any
}
```

다음과 동등합니다:

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "email": { "type": "string" },
    "age": { "type": "integer" }
  },
  "required": ["name", "email", "age"]
}
```

`additionalProperties`가 타입(스키마)이라면, 다음과 같이 작성합니다.

```jssn
{
  name: str
  email: str
  age: int
  ...: str
}
```

다음과 동등합니다:

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "email": { "type": "string" },
    "age": { "type": "integer" }
  },
  "required": ["name", "email", "age"],
  "additionalProperties": { "type": "string" }
}
```

## 패턴 속성

> **JSON Schema 대응:** `patternProperties`

JSON Schema에서 `patternProperties`는 정규식으로 키를 제어합니다. JSSN에서는 `/`로 감싼 정규식을 키 위치에 씁니다. `/`가 구분자로 사용되므로, 정규식 내부의 `/`는 반드시 이스케이프해야 합니다.

```jssn
{
  /^S_/: str
  /^I_/: int
}
```

다음과 동등합니다:

```json
{
  "type": "object",
  "patternProperties": {
    "^S_": { "type": "string" },
    "^I_": { "type": "integer" }
  },
  "additionalProperties": false
}
```

패턴 속성과 일반 속성을 함께 사용할 때는 패턴 속성을 위쪽에 두는 것을 권장하지만, 가독성을 위해 이를 완화할 수 있습니다.

```jssn
{
  /^S_/: str
  S_name
  S_email
  /^I_/: int
  I_age
}
```

## 객체 크기

> **JSON Schema 대응:** `minProperties`, `maxProperties`

요소가 고정된 위치에 있어 `[]` 안에 개수를 함께 표기할 수 있는 `arr`과 달리, `obj`는 `{}` 안에 키 이름과 값 타입 제약만 담습니다. 개수 제약은 종류가 다른 제약이므로 `{}` 바깥에 작성합니다.

JSON Schema의 `minProperties`/`maxProperties`는 이름 있는 속성이든, 패턴 속성이든, 추가 속성이든 상관없이 객체의 전체 속성 개수를 제약합니다. JSSN은 이를 위해 [array.ko.md](array.ko.md)에서 다룬 `min..max` 표기법을 재사용하며, 괄호로 감싸 obj 본문을 여는 `{` 바로 앞에 둡니다: `(min..max) {`.

```jssn
(3..5) {
  name: str
  email: str
  age: int
  ...
}
```

다음과 동등합니다:

```json
{
  "type": "object",
  "minProperties": 3,
  "maxProperties": 5,
  "properties": {
    "name": { "type": "string" },
    "email": { "type": "string" },
    "age": { "type": "integer" }
  },
  "required": ["name", "email", "age"]
}
```

## 범위 밖 (당분간)

- `propertyNames`는 크기와 obj 본문(`{}`) 사이에 올 수 있습니다. 세부 사항은 아직 정해지지 않았습니다.
- 관계형/조건부 요구 사항 — 예: "속성 A가 존재하면 속성 B가 필수" (JSON Schema의 `dependentRequired`, `dependentSchemas`, `if`/`then`/`else`) — 는 여기서 다루지 않습니다. 이는 단일 키의 속성이라기보다 속성들 간의 관계를 설명하므로, `?`를 확장하는 대신 자신만의 구성 요소가 필요할 것입니다.
