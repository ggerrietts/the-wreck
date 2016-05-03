#
# Cookbook Name:: tw-foundation
# Recipe:: dev-firewall
#

if node.environment == "vagrant" then
    firewall_rule "open the pod bay doors" do
        command :allow
    end
else
    firewall_rule "open up http" do
      port 80
      protocol :tcp
      position 1
      command :allow
    end
end

