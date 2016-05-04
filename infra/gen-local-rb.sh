#!/bin/bash
ROLE=`cat /home/ubuntu/role`
OUT='/home/ubuntu/cookbooks/tw-foundation/attributes/local.rb'
if [ "$ROLE" = "db" ] ; then
  echo -e "default['wreck']['dns_name'] = 'db.wreck.tlys.us'\ndefault['wreck']['db_host'] = 'localhost'\n" >| $OUT
else
  echo -e "default['wreck']['dns_name'] = '$1.wreck.tlys.us'\ndefault['wreck']['db_host'] = 'db.wreck.tlys.us'\n" >| $OUT
fi
