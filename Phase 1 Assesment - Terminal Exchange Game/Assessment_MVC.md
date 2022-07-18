# Phase 1 Assessment: Terminal Exchange Game

### Description

* We will be building a terminal stock trader game using MVC architecture. 
* Our game is going to give users a starting amount of money - maybe $100,000? and let them buy and sell stocks based on the current market info we get from the Yahoo Finance API. (https://rapidapi.com/apidojo/api/yahoo-finance1/endpoints) # use any other finance api of your choice if required 

### Objectives

##### Part 1 - Play with the Api 

* We'll be using the Yahoo-Finance-Api
* We will be pulling data from this API in JSON format.

* Timezone_search: takes a ExchangeTimezone name and returns some basic data. 
    * Full exchange name 
    * symbol
    * quoteType
    * marketPrice
    * tradeable
    * region
    * marketPriceClose 

##### Part 2 - Set up your database

* Persist your database with the above fields. (SQLITE3)
* Create a users database with username and password.
* Design a schema. What kind of relationship will these tables have?

##### Part 3 - Game Functionality

* Users should be able to
    * search companies and get the exact exchange symbol
    * log in with a username and password
    * buy and sell stock
        * buying should subtract from their funds, they cannot spend more money then what they have
        * selling will add to their funds, they cannot sell more stocks then what they have
        * users should be buying and selling at the current rate of the market price
    * view their "portfolio"        self.name = name
        * what are their current earnings
        * view their list of exchanges w.r.t buy/sell

##### Part 4 - Admin

* Create a superuser who can see a leaderboard that displays the top ten users by portfolio earnings. 


