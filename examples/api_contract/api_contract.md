# API Contract (REST Payload Example)

이 예시는 **REST API request/response 계약(contract)** 을 JSSN으로 표현한 예시다.

- Request / Response payload
- ErrorResponse 표준화
- Pagination
- query object (선택 필드 + open object)
- enum / format / 길이/범위 제약

> `ApiContract`는 “예제 묶음”을 위해 만든 루트 schema다. 실제 사용에서는 endpoint별로 entry를 나누거나, 한 entry에서 components처럼 참조해도 된다.

---

## Files

- `api_contract.jssn`: JSSN 원본
- (선택) `api_contract.schema.json`: JSON Schema 생성 결과를 넣고 싶으면 나중에 추가

---

## JSON Examples

### 1) POST /users — CreateUserRequest

```json
{
  "email": "alice@example.com",
  "name": "Alice"
}
```

### 2) 201 Created — CreateUserResponse

```json
{
  "user": {
    "id": "d64b7c7e-61a7-4a19-9f9e-6c8b2b0f4f2e",
    "email": "alice@example.com",
    "name": "Alice",
    "status": "ACTIVE",
    "created_at": "2026-02-05T13:22:10Z"
  }
}
```

### 3) ErrorResponse (example)

```json
{
  "error": {
    "code": "INVALID_ARGUMENT",
    "message": "email is invalid",
    "request_id": "req_01HZYQ8F6T0WQ1YQW8FQ2W7K3Z",
    "details": {
      "field": "email"
    }
  }
}
```

### 4) GET /users — ListUsersQuery (as JSON-like object)

> 실제 HTTP querystring이지만, 여기서는 스키마/타입 관점에서 object로 예시를 든다.

```json
{
  "page": 1,
  "page_size": 20,
  "status": "ACTIVE",
  "sort": {
    "by": "created_at",
    "order": "DESC"
  }
}
```

### 5) 200 OK — ListUsersResponse

```json
{
  "users": [
    {
      "id": "11111111-1111-4111-8111-111111111111",
      "email": "alice@example.com",
      "name": "Alice",
      "status": "ACTIVE",
      "created_at": "2026-02-05T13:22:10Z"
    },
    {
      "id": "22222222-2222-4222-8222-222222222222",
      "email": "bob@example.com",
      "name": "Bob",
      "status": "SUSPENDED",
      "created_at": "2026-02-05T13:30:00Z",
      "updated_at": "2026-02-05T14:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 2,
    "total_pages": 1
  }
}
```

## **Notes**

- object는 기본적으로 closed(`additionalProperties: false`)로 emit되는 것이 목표다. 필요한 곳에서만 ...로 open.
- `ErrorResponse.error.details`는 `*: str` + `...`로 “키는 자유, 값은 string” 패턴을 표현했다.
- query는 실제로는 querystring이지만, 타입 레벨에선 object로 정의하는 편이 구현/검증에 유리하다.
