## v0.12.2 (2025-03-05)

### Fix

- move io to fileutils
- **utils.logger**: fix compatibility with py310

## v0.12.1 (2025-03-03)

### Feat

- **pyauxlib.utils.dictionaries.py**: add more types to 'remove' in remove_keys

### Fix

- small fixes

### Refactor

- **filesfolders.py**: refactor the iterate_files and iterate_folders and improved their docstrings

## v0.12.0 (2025-01-23)

### Feat

- add filegroup to manage groups of files with related names

### Fix

- fix return type of require_class decorator and examples section of check_dependency docstring

## v0.11.0 (2025-01-16)

### Feat

- improved decorators for required imports

## v0.10.3 (2024-12-09)

### Fix

- **Timer**: fix timer not reset in __call__

## v0.10.2 (2024-11-05)

## v0.10.1 (2024-09-30)

### Fix

- fix lint error

## v0.10.0 (2024-09-30)

## v0.9.3 (2024-07-23)

### Fix

- **whole-project**: fix some troubles with tests

## v0.9.2 (2024-07-23)

### Fix

- **encoding**: fix some code unreachable errors and other minor things

## v0.9.1 (2024-07-23)

### Fix

- **actions**: update setup-python to v6

## v0.9.0 (2024-07-23)

### Feat

- **logger.py**: improve logger functioning

### Refactor

- **iterate_folder**: simplify code to iterate folders
- update certifi
- **encoding.py**: improve and simplify handling of encoding

## v0.8.1 (2024-02-17)

### Feat

- **pyauxlib.io.filesfolders**: add safe open file that creates folder path if it doesn't exist

## v0.8.0 (2024-02-09)

### Feat

- **callables.args**: add validation for arguments

## v0.7.0 (2024-01-29)

### Feat

- **pyauxlib.io.yamlio**: add generator of yaml template from a pydantic model

### Refactor

- **pyauxlib.io.yamlio.py**: parse yaml files using ruamel.yaml instead of pyyaml
- **decorators.warning**: change behavior of warning decorators

## v0.6.1 (2023-12-27)

### Feat

- **io.filesfolders**: add 'generate_unique_filename'

## v0.6.0 (2023-12-27)

### Feat

- **utils.zip**: add handling of zip files

## v0.5.0 (2023-12-18)

### Feat

- **utils.inspect_callables**: add public_callables function
- **utils.uuid**: create unique uuid objects

## v0.4.1 (2023-12-01)

### Fix

- **encoding.py**: fix mypy error when checking if chardet can be imported

## v0.4.0 (2023-12-01)

### Feat

- **decorators/log.py**: add decorator to log messages at the start/end execution of functions

### Refactor

- **encoding.py**: take out code from try-except

## v0.3.0 (2023-10-30)

### Feat

- improve usage of timer

## v0.2.0 (2023-10-23)

### Feat

- **logger.py**: save log file in given path with a timestamp

## v0.1.2 (2023-10-16)

### Feat

- **pyauxlib.decorators.import_errors**: add decorator to check that required imports are available

## v0.1.1 (2023-10-02)

### Fix

- **whole-project**: fix workflows, tests and mkdocs conf

## v0.1.0 (2023-09-30)

### Refactor

- **project**: sanitize the porject backbone and code

## v0.0.6 (2023-09-11)

## v0.0.5 (2023-09-08)

## v0.0.4 (2023-07-22)

## v0.0.2 (2023-06-30)

## v0.0.1 (2023-06-02)

## v0.0.0 (2023-06-01)
