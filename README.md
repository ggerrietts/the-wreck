# The Wreck

Infrastructure and code to support "Diving Into the Wreck".

Performance problems to highlight:

- Noisy neighbor
- Memory fragmentation in Python
- Remote timeout
- Web server queueing

1. create infra/.secret-vars with access_key and secret_key in them.
2. create ./chef/cookbooks/tw-foundation/attributes/secret.rb with wreck.tly_key and wreck.db_password
3. add ./chef/cookbooks/tw-webserver/files/default/oboeware.zip (unreleased Py3K instrumentation)


##TODO

- [x] db server recipe
  - [x] base install
  - [x] schema
  - [x] data
- [x] webserver recipe
  - [x] base install
  - [x] gunicorn config
  - [x] nginx config
  - [x] instrumentation
- [x] traffic generation strategy
- [x] update Packer image
- [x] make terraform spit out nodes

- [x] Truculent Query
  - [x] big query
  - [x] rewrite as SQL
- [x] Thousand Selects
- [x] Noisy Neighbor
  - [x] refactor for better noise
- [ ] memory fragmentation
- [x] externalize postgres password
- [x] postgres server config: listen address in postgresql.conf and auth line in pg_hba.conf
- [x] need to fix the git stuff so it freshens
- [x] nginx logging for latency
