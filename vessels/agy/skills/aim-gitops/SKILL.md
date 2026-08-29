---
name: aim-gitops
description: Automates the strict GitOps worktree and TDD workflow (formerly `aim fix` and `aim promote`) natively using PowerShell and git.
---
# `aim-gitops`

> **MANDATE:** Use this skill to spawn isolated git worktrees for development (fixing bugs/issues) and for promoting those changes back to the main branch natively on Windows. You are strictly bound by the rules of Surgical Staging and Test-Driven Development (TDD).

## 1. Spawning the Sandbox (The `fix` operation)
When assigned a task or issue (e.g., issue 42), do NOT perform development directly on `main`.
1. Ensure you are at the repository root.
2. Execute the native git worktree command: 
   `git worktree add -b fix/issue-42 workspace/issue-42`
3. **CRITICAL:** Change your working directory (`Cwd`) for all subsequent coding and testing to `workspace/issue-42`. Do not pollute the root repository.

## 2. Test-Driven Development (TDD)
While operating in your sandbox:
1. Write tests before or alongside your implementation.
2. **Empirical Proof:** You must prove the code works by running the test suite in your worktree. Never rely on blind output.
3. Do not proceed to staging or promotion until tests pass.

## 3. Surgical Staging
When preparing to commit your work:
1. **Never use `git add .` blindly.** 
2. Use `git status` to identify modified files.
3. Explicitly stage only the specific files necessary for the fix using `git add <file_path>`. This prevents localized test artifacts or scratch files from polluting the commit.
4. Commit with a descriptive message.

## 4. The Teardown (The `promote` operation)
Once your code is empirically proven to work (TDD) and surgically committed:
1. Return your working directory to the root of the repository.
2. To cleanly merge the worktree into the main branch, archive the previous main state, and tear down the worktree, run this exact sequence in PowerShell:
   ```powershell
   git checkout main
   
   # Archive the current main state for safety
   $archiveBranch = "archive/main-$(Get-Date -Format 'yyyyMMddHHmmss')"
   git branch $archiveBranch
   
   # Safely merge your fix
   git merge fix/issue-42
   
   # Cleanly delete the isolated workspace
   git worktree remove workspace/issue-42
   git branch -d fix/issue-42
   ```
3. After teardown, notify the operator that the promotion is complete.
