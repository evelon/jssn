# Git Convention

## Commit Convention

type(scope): subject

### Type

- feat: Add a new feature (including writing spec docs for new features)
- fix: Bug fix
- docs: Add or improve documentation/explanations for existing content
- refactor, test, chore ...

### Scope

- spec: Spec documents
- conv: Converter program
- (optional) Omit the scope when modifying files in the root directory

### Examples

feat(spec): Write spec for OO feature
feat(conv): Add JSON→XML conversion logic
docs(spec): Improve existing spec explanation

## Branch Naming Convention

`<type>-<scope>/<subject>`, matching the scopes above.

- Branches related to spec: `feat-spec/object-notation`, `docs-spec/...`, `fix-spec/...`, ...
- Branches related to the converter: `feat-conv/...`, `docs-conv/...`, `fix-conv/...`, ...
- Otherwise (no scope): `feat/...`, `docs/...`, `fix/...`, ...

## PR Convention

- Write PR titles and descriptions in English by default.
- If you also want Korean, write English first, then Korean below it (bilingual, English on top).

### Example

```
Add spec for object type

---

object 타입에 대한 스펙을 추가합니다.
```
