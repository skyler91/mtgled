#!/bin/bash

pushd pylights
docker build -t skyler91/pylights:latest .
popd

pushd svelte
npm i
npm run build
docker build -t skyler91/mtgled-svelte:latest .
popd

docker push skyler91/pylights:latest
docker push skyler91/mtgled-svelte:latest