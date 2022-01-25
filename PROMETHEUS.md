# Prise en main de Prometheus

## Premieres commandes
allez dans status et selectionnez Targets et Check  
enter go_threads  
process_virtual_memory_bytes  
prometheus_tsdb_storage_blocks_bytes  
node_context_switches_total  
scrape_duration_seconds  

## PromQL Basic Filters Regex  
`node_cpu_seconds_total{mode=~".*irq"}`  
Prometheus uses regular expressions RE2 syntax    
https://github.com/google/re2/wiki/Syntax  
`node_cpu_seconds_total{mode=~"soft.*"}`  
scrape_duration_seconds  
## Data Types
Scalar  
Instant vector  
`node_cpu_seconds_total{mode=~"soft.*"}`  
`scrape_duration_seconds{job="prometheus"}`  
Range vector we can't see a range vector 
`scrape_duration_seconds{job="prometheus"}[1m]`  
`date -d  @1643100478.369` # check date  
## overwritten a range vector 
`scrape_duration_seconds{job="prometheus"}[1m:15s]`  
Convert range vector to an instant vector using rate() function      
`rate(scrape_duration_seconds{job="prometheus"}[1m:15s])` 
# Explanation
`node_netstat_Tcp_InSegs{job="linux-prometheus"}`






## Start an example database
docker run -d --name db --net=host -it --rm -e POSTGRES_PASSWORD=password postgres
# Connect to it
docker run  -d --name node-exporter-pg \
--net=host \
-e DATA_SOURCE_NAME="postgresql://postgres:password@localhost:5432/postgres?sslmode=disable" \
quay.io/prometheuscommunity/postgres-exporter


## Reload
curl -X POST http://localhost:9090/-/reload