# Dev manual

To run in dev mode use dev docker:

    docker-compose -f docker-compose.dev.yml up

It will mount /tmp folder for tests. Run bash

    docker-compose -f docker-compose.dev.yml exec cron-and-queue bash

You can run manual tests:

    cd bin/
    python3 manual_test_rows.py
