
FE_DIR = $(CURDIR)
IMAGE_NAME =jakdf-fe
CONTAINER_NAME =jakdf-fe-container

info:
	@echo "FE_DIR: $(FE_DIR)"
	@echo "IMAGE_NAME: $(IMAGE_NAME)"
	@echo "CONTAINER_NAME: $(CONTAINER_NAME)"

run-docker:
	docker run -it --rm -v ${FE_DIR}:/app -w /app -p 3000:3000 --name CONTAINER_NAME ${IMAGE_NAME} /bin/sh

build:
	docker build -t ${IMAGE_NAME} .

exec:
	docker exec -it ${CONTAINER_NAME} /bin/sh

run-dev:
	docker run -it --rm -v $(FE_DIR):/app -w /app -p 3000:3000 --name ${CONTAINER_NAME} ${IMAGE_NAME} npm run dev

run-build:
	docker run -i --rm -v $(FE_DIR):/app -w /app --name ${CONTAINER_NAME}-build ${IMAGE_NAME} npm run build

clean-dis:
	rm -rf ${FE_DIR}/dist

init_env:
	sh scripts/init_env.sh
