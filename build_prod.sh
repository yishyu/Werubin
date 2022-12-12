GIT_SSH_COMMAND='ssh -i /home/ubuntu/.ssh/id_rsa_werubin -o IdentitiesOnly=yes' git pull

docker-compose -f docker/docker-compose.yml -p werubin up --build -d
docker-compose -f docker/docker-compose.yml -p werubin exec web poetry run /srv/manage.py collectstatic --no-input --clear
docker-compose -f docker/docker-compose.yml -p werubin exec web poetry run /srv/manage.py migrate --no-input
docker-compose -f docker/docker-compose.yml -p werubin restart nginx