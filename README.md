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
  - [ ] nginx config
  - [ ] gunicorn config
  - [ ] instrumentation
  - [ ] the apps formidable
- [ ] traffic generation strategy

- [x] Truculent Query
  - [x] big query
- [x] Thousand Selects
- [ ] Noisy Neighbor
- [ ] memory fragmentation
- [ ] remote timeout
- [ ] webserver queueing
- [ ] externalize postgres password
