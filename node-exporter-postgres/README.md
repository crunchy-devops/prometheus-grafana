# New Node-exporter postgresql 

```shell
docker cp air.dump db:/tmp
```

##  DB  postgres_airport
```shell
pg_dump -Fc postgres > air.dump 
pg_restore -j 8 -d postgres air.dump
```
