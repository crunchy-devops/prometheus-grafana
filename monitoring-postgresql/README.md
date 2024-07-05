# install custom node-exporter postgresql

###
```shell
pip3 install psycopg2-binary prometheus-client

docker volume create data
docker volume ls
docker run -d \
	--name db \
	-e POSTGRESQL_PASSWORD=Tcwowa12 \
	-v data:/bitnami/postgresql \
	-p 32432:5432 \
	bitnami/postgresql:latest



```
