# maplecroft-tech-test

[![Build Status](https://travis-ci.org/maplecroft/maplecroft-tech-test.svg?branch=master)](https://travis-ci.org/maplecroft/maplecroft-tech-test)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

"The maplecroft technical test". Check out the project's [documentation](http://maplecroft.github.io/maplecroft-tech-test/).


The project contains two simple models `Index` and `IndexVersion` that we are going to populate using
the data in .csv

Your tasks are to create the following api endpoints that (for details see below) 

1. `/index/` - this endpoint should return all indices with there associated versions attached
2. `/stats` - this endpoint should return the max, min and median
3. `/{index_id}/windowed?time_from=<iso_string>&time_to=<iso_string>` - this endpoint should return the windowed/average of values

### Task 1 - List indices
This endpoint lists all indices with each index including a `versions` key which is a list
of its associated versions.

```
[{
    id: int
    name: string
    versions:[{score: decimal, timestamp: string, version: int}] 
}]

```

We should be able to sort by `name` and filter by `id`


### Task 2 - Stats
Return a list of stats objects that represent the maximum, minimum and median for each object e.g

```
[{
    id: int
    name: string
    mean: decimal
    max: decimal
    median: decimal
}]

```

### Task 3 - Windowed/Average
A common way to display a large amount of historical data points on a graph is to average over a window.
If we set the window to be a 24h period starting at 12pm (noon) your challenge is to aggregate all values
for this period and provide a single mean.

It should accept two range query params that limit the returned scores

```


```



# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```
