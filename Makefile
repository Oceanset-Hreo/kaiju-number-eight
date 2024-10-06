up:
	docker compose -f docker-compose.yaml up --build

prod-up:
	docker compose -f docker-compose.prod.yml up --build  --force-recreate -d

git-pull-main:
	git pull origin main

build-be-image:
	$(MAKE) -C backend build

build-fe-image:
	$(MAKE) -C frontend build

run-fe-build:
	$(MAKE) -C frontend run-build

run-clean-dis:
	$(MAKE) -C frontend clean-dis

deploy: git-pull-main build-be-image build-fe-image prod-up

issue-certificate:
	docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d jakdf.us
