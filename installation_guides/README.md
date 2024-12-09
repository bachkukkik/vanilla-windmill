# vanilla-windmill

[Installation Guide](https://www.windmill.dev/docs/advanced/self_host#docker)

```bash
$ cd installation_guides
$ curl https://raw.githubusercontent.com/windmill-labs/windmill/main/docker-compose.yml -o docker-compose.original.yml
$ curl https://raw.githubusercontent.com/windmill-labs/windmill/main/Caddyfile -o Caddyfile.original
$ curl https://raw.githubusercontent.com/windmill-labs/windmill/main/.env -o .env.original

$ docker compose up -d
```