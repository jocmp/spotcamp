.PHONY: deps run watch-styles

run:
	@poetry run flask run

watch-styles:
	sass --watch spotcamp/web/styles:spotcamp/web/static/stylesheets

build:
	sass spotcamp/web/styles:spotcamp/web/static/stylesheets

deps:
	poetry install
