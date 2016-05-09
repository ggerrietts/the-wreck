#!/bin/bash 
DB = $1
ROLE = $2
OUT='/home/ubuntu/cookbooks/tw-foundation/attributes/local.rb'
  echo "default['wreck']['dns_name'] = '${ROLE}.wreck.tlys.us'" >| $OUT
  echo "default['wreck']['db_host'] = 'db.wreck.tlys.us'" >> $OUT
fi
case $ROLE in
  "db") sudo chef-client -z -o "tw-database";;
  "aux") sudo chef-client -z -o "tw-webserver";;
  "web") sudo chef-client -z -o "tw-webserver";;
  "traffic") sudo chef-client -z -o "tw-foundation";;
  *) echo "nothing to do" ;;
esac
