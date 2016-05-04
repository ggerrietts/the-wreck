#!/bin/bash

PATH="${PATH}:/opt/chef/bin:/opt/chef/embedded/bin"
cd /home/ubuntu/the-wreck
git fetch
git pull origin master

cd /home/ubuntu
ROLE=`cat /home/ubuntu/role`
case $ROLE in
  "db") sudo chef-client -z -o "tw-database";;
  "aux") sudo chef-client -z -o "tw-webserver";;
  "web") sudo chef-client -z -o "tw-webserver";;
  *) echo "nothing to do" ;;
esac

