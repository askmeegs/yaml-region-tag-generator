# yaml-region-tag-generator


```
docker build -t gcr.io/megandemo/yamltag:latest .

docker run -e ID_RSA=$ssh_key -e KNOWN_HOSTS=$known_hosts -e PRODUCT="istio" \
 -e GITHUB_REPOSITORY="askmeegs/istio-samples" -e GITHUB_REF="saturday" \
 gcr.io/megandemo/yamltag:latest
```