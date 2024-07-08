# prometheus-grafana
Training on the ubiquitous monitoring tools: Prometheus and Grafana

## Pre-requisites on your VM
### Useful packages
```shell
   sudo apt update  # update links to repos
   sudo apt -y install git wget htop iotop iftop # install git and monitoring tools
   sudo apt -y install python3 python3-venv # install python3 and virtualenv
   sudo apt -y install build-essential   # need for installing docker-compose
   sudo apt -y install python3-dev libxml2-dev libxslt-dev libffi-dev # need for installing docker-compose
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
pip3 install pyyaml==5.3.1
pip3 install docker==6.1.3
pip3 install requests==2.31.0
pip3 install docker-compose # pip lib for docker-compose 

### Rappel Docker
#### install docker   
```shell
sudo apt update && sudo apt upgrade
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt install -y docker-ce
sudo usermod -aG docker ubuntu 
cd lab-prometheus
docker-compose up -d 
```

## Portainer version 2.20.3
```shell
docker volume create portainer_data
docker run -d -p 32125:8000 -p 32126:9443 --name portainer \ 
 --restart=always \
 -v /var/run/docker.sock:/var/run/docker.sock \  
 -v portainer_data:/data portainer/portainer-ce:2.20.3
```

## install postgresql container
```shell
docker volume create data
docker volume ls
docker run -d \
	--name db \
	-e POSTGRES_PASSWORD=Tcwowa12 \
	-e PGDATA=/var/lib/postgresql/data/pgdata \
	-v data:/var/lib/postgresql/data \
	-v /home/ubuntu/postgres_air_2023.sql:/tmp/postgres_air_2023.sql \
	-p 32432:5432 \
	postgres:latest
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
## Install node_exporter
```shell
ansible-playbook -i inventory install_node_exporter_linux.yml --limit metric-types, db
```

## Install metric-types
```shell
docker ps
git clone  https://github.com/crunchy-devops/metric-types.git 
cd metric-types/
sudo apt update
java --version
sudo apt install openjdk-11-jre-headless
java --version
VERSION=7.3.3
wget https://services.gradle.org/distributions/gradle-${VERSION}-bin.zip -P /tmp
sudo unzip -d /opt/gradle /tmp/gradle-${VERSION}-bin.zip
sudo apt install unzip
sudo unzip -d /opt/gradle /tmp/gradle-${VERSION}-bin.zip
sudo ln -s /opt/gradle/gradle-${VERSION} /opt/gradle/latest
sudo vi /etc/profile.d/gradle.sh
sudo chmod +x /etc/profile.d/gradle.sh
source /etc/profile.d/gradle.sh
gradle -v
gradle build
cd build
cd libs

## petclinic example todo
ansible-playbook -i inventory install_metric_types.yml --limit petclinic 
```

## Reload Prometheus configuration 
curl -s -XPOST localhost:9090/-/reload