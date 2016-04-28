#
# Cookbook Name:: tw-database
# Recipe:: createdb

appr = node['wreck']['app_root']
vusr = node['wreck']['user']
venv = node['wreck']['virtualenv']
dusr = node['wreck']['db_user']

execute "run generate db" do
    cwd "#{appr}/src"
    user vusr
    command "#{venv}/bin/python ./gen_db.py"
    # not_if { `sudo -u postgres psql -tAd the_wreck -c \"SELECT count(*) from pg_tables where tableowner='#{dusr}'\" | wc -l`.chomp == "4" }
end
