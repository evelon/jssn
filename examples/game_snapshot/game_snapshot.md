# Game Snapshot (JSSN Example)

이 폴더는 **JSSN v0.2**로 작성한 `game_snapshot.jssn` 예시를 보여준다.

- 목적: 게임 진행 상태를 한 번에 내려주는 **snapshot payload**를 스키마로 정의
- 포인트: nested object, `$defs/$ref` 재사용 타입, enum, optional(`?`) 필드, 배열/오브젝트 조합

> 참고: `vote_meta` / `vote_result`는 optional이다.

---

## Files

- `game_snapshot.jssn`: JSSN 원본 스키마
- `game_snapshot.schema.json`: 생성된 JSON Schema (draft 2020-12)

---

## JSON Example

아래는 `schema GameSnapshot`에 맞는 **실제 JSON 예시**다.

```json
{
  "schema_version": 1,
  "case_state": {
    "case_id": "d64b7c7e-61a7-4a19-9f9e-6c8b2b0f4f2e",
    "status": "RUNNING",
    "round_no": 2
  },
  "phase_state": {
    "phase_id": "2f0e6a8a-4c0a-4b6b-9a0c-9f5f4e1e9c0b",
    "type": "VOTE",
    "round": 2,
    "opened_at": "2026-02-05T13:22:10Z"
  },
  "players": [
    {
      "id": "e1b6b3d9-3b1c-4b2a-9f0e-6c6a0c0b8f11",
      "seat": 0,
      "name": "Alice",
      "life": "ALIVE"
    },
    {
      "id": "a3a0b6b4-1f61-4d74-8a62-4b4c4c24f7a2",
      "seat": 1,
      "name": "Bob",
      "life": "ALIVE"
    },
    {
      "id": "7f0a3c7d-8a19-4d0b-9f3c-2c2b9a4a91d1",
      "seat": 2,
      "name": "Chloe",
      "life": "DEAD",
      "eliminated": true
    }
  ],
  "vote_meta": [
    {
      "type": "RED",
      "from": 0,
      "to": 1,
      "weight": 1
    },
    {
      "type": "RED",
      "from": 1,
      "to": 0,
      "weight": 1
    },
    {
      "type": "BLUE",
      "from": 0,
      "to": 2,
      "weight": 2
    }
  ],
  "vote_result": {
    "vote_type": "BLUE",
    "targeted": 2,
    "executed": true
  }
}
```

---

## Additional Examples

### 1. DISCUSS phase (no vote yet)

투표 단계 이전의 스냅샷 예시. `vote_meta`와 `vote_result`가 없다.

```json
{
  "schema_version": 1,
  "case_state": {
    "case_id": "a0a1f9d2-4d71-4d87-8c55-5d9d7a6a9b0c",
    "status": "RUNNING",
    "round_no": 1
  },
  "phase_state": {
    "phase_id": "b1e8c90f-9b0f-4d91-9f1d-8a7d6c2e8f1a",
    "type": "DISCUSS",
    "round": 1,
    "opened_at": "2026-02-05T12:00:00Z"
  },
  "players": [
    {
      "id": "11111111-1111-4111-8111-111111111111",
      "seat": 0,
      "name": "Alice",
      "life": "ALIVE"
    },
    {
      "id": "22222222-2222-4222-8222-222222222222",
      "seat": 1,
      "name": "Bob",
      "life": "ALIVE"
    },
    {
      "id": "33333333-3333-4333-8333-333333333333",
      "seat": 2,
      "name": "Chloe",
      "life": "ALIVE"
    }
  ]
}
```

---

### 2. NIGHT phase with minimal players

플레이어 수가 적고, 아직 투표 정보가 없는 NIGHT 단계.

```json
{
  "schema_version": 1,
  "case_state": {
    "case_id": "9f8c2d11-5a2a-4c3e-90df-01c6d0fbc9e2",
    "status": "RUNNING",
    "round_no": 0
  },
  "phase_state": {
    "phase_id": "8b5a2f8e-33d9-4c54-a1f7-0b6c2f9e7a11",
    "type": "NIGHT",
    "round": 0,
    "opened_at": "2026-02-05T11:30:00Z"
  },
  "players": [
    {
      "id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
      "seat": 0,
      "name": "Host",
      "life": "ALIVE"
    }
  ]
}
```

---

### 3. Game ended snapshot

게임이 종료된 상태. `case_state.status = ENDED`.

```json
{
  "schema_version": 1,
  "case_state": {
    "case_id": "55c3e8f4-2e3a-4f8b-8c11-2d6a9e7b1c00",
    "status": "ENDED",
    "round_no": 4
  },
  "phase_state": {
    "phase_id": "7c1d9e11-44b0-4a8e-9b88-0b0e1d2c3f44",
    "type": "VOTE",
    "round": 4,
    "opened_at": "2026-02-05T14:00:00Z"
  },
  "players": [
    {
      "id": "abcdabcd-abcd-4abc-8abc-abcdabcdabcd",
      "seat": 0,
      "name": "Alice",
      "life": "ALIVE"
    },
    {
      "id": "dcbaabcd-abcd-4abc-8abc-dcbaabcdabcd",
      "seat": 1,
      "name": "Bob",
      "life": "DEAD",
      "eliminated": true
    }
  ],
  "vote_result": {
    "vote_type": "RED",
    "targeted": 1,
    "executed": true
  }
}
```

---

## Invalid Example

아래 JSON은 **JSSN 스키마 기준 invalid** 예시다.

이 예시에서는 `seat` 값이 허용 범위(0..7)를 벗어나므로 validation에 실패해야 한다.

```json
{
  "schema_version": 1,
  "case_state": {
    "case_id": "d64b7c7e-61a7-4a19-9f9e-6c8b2b0f4f2e",
    "status": "RUNNING",
    "round_no": 1
  },
  "phase_state": {
    "phase_id": "2f0e6a8a-4c0a-4b6b-9a0c-9f5f4e1e9c0b",
    "type": "DISCUSS",
    "round": 1,
    "opened_at": "2026-02-05T13:22:10Z"
  },
  "players": [
    {
      "id": "e1b6b3d9-3b1c-4b2a-9f0e-6c6a0c0b8f11",
      "seat": 12,
      "name": "Alice",
      "life": "ALIVE"
    }
  ]
}
```

### Why invalid?

- `seat` must be between **0 and 7** (inclusive)
- value `12` violates the `SeatNo = int(0..7)` constraint
