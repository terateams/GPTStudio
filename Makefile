arm64:
	docker buildx build --build-arg GoArch="arm64" --platform=linux/arm64 -t \
	talkincode/gptstudio:latest-arm64 .
	docker push talkincode/gptstudio:latest-arm64

fastpub:
	docker buildx build --build-arg GoArch="amd64" --platform=linux/amd64 -t \
	talkincode/gptstudio:latest .
	docker push talkincode/gptstudio:latest


.PHONY: clean build
