# yaml-region-tag-generator


```
docker build --build-arg SSH_PRIVATE_KEY=$ssh_key --build-arg KNOWN_HOSTS=$known_hosts -t gcr.io/megandemo/yamltag:0.0.1 .

docker run -e PRODUCT="istio" -e GITHUB_USER="askmeegs" -e GITHUB_REPO_NAME="istio-samples" -e REPO_BRANCH="yamltest" gcr.io/megandemo/yamltag:0.0.1
```