#!/bin/sh

cd ./jindam_site/
hugo build --themesDir=./theme/ --ignoreCache --destination ../docs/

echo "build complete"
