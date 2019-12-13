#!/bin/sh

echo ${LOCAL_PATH}
echo ${COMMIT_MESSAGE}
echo ${BRANCH}

cd ${LOCAL_PATH}
git config --global user.name "yamlbot"
git config --global user.email "yamlbot-github@gmail.com"
git add .
git commit -m "${COMMIT_MESSAGE}"
git push origin ${BRANCH}