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
Range vector we can't see  a range vector graph 
`scrape_duration_seconds{job="prometheus"}[1m]`  
`date -d  @1643100478.369` # check date  
## overwritten a range vector 
`scrape_duration_seconds{job="prometheus"}[1m:15s]`  
Convert range vector to an instant vector using rate() function      
`rate(scrape_duration_seconds{job="prometheus"}[1m:15s])` 
## Explanation
`node_netstat_Tcp_InSegs{job="linux-prometheus"}`  
`rate(node_netstat_Tcp_InSegs{job="linux-prometheus"}[15m])`  

## Function 
`sum(go_threads)`

## sum and rate 
How to apply aggregation and other operation when using the rate and other counter-only functions.    
Only functions you can apply to a counter's value are rate, irate, increase, and resets.  
only rate then sum.    
otherwise rate() cannot detect counter resets when your target restarts  


## Function in Function equals sub-queries 
`node_netstat_Tcp_InSegs{job="linux-prometheus"}`
ceil  
`node_netstat_Tcp_InSegs{job="linux-prometheus"}`   # instant vector  
`node_netstat_Tcp_InSegs{job="linux-prometheus"}[2m:15s]` # range vector  
`rate(node_netstat_Tcp_InSegs{job="linux-prometheus"}[2m:15s])` # instant vector

ceil(v instant-vector) rounds the sample values of all elements in v up to the nearest integer.
`ceil(rate(node_netstat_Tcp_InSegs{job="linux-prometheus"}[2m:15s]))`

## Number 
Prometheus supports all 64-bits floating point values, including positive infinity, negative infinity and 
NaN. 




## Start an example database
docker run -d --name db --net=host -it --rm -e POSTGRES_PASSWORD=password postgres
# Connect to it
docker run  -d --name node-exporter-pg \
--net=host \
-e DATA_SOURCE_NAME="postgresql://postgres:password@localhost:5432/postgres?sslmode=disable" \
quay.io/prometheuscommunity/postgres-exporter


## Reload
curl -X POST http://localhost:9090/-/reload