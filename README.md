# sortedcontainers-stubs

Community-maintained Python type stubs for the
[sortedcontainers](https://grantjenks.com/docs/sortedcontainers/) Python
library. sortedcontainers provides dict, set and list data structures that
maintain the order of their elements by value (not by insertion order).

The sortedcontainers API has some differences and additional methods compared to
regular Python dict, set and list types, and has additional requirements for
keys/values on whether they need to be hashable or comparable. These type stubs
allow type checkers to enforce these details, which makes sortedcontainers
easier to use.

## Install

```
$ pip install sortedcontainers-stubs
```

Once you've installed the package, mypy (or other tools) should automatically
find the types without any configuration.

## Usage Notes

`sortedcontainers.sorteddict.SortedKeyDict` and
`sortedcontainers.sortedset.SortedKeySet` are stub-only subclasses of
`SortedDict` and `SortedSet` — they don't exist at runtime. They exist as type
stubs to describe the different return types of the `SortedDict` and `SortedSet`
constructors, which vary depending if a key function is used or not.

However, `sortedcontainers.sortedlist.SortedKeyList` _is_ a real type that
exists at runtime.

## Version numbers

The sortedcontainers-stubs major and minor versions correspond to major and
minor versions of sortedcontainers. The patch number increments independently if
required to fix an issue. So if you're using sortedcontainers `2.4.X`, use the
latest `2.4.X` version of sortedcontainers-stubs.

Currently sortedcontainers-stubs version `2.4.0` has dependency metadata
supporting sortedcontainers `>=2,<3` as there are minimal API differences so far
since 2.0.

## Reporting Issues

Report issues with type stubs [here, at the sortedcontainers-stubs
issues][issues], not at the sortedcontainers repo.

[issues]: https://github.com/h4l/sortedcontainers-stubs/issues

## History

These stubs were initially offered to sortedcontainers in a
[PR](https://github.com/grantjenks/python-sortedcontainers/pull/107). After some
discussion, the sortedcontainers developer, Grant Jenkins, indicated they'd
prefer to keep the sortedcontainers codebase without type annotations, and
publish the type stubs in a separate package. This repo is based on the stubs
from that PR.
