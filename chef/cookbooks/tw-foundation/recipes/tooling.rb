#
# Cookbook Name:: tw-foundation
# Recipe:: tooling
# This recipe is about installing some niceties.
# Currently it sets up a modest .vimrc and .bashrc

vusr = node['wreck']['user']
vgrp = node['wreck']['group']

cookbook_file "/home/#{vusr}/.bashrc" do
    user vusr
    group vgrp
    source "bashrc"
end


cookbook_file "/home/#{vusr}/.vimrc" do
    user vusr
    group vgrp
    source "vimrc"
end
