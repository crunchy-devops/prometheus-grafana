# Prise en main de Prometheus



## Start an example database
docker run -d --name db --net=host -it --rm -e POSTGRES_PASSWORD=password postgres
# Connect to it
docker run  -d --name node-exporter-pg \
--net=host \
-e DATA_SOURCE_NAME="postgresql://postgres:password@localhost:5432/postgres?sslmode=disable" \
quay.io/prometheuscommunity/postgres-exporter


## Reload
curl -X POST http://localhost:9090/-/reload