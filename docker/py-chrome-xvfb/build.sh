#!/usr/bin/env bash
docker build -t registry.gitlab.com/eduarias/home_crawler/bdd_tests .
docker push registry.gitlab.com/eduarias/home_crawler/bdd_tests
