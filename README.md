
# Wikipedia API
An API for accessing page view data for Wikipedia pages

Uses the [Wikimedia PageView API](https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageviews) as the data source

*Grow Therapy Programming Take-Home Project*

## Features
- Retrieve the most viewed articles for a given week
- Retrieve the most viewed articles for a given month
- Retrieve the view count of a specific article for a given week
- Retrieve the view count of a specific article for a given month
- Retrieve the day of a given month where a specific article got the most page views




## How to run server
1. Clone this repository to your local machine
2. Create a Python Virtual Environment (venv)
3. Open the root directory of the project in a terminal (wiki-api) and run the following command to install the required packages:
```
  pip install -r 'requirements.txt'
```
4. Start the server by running the following command in the terminal:
```
flask run
```
To specify a port:
```
flask run -p 5000
```



## API Reference

### Get the most viewed articles for a given week
Returns a list of the most viewed articles for the week of a given date. Cannot be a future week. This uses **Monday** as the start of the week. You can use any date during the week and it will return the entire week's results.

```http
  GET http://127.0.0.1:5000/api/v1/articles/most_viewed/<domain>?year=<year>&month=<month>&day=<day>
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `<domain>` | `string` | The wiki site you want to access data for (ie. *'en.wikipedia'*, *'de.wikipedia'*, *'es.wiktionary'*, etc.) |
| `<year>` | `string` | The year number of the date |
| `<month>` | `string` | The month number of the date |
| `<day>` | `string` | The day number of the date |

Example request to get the most viewed articles during the week with the date of October 19, 2023:
```http
  GET http://127.0.0.1:5000/api/v1/articles/most_viewed/en.wikipedia?year=2023&month=10&day=19
```

### Get the most viewed articles for a given month
Returns a list of the most viewed articles for the given month. Must be a month before (and not including) the current month.

```http
  GET http://127.0.0.1:5000/api/v1/articles/most_viewed/<domain>?year=<year>&month=<month>
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `<domain>` | `string` | The wiki site you want to access data for (ie. *'en.wikipedia'*, *'de.wikipedia'*, *'es.wiktionary'*, etc.) |
| `<year>` | `string` | The year number of the date |
| `<month>` | `string` | The month number of the date |

Example request to get the most viewed articles during the month of October 2023:
```http
  GET http://127.0.0.1:5000/api/v1/articles/most_viewed/en.wikipedia?year=2023&month=10
```

### Get the view count of an article during a given week
Returns the view count of an article for the week of a given date. Cannot be a future week. This uses **Monday** as the start of the week. You can use any date during the week and it will return the entire week's results.

```http
  GET http://127.0.0.1:5000/api/v1/view_count/article/<article_name>/<domain>?year=<year>&month=<month>&day=<day>
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `<article_name>` | `string` | The name of the article |
| `<domain>` | `string` | The wiki site you want to access data for (ie. *'en.wikipedia'*, *'de.wikipedia'*, *'es.wiktionary'*, etc.) |
| `<year>` | `string` | The year number of the date |
| `<month>` | `string` | The month number of the date |
| `<day>` | `string` | The day number of the date |

Example request to get the view count of the 'YouTube' article during the week with the date of April 3, 2021:
```http
  GET http://127.0.0.1:5000/api/v1/view_count/article/YouTube/en.wikipedia?year=2023&month=04&day=03
```

### Get the view count of an article during a given month
Returns the view count of an article for a given month. Must be a month before (and not including) the current month.

```http
  GET http://127.0.0.1:5000/api/v1/view_count/article/<article_name>/<domain>?year=<year>&month=<month>
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `<article_name>` | `string` | The name of the article |
| `<domain>` | `string` | The wiki site you want to access data for (ie. *'en.wikipedia'*, *'de.wikipedia'*, *'es.wiktionary'*, etc.) |
| `<year>` | `string` | The year number of the date |
| `<month>` | `string` | The month number of the date |

Example request to get the view count of the 'Taylor_Swift' article during the month of January 2024:
```http
  GET http://127.0.0.1:5000/api/v1/view_count/article/Taylor_Swift/en.wikipedia?year=2024&month=01
```

### Get the day of a given month where an article got the most page views
Returns an article's highest viewed day in a given month. Must be a month before (and not including) the current month.

```http
  GET http://127.0.0.1:5000/api/v1/max_views/day/<article_name>/<domain>?year=<year>&month=<month>
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `<article_name>` | `string` | The name of the article |
| `<domain>` | `string` | The wiki site you want to access data for (ie. *'en.wikipedia'*, *'de.wikipedia'*, *'es.wiktionary'*, etc.) |
| `<year>` | `string` | The year number of the date |
| `<month>` | `string` | The month number of the date |

Example request to get the highest view day for the 'Bruce_Willis' article during the month of August 2022:
```http
  GET http://127.0.0.1:5000/api/v1/max_views/day/Bruce_Willis/en.wikipedia?year=2022&month=08
```
## Running Tests

To run tests, run the following command in the project root directory

```bash
  pytest
```


## Potential Improvements & Next Steps

- Caching results from 3rd party API
- Use concurrency when summing view count totals where possible
- Mocking 3rd party API calls in tests
- More tests (ie. verifying counts are calculated correctly)
- Logging and storing errors
- Storing API returns in a database


## Author(s)

- [Brandon Claiborne (@bclai7)](https://www.github.com/bclai7)

