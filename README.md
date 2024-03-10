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

See https://docs.overseerr.dev/getting-started/installation

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

Access http://localhost:5055 . Find the API key in the Settings. You can call the API like this:

    export Overseerr_API_KEY=MTc............==
    curl -H "X-Api-Key: $OVERSEERR_API_KEY" http://localhost:5055/api/v1
    curl -H "X-Api-Key: $OVERSEERR_API_KEY" http://localhost:5055/api/v1/request

## Tips

DNS in the container 

    echo '{"dns": ["8.8.8.8", "8.8.4.4", "1.1.1.1"], "max-concurrent-downloads": 3}' | sudo tee /etc/docker/daemon.json
    docker exec tautulli curl https://plain.tv


Overseerr response to `request` 

```json
{
  "pageInfo": {
    "pages": 1,
    "pageSize": 10,
    "results": 1,
    "page": 1
  },
  "results": [
    {
      "id": 1,
      "status": 2,
      "createdAt": "2024-03-10T15:01:29.000Z",
      "updatedAt": "2024-03-10T15:01:29.000Z",
      "type": "movie",
      "is4k": false,
      "serverId": null,
      "profileId": null,
      "rootFolder": null,
      "languageProfileId": null,
      "tags": [],
      "isAutoRequest": false,
      "media": {
        "downloadStatus": [],
        "downloadStatus4k": [],
        "id": 1,
        "mediaType": "movie",
        "tmdbId": 763215,
        "tvdbId": null,
        "imdbId": null,
        "status": 3,
        "status4k": 1,
        "createdAt": "2024-03-10T15:01:29.000Z",
        "updatedAt": "2024-03-10T15:01:29.000Z",
        "lastSeasonChange": "2024-03-10T15:01:29.000Z",
        "mediaAddedAt": null,
        "serviceId": null,
        "serviceId4k": null,
        "externalServiceId": null,
        "externalServiceId4k": null,
        "externalServiceSlug": null,
        "externalServiceSlug4k": null,
        "ratingKey": null,
        "ratingKey4k": null
      },
      "seasons": [],
      "modifiedBy": {
        "permissions": 2,
        "id": 1,
        "email": "tv@gmail.com",
        "plexUsername": "tv",
        "username": null,
        "recoveryLinkExpirationDate": null,
        "userType": 1,
        "plexId": 334604257,
        "avatar": "https://plex.tv/users/e3ac313e3e1ccd62/avatar?c=1710075448",
        "movieQuotaLimit": null,
        "movieQuotaDays": null,
        "tvQuotaLimit": null,
        "tvQuotaDays": null,
        "createdAt": "2024-03-10T12:57:29.000Z",
        "updatedAt": "2024-03-10T12:57:29.000Z",
        "requestCount": 1,
        "displayName": "tv"
      },
      "requestedBy": {
        "permissions": 2,
        "id": 1,
        "email": "tv@gmail.com",
        "plexUsername": "tv",
        "username": null,
        "recoveryLinkExpirationDate": null,
        "userType": 1,
        "plexId": 334604257,
        "avatar": "https://plex.tv/users/e3ac313e3e1ccd62/avatar?c=1710075448",
        "movieQuotaLimit": null,
        "movieQuotaDays": null,
        "tvQuotaLimit": null,
        "tvQuotaDays": null,
        "createdAt": "2024-03-10T12:57:29.000Z",
        "updatedAt": "2024-03-10T12:57:29.000Z",
        "requestCount": 1,
        "displayName": "tv"
      },
      "seasonCount": 0
    }
  ]
}
```