install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 gendiff

lint-test:
	poetry run flake8 tests

test:
	poetry run pytest -vv

coverage:
	poetry run pytest --cov=gendiff tests/ --cov-report xml

test-coverage:
	poetry run pytest --cov=gendiff
