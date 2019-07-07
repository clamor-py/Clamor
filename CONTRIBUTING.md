# Contributing to Clamor

Clamor is a Discord API framework that couldn't exist without amazing people like you.
So you decided to contribute? Great! But first, read these contribution guidelines to get started.

## Code of Conduct

Please note that this project has a [Code of Conduct][CoC] to which all contributors must adhere.

## Reporting bugs

Found a bug? Report it! Bug reports help us improving this software and making it more usable for everyone.

**Please follow these simple standards for bug reports:**

- Fill out the bug report template

- Include the code you tried, all necessary details and the error you received

## Contributing code or docs

Before you start, please browse the [open issues][issues]. Contributions corresponding to issues labeled with
`help wanted` are especially appreciated.

However, other contributions are welcome too. We love to hear your ideas and suggestions on how to improve this
project or review your submissions of code or docs. If you're planning to do major changes to the code, please
open an issue in advance to discuss the changes or join our [Discord guild][Discord].

If you're new to Pull Requests on GitHub, here's an [introduction][PR introduction].

Pull Requests should, as much as possible, be self-contained and only address one issue. Therefore ten Pull Requests
for ten small and unrelated changes are more appreciated than one big Pull Request with everything mixed together.
This way, it is easier for us to maintain and review the changes and if there are problems with one of them, it
won't hold up the others.

By making a contribution to this repository, you certify that:

- The contribution was created in whole or in part by you and you have the right to submit it under the conditions
of the [MIT License][MIT] this project uses.

- All the code is covered by carefully crafted tests and works flawlessly. If this is not the case, feel free to
ask for help in the corresponding issue and state in detail with what you need help, what you've tried so far and
what's the thing that makes you struggle.

- You didn't increase any version number yourself unless you were told to do so. That's what we usually do for new
releases when we think it is appropriate to do so.

- Your code is consistent, follows the style guidelines and is well-documented.

After your PR has passed all checks, Continuous Integration and has been approved by the maintainers,
it'll be merged.

## Code guidelines

- Code in general should follow [PEP 7 standards for C code](https://www.python.org/dev/peps/pep-0008/) and
[PEP 8 standards for Python code](https://www.python.org/dev/peps/pep-0008/).

- Before committing, please lint your code by running `pylama .` and resolving the issues.
This helps everyone to keep the code overall consistent, easy to read and maintainable.

- Python source files are meant to start with `# -*- coding: utf-8 -*-`, followed by an empty line.

- Please follow the way we structure `include` statements.

```python
# Imports are to be arranged alphabetically

# Imports from the standard library
import audioop as audio
import os.path
import re
# followed by from ... include ... statements from the standard library
from json import dumps

# Imports from external dependencies
import anyio
from anysocks import open_connection
from asks import Session

# Imports from Clamor itself
from .meta import __version__ as version
```

- Please use expressive variable and function names. They should give users
a clear understanding of what they are supposed to do.

```python
# Good:
heartbeat_interval = payload['hearbeat_interval']

# Bad:
# What is xyz supposed to do? Why 5? What is it used for?
xyz = 5
```

- Keep your code readable, self-explanatory and clean. If you're adding
new source files or expand existing ones, don't forget to add corresponding
unit tests to the `tests/` directory.

- Documentation is important for users to give them a clear overview of the
public API of this library. Attributes, functions, and methods starting with
an underscore (`_`) are generally meant to be part of the private API and
therefore doesn't need documentation. Please refer to the
[NumPy docstring style guide](https://numpydoc.readthedocs.io/en/latest/format.html)
or documented source code.

- Keep it usable. No fast-and-loose JSON dicts, manual HTTP requests or gateway
messages that aren't wrapped.

## Contribution ideas

There are many ways of contributing. If there is no [open issue][issues] that arouses your interest, here
are some suggestions on ways of contributing. All contributions are valued.

- Help people in the issues or on our [Discord guild][Discord]

- Use Clamor in a project and give us feedback about what worked and what didn't

- Write a blog post about your experiences with Clamor, good or bad

- Comment on issues.

- Review Pull Requests

- Add tests

- Fix bugs

- Add features

- Improve code or documentation

[CoC]: ./CONTRIBUTING.md
[issues]: https://github.com/clamor-py/Clamor/issues
[Discord]: https://discord.gg/HbKGrVT
[PR introduction]: https://help.github.com/articles/using-pull-requests
[MIT]: https://choosealicense.com/licenses/mit
[editorconfig]: ./.editorconfig
