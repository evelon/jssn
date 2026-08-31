# JSSN 명세

이 디렉터리는 JSSN 명세를 기능별로 하나의 문서로 정리하여 담고 있습니다. JSSN에 대한 개요는 [프로젝트 README](../README.ko.md)를 참고하세요.

JSSN의 명세는 **JSON Schema Draft 2020-12**를 대상으로 합니다. 이전 드래프트(Draft 7 / 2019-09)와 문법이 다른 경우, 해당 문서에서 2020-12 형식과 함께 이전 드래프트에서의 동등한 표현을 함께 설명합니다.

## 문서

- [indentation.ko.md](./indentation.ko.md) — 들여쓰기 권장 사항
- [json-schema-reference.ko.md](./json-schema-reference.ko.md) — JSON Schema의 핵심 문법을 정리한 참고용 체크리스트로, JSSN 자체 로드맵의 범위를 정하는 데 사용됩니다

### 기능

- [types.ko.md](./features/types.ko.md) — 기본 타입 이름과 배열/객체 문법
- [array.ko.md](./features/array.ko.md) — 배열 길이와 열린/닫힌 배열 문법 (`items`, `prefixItems`, `minItems`, `maxItems`)
- [object.ko.md](./features/object.ko.md) — 객체 문법: 필수/선택 속성(`?` 접미사), `additionalProperties`, `patternProperties`, `minProperties`/`maxProperties`
- [boolean-logic.ko.md](./features/boolean-logic.ko.md) — `&`(`allOf`), `|`(`anyOf`), `^(...)`(`oneOf`), `~`(`not`)
- [references.ko.md](./features/references.ko.md) — 재사용 가능한 스키마(`defs < ... >`)와 참조 문법: 가장 가까운 참조(`$name`), 절대 경로(`#$name`), `$anchor`

## 문서 작성 규칙

각 기능 문서는 제목 바로 아래(그리고 관련된 하위 섹션 아래에도)에 `> **JSON Schema 대응:** ...` 형식의 인용구를 사용해, 해당 문법이 대응하는 JSON Schema 키워드나 요소를 표시합니다.

## 로드맵 (아직 다루지 않음)

- 유니온 타입 / nullable 값
- `enum` / `const`
- 문자열, 숫자, 배열 값 제약 조건 (`minLength`, `pattern`, `minimum`, `maximum`, `uniqueItems`, `contains`/`minContains`/`maxContains`, `propertyNames` 등)
- `$dynamicRef`/`$dynamicAnchor`
- `if`/`then`/`else` (조건부 검증)
- 관계형/조건부 필수 속성 (JSON Schema의 `dependentRequired`/`dependentSchemas`에 해당)
- `default` / `examples`
