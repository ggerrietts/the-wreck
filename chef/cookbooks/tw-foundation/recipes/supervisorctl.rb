#
# Cookbook Name:: tw-foundation
# Recipe:: supervisorctl


execute "supervisorctl reload" do
    command "/usr/bin/supervisorctl reload"
    user "root"
    action :nothing
end
