# Dev manual

To run in dev mode use dev docker:

    docker-compose -f docker-compose.dev.yml up

It will mount /tmp folder for tests

    docker-compose -f docker-compose.dev.yml run cron-and-queue python bin/manual_test_rows.py