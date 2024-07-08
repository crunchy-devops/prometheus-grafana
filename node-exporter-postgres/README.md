# New Node-exporter postgresql 

##  DB  postgres_airport
```shell
pg_dump -Fc mon > air.dump 
pg_restore -j 8 -d mon air.dump
```
