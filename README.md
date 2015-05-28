## gnJSON
A RESTful API interface that runs on your local machine to access [Gracenote](http://www.gracenote.com/), return rich music metadata in JSON format.

## Summary
This web application is a RESTful API that wraps around [Gracenote WebAPI](https://developer.gracenote.com/web-api), retrieves Gracenote music metadata and returns in JSON format. The goal of this project is to support all four API's Gracenote WebAPI provides - Album search, Album fingerpring, Album toc and Album fetch. You simply use the same input parameters as you do for the WebAPI.

Currently, the Album fingerprint part is still under development.

## Installation
In order to get Gracenote metadata, you first need a Gracenote Client ID (an API key). Please visit [https://developer.gracenote.com/](https://developer.gracenote.com/) to obtain one.

Also, you will need to install Flask module on your machine to run this web app.

You can simply copy both gnapi.py and pygn2.py to your local folder, execute python gnapi.py to run this web app on your local machine, and start querying Gracenote database. For your convenience, few sample calls provided below to get you started.

## Quick Guide on API's
**/register**

Required input: client
 
**/album_search**

Required input: client, user, artist and/or album_title and/or track_title (at least one of the three)


**/album_toc**

Required input: client, user, toc

**/album_fetch**

Required input: client, user, gn_id
***Optional parameter*** for album_search, album_toc and album_fetch:

lang, country, mode, *range, cover_size, fallback_genrecover, select_extended, select_detail

Please refer to the Gracenote [WebAPI documentation](https://developer.gracenote.com/web-api) for values accepted on optional inputs.

*Note: when using optional **range** parameter, you only specify the starting count of the returned metadata. The interface will form the query to get next 10 matching results starting from the count you provided.

## Sample Query
**Album Search API**

    http://127.0.0.1:5000/album_search?client=XXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX&user=XXXXXXXXXXXXXXXXXXXXXXXXX&artist=pink%20floyd&select_extended=genre,mood,tempo,artist_oet&select_detail=GENRE:3LEVEL,MOOD:2LEVEL,TEMPO:3LEVEL,ARTIST_ORIGIN:4LEVEL&range=22

Parameters used in query above: client, user, artist, select_extended, select_detail, range.

And the returned metadata is in the format below:

    {
      RESPONSE: {
        ALBUM: {
          1: {
            TRACK_COUNT: "13",
            TITLE: "The Wall [Disc 1]",
            GN_ID: "6976288-E5DB6C606D4FAB823E9788B36C7EE05C",
            ARTIST: "Pink Floyd",
            GENRE: {
              1: {
                GENRE: "Rock",
                ORD: "1",
                NUM: "61341",
                ID: "25313"
              },
              2: {
                GENRE: "70's Rock",
                ORD: "2",
                NUM: "61365",
                ID: "25333"
              },
              3: {
                GENRE: "Classic Prog",
                ORD: "3",
                NUM: "61634",
                ID: "25500"
              }
            },
            PKG_LANG: "ENG",
            DATE: "1979",
            ORD: "1",
            TRACK: {
              1: {
                GN_ID: "6976289-1BF00C23F4FF770936AA7C1B7F7B6AA3",
                TRACK_NUM: "1",
                TITLE: "In The Flesh?"
              },
              ...(returned track metadata truncated)...
            }
          },
          ...(returned album metadata truncated)...
        },
        STATUS: "OK",
        RANGE: {
          COUNT: "4949",
          START: "22",
          END: "32"
        }
      }
    }


## Credit
Some core functions applied in this project adapted and modified from [pygn (by cweichen)](https://github.com/cweichen/pygn).
