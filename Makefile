install:
	poetry install
page_loader:
	poetry run page_loader
lint:
	poetry run flake8 page_loader
test:
	poetry run pytest -vvvv
check:
	make lint
	make test
test-coverage:
	poetry run pytest --cov --cov-report term-missing --cov-report xml
build:
	poetry build
publish:
	poetry publish --dry-run
package-install:
	python3 -m pip install dist/*.whl --force-reinstall
bpp:
	make build
	make publish
	make package-install