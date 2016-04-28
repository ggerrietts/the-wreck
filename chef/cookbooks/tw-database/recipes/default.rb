#
# Cookbook Name:: tw-database
# Recipe:: default
#

include_recipe "tw-foundation::default"

include_recipe "tw-database::pgserver"
include_recipe "tw-database::createdb"

