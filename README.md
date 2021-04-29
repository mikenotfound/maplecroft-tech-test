# maplecroft-tech-test

Welcome to the maplecroft techinical test! This project contains an api only pre-built django application.

Maplecroft is a global risk analytics company that aims to standardise risk across a variety of different issues across the world.
Maplecroft refers to these different issues as "indices", for example we have an enviromental risk called Air Quality. 

The project contains two simple models that represent an issue/index: `Index` and a score in time for that index: `IndexVersion`.

To get started all you need is [Docker](https://docs.docker.com/):

# Getting started

Start the dev server for local development:

```bash
docker-compose up
```

Create a superuser to login to the admin:

```bash
docker-compose run --rm web ./manage.py createsuperuser
```

Load into some data

```bash
docker-compose run --rm web ./manage.py load_data
```

If you need to access the django shell you run 

```bash
docker-compose run --rm web ./manage.py shell
```

---
**Note**

If you need to reload the database at any time simply re-run the load_data command

---


# Tasks

Your task is to update the `index` app to include the following api endpoints (for further details see below) 

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
for the preceding 24 hours and provide a single mean score.

It should accept two range query params that limit the returned scores

```
[{
    id: int,
    name: string,
    averaged_scores: [{
        timestamp: iso_format_string, #12pm,
        score: # average of scores within last 24 hours        
    }]
}]
```

