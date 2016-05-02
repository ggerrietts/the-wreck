#
# Cookbook Name:: tw-webserver
# Recipe:: traceview

hdir = node['wreck']['homedir']
tvkey = node['wreck']['tly_key']
vusr = node['wreck']['user']
vgrp = node['wreck']['group']
venv = node['wreck']['virtualenv']

remote_file "#{hdir}/install_appneta.sh" do
  source 'https://files.appneta.com/install_appneta.sh'
  action :create
end

execute "install appneta" do
  cwd hdir
  command "sh ./install_appneta.sh #{tvkey}"
  user "root"
  action :run
end

package 'unzip'

cookbook_file "#{hdir}/oboeware.zip" do
  user vusr
  group vgrp
  source "oboeware.zip"
end

bash "install oboeware" do
  user vusr
  cwd hdir
  code <<-EOH
    unzip oboeware.zip
    mv oboeware-master oboeware
    cd oboeware
    #{venv}/bin/python setup.py install
    EOH
end
