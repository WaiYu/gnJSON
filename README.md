# gnJSON
A RESTful API runs on your local machine that access [Gracenote](http://www.gracenote.com/), return rich music metadata in JSON format.

# Summary
This web application is a RESTful API that wraps around [Gracenote WebAPI](https://developer.gracenote.com/web-api), and retrieve Gracenote music metadata in JSON format. The goal of this project is to support all four API's Gracenote WebAPI provides - Album search, Album fingerpring, Album toc and Album fetch. Generally, you use the same input parameters as provided by the WebAPI.

Currently, the Album fingerprint part is still under development.

# Quick Start
In order to get Gracenote metadata, you first need a Gracenote Client ID (an API key). Please visit [https://developer.gracenote.com/](https://developer.gracenote.com/) to obtain one.

Also, you will need to install Flask module on your machine to run this web app.

You can simply download both gnapi.py and pygn2.py and start running this web app on your local machine and start querying Gracenote database. For your convenience, few sample calls provided below to get you started.

# Sample Query
(under construction...)

# Credit
Some core functions applied in this project adapted and modified from [pygn (by cweichen)](https://github.com/cweichen/pygn).
