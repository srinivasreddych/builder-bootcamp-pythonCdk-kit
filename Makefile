create-infra:
			chmod +x ./pipeline-infra/deploy.sh
			./pipeline-infra/deploy.sh

delete-infra: 
			chmod +x ./pipeline-infra/delete.sh
			./pipeline-infra/delete.sh

dev:
	trap 'kill %1' SIGINT
	sam local start-api

build:
	./src/get/build.sh
	./src/post/build.sh
	./src/simple/build.sh


test: build
	./src/get/test.sh
	./src/post/test.sh
	./src/simple/test.sh

