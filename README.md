# Goals

* Monitor User Requests Through Overseerr: track what media items users are requesting through Overseerr, which is a tool used for managing media requests.
* Calculate Watch Rates with Tautulli: determine the watch rates of these requested items, which involves seeing how much of the requested media users actually watch. Tautulli, a monitoring tool for Plex servers, can provide this information.
* Record Data to a Database: Finally, they want this information (both the requests and the watch rates) to be recorded in a database. This could be for further analysis or reporting.

Essentially, the script would automate the process of collecting data on what users are requesting and how much of it they end up watching, and then store this data for future reference or analysis.


# How to

## Plex 

Based on https://pimylifeup.com/plex-docker/
Get claim token https://www.plex.tv/claim/

    git clone https://github.com/plexinc/pms-docker.git
    mkdir database && mkdir  temp && mkdir media
    docker run -d --name plex --network=host \
        -e TZ="UTC" -e PLEX_CLAIM="claim-XXXXXXXXXXXXXXXX" \
        -v $PWD/database:/config -v $PWD/temp:/transcode -v $PWD/media:/data \
        pms-docker/plexinc/pms-docker

Access http://192.168.68.109:32400/web

## Tautulli

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


## Overseerr

    mkdir -p overseer/config
    docker run -d \
        --name overseerr \
        -e LOG_LEVEL=debug \
        -e TZ=UTC \
        -e PORT=5055 `#optional` \
        -p 5055:5055 \
        -v $PWD/overseer/config:/app/config \
        --restart unless-stopped \
        sctx/overseerr

Access http://localhost:5055

## Tips

DNS in the container 

    echo '{"dns": ["8.8.8.8", "8.8.4.4", "1.1.1.1"], "max-concurrent-downloads": 3}' | sudo tee /etc/docker/daemon.json
    docker exec tautulli curl https://plain.tv
