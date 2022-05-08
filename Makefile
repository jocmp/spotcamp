.PHONY: deps run build-styles style-watch build-image run-image

run:
	@poetry run flask run -p 3030

build-styles:
	sass styles:web/static/stylesheets

style-watch:
	sass --watch styles:web/static/stylesheets

build: build-styles

deps:
	poetry install

build-image:
	docker build -t spotcamp:latest .

run-image:
	docker run -d -p 3030:8080 spotcamp
