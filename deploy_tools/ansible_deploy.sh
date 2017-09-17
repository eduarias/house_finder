#!/usr/bin/env bash
ansible-playbook -i inventory.ansible provision.ansible.yaml --limit=staging --tags deploy --ask-become-pass