# Capacity planning in prometheus

Two capacity concerns: memory and disk

## rate of samples
see the rate of sample collections using this query
`rate(prometheus_tsdb_head_samples_appended_total[1m])`  
This will show you the per-second rate of sample being added to the database over the last minute.  

## number of metrics
`prometheus_tsdb_head_series`  
Memory used is 4557 * 2 * 3600 * 24 / 1024 /1024 - 400 Mb 

