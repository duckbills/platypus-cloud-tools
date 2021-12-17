# Platypus Docker Image
## Image Build: New cluster

You can build this image by identifying the base image tag from [docker hub](https://hub.docker.com/repository/docker/duckbills/platypus) and then running the following command:

``` bash
docker build   --build-arg PLATYPUS_BASE_IMAGE_TAG=testing -t "platypus-oss:testing" .
```

## Image Build: Restore a cluster with previously created indexes

```bash
docker build   --build-arg PLATYPUS_BASE_IMAGE_TAG=testing --build-arg SERVICE_NAME=platypus-s3-path --build-arg RESTORE_STATE=yes  -t "platypus-oss:testing" .
```
This will ensure to download metadata/state for previously created indexes. To get the data simply issue `startIndex` command on both primary and replica once the container is running.

## Single Node Deployment for a new cluster

```bash
docker run -ti -p 8900:8900 -p 8902:8902  --rm platypus-oss:testing
```
This includes a single node deployment that starts up a single daemon that includes:
* Server in primary mode
* Server in replica mode

---


## Multi-node Deployment

Use containers in a Kubernetes environment to deploy multi-node Platypus. See the published [helm chart](../../charts/platypus) for instructions.
