# CLAUDE.md

Guidance for AI agents (and humans) working in this repository.

ELFWS (EDA Log File Warning Suppressor) reads warnings from EDA tool log files, applies suppression rules written in YAML, and reports what is left as a text report, on screen, or as a JUnit file for CI.

## Before starting work

* **Interview first.** Before proposing features or opening a pull request, ask how the change will be used and confirm the conventions below. Most proposals declined in this project would have been ruled out by one question about how ELFWS is actually used.
* **Check for an existing tool** before building one (for example, `sdsort` already checks function ordering).
* **Discuss designs before coding** any change that affects users: command line options, the suppression file format, or the user parser API.

## Commands

Requires Python 3.9 or newer. The lint tools need Python 3.11 or newer.

```bash
pip install . coverage          # install ELFWS and its dependencies

python -m unittest              # run the tests
pyflakes elfws $(find tests -name '*.py' -not -path 'tests/user_defined_tools/*')
sdsort --check elfws            # functions follow the Stepdown Rule
python -m build && twine check --strict dist/*   # package builds and README renders on PyPI
```

CI (`.github/workflows/main.yml`) runs the tests on Python 3.9 to 3.14, plus the lint and package checks. Run them locally before pushing.

## Workflow

* **One GitHub issue per pull request.** Create the issue first; the PR body starts with `Fixes #N`.
* **Branch** `issue-N`, created from an up-to-date `origin/master`. Never push to `master`.
* **PR title and commit subject:** `Issue#N:  Description.` (two spaces after the colon).
* **Fixes from review** are separate commits titled `Addressing review comments:  Description.` PRs are squash-merged.
* **PR descriptions** explain the Clean Code pattern applied, why it matters, and a short before/after example. The maintainer uses PRs to learn patterns.
* **Verify behavior is unchanged** for refactors: add characterization tests that pass before *and* after, and compare command output with `master` byte for byte.
* **`release_notes.txt` is only updated at release time.** Leave it out of normal changes.

### Releasing

1. Bump `elfws/version.py` and update `release_notes.txt` in a PR.
2. After it merges, publish a GitHub release tagged with the version, without a leading `v` (for example `1.0.0`).
3. `.github/workflows/publish.yml` builds the package and uploads it to PyPI through trusted publishing. It refuses to publish if the tag does not match `elfws/version.py`.

Release notes use the sections *New Features*, *Retired Issues*, *Bug Fixes* and *Miscellaneous*, with entries like:

```
  issue #46:
    Suppression rule warning IDs must now match the entire warning ID.
    Note:  Rules relying on prefix matching must add .* to the ID.
```

Issues closed without being implemented go under *Retired Issues*. Changes users must act on get a `Note:` line.

## Architecture

| Module | Responsibility |
|---|---|
| `__main__.py` | Entry point. The only place that calls `sys.exit()`; catches `ElfwsError`. |
| `cmd_line_args.py` | argparse; each subcommand stores its function in `run_subcommand`. |
| `subcommand/*.py` | One module per subcommand; each returns an `ExitCode`. |
| `suppression_results.py` | `SuppressionResults`: the warnings in a log after a suppression file is applied. |
| `suppression_file.py` | Reads and validates the suppression YAML (`SuppressionRuleExtractor`). |
| `log_file.py` | Reads the log file. |
| `parser_loader.py` | Finds the parser for a log: user parsers (`ELFWS_USER_VENDOR_DIR`) first, then built-in ones. |
| `rule_matching.py` | Matches one warning against one rule. |
| `display.py`, `junit_results.py`, `junit.py`, `output_file.py` | Screen and report text, JUnit, and writing files. |
| `warning.py`, `warning_list.py`, `suppression.py`, `suppression_list.py` | Core data classes. |
| `error.py`, `exit_code.py` | `ElfwsError(sMessage, iExitCode)` and the `ExitCode` enum (values are a public interface: do not renumber). |
| `vendor/<vendor>/<tool>.py` | One parser per tool. |

Library code raises `ElfwsError`; only `main()` prints the error and exits.

## Code style

The maintainer follows Uncle Bob's *Clean Code*. House rules:

* **Hungarian notation** for variables and parameters: `sName`, `iCount`, `lItems`, `dMap`, `oObject`, `fFlag`. This is deliberate; do not propose removing it. Constants are `UPPER_CASE`; classes are `CapWords` nouns.
* **Function names are verb phrases** saying what they do (`extract_warning_section`, not `warning_section`). Checks returning a bool read as questions: `is_`, `has_`, `do_`, `would_`.
* **Small functions with guard clauses.** Extract conditionals into named predicates (`if not is_mapping(dSup):`), and put `try/except` blocks and error formatting in their own functions.
* **Top-level functions read as their steps,** one named call per line at the same level of detail:
  ```python
  def create(oCommandLineArguments):
      lWarnings = extract_warnings_to_suppress(...)
      dSup = create_suppression_dict(lWarnings)
      write_suppression_file(..., dSup)
  ```
  Explaining variables used once are fine. Do not nest calls (`f(g(x))`); assign the inner result to a named variable first.
* **Stepdown Rule:** each function sits below the functions that use it, in the order they are used. Checked by `sdsort --check`.
* **Classes over tuples** when values travel together (data clumps). Pass a function only what it needs.
* **Return a condition directly** only when it is a plain comparison (`return len(lItems) > 0`). For calls like `re.match(...)`, keep `if ...: return True` / `return False`.
* **Separate building output from emitting it** (`build_results_lines()` returns lines; `print_lines()` prints them).
* **No `None` placeholders in classes;** initialize collections to `[]` or `{}`.
* **No comments that narrate the code.** If code needs explaining, extract a well-named function.
* **Blank lines** between logical blocks and before the final `return`. Docstrings use `'''` with `Parameters:` / `Returns:`. String concatenation, not f-strings. Lines up to 160 characters.
* **Prefer plain loops** over clever `zip` or comprehension tricks when they are harder to read.
* **User-facing docs** (`docs/source/*.rst`) describe behavior, not implementation details such as module or class names.

## Parsers

* **Each vendor parser is self-contained.** Vendors change their log formats independently, so parsers share no parsing logic across vendors, even when the code looks similar. Users also copy parsers as templates for their own.
  * Allowed to share: format-free primitives (`vendor/utils.do_lines_start_with_sequence`), user-facing contracts (`vendor/utils.NO_ID`), and helpers for the same tool's format (`vendor/mentor_graphics/utils.py`, used by both Questa CDC parsers).
* **Public parser API,** kept at the top of each parser: `get_vendor()`, `get_tool_name()`, `is_logfile(lFile)`, `extract_warnings(lFile)`. User-defined parsers depend on it.
* **Renaming anything user parsers use** goes through `elfws/deprecation.py`, which keeps the old name working with a `DeprecationWarning`. Internal helpers are renamed outright.
* `tests/user_defined_tools/` stands in for a *user's* parser and is intentionally old-style. Do not refactor it.

## Python versions and dependencies

* Supported: **Python 3.9 to 3.14.** EDA servers (often RHEL) upgrade slowly, so 3.9 stays supported even though it is past upstream end of life. Do not use syntax or library features newer than 3.9 in `elfws/`.
* The only runtime dependency is `PyYAML>=6.0`.
* License: `GPL-3.0-only`.

## Product context

* **ELFWS is used in CI/CD pipelines** to catch new warnings. The outputs that matter are the text report (for people reviewing suppressions) and JUnit (for CI).
* **The maintainer's workflow:** the suppression YAML open in their own editor, the report in another terminal; they scan for groups of similar warnings and write rules by copying and editing existing ones.
* **EDA tools rarely report the source file and line of a warning.** Warnings are located by their line in the log file only. Do not propose features that depend on source locations.
* **Declined; do not re-propose:**
  * a TUI;
  * editor-driven triage;
  * a report watch mode;
  * auto-generated rule snippets;
  * SARIF, Markdown summary or JSON output;
  * baseline / diff mode.
* **Planned for 2.0.0:**
  * `--fail-on` (#56), rule validation (#58), multiple logs per run (#61) and rule metadata (#63);
  * the parser interface redesign (#59, #82). It changes the user parser API, so it waits for a major release.
