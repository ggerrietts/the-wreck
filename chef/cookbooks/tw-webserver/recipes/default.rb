#
# Cookbook Name:: tw-webserver
# Recipe:: default
#
# Copyright (c) 2016 The Authors, All Rights Reserved.
#
include_recipe "tw-foundation::default"

vusr = node['wreck']['user']
vgrp = node['wreck']['group']

directory "/deploy" do
    user vusr
    group vgrp
end

include_recipe "tw-webserver::traceview"
include_recipe "tw-webserver::nginx"
include_recipe "tw-webserver::gunicorn"

