# Postgresql sql query 

## install tpc-postgresql
```shell
git clone https://github.com/system-dev-formations/tpc-ds-postgresql.git
  sudo apt install bison flex
cd /home/ubuntu/tpc-ds-postgresql/tpcds-kit/tools
make 
./dsdgen -DIR /tmp -SCALE 1 -FORCE -VERBOSE
```

## install postgresql12
```shell
docker run -d --name db -e POSTGRES_PASSWORD=password  -v /opt/postgres:/var/lib/postgresql/data \
-p 5432:5432  systemdevformations/docker-postgres12
```