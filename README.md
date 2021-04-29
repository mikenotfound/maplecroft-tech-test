# maplecroft-tech-test

Welcome to the maplecroft techinical test! This project contains an api only pre-built django application.

Maplecroft is a global risk analytics company that aims to standardise risk across a variety of different issues across the globe.
Maplecroft refers to these issues as "indices", for example we have an environmental risk called Air Quality. 

The project contains two simple models that represent an index (`Index`) and instance in time of that index (`IndexVersion`).
The `IndexVersion` model has a `score` attribute that provides the 0-10 risk score at that particular time.

## Getting started

To get started all you need is [Docker](https://docs.docker.com/):

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


## Tasks

Your task is to update the `index` app to include the following api endpoints (for further details see below) 

1. `/index` - this endpoint should return all indices
2. `/stats` - this endpoint should return the max, min and median for all indices
3. `/{index_id}/windowed?time_from=<iso_string>&time_to=<iso_string>` - this endpoint should return the windowed/average of values

### Task 1 - List indices
This endpoint lists all indices. We should be able to sort by `name` and filter by `id`

```
[{
    id: int
    name: string
}]

```


### Task 2 - Stats
Return a list of stats objects that represent the maximum, minimum and median for each index e.g

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

---
**Note**

For each task please provide some simple unit tests. We don't expect all edge cases to be covered.

---
