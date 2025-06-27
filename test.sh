#!/bin/sh

cd ./jindam_site/

hugo server --themesDir=./theme/ --disableFastRender --ignoreCache

echo "서버가 종료되었습니다. build 완료된 public 디렉토리를 삭제합니다."

rm -r ./public

cd ..

