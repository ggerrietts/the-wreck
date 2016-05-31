# The Wreck

Infrastructure and code to support "Diving Into the Wreck".

Slides are available [via Google](https://docs.google.com/presentation/d/1YpgYwy8YPqFHsQ6Br6_DRIKlxC6mxGs-Sd9FfBaudLg/edit?usp=sharing)
or through PyCon's talk archive.

Performance problems highlighted here:

- Slow queries
- Excessive queries
- Noisy neighbor
- Memory fragmentation in Python


## To Replicate

1. create infra/.secret-vars with access_key and secret_key in them.
2. create ./chef/cookbooks/tw-foundation/attributes/secret.rb with wreck.tly_key and wreck.db_password
3. see infra/README.md for instructions on setting up the servers.

URLs are in the slides, but the Flask app is not too complicated.

