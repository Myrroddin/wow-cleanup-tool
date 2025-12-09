# Sapling Box Style Debug Checklist

## Pass/Fail Checklist for Box Style

| Test Case / Feature                        | Pass | Fail | Notes |
|--------------------------------------------|------|------|-------|
| 1. Indentation: Children under parent      |      |   X  | file1, file2, file6, file7 not indented   |
| 2. Expander: [+]/[-] toggles correctly     |      |   X  | Only the root, game folder, works correctly    |
| 3. Checkbox: Parent tick selects children  |      |   X  | Only the root, game folder, works correctly    |
| 4. Checkbox: Visual feedback updates       |      |   X  | Only the root, game folder, works correctly    |
| 5. Collapse/Expand preserves selection     |  X   |      |       |
| 6. Node label displays correctly           |  X   |      |       |
| 7. Debug prints show only box style info   |  X   |      |       |
| 8. No debug prints for other styles        |  X   |      |       |
| 9. Node positions map correctly            |      |  X   |       |
| 10. No exceptions on rapid expand/collapse |  X   |      |       |

## Usage
- Mark Pass/Fail for each test after running Sapling.
- Add notes for any issues or observations.
- Update checklist as features/bugs are added or resolved.

---
Last updated: 2025-12-09
