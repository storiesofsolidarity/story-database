API Documentation
====

Using the [django-rest-framework](http://www.django-rest-framework.org), this API is meant to be explorable and self-discoverable. It can be browsed at [http://app.storiesofsolidarity.org/api/](http://app.storiesofsolidarity.org/api/).

## GET /api

```
HTTP 200 OK
Vary: Accept
Content-Type: application/json
Allow: GET, HEAD, OPTIONS

{
    "story": "https://app.storiesofsolidarity.org/api/story/",
    "state": "https://app.storiesofsolidarity.org/api/state/",
    "county": "https://app.storiesofsolidarity.org/api/county/",
    "location": "https://app.storiesofsolidarity.org/api/location/",
    "author": "https://app.storiesofsolidarity.org/api/author/",
    "search": "https://app.storiesofsolidarity.org/api/search/"
}
```

## /api/story

Returns a StoryViewSet, with Story objects filtered for display=True and ordered by creation date, descending.
Accepts `?state` (two-character abbreviation) `?state_name` (full name, capitalization required) and `?zipcode` (5 digits only) parameters to filter further by geography. Includes Author information, to avoid multiple lookups. 

Results are encapsulated in a list, with count and pagination metadata.

example GET

```
HTTP 200 OK
Vary: Accept
Content-Type: application/json
Allow: GET, POST, HEAD, OPTIONS

{
    "count": 335,
    "next": "https://app.storiesofsolidarity.org/api/story/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1120,
            "created_at": "2017-08-25T18:18:00.018876Z",
            "updated_at": "2017-08-25T18:18:09.085196Z",
            "location": {
                "id": 824,
                "zipcode": "94612",
                "city": "Oakland",
                "county": "Alameda",
                "state": "CA",
                "lon": -122.2708,
                "lat": 37.80437
            },
            "content": "I love stories of solidarity!",
            "photo": "",
            "author": {
                "id": 731,
                "user": {
                    "id": 734,
                    "first_name": "Anonymous",
                    "last_name": "SMS#10"
                },
                "photo": null,
                "employer": null,
                "occupation": null,
                "employed": true,
                "part_time": false,
                "anonymous": false
            },
            "anonymous": false
        },
    ]
}
```


Creates a new story with either an anonymous author, or one authenticated via a login token. Only accepts requests from domains in settings.CORS_ORIGIN_WHITELIST. Returns newly created story response.

example POST

```
{
    "name": "Josh Levinger",
    "occupation": "web developer",
    "employer": "Spacedog XYZ",
    "location.city": "Oakland",
    "location.county": "Alameda",
    "location.state": "CA",
    "content": "this is a test story"
}

```

example response

```
{
    "id": 1121,
    "created_at": "2017-12-19T19:37:46.421014Z",
    "updated_at": "2017-12-19T19:37:46.421075Z",
    "location": {
        "id": 824,
        "zipcode": "94612",
        "city": "Oakland",
        "county": "Alameda",
        "state": "CA",
        "lon": -122.2708,
        "lat": 37.80437
    },
    "content": "this is a test story",
    "photo": "",
    "author": {
        "id": 779,
        "user": {
            "id": 1,
            "first_name": "Josh",
            "last_name": "Levinger"
        },
        "photo": null,
        "employer": "Spacedog XYZ",
        "occupation": "web developer",
        "employed": true,
        "part_time": false,
        "anonymous": false
    },
    "anonymous": false
}
```

## /api/state

Returns a read-only StateStoriesViewSet, including story counts for all states and a short preview for initial display. Lengths are limited by sos.serializers.STORY_PREVIEW_MAX_COUNT, STORY_PREVIEW_MAX_LENGTH

example GET

```
HTTP 200 OK
Vary: Accept
Content-Type: application/json

{
    "count": 39,
    "next": null,
    "previous": null,
    "results": [
        {
            "abbr": "AL",
            "name": "Alabama",
            "story_count": 3,
            "preview": [
                "I recently purchased a firearm at walmart store 0287 and I feel as if i was accused of a crime and b",
                "I am currently an associate at store 0681 in Guntersville Al. Though my story is long I have to keep",
                "My name is Tammi Cannon i worked at the 0766 store in Florence Alabama for almost 5 years and was le"
            ]
        },
        ...
    ]
}
```

## /api/county

Returns a read-only CountyStoriesViewSet, paginated in sets of 100, optionally filtered by `?state_name`. Results include story counts for counties and a short preview for initial display. Lengths are limited by sos.serializers.STORY_PREVIEW_MAX_COUNT, STORY_PREVIEW_MAX_LENGTH. Pagination is controlled by sos.pagination.MediumResultsSetPagination.page_size

example GET

```
HTTP 200 OK
Vary: Accept
Content-Type: application/json

{
    "count": 117,
    "next": "https://app.storiesofsolidarity.org/api/county/?page=2",
    "previous": null,
    "results": [
        {
            "name": "Alameda County",
            "story_count": 2,
            "preview": [
                "As a freelancer, I depend on the CoveredCA marketplace to buy health insurance. It can be expensive,",
                "I love stories of solidarity!"
            ]
        },
        ...
    ]
}
```

## /api/location

Returns a read-only LocationStoriesViewSet, paginated in sets of 1000, optionally filtered by `?state` abbreviation, `?state_name` or `?county`. Results include story counts by zipcode.  Pagination is controlled by sos.pagination.LargeResultsSetPagination.page_size

example GET

```
HTTP 200 OK
Vary: Accept
Content-Type: application/json
Allow: GET, HEAD, OPTIONS

{
    "count": 170,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 835,
            "zipcode": "95616",
            "city": "Davis",
            "state": "CA",
            "lon": -121.64,
            "lat": 38.48,
            "story_count": 8
        },
        ...
    ]
}
```

## /api/author

Returns a read-only AuthorViewSet. Authors can be marked anonymous in the database, which will limit display of their name, but not location or story text.

example GET
```
HTTP 200 OK
Vary: Accept
Content-Type: application/json
Allow: GET, HEAD, OPTIONS

{
    "count": 325,
    "next": "https://app.storiesofsolidarity.org/api/author/?page=2",
    "previous": null,
    "results": [
        {
            "id": 728,
            "user": {
                "id": 731,
                "first_name": "Vermont",
                "last_name": "Workers' Center"
            },
            "photo": null,
            "employer": null,
            "occupation": null,
            "employed": true,
            "part_time": false,
            "anonymous": false
        },
        ...
    ]
}
```


## /api/search

Simple full-text search on the `?content` parameter, using Postgres icontains. Facets and ts-vector searches are possible, but not implemented.

example GET

```
HTTP 200 OK
Vary: Accept
Content-Type: application/json
Allow: GET, HEAD, OPTIONS

{
    "count": 35,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1120,
            "created_at": "2017-08-25T18:18:00.018876Z",
            "updated_at": "2017-08-25T18:18:09.085196Z",
            "location": {
                "id": 824,
                "zipcode": "94612",
                "city": "Oakland",
                "county": "Alameda",
                "state": "CA",
                "lon": -122.2708,
                "lat": 37.80437
            },
            "content": "I love stories of solidarity!",
            "photo": "",
            "author": {
                "id": 731,
                "user": {
                    "id": 734,
                    "first_name": "Anonymous",
                    "last_name": "SMS#10"
                },
                "photo": null,
                "employer": null,
                "occupation": null,
                "employed": true,
                "part_time": false,
                "anonymous": false
            },
            "anonymous": false
        },
        ...
    ]
}
```
