.PHONY: deps run

run:
	@poetry run flask run

deps:
	poetry install
