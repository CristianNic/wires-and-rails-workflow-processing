# Dev manual

### Prerequirments 

1. Clone https://github.com/freen/wires-and-rails-workflow-processing

	git clone git@github.com:freen/wires-and-rails-workflow-processing.git

2. Setup docker and docker compose.

	https://docs.docker.com/install/linux/docker-ce/ubuntu/
	https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-16-04

### Enviroment files

1. Copy `.env.example` file to `.env`. Fill with
	
	PANOPTES_USERNAME=denys.potapov
	PANOPTES_PASSWORD=12345678
	PROJECT_SLUG=rails
	PROJECT_ID=3370
	RQ_DASHBOARD_PASSWORD=nop

2. Load *Subject export* (small link  download your data export) from https://www.zooniverse.org/lab/3370/. And save it as wires-and-rails-subjects.csv to `etc/`.

### Manual test the row segmenation

1. Run docker image (without redis and paralelism): 

	docker-compose -f docker-compose.dev.yml up

It will mount /tmp folder for tests image load and saving results.

2. Run bash to connect to server:

    docker-compose -f docker-compose.dev.yml exec cron-and-queue bash

3. `/tmp` folder in app is shared between container and host. So you 
can place colums files to preview.

4. Run actual script preview:

    cd bin/
    python3 bin/manual_test_rows.py --path /tmp/tele1.png --type tele
    python3 bin/manual_test_rows.py --path /tmp/rails1.png --type rails

This will create folder `/tmp/tele1` with indexed elements. Your probably
will need to change rights to see it on host (ex. `chmod 777 /tmp/19320676.png`)

