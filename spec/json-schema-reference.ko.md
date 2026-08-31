# JSON Schema — 핵심 문법 참고 자료

이 문서는 실무에서 필수적이라고 여겨지는 JSON Schema 키워드를 정리한 참고용 체크리스트입니다. JSSN 설계의 배경이 되는 자료로, JSSN이 앞으로 축약 표현을 제공하고자 하는 목표 목록이지 JSSN 자체를 설명하는 문서는 아닙니다.

JSSN은 **JSON Schema Draft 2020-12**를 대상으로 하므로([프로젝트 README](../README.ko.md) 참고), 아래 섹션들은 2020-12 문법을 설명합니다. 2020-12에서 이름이 바뀌거나 대체된 이전 드래프트의 키워드는, JSSN의 목표 대상이 아니라 참고용으로 알아볼 수 있도록 문서 맨 끝에 따로 모아두었습니다.

## 기본 구조

- `$schema` — 문서가 어떤 드래프트/dialect를 따르는지 선언합니다
- `$id` — 스키마 자신의 식별자
- `type` — 기본 타입 제약 (`string`, `number`, `integer`, `boolean`, `object`, `array`, `null`)

## 객체 검증

- `properties` — 키별 스키마
- `required` — 반드시 존재해야 하는 키의 배열
- `additionalProperties` — `properties`에 나열되지 않은 속성을 허용할지, 허용한다면 어떤 스키마로 허용할지
- `patternProperties` — 정규 표현식에 매칭되는 키에 대한 스키마
- `minProperties` / `maxProperties` — 속성 개수의 상한/하한

## 배열 검증

- `items` — 모든 배열 요소(또는 `prefixItems`도 있는 경우 `prefixItems`가 다루는 위치 이후의 모든 요소)를 제약하는 단일 스키마
- `prefixItems` — 위치 기반(튜플) 요소 스키마
- `minItems` / `maxItems` — 배열 길이의 상한/하한
- `uniqueItems` — 중복 요소 금지
- `contains` — 최소 하나의 배열 요소가 이 스키마를 만족해야 함
- `minContains` / `maxContains` — `contains`를 만족해야 하는 요소 개수의 상한/하한 (기본값: 최소 1개, 상한 없음)

## 값 제약

- `minLength` / `maxLength` / `pattern` — 문자열 제약
- `minimum` / `maximum` / `exclusiveMinimum` / `exclusiveMaximum` / `multipleOf` — 숫자 제약
- `enum` — 값이 고정된 값 집합 중 하나여야 함
- `const` — 값이 특정한 하나의 고정 값과 일치해야 함
- `format` — 잘 알려진 문자열 형식 (예: `email`, `date-time`, `uri`); 명세상 권고 사항이며, 검증기(validator)가 항상 강제하지는 않습니다

## 조합자

- `allOf` / `anyOf` / `oneOf` / `not` — 스키마 조합
- `if` / `then` / `else` — 조건부 검증

## 재사용

- `$defs` — 재사용을 위한 이름 있는 하위 스키마
- `$ref` — 스키마에 대한 참조로, 보통 `$defs` 아래에 정의된 것을 가리킵니다

## 문서화 / 어노테이션 키워드

- `title` / `description` — 검증에 관여하지 않는 문서화용 정보
- `default` — 값이 주어지지 않았을 때 사용할 값; 문서화 목적일 뿐이며, 검증기가 자동으로 주입하지는 않습니다
- `examples` — 예시 값; 문서화 목적일 뿐이며 강제되지 않습니다

## 관계형 / 조건부 요구 사항

- `dependentRequired` — "키 A가 존재하면 키 B도 존재해야 한다"
- `dependentSchemas` — "키 A가 존재하면 인스턴스 전체가 이 스키마도 만족해야 한다"

## 2020-12 드래프트에 속하지 않는 것 (이전 드래프트 문법)

이 항목들은 이전 드래프트(주로 Draft 7)에서 온 것으로, 2020-12에 이르러 이름이 바뀌거나 대체되었습니다. JSSN 자체 문법의 목표 대상은 아니지만, 실제로 작성된 JSON Schema 중 여전히 이를 사용하는 것이 많으므로 참고용으로 여기 나열합니다.

- 스키마의 배열로 쓰인 `items` — 위치 기반(튜플) 검증을 작성하던 Draft 7의 방식이며, 2020-12에서 `prefixItems`로 대체되었습니다
- `additionalItems` — 튜플 이후의 요소를 제약하던 Draft 7의 동반 키워드이며, 2020-12에서 (단일 스키마인) `items`로 대체되었습니다
- `definitions` — 재사용 가능한 하위 스키마를 가리키던 Draft 7의 이름이며, draft 2019-09부터 `$defs`로 이름이 바뀌었습니다
- `dependencies` — "A가 존재하면 B도 존재해야 한다"와 "A가 존재하면 이 스키마를 만족해야 한다"를 모두 다루던 Draft 7의 단일 키워드이며, draft 2019-09부터 `dependentRequired`와 `dependentSchemas`로 분리되었습니다
