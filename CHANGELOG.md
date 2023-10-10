# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

Version numbers track
[sortedcontainers versions](https://github.com/grantjenks/python-sortedcontainers/blob/master/HISTORY.rst).
The major and minor versions correspond to the same sortedcontainers major,
minor version; the patch version increments independently to release fixes.

## [Unreleased]

- Nothing yet

## [2.4.1] — 2023-10-10

### Fixed

- Add `__all__` to define the explicit exports of `sortedcontainers.sorteddict`
- Remove an internal `TypeVar` from the `__all__` of
  `sortedcontainers.sortedlist`

## [2.4.0] — 2023-10-09

### Added

- Stubs now published as a standalone package from this separate repo.
- Tests for stubs using `pytest-mypy-plugins`
- Stub-only types for `SortedKeySet` and `SortedKeyDict` which describe the
  differences that apply when key functions are used (mirrors `SortedKeyList`).

### Changed

- Constructors return types that reflect the API differences that apply when key
  functions are used
- The restrictions on key/value types are enforced by the types. Keys/values
  need to be hashable and or comparable, or unrestricted, according to the
  collection type and whether a key function is used.
- Unsafe operations that would cause type errors at runtime are disallowed. For
  example, taking a union of two sets with different element types, that could
  cause a type error due to types not being orderable with respect to each
  other.

### Fixed

- A few minor typos, missing methods etc.

### Removed

- Most private methods, except `_reset()` (which is documented and used to
  change the SortedList load factor for performance reasons).

## Unreleased — [PR to sortedcontainers proposing stubs]

[PR to sortedcontainers proposing stubs]:
  https://github.com/grantjenks/python-sortedcontainers/pull/107

Created by Martin Larralde with review from several people in the PR.

[unreleased]:
  https://github.com/h4l/sortedcontainers-stubs/compare/v2.4.1...HEAD
[2.4.1]: https://github.com/h4l/sortedcontainers-stubs/compare/v2.4.0...2.4.1
[2.4.0]: https://github.com/h4l/sortedcontainers-stubs/releases/tag/v2.4.0
