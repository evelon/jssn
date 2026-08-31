# 변경 이력

이 파일은 JSSN 명세(spec/)에 대한 주요 변경 사항을 기록합니다. 컨버터(converter)는 독립적으로 버전이 관리되는 별도의 CHANGELOG.md를 유지합니다.

형식은 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)를 기반으로 하며, 이 프로젝트는 [Semantic Versioning](https://semver.org/)을 따릅니다.

## [0.5.2] - 2026-08-31

### 추가됨 (Added)

- `boolean-logic.md`에 기존 `unevaluatedProperties` 내용과 함께 `unevaluatedItems` 내용을 추가했습니다. 관련 섹션 제목을 "Closed Objects and `&`"에서 "Closed Collections and `&`"로 변경했습니다: 배열도 객체와 마찬가지로 `&` 아래에서 기본적으로 닫히며, `& [...]`로 명시적으로 다시 열 수 있습니다. 중첩된 `unevaluatedItems: true`가 바깥쪽 `false`에 의해 덮어써지는 사례에 대한 주의 사항도 함께 다루며, JSON Schema → JSSN 컨버터가 각 `allOf` 분기를 독립적으로 변환하는 대신 이를 감지하고 반영해야 하는 이유를 설명합니다

## [0.5.1] - 2026-08-31

### 변경됨 (Changed)

- 필수/선택 속성 표기법을 뒤집었습니다: 이제 속성은 기본적으로 필수이며, `?`(`!`가 아님)가 속성을 선택으로 표시합니다 — 이전 기본값의 정반대입니다. 이렇게 하면 필수/선택 표기가 JSSN이 이미 JSON Schema의 "기본적으로 열림"을 "기본적으로 닫힘"으로 뒤집은 나머지 두 곳(배열 요소, `additionalProperties`)과 일관성을 갖게 되고, 더 치명적인 실수(의도치 않게 선택이 되어버린 속성)를 눈에 띄는 `?`로 드러나게 하며, 이전의 놓치기 쉬운 실수(빠뜨린 `!`)를 방지합니다. `object.md`, `boolean-logic.md`, `references.md` 전반의 모든 예제를 이에 맞게 업데이트했습니다.

## [0.5.0] - 2026-08-31

### 추가됨 (Added)

- 새로운 `references.md`에 재사용 가능한 스키마와 참조를 추가했습니다: `$defs`를 선언하는 `defs < ... >`; 세 가지 참조 형식 — 가장 가까운 참조(`$name`), 절대 경로(`#$name`, 루트 밖의 defs의 경우 `#path.to$name`), 원본 JSON Pointer(`#/$defs/...`); `$anchor`; 루트 참조(`#`); 자기 참조/상호 재귀적인 defs

## [0.4.0] - 2026-08-31

### 추가됨 (Added)

- 새로운 `boolean-logic.md`에 불리언 로직 조합자를 추가했습니다: `&`(`allOf`), `|`(`anyOf`), `^(...)`(`oneOf`), `~`(`not`); 연산자 종류를 섞어 쓸 때는 이들 사이에 정의된 우선순위가 없으므로 괄호가 필요합니다

## [0.3.0] - 2026-08-25

### 추가됨 (Added)

- 객체 문법: `additionalProperties`(단독 `...` / `...: type`), `patternProperties`(`/regex/: type`), `minProperties`/`maxProperties`(`(min..max) {`)

### 변경됨 (Changed)

- `required.md`의 내용을 `object.md`에 병합하여, 객체 문법(필수/선택 속성, `additionalProperties`, `patternProperties`, `minProperties`/`maxProperties`)이 한 파일에 모이도록 했습니다; `required.md`는 삭제되었습니다
- `tuple-length.md`를 `array.md`로 이름을 바꾸고, "tuple" 용어를 전체적으로 "array"로 대체했습니다. 이 파일은 길이만 다루는 데서 그치지 않고 배열 문법 전체에 대한 참고 자료로 성장할 예정이기 때문입니다
- `array.md`는 이제 배열 요소 구분 규칙(한 줄에서는 쉼표, 여러 줄에서는 줄바꿈만으로 구분)을 `types.md`를 통하지 않고 직접 명시합니다

## [0.2.0] - 2026-08-22

### 추가됨 (Added)

- 튜플 길이 문법: 열린/닫힌 튜플(`...type` / 단독 `...`), 제한된 후행 요소, 튜플을 정확히 하나의 요소만큼 확장하는 방법, 도달할 수 없는 요소나 뒤집힌(inside-out) 튜플 같은 엣지 케이스
- `json-schema-reference.md`: JSON Schema Draft 2020-12의 핵심 키워드를 정리한 체크리스트로, JSSN 자체 로드맵의 범위를 정하는 데 사용됩니다

### 변경됨 (Changed)

- 기능 문서(`types.md`, `required.md`, `tuple-length.md`)가 이제 명세 수준 문서(`README.md`, `indentation.md`, `json-schema-reference.md`)와 분리되어 `spec/features/` 아래에 위치합니다
- `types.md`의 Array 섹션이 이제 items 관련 전체 명세를 위해 `tuple-length.md`를 가리킵니다

## [0.1.1] - 2026-08-16

### 추가됨 (Added)

- 필수 및 선택 속성 문법: 키 이름 뒤에 `!`를 붙이면 필수를 의미하며, 속성은 기본적으로 선택입니다
- 타입 제약이 없는 값을 위한 `any` 타입 — `properties`에 대응 항목이 없지만 필수인 키의 경우를 다룹니다

### 변경됨 (Changed)

- 명세를 기능별로 하나의 문서(`types.md`, `required.md`)로 분리하고, `README.md` 색인과 로드맵을 추가했습니다
- 각 기능 문서(및 관련 하위 섹션)가 이제 대응하는 JSON Schema 키워드나 요소를 명시합니다

## [0.1.0] - 2026-08-16

### 추가됨 (Added)

- 들여쓰기 권장 사항
- 기본 타입 규칙

[0.5.2]: https://github.com/evelon/jssn/compare/spec-v0.5.1...spec-v0.5.2
[0.5.1]: https://github.com/evelon/jssn/compare/spec-v0.5.0...spec-v0.5.1
[0.5.0]: https://github.com/evelon/jssn/compare/spec-v0.4.0...spec-v0.5.0
[0.4.0]: https://github.com/evelon/jssn/compare/spec-v0.3.0...spec-v0.4.0
[0.3.0]: https://github.com/evelon/jssn/compare/spec-v0.2.0...spec-v0.3.0
[0.2.0]: https://github.com/evelon/jssn/compare/spec-v0.1.1...spec-v0.2.0
[0.1.1]: https://github.com/evelon/jssn/compare/spec-v0.1.0...spec-v0.1.1
[0.1.0]: https://github.com/evelon/jssn/releases/tag/spec-v0.1.0
