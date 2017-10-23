#!/usr/bin/env bash
ansible-playbook playbook.yml -i hosts/staging/inventory --ask-vault-pass