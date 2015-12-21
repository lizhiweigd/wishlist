#!/bin/bash

coverage run --source="desirables" --omit="*/tests.py,*/apps.py,*/migrations/*" manage.py test
coverage report -m