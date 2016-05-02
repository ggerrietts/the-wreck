#
# Cookbook Name:: tw-webserver
# Recipe:: gunicorn
#
# config file, from template
#
template "/etc/init/gunicorn.conf" do
  source "gunicorn.conf.erb"
end

service "gunicorn" do
    action :start
end

