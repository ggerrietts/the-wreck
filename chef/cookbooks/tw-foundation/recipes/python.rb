#
# Cookbook Name:: tw-foundation
# Recipe:: python

vusr = node['wreck']['user']
vgrp = node['wreck']['group']
venv = node['wreck']['virtualenv']
appr = node['wreck']['app_root']
repo = node['wreck']['github_repo']
share = node['wreck']['shared_folder']

python_runtime "3"

python_virtualenv venv do
    python "3"
    user vusr
    group vgrp
end

execute "chown-venv" do
  command "chown -R #{vusr}:#{vgrp} #{venv}"
  user "root"
  action :run
end


if node.chef_environment == 'vagrant' then
    link appr do
        to share
        only_if { File.exist?(share) }
        not_if { File.exist?(appr) }
    end
else
    git appr do
        repository repo
        action :checkout
        user vusr
        group vgrp
        not_if { File.exist?(appr) }
    end
end

pip_requirements "#{appr}/src/requirements.txt" do
    user vusr
    group vgrp
    virtualenv venv
end
