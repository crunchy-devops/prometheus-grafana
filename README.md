# prometheus-grafana
Training on the ubiquitous monitoring tools: Prometheus and Grafana

## Pre-requisites on your VM
### Useful packages
```shell
   sudo apt-get update  # update links to repos
   sudo apt-get -y install git wget htop iotop iftop # install git and monitoring tools
   sudo apt-get -y install python3 python3-venv # install python3 and virtualenv
   sudo apt-get -y install build-essential   # need for installing docker-compose
   sudo apt-get -y install python3-dev libxml2-dev libxslt-dev libffi-dev # need for installing docker-compose
   htop  # check your vm config
   Crtl-c  # exit 
``` 
### install this repo and docker
```shell script
cd 
git clone   https://github.com/crunchy-devops/prometheus-grafana.git 
cd prometheus-grafana
python3 -m venv venv  # set up the module venv in the directory venv
source venv/bin/activate  # activate the virtualenv python
pip3 install wheel  # set for permissions purpose
pip3 install --upgrade pip # update pip3
pip3 install ansible # install ansible 
pip3 install requests # extra packages
ansible --version # check the version number # should be the latest 2.11.6
ansible-playbook -i inventory install_docker_ubuntu.yml --limit local  # run the playbook for installing docker
# close your IDE and start again 
cd
cd prometheus-grafana
source venv/bin/activate
docker ps 
pip3 install docker 
pip3 install docker-compose
```

## Configure Linux-remote, db, petclinic
```shell
ssh-keygen -t rsa -b 4096
ssh-copy-id ubuntu@51.254.227.23
ansible-playbook -i inventory install_docker_ubuntu.yml --limit linux,db,petclinic 
```
## Install postgresql db on remote
```shell
ansible-playbook -i inventory install_db-node_exporter.yml --limit db 
```
## Install node_exporter
```shell
ansible-playbook -i inventory install_node_exporter_linux.yml --limit linux 
```

## Install metric-types
```shell
ansible-playbook -i inventory install_metric_types.yml --limit petclinic 
```



## Reload Prometheus configuration 
curl -s -XPOST localhost:9090/-/reload