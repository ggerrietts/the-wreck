
# default recipe: let's install some niceties
include_recipe 'apt::default'
include_recipe 'firewall::default'
include_recipe 'tw-foundation::web-user'
include_recipe 'tw-foundation::dev-firewall'

package 'vim'
include_recipe "tw-foundation::tooling"

package 'git'

include_recipe 'tw-foundation::traceview'

include_recipe 'tw-foundation::pgclient'
include_recipe 'tw-foundation::python'
