#!/bin/sh

cd ./jindam_site/
hugo build --themesDir=./theme/ --ignoreCache
cd ../

rm -r ./docs/*
mv ./jindam_site/public/* ./docs/
rmdir ././jindam_site/public

