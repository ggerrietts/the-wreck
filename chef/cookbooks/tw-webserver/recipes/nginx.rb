#
# Cookbook Name:: tw-webserver
# Recipe:: nginx

package "nginx-full"

service 'nginx' do
    supports :restart => true, :start => true, :stop => true
    action :nothing
end

template "/etc/nginx/sites-available/thewreck" do
  source "thewreck.erb"
  notifies :restart, 'service[nginx]', :delayed
end

link "/etc/nginx/sites-enabled/thewreck" do
  to "/etc/nginx/sites-available/thewreck"
  notifies :restart, 'service[nginx]', :delayed
end

file "/etc/nginx/sites-enabled/default" do
  action :delete
  notifies :restart, 'service[nginx]', :delayed
end

cookbook_file "/etc/nginx/nginx.conf" do
  source "nginx.conf"
  notifies :restart, 'service[nginx]', :delayed
end

