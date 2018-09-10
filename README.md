# House finder
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/600daa8612c243f5a5cf62b677a9e230)](https://www.codacy.com/app/eduarias/house_finder?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=eduarias/house_finder&amp;utm_campaign=Badge_Grade)

Find a house crawling real state portals.
Currently supporting Fotocasa and Habitaclia.

## To run it
```bash
docker-compose up -d
```
The crawling proccess will start and results can be view on http://ip:8000

To run again the crawler for updates just:
```bash
docker-compose up -d crawler
```
