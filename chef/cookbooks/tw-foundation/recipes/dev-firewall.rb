#
# Cookbook Name:: tw-foundation
# Recipe:: dev-firewall
#

if node.environment == "vagrant" then
    firewall_rule "open the pod bay doors" do
        command :allow
    end
end

