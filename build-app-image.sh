#!/bin/bash
set -e
SCRIPT_PATH=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
IMAGE="silyashevich/core.storage.secret"
VERSION="latest"
IMAGE_AND_TAG="${IMAGE}:${VERSION}"

docker build \
    --build-arg APP_VERSION="${VERSION}" \
    --tag "${IMAGE_AND_TAG}" \
    --file "${SCRIPT_PATH}/Dockerfile" \
    "${SCRIPT_PATH}"

echo "image builded:"
echo "${IMAGE_AND_TAG}"
