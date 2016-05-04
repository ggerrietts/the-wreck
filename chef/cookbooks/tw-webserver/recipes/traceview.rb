#
# Cookbook Name:: tw-webserver
# Recipe:: traceview

hdir = node['wreck']['homedir']
tvkey = node['wreck']['tly_key']

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

