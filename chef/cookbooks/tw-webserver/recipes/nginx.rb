#
# Cookbook Name:: tw-webserver
# Recipe:: nginx

package "nginx-full"

template "/etc/nginx/sites-available/thewreck" do
  source "thewreck.erb"
end

link "/etc/nginx/sites-enabled/thewreck" do
  to "/etc/nginx/sites-available/thewreck"
end

service "nginx" do
  action :restart
end
