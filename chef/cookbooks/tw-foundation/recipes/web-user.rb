
wgrp = node["wreck"]["group"]
wusr = node["wreck"]["user"]
wdir = node["wreck"]["homedir"]
wpwd = node["wreck"]["password"]

rgrp = node["wreck"]["web_group"]
rusr = node["wreck"]["web_user"]

group rgrp do
    not_if "grep '^#{rgrp}:' /etc/group"
end

user rusr do
    group rgrp
    system true
    shell '/bin/bash'
    not_if "grep '^#{rusr}:' /etc/passwd"
end

group wgrp do
    not_if "grep '^#{wgrp}:' /etc/group"
end

user wusr do
    group wgrp
    shell '/bin/bash'
    password wpwd
    not_if "grep '^#{wusr}:' /etc/passwd"
end

directory wdir do
    group wgrp
    user wusr
    not_if { File.exist?(wdir) }
end

directory "#{wdir}/.ssh" do
  mode '0700'
  group wgrp
  user wusr
  not_if { File.exist?("#{wdir}/.ssh") }
end

cookbook_file "#{wdir}/.ssh/authorized_keys" do
  mode '0600'
  group wgrp
  user wusr
  source "authorized_keys"
  not_if { File.exist?("#{wdir}/.ssh/authorized_keys") }
end
