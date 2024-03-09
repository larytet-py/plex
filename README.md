** Plex 

Based on https://pimylifeup.com/plex-docker/
Get claim token https://www.plex.tv/claim/

    git clone https://github.com/plexinc/pms-docker.git
    mkdir database && mkdir  temp && mkdir media
    docker run -d --name plex --network=host \
    -e TZ="UTC" -e PLEX_CLAIM="claim-XXXXXXXXXXXXXXXX" \
    -v $PWD/database:/config -v $PWD/temp:/transcode -v $PWD/media:/data \
    pms-docker/plexinc/pms-docker

Access http://192.168.68.109:32400/web

 ** Tautulli

Based on https://github.com/Tautulli/Tautulli/wiki/Installation#linux

    git clone https://github.com/Tautulli/Tautulli.git
    sudo addgroup tautulli && sudo adduser --system --no-create-home tautulli --ingroup tautulli
    cd Tautulli
    mkdir data
    docker run -d --security-opt seccomp=unconfined \
    --name=tautulli --restart=unless-stopped \
    -v $PWD/data:/config -e PUID=129 -e PGID=1001 -e TZ=UTC \
    -p 8181:8181 \
    ghcr.io/tautulli/tautulli

Access http://localhost:8181


** Tips

DNS in the container 

    echo '{"dns": ["8.8.8.8", "8.8.4.4", "1.1.1.1"], "max-concurrent-downloads": 3}' | sudo tee /etc/docker/daemon.json
    curl https://plex.tv
