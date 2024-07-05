<!-- omit in toc -->
# Contributing to nc_tg_bot

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them. Please make sure to read the relevant section before making your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved. The community looks forward to your contributions. 🎉

> And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
> - Star the project
> - Tweet about it
> - Refer this project in your project's readme
> - Mention the project at local meetups and tell your friends/colleagues

<!-- omit in toc -->
## Table of Contents

- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)

## Code of Conduct

This project and everyone participating in it is governed by the
[nc_tg_bot Code of Conduct](https://github.com/blvdek/nc_tg_bot/blob/main/.github/CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code.

## I Have a Question

Before you ask a question, it is best to search for existing [Issues](https://github.com/blvdek/nc_tg_bot/issues) and [Discussions](https://github.com/blvdek/nc_tg_bot/discussions) that might help you. In case you have found a suitable issue or discussion and still need clarification, you can write your question in there. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/blvdek/nc_tg_bot/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions, depending on what seems relevant.

## I Want To Contribute

### Reporting Bugs

<!-- omit in toc -->
#### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions.
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://github.com/blvdek/nc_tg_botissues?q=label%3Abug).
- Also make sure to search the internet (including Stack Overflow) to see if users outside of the GitHub community have discussed the issue.
- Collect information about the bug.

<!-- omit in toc -->
#### How Do I Submit a Good Bug Report?

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Issue](https://github.com/blvdek/nc_tg_bot/issues/new?template=BUG_REPORT.md).
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the *reproduction steps* that someone else can follow to recreate the issue on their own. This usually includes your code. For good bug reports you should isolate the problem and create a reduced test case.
- Provide the information you collected in the previous section.


### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for nc_tg_bot, **including completely new features and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.

<!-- omit in toc -->
#### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Find out if the functionality is already covered, maybe by an individual configuration.
- Perform a [search](https://github.com/blvdek/nc_tg_bot/issues) to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
- Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset. If you're just targeting a minority of users, consider writing an add-on/plugin library.

<!-- omit in toc -->
#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/blvdek/nc_tg_bot/issues). We have a template for enhancement suggestions that you can use as a guide. You can access it [here](https://github.com/blvdek/nc_tg_bot/issues/new?template=FEATURE_REQUEST.md).

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point you can also tell which alternatives do not work for you.s
- **Explain why this enhancement would be useful** to most nc_tg_bot users. You may also want to point out the other projects that solved it better and which could serve as inspiration.

### Your First Code Contribution

1. `Fork` this repository
2. Create a `branch`
3. `Clone` your nc_tg_bot fork.
4. Set current working dir to the root folder of cloned nc_tg_bot.
```bash
cd nc_tg_bot
```
5. Setup environment:
```bash
poetry install
```
6. Create and edit .env.prod file:
```bash
cp .env .env.prod
vi .env
```
7. Install pre-commit hooks:
```bash
pre-commit install
```
8. You can run bot with your changes using docker compose:
```bash
docker compose -f docker-compose.build.yml
```
8.1 Or without docker compose:
  - Run db in any way convenient to you:
  ```bash
  docker compose -f docker-compose.build.yml up db -d
  ```
  - Make migrations:
  ```bash
  make migrate
  ```
  - Run bot:
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
