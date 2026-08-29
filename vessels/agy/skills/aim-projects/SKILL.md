---
name: aim-projects
description: Interacts with the GitHub Projects kanban board natively using the `gh` CLI on Windows.
---
# `aim-projects`

> **MANDATE:** Use the native GitHub CLI (`gh`) to read and update the shared Kanban board (the source of truth for multi-agent work). Never invent board state offline.

## PREREQUISITES
The host must have the project scope authorized. If any commands fail with scope errors, instruct the operator to run:
`gh auth refresh -s project,read:project`

Configuration required (fetch these from environment or operator):
- `AIM_PROJECTS_OWNER` (e.g., `@me` or an org name)
- `AIM_PROJECTS_NUMBER` (e.g., `5`)

## 1. See the Board (List Items)
To view the current kanban state, you must list the items in the project:
```powershell
gh project item-list <PROJECT_NUMBER> --owner <OWNER> --format json
```
*Note: Parsing the JSON output is required to find specific Issue Item IDs and their current statuses.*

## 2. Claim Work (In Progress)
Before coding, you MUST claim the issue so other agents share the same page.
To update an item's status, you need the Project ID, Item ID, the ID of the Status field, and the Option ID for the specific status.
1. Fetch Project ID: `gh project view <PROJECT_NUMBER> --owner <OWNER> --format json`
2. Fetch Field ID and Option IDs for "Status": `gh project field-list <PROJECT_NUMBER> --owner <OWNER> --format json`. Parse the JSON to find the `id` of the "Status" field and the `id` of the specific status option (e.g. "In progress", "Done") within its `options` array.
3. Update Status using the single-select-option-id flag: 
   ```powershell
   gh project item-edit --id <ITEM_ID> --field-id <STATUS_FIELD_ID> --project-id <PROJECT_ID> --single-select-option-id <OPTION_ID>
   ```

## 3. Ship (Done)
After your PR is shipped or the branch is promoted via `aim-gitops`, you must move the issue to Done:
```powershell
gh project item-edit --id <ITEM_ID> --field-id <STATUS_FIELD_ID> --project-id <PROJECT_ID> --single-select-option-id <DONE_OPTION_ID>
```

## 4. Blocked
When waiting on the Operator, DNS changes, or external factors:
```powershell
gh project item-edit --id <ITEM_ID> --field-id <STATUS_FIELD_ID> --project-id <PROJECT_ID> --single-select-option-id <BLOCKED_OPTION_ID>
```
