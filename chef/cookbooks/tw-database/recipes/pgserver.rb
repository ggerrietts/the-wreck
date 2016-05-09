#
# Cookbook Name:: tw-database
# Recipe:: pgserver
#
# Copyright (c) 2016 The Authors, All Rights Reserved.
#

dusr = node['wreck']['db_user']
dpss = node['wreck']['db_password']
ppss = node['wreck']['postgres_password']
db = node['wreck']['db_name']

package 'postgresql'
package 'postgresql-contrib'

# change postgres password
execute "change postgres password" do
  user "postgres"
  command "psql -c \"alter user postgres with password '#{ppss}';\""
end

# create new postgres user
execute "create new db user" do
    user "postgres"
    command "psql -c \"create user #{dusr} with createdb password '#{dpss}';\""
    not_if { `sudo -u postgres psql -tAc \"SELECT * FROM pg_roles WHERE rolname='#{dusr}'\" | wc -l`.chomp == "1" }
end

# create new database
execute "create new db" do
    user "postgres"
    command "psql -c \"create database #{db} owner #{dusr};\""
    not_if { `sudo -u postgres psql -tAc \"SELECT 1 FROM pg_database WHERE datname='#{db}'\" | wc -l`.chomp == "1" }
end

firewall_rule 'open up pgsql' do
  command :allow
  port 5432
end

cookbook_file "/etc/postgresql/9.3/main/postgresql.conf" do
  source "postgresql.conf"
  user "postgres"
  group "postgres"
  mode '0640'
  notifies :restart, 'service[postgresql]', :delayed
end

cookbook_file "/etc/postgresql/9.3/main/pg_hba.conf" do
  source "pg_hba.conf"
  user "postgres"
  group "postgres"
  mode '0640'
  notifies :restart, 'service[postgresql]', :delayed
end
