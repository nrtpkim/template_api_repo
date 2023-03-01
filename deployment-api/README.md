1. Run script for certs nginx
```
cd scripts
./generate_nginx_server_ssl.sh
```

2. Run: build docker image by using

```
cd face-rec
sudo docker compose -f deployment/prod/docker-compose.build.yaml build
```

start service run this script
```
cd face-rec
sudo docker compose -f deployment/prod/docker-compose.yaml up -d
```


3. Branching strategy:
   - **production** - archived project. project which in production state.
   - **develop** - project in development status. should be runable. contains all of finished features. may different compared to release branch.
   - **feature/{ feature-name in lowercase, dash separate }** - should contain meaningful feature name. should be independent as much as possible.
   - **refactor/{ context in lowercase, dash separate }** - same as feature branch. But no new features introduced in this branch.
   - **bugfix/{ bug-name or id in lowercase, dash separate }** - bugfix prioritized by planing.
   - **hotfix/{ bug-name or id lowercase, dash separate }** - on production bugfix. emergency bugfix.

