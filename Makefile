.PHONY: deps run build-styles style-watch build-image run-image

run:
	@poetry run flask run

build-styles:
	sass styles:web/static/stylesheets

style-watch:
	sass --watch app/styles:4app/web/static/stylesheets

build:
	sass app/styles:app/web/static/stylesheets

deps:
	poetry install

build-image:
	docker build -t spotcamp:latest .

run-image:
	docker run -d -p 3030:8080 spotcamp
