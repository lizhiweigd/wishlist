#!/bin/bash

mkdir settings
cd settings
touch ALLOWED_HOSTS
touch secret.key
echo "True" > DEBUG