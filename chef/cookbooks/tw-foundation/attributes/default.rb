default['firewall']['allow_ssh'] = true

default['wreck']['http_ports'] = 80

default['wreck']['user'] = 'ubuntu'
default['wreck']['group'] = 'ubuntu'
default['wreck']['homedir'] = '/home/ubuntu'

default['wreck']['web_user'] = 'www-data'
default['wreck']['web_group'] = 'www-data'

default['wreck']['app_root'] = '/home/ubuntu/the-wreck'
default['wreck']['virtualenv'] = '/home/ubuntu/.env'
default['wreck']['github_repo'] = 'git://github.com/ggerrietts/the-wreck.git'

default['wreck']['postgres_password'] = 'funkyjunk'
default['wreck']['db_user'] = 'wreck'

default['wreck']['db_name'] = 'the_wreck'

default['wreck']['pip_requirements'] = '/home/www/wreck/leadpipe/etc/requirements.txt'
