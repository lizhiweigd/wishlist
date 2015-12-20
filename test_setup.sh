#!/bin/bash

mkdir settings
cd settings
touch ALLOWED_HOSTS
echo "REALLY INSECURE TESTING KEY" > secret.key
echo "True" > DEBUG