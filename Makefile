amd64:
	docker buildx build --build-arg GoArch="amd64" --platform=linux/amd64 -t \
	teamsgpt.azurecr.io/gptstudio:latest .

pub:
	docker push teamsgpt.azurecr.io/gptstudio:latest

updocker:
	ssh teamsgpt-azure "cd /home/master/gptstudio-deploy && sudo sh upgrade.sh"


.PHONY: clean build

