#!/bin/bash

OUT='../chef/vendor/tw-foundation/attributes/local.rb'
if [ "$1" = "db" ] ; then
  echo -e "default['wreck']['dns_name'] = 'db.wreck.tlys.us'\ndefault['wreck']['db_host'] = 'localhost'\n" >| $OUT
else
  echo -e "default['wreck']['dns_name'] = '$1.wreck.tlys.us'\ndefault['wreck']['db_host'] = 'db.wreck.tlys.us'\n" >| $OUT
fi
