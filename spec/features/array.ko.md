# 배열

> **JSON Schema 대응:** `items`, `prefixItems`, `minItems`, `maxItems`. Draft 7 / 2019-09에는 `prefixItems`가 존재하지 않습니다 — 대신 `items`가 스키마 배열을 받고, 여기서 `items`가 담당하는 후행 요소 역할을 `additionalItems`가 대신합니다 (`minItems`/`maxItems`는 동일합니다).

배열은 대괄호로 작성합니다. 한 줄에 작성할 때는 요소를 쉼표(`,`)로 구분합니다. 여러 줄에 걸쳐 작성할 때는 줄바꿈만으로도 구분하기에 충분합니다 — 아래 예제 전반에 두 형식이 모두 등장합니다.

## 닫힌 배열

고정된 길이의 배열은 요소 타입을 나열하기만 하면 됩니다:

```jssn
[bool, str, int]
```

또는

```jssn
[
  bool
  str
  int
]
```

다음과 동등합니다:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 3,
  "items": false
}
```

## 열린 배열

고정된 접두 부분(prefix) 이후에도 특정 타입의 요소를 계속 받아들이는 배열은, 해당 타입 바로 앞에 `...`를 붙여 작성합니다. 아래 예제는 처음 세 요소 이후에 `num`을 계속 받아들입니다:

```jssn
[bool, str, int, ...num]
```

다음과 동등합니다:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 3,
  "items": {
    "type": "number"
  }
}
```

접두 부분 이후에 어떤 타입이든 받아들이는 배열은 단독 `...`로 작성합니다:

```jssn
[bool, str, int, ...]
```

이는 다음의 `any` 생략형입니다:

```jssn
[bool, str, int, ...any]
```

이는 다음과 동등합니다:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 3,
  "items": true
}
```

## 제한된 후행 요소

배열의 고정된 접두 부분 이후, 특정 타입의 후행 요소 허용 개수는 `(min)..(max) (type)` — 개수와 타입 사이에 공백 하나 — 로 작성합니다. 예를 들어 "`num` 2개에서 4개 사이"는 `2..4 num`이고, "3개 이상"은 `3.. num`이며, "최대 4개"는 `..4 num`입니다. 이 위치에서는 `any`를 생략할 수 있으므로, `2..4`, `3..`, `..4`도 모두 유효합니다.

이 개수 제한 표기법은 `...`와는 별개의 토큰입니다. 위 규칙대로라면 제한 없는(최솟값도 최댓값도 없는) 후행 개수는 `.. (type)`으로 써야 하겠지만 — 대신 이전 섹션의 완전히 열린 표기법을 재사용해 `...(type)`으로 씁니다. 이 예외는 순전히 가독성을 위한 것입니다: `...num`이 `..num`보다 더 잘 읽힙니다.

### 선택적으로 존재하는 요소

배열은 각 인덱스의 타입을 고정한 채로도 가변 길이를 가질 수 있습니다. 아래 예제에서 인덱스 0(`bool`)은 항상 존재해야 하며, 배열이 더 길어진다면 인덱스 1은 `str`, 인덱스 2는 `int`여야 하지만 길이가 3을 넘을 수는 없습니다. 필수 부분과 선택 부분의 경계는 `;`로 표시하며, 이 경계에는 `,`를 절대 사용하지 않습니다.

```jssn
[bool; str, int]
```

또는

```jssn
[
  bool;
  str
  int
]
```

다음과 동등합니다:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 1,
  "items": false
}
```

### 최소 개수가 제한된 후행 요소

열린 배열은 후행 요소의 최소 개수를 요구할 수 있습니다.

```jssn
[bool, str, int, 2..]
```

또는

```jssn
[bool, str, int, 2.. any]
```

다음과 동등합니다:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 5
}
```

타입과 함께:

```jssn
[bool, str, int, 2.. num]
```

또는

```jssn
[
  bool
  str
  int
  2.. num
]
```

다음과 동등합니다:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 5,
  "items": { "type": "number" }
}
```

### 최대 개수가 제한된 후행 요소

열린 배열은 후행 요소의 개수 상한을 둘 수도 있습니다. 아래 예제는 열려 있지만, 이후 요소는 최대 3개까지만 올 수 있습니다.

```jssn
[bool, str, int, ..3]
```

또는

```jssn
[
  bool
  str
  int
  ..3
]
```

다음과 동등합니다:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 3,
  "maxItems": 6
}
```

### 최소/최대 개수가 제한된 후행 요소

후행 요소의 최솟값과 최댓값을 함께 지정할 수도 있습니다.

```jssn
[bool, str, int, 2..5]
```

다음과 동등합니다:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 5,
  "maxItems": 8
}
```

### 정확히 하나의 요소만큼 확장하기

`minItems`와 `maxItems`가 같고, 그 값이 `prefixItems`의 길이보다 정확히 1 크다면, 이 배열은 `prefixItems`가 요소 하나만큼 단순히 늘어난 것처럼 동작합니다 — 의미상 닫힌 배열과 동일합니다.

이는 새로운 문법이 아닙니다. `minItems`와 `maxItems`가 둘 다 `prefixItems`의 길이와 같아지는 순간, 어떤 배열 인덱스도 `items`가 적용될 위치에 도달할 수 없습니다 — 따라서 `items: false`, `items: { ... }`, `items: true`는 모두 동일하게 동작합니다. 아래 두 스키마는 그러므로 앞서 닫힌 배열에서 다룬 `items: false` 형태와 동등하며, 같은 방식으로 작성되고 별도의 구두점도 필요 없습니다. 이 섹션은 서로 다른 모양(그리고 다소 어색하게 쓰인)의 이런 스키마들이 결국 닫힌 배열로 귀결된다는 것을 보여주기 위해서만 존재합니다.

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 4,
  "maxItems": 4,
  "items": { "type": "number" }
}
```

```jssn
[bool, str, int, num]
```

또는

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 4,
  "maxItems": 4,
  "items": true
}
```

```jssn
[bool, str, int, any]
```

> `any`는 여기서 명시적으로 작성해야 합니다 — 이는 배열의 한 자리이며, 배열 내부에서는 `any` 생략이 적용되지 않습니다 ([types.ko.md](types.ko.md) 참고).

## 흔치 않은 배열

아래 섹션들은 의도된 경우가 드문 결과를 다룹니다. 대부분의 독자는 이 섹션을 건너뛰어도 됩니다.

JSON Schema는 `minItems`와 `maxItems`가 음이 아닌 정수여야 한다는 것만 요구합니다 — 둘 중 하나만 있어도 유효합니다. 하지만 둘을 함께 쓰거나 `prefixItems`/`items`와 함께 쓰면, 일부 조합은 앞뒤가 맞지 않는 배열 형태를 나타내게 됩니다.

유효한 부분만 조용히 렌더링하는 대신, jssn은 이런 조합을 `;;`로 드러내어, 원본 JSON Schema가 실수로 작성되었을 가능성을 저자에게 경고합니다. 배열의 일부가 유효하지 않은 경우, 가독성을 위해 해당 타입 앞에 `-`를 붙입니다.

jssn 배열에 `;;`가 포함되어 있다면, 그 원본 JSON Schema는 아마도 실수일 것입니다.

### 도달할 수 없는 요소

`prefixItems`는 배열의 길이가 절대 도달할 수 없는 인덱스에 대한 타입을 선언할 수도 있습니다.

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "maxItems": 2
}
```

여기서 인덱스 2는 `integer` 타입이지만, `maxItems: 2` 때문에 이는 무의미합니다. jssn은 이를 `;;`로 표시해, 실제 길이는 2이고 그 이후는 모두 버려진다는 것을 보여줍니다. 원래 그 앞에 와야 할 `,`는 생략됩니다.

```jssn
[bool, str;; -int]
```

또는

```jssn
[
  bool
  str;;
  -int
]
```

`;;`는 선택적으로 존재하는 요소에서 다룬 `;`와 같은 문자를 재사용하기 때문에 헷갈릴 수 있습니다. 다음 JSON Schema는 결과 표기법을 더 예측하기 쉽게 해줍니다:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" },
    { "type": "integer" }
  ],
  "minItems": 1,
  "maxItems": 3
}
```

jssn은 이를 다음과 같이 씁니다:

```jssn
[bool; str, int;; -int]
```

또는

```jssn
[
  bool;
  str
  int;;
  -int
]
```

`minItems`와 `maxItems`가 같고, `prefixItems`가 둘 다보다 긴 경우:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" },
    { "type": "integer" }
  ],
  "minItems": 2,
  "maxItems": 2
}
```

jssn은 `minItems`가 만들어낼 `;`를 생략합니다. 이는 `;;`와 정확히 같은 위치에 놓이게 되기 때문입니다:

```jssn
[bool, str;; -int, -int]
```

또는

```jssn
[
  bool
  str;;
  -int
  -int
]
```

### 뒤집힌 배열

`minItems`가 `maxItems`보다 큰 경우를 생각해봅시다: 어떤 배열도 이런 스키마를 만족할 수 없습니다. 그럼에도 jssn은 원래 실수의 형태가 계속 보이도록, 단순한 `[]`보다 더 풍부한 표기법을 사용합니다.

`;`는 `minItems`가 가리키는 위치에, `;;`는 `maxItems`가 가리키는 위치에 놓입니다 — 도달할 수 없는 요소에서와 같은 규칙입니다. 그곳에서는 `minItems <= maxItems`였기 때문에 `;`가 `;;`보다 앞에 왔지만, 여기서는 정의상 `minItems > maxItems`이므로 두 표시가 값 순서대로 놓이며 `;;`가 항상 먼저 옵니다. 그리고 이 스키마는 어떤 배열도 만족할 수 없으므로, 모든 요소와 토큰에 `-` 접두사가 붙습니다 — `;;` 앞의 요소들도 포함해서입니다. 도달할 수 없는 요소에서는 그 앞부분이 여전히 도달 가능했던 것과 다릅니다.

`minItems`가 `prefixItems`의 끝을 넘어서는 경우, 그 초과분은 실제 `prefixItems` 요소가 아니라 가상 슬롯이므로 열린 배열 표기법을 재사용합니다: 초과 슬롯이 하나라면 정확히 하나의 요소만큼 확장하기에서처럼 단독 타입(또는 `any`)으로 씁니다; 초과 슬롯이 둘 이상이라면 최소 개수가 제한된 후행 요소의 `(count)..` 표기법을 재사용합니다(주어진 타입이 없으므로 뒤에 타입은 붙지 않습니다). `;`가 표기법의 맨 마지막 위치에 놓일 때는 그 뒤에 아무것도 오지 않습니다 — 후행 `;`로 나타납니다.

두 값이 모두 `prefixItems`의 길이보다 작은 예를 봅시다:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" },
    { "type": "integer" }
  ],
  "minItems": 3,
  "maxItems": 2
}
```

`minItems`는 `maxItems`보다 1 큽니다. 이는 다음과 같이 씁니다:

```jssn
[-bool, -str;; -int; -int]
```

`;;`는 `maxItems`(2)가 가리키는 위치 — 두 번째 요소 뒤 — 에 놓이고, `;`는 `minItems`(3)가 가리키는 위치 — 세 번째 요소 뒤 — 에 놓입니다. `;;`가 `;`보다 앞에 오며, 여기서는 어떤 인덱스도 `prefixItems`의 길이(4)를 넘지 않으므로 가상 슬롯이 필요하지 않습니다.

이번에는 `minItems`가 `prefixItems`의 길이보다 1 크고, `maxItems`는 그보다 작은 예를 봅시다:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" },
    { "type": "integer" }
  ],
  "minItems": 5,
  "maxItems": 2
}
```

```jssn
[-bool, -str;; -int, -int, -any;]
```

`minItems`(5)는 `prefixItems`의 길이(4)보다 1 크므로 — 정확히 하나의 요소만큼 확장하기에서와 마찬가지로 — 초과 슬롯 하나가 `(count)..` 표기법 없이 단독 타입으로 덧붙습니다. `items`가 지정되어 있지 않으므로 타입은 `any`이며, 스키마가 충족 불가능하므로 `-`가 붙습니다. `minItems`의 위치가 표기법의 맨 끝과 겹치므로, `;`는 `-any` 뒤에 붙습니다.

`minItems`가 `prefixItems`의 길이보다 2 이상 큰 경우:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" },
    { "type": "integer" }
  ],
  "minItems": 7,
  "maxItems": 1
}
```

```jssn
[-bool;; -str, -int, -int, -3..;]
```

`minItems`(7)는 `prefixItems`의 길이(4)보다 3 크므로, 초과 슬롯이 둘 이상일 때의 규칙에 따라 최소 개수가 제한된 후행 요소의 `(count)..` 표기법을 `3..`으로 재사용하며 `-`를 붙입니다. 여기서도 `minItems`의 위치가 표기법의 끝과 겹치므로, `;`는 맨 끝에 붙습니다.

### 설계 노트

흔치 않은 배열 — 특히 그중에서도 충족 불가능한 것들 — 은 검증 단계에서 걸러내고, 임의의 표기법을 채택해 잘못된 입력으로 표시할 수도 있었을 것입니다. 하지만 현재로서는 jssn이 정보 손실 없이 JSON Schema를 그대로 반영하는 것을 목표로 하는 표기법이며, 이를 위한 컨버터는 검증을 수행하지 않는 것으로 간주됩니다.
