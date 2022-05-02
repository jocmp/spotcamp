.PHONY: deps run build-styles watch-styles build-image run-image

run:
	@poetry run flask run

build-styles:
	sass styles:web/static/stylesheets

watch-styles:
	sass --watch spotcamp/styles:spotcamp/web/static/stylesheets

build:
	sass spotcamp/styles:spotcamp/web/static/stylesheets

deps:
	poetry install

build-image:
	docker build -t spotcamp:latest .

run-image:
	docker run -d -p 3030:8000 spotcamp
