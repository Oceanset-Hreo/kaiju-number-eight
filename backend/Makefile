
BE_DIR = $(CURDIR)
IMAGE_NAME =jakdf-be
CONTAINER_NAME =jakdf-be-container

info:
	@echo BE_DIR: $(BE_DIR)"
	@echo "IMAGE_NAME: $(IMAGE_NAME)"
	@echo "CONTAINER_NAME: $(CONTAINER_NAME)"

run-docker:
	docker run -it --rm -v ${BE_DIR}:/app -w /app --user root:root --name CONTAINER_NAME ${IMAGE_NAME} /bin/bash

build:
	docker build -t ${IMAGE_NAME} .

exec:
	docker exec -it ${CONTAINER_NAME} /bin/sh

run-dev:
	docker run -it --rm -v $(BE_DIR):/app -w /app -p 8000:8000 --name ${CONTAINER_NAME} ${IMAGE_NAME} /bin/sh /app/scripts/run_server.sh

init_settings:
	sh scripts/init_settings.sh
