# Grad School Party

Grad School Party is a Yale MGT 656 project. Sprint 1 is a walking skeleton: account signup, login/logout, a protected dashboard, and PostgreSQL-backed Django authentication. Minigames, the campus map, AI, and leaderboards are not part of this sprint.

## Local Setup

Requirements: Python 3.10+ and PostgreSQL 13+.

1. Create and activate a virtual environment:

	```sh
	python3 -m venv .venv
	source .venv/bin/activate
	```

2. Install dependencies:

	```sh
	python -m pip install -r requirements.txt
	```

3. Create a PostgreSQL database and login. For example, from `psql` as a database administrator:

	```sql
	CREATE ROLE grad_party_user LOGIN PASSWORD 'choose-a-local-password';
	CREATE DATABASE grad_school_party OWNER grad_party_user;
	```

4. Copy `.env.example` to `.env`. Set `DATABASE_URL` to the PostgreSQL login you created, generate a unique local `SECRET_KEY`, and set the other values for your machine. Generate a key with:

	```sh
	python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
	```

	`.env` is ignored by Git. Never commit it or share its values. Set `DEBUG=False` and a production-only secret in deployment, and set `ALLOWED_HOSTS` to the deployed hostnames.

5. Apply Django's built-in migrations and start the development server:

	```sh
	python manage.py migrate
	python manage.py runserver 0.0.0.0:${PORT:-8000}
	```

	Open `http://localhost:8000/`. Create an account at `/signup/`; the dashboard is only available after login.

## Grader Accounts

Set `GRADER_ACCOUNTS_JSON` in the local ignored `.env` or your deployment provider's secret environment settings. Its value must be a JSON list, for example:

```text
GRADER_ACCOUNTS_JSON=[{"username":"grader-one","password":"use-a-unique-password"}]
```

Then run:

```sh
python manage.py create_fake_graders
```

The command uses Django's password hashing, never prints passwords, and skips usernames that already exist, so rerunning it is safe. Existing account passwords are not changed.

## Tests

Run the test suite against the PostgreSQL database configured by `DATABASE_URL`:

```sh
python manage.py test
```

The tests cover signup, login/logout, dashboard access control, user persistence, and repeatable grader creation. Django creates and removes a separate test database automatically.

## Deployment

Provide `SECRET_KEY`, `DATABASE_URL`, `DEBUG=False`, and comma-separated `ALLOWED_HOSTS` as environment variables in the hosting provider. Set `PORT` if the provider supplies one. Install from `requirements.txt`, run `python manage.py migrate` and `python manage.py collectstatic --noinput` as release steps, and start the web process with the included `Procfile` (Gunicorn binds to `0.0.0.0:$PORT`). The PostgreSQL URL should use a TLS-enabled connection in production.