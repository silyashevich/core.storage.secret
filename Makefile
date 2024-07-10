VENV=.venv
PYTHON=$(VENV)/bin/python3
PIP=$(VENV)/bin/pip
green=`tput setaf 2`
blue=`tput setaf 4`
reset=`tput sgr0`
bold=`tput bold`

default: docker-env/up

env/python-venv:
	@ test -d ${VENV} || (echo "> ${blue}create venv '${VENV}'${reset}" && python3 -m venv ${VENV}) \
	&& source ./.venv/bin/activate \
	&& echo "> ${blue}update pip and setuptools${reset}" \
	&& ${PIP} install -U pip setuptools \
	&& echo "> ${blue}install app requirements${reset}" \
	&& ${PIP} install -r ./app/requirements.txt

docker-env/up:
	@ read -p "${green}run docker-compose file:${reset} [${bold}prod${reset}]/dev:" task \
	&& echo "> ${blue}run docker-compose up with docker-compose-$${task:-prod}.yml${reset}" \
	&& docker-compose -f ./docker-compose-$${task:-prod}.yml up -d \
	&& echo "> ${blue}list containers${reset}" \
	&& docker-compose -f ./docker-compose-$${task:-prod}.yml ps -a

docker-env/dev/up:
	@echo "> ${blue}run docker-compose up with docker-compose-dev.yml${reset}" \
	&& docker-compose -f ./docker-compose-dev.yml up -d \
	&& echo "> ${blue}list containers${reset}" \
	&& docker-compose -f ./docker-compose-dev.yml ps -a

docker-env/down:
	@read -p "${green}run docker-compose file:${reset} [${bold}prod${reset}]/dev:" task \
	&& echo "> ${blue}docker-compose down with docker-compose-$${task:-prod}.yml${reset}" \
	&& docker-compose -f ./docker-compose-$${task:-prod}.yml down \
	&& echo "> ${blue}list containers${reset}" \
	&& docker-compose -f ./docker-compose-$${task:-prod}.yml ps -a

docker-env/dev/down:
	@echo "> ${blue}docker-compose down with docker-compose-dev.yml${reset}" \
	&& docker-compose -f ./docker-compose-dev.yml down \
	&& echo "> ${blue}list containers${reset}" \
	&& docker-compose -f ./docker-compose-dev.yml ps -a

docker-env/logs:
	@read -p "${green}run docker-compose file:${reset} [${bold}dev${reset}]/prod:" task \
	&& echo "> ${blue}docker-compose down with docker-compose-$${task:-dev}.yml${reset}" \
	&& docker-compose -f ./docker-compose-$${task:-dev}.yml logs --tail=100 -f

docker-env/down-and-remove-volumes:
	@read -p "${green}run docker-compose file:${reset} [${bold}dev${reset}]/prod:" task \
	&& echo "> ${blue}docker-compose down with docker-compose-$${task:-dev}.yml${reset}" \
	&& docker-compose -f ./docker-compose-$${task:-dev}.yml down --remove-orphans -t 0 --volumes\
	&& echo "> ${blue}list containers${reset}" \
	&& docker-compose -f ./docker-compose-$${task:-dev}.yml ps -a

docker-env/restart:
	@read -p "${green}run docker-compose file:${reset} [${bold}dev${reset}]/prod:" task \
	&& echo "> ${blue}docker-compose down with docker-compose-$${task:-dev}.yml${reset}" \
	&& docker-compose -f ./docker-compose-$${task:-dev}.yml restart -t 0 \
	&& echo "> ${blue}list containers${reset}" \
	&& docker-compose -f ./docker-compose-$${task:-dev}.yml ps -a

docker/app-rebuild:
	@echo "> ${blue}rebuild app docker image${reset}" \
	&& /bin/bash ./build-app-image.sh
