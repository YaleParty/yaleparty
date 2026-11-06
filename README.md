# Yale Party

Yale Party is a campus-themed multiplayer game. Players create characters, travel around Yale, and enter short mini-games inspired by the campus and the university community.

This repository is the team's project workspace for the MGT 656 final project. The team has selected Django and PostgreSQL. The application scaffold and exact install and run commands still need to be added. Do not treat this documentation scaffold as evidence that the application or assignment requirements are already implemented.

## Project status

- Team nickname: `wandering-shape`
- Framework: Django
- Database: PostgreSQL
- A/B test route: [`/341e00b`](#a-b-test)
- Staging and production URLs: to be added when deployed
- Team roster: GitHub usernames are listed in [`docs/mgt656/team.yaml`](docs/mgt656/team.yaml); course nicknames still need to be filled in

## Getting started

After the Django application scaffold is added, replace this note with the exact supported Python version and runnable commands. The intended setup flow is:

1. Install the supported Python version and create a virtual environment.
2. Create a local environment file from a committed example file. Keep real secrets in the environment, never in Git.
3. Configure the database through `DATABASE_URL` and configure the application secret and OpenRouter key through environment variables.
4. Install dependencies, apply database migrations, and run the idempotent seed command to create demo data and grader accounts.
5. Run the automated tests, then start the application locally. The deployed application must listen on `$PORT`.

The Django project files, exact dependency installation and run commands, required environment-variable names, and demo account details are pending implementation. Use PostgreSQL locally and configure it through `DATABASE_URL`; do not commit real API keys, passwords, or production credentials.

## Working agreement

The GitHub Project board is the source of truth for the backlog and sprint commitments. Each backlog issue should be labeled `user story`, use the form “As a ..., I want ..., so that ...”, and include testable acceptance criteria. Split stories into sub-issues when they require several independent pieces of work.

At the start of each sprint, assign committed stories to that sprint's iteration. Move unfinished work to a later iteration rather than deleting it. Work on branches; open pull requests that reference the issue with `Closes #<issue>`, describe what the coding agent produced and what the team changed or rejected, and get a teammate's review before merging. Do not use story points, velocity, or burndown charts.

For AI-assisted work, give the agent the acceptance criteria and relevant project context, review the resulting code, and run the appropriate tests before merging. Tests must mock the LLM and other external services; they must not make real external calls.

## Development and deployment requirements

The project uses Django and PostgreSQL. Staging and production need separate PostgreSQL databases and public URLs. Keep configuration and secrets in environment variables, connect to the database through `DATABASE_URL`, write logs to stdout, store lasting uploads outside local disk, and make schema changes through Django migrations.

Document the exact local commands here when the Django scaffold is committed. The expected local workflow is to install dependencies, configure environment variables, apply Django migrations, run the idempotent demo-data seed command, run Django's automated test suite, and start the web process. The seed command must be safe to run more than once and should be run after a database reset.

## A/B test

The team nickname is `wandering-shape`. Hashing it without a trailing newline gives the required public route `/341e00b`:

```sh
printf %s wandering-shape | shasum
```

The assignment's example was checked with the same method: `printf %s bright-forest | shasum` starts with `211c220`.

The finished app must serve the public A/B page at `/341e00b` and its JSON results at `/341e00b/stats`. The page must meet all assignment requirements: a stable random `kudos` or `thanks` variant per visitor, exactly one matching button, one database-backed impression per visitor, at most one database-backed click per visitor, and timestamps for both events. The stats endpoint must calculate the preferred variant's click rate from the database. The application and these behaviors are not implemented or verified in this documentation-only scaffold.

## Course documentation

Keep the required project evidence under [`docs/mgt656/`](docs/mgt656/):

- `team.yaml`: framework, database, and member roster.
- `technical.md`: technical-challenge choices and testing strategy.
- `sprints/sprint-1.md` through `sprint-4.md`: one short report per sprint, including shipped work, staging status, agent experience, and backlog changes.
- `retrospective.md`: final lessons from the project.

Fill each report with links to real issues and merged pull requests. Record what works on staging, not merely what was planned. Do not invent progress or credentials in these documents.

## Submission checklist

- [ ] Complete the framework, database, team member nicknames, and public URLs.
- [ ] Verify the required app features, migrations, repeatable seed command, and grader accounts.
- [ ] Verify automated tests run without real LLM or other external-service calls.
- [ ] Verify the public A/B page and stats endpoint, including visitor-level counting and variant persistence.
- [ ] Complete each sprint report, `technical.md`, and the final retrospective.
- [ ] Put staging/production access details and any known limitations in the course submission notes, not in this README or source control when they include passwords.