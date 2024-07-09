<!-- omit in toc -->
# Contributing to nc_tg_bot

Contributions are welcome! Please see the [Table of Contents](#table-of-contents) for details on how to contribute.

<!-- omit in toc -->
## Table of Contents

- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Your First Code Contribution](#your-first-code-contribution)

## I Have a Question

Before you ask a question, it is best to search for existing [Issues](https://github.com/blvdek/nc_tg_bot/issues) and [Discussions](https://github.com/blvdek/nc_tg_bot/discussions) that might help you. In case you have found a suitable issue or discussion and still need clarification, you can write your question in there. It is also advisable to search the internet for answers first.

- Open an [Issue](https://github.com/blvdek/nc_tg_bot/issues/new) or [Discussions](https://github.com/blvdek/nc_tg_bot/discussions).
- Provide context and project/platform versions as needed.

## I Want To Contribute

### Reporting Bugs

- Make sure you are using the latest version.
- Determine if your bug is really a bug and not an error on your side.
- Check for existing bug reports and internet discussions.
- Open an [Issue](https://github.com/blvdek/nc_tg_bot/issues/new?template=BUG_REPORT.md).
- Provide a clear description of the expected and actual behavior.
- Describe the reproduction steps and provide context and version information.

### Your First Code Contribution

> 💡 Remember that nc_tg_bot is built on top of [aiogram](https://github.com/aiogram/aiogram) and [nc_py_api](https://github.com/cloud-py-api/nc_py_api) libraries, so integrating new features with these libraries is pretty easy.

1. `Fork` this repository
2. Create a `branch`
3. `Clone` your nc_tg_bot fork.
4. Set current working dir to the root folder of cloned nc_tg_bot.
```bash
cd nc_tg_bot
```
5. Install dependencies using [Poetry](https://python-poetry.org "python package manager"):
```bash
poetry install
```
6. Create and edit .env file:
```bash
cp .env.exmaple .env
vi .env
```
7. Install pre-commit hooks:
```bash
pre-commit install
```
8. Run bot:
  - With docker compose:
    ```bash
    make bot-build
    make bot-run
    ```
 - Or without docker compose:

    * Make migrations:
    ```bash
    make migrate
    ```
    * Run bot:
    ```bash
    poetry run python -m bot
    ```
9. Run tests to check that everything works:
```bash
poetry run python -m pytest
```
10. `Commit` your changes
11. `Push` your commits to the branch
12. Submit a `pull request`
