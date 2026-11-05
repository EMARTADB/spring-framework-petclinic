# PR Publisher Context — spring-framework-petclinic

## Platform Details

Version Control Platform: GitHub (Pull Request terminology). Repository: `EMARTADB/spring-framework-petclinic` (remote `origin`, git@github.com:EMARTADB/spring-framework-petclinic.git). CLI: `gh`. Authentication: token-based via `gh auth` (git operations over SSH).

## Base Branch

base_branch: main

## CLI Check Command

Command to check if Version Control Platform CLI is properly installed and configured:

vcp_check_command: gh pr list

## PR Check Command

Command to verify whether an open PR already exists for the change branch:

pr_check_command: gh pr list --head {head} --state open --json url --jq '.[].url'

### Command Placeholders
- `{head}` — source branch of the change. Output is a list of PR URLs (empty means no open PR).

## PR Create Command

Command to open a new pull request:

pr_create_command: gh pr create --base {base} --head {head} --title "{title}" --body-file {body_file}

### Command Placeholders
- `{base}` — target base branch (`main` by default)
- `{head}` — source branch
- `{title}` — PR title (max 72 characters)
- `{body_file}` — temporary file (under `.ai-native-config/tmp/`) holding the PR body markdown; equivalent to `--body "{body}"` (`{body}` = PR description). Use the file for multiline markdown to avoid quoting issues, and remove it afterwards.

## Additional Context

- **VCP Platform**: GitHub
- **Repository**: EMARTADB/spring-framework-petclinic
- **CLI Tool**: gh
- **CLI Version**: 2.103.0
- **Authentication Type**: Token (OAuth, scopes gist/read:org/repo), SSH for git operations

## Extract Command Information

For commands retrieving repository or PR information use `--json url --jq '.[].url'` and interpret output as PR URLs.

## Notes (Content Standards)

- Do not generate title or body content; use the supplied `{title}` and `{body}`.
- Do not add default reviewers or labels; add them only when explicitly configured.
