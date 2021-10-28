CS50X - Final Project - CrypToYou

# CrypToYou
#### Video Demo:  <https://www.youtube.com/watch?v=lvi6RCwbyaY>
## Description:

First step of the project was to find how to deploy a Python Flask Application using Heroku. The [Real Python](https://realpython.com/flask-by-example-part-1-project-setup/) was too useful and if you want to learn how to deploy one too, you can find in the link previously added. 

Then, a postgres database was set using [Heroku Tutorial](https://devcenter.heroku.com/articles/heroku-postgresql). I've created a local database to change locally the files, than time after time deploying for a staging part at Heroku. This staging proccess you can learn at the first link above at Real Python. 

After that was time to start the project with Python.

At first i will explain what each file does and then how to use the web application. Let's start by the Static folder.

#### STATIC
Here are 3 files. 

1. The first one is calculator.js. This is a Javascript calculator to calculate Impermanent Loss that will be explained later on. 
I've declared some variables getting the values that the user will input on the application. Then there are some checks to verify if the user input 0 as value or it somewhere in the math the value is None, if any of those are true the function return 1 and a message error will be shown.
If none of those happen, the calculation goes on and with .innerHtml we put the result at the html file.

2. Here is just an image of magnifying glass to represent the search button. I didn't create a folder for images as this is the only image in the project.

3. The CSS styles file where all changes in the page style happens. There are a long way till the end of the file, but each part is separate with comments to know what part is being modified.

    
#### TEMPLATES
Then we have the template folder. The Html files are all in here.

**Add Funds** - Have an input to get a number from the user and a button to submit it to the database.

**Calculator** - Here we have 6 inputs to get from the user numbers. Four of them have onkeyup Event to call the Calculator function(Javascript one explained before), so each change in the input will change the calculation and different numbers will be inserted with .innerHTML.

**History** - The history file is just a table that get values from function that access the database. This function is the "get_history" that was declared at helpers.py. All it does is to get information from database, returnin all vales associated with the user. This is only possible as we use session from flask to keep track of cookies and to know which ID is logged in. 

**Index** - This is the first page when you log in, the "Wallet". Like the history is a file with a table that get values from a function, but this one is called "get_crypto_db" and there is another one called "get_cash"(this one to get the cash value from the database). Both of those functions were declared at index.py.

**Layout** - The layout is the fixed one that all of others are going to extends it. Layout have the navbar, the footer and the header that all pages will use. This was just to not repeat those in all pages.

**Login** and **Register** - Those two files were created with almost the same design, but they differ collors to the user know the difference between creating the account and log in. Those files have inputs to user type their username and password. Those are going to be explained with more details later on.

**Quote** and **Quoted** - This one is the HTML with an input and a submit button. After submit will redirect to quoted. The **Quoted** is a table where we get information from the API provided by CoinMarketCap. To setup the API I've used their documentation [CoinMarketCap Documentation](https://coinmarketcap.com/api/documentation/v1/).

**Trade** - The last one in the list is Trade. Here we have a form with 2 inputs and a submit button. There are some functions declared at "trade.py" to update the database with new information. Buy and sell functions insert whatever was the crypto the user typed in, the only difference is that on sell the number is negative to indicate the sale. The other 2 functions there are "get_user" and "get_cash", as their own name one is to get the user from the database and the other one the cash.

    
#### HELPERS(FUNCTIONS)
Other functions at helpers.py are: 

- Login Required: If the user is logged in and have a session will render the index(Wallet) page, if not, will render the calculator one(First page). 
- Errors: There are lots of errors functions, but the basics are the same, they return a render template with a message, each one for each page defined at the name of the functions.
- Lookup: Will search with the API the symbol that users will type in the forms.

The other .py ones were already explained inside the HTML files text.


To have more details about how to use the web application, the text below will help you to learn about it.

## HOW TO USE THE WEB APPLICATION

CrypToYou is a simulator for enthusiasts in Crypto currencies with the goal for those to practice their knowledges and make trades and know if they would win or lose money when investing in some Cryptos.

    
### Impermanent Loss Calculator
The first page is an **Impermanent Loss Calculator** to calculate possible losses when investing on liquidity pools.
On this page we have 6 inputs: 
- 2 of them are for assets, the user will input a symbol of Crypto(ex: BTC - Bitcoin)
- 2 are for price change, how much in percentage the crypto raised or dropped
- The last 2 are the pool weight, how much in percentage each assest have in the liquidity pool(ex: BTC 70% - ETH 30%). The 2 added must be 100%.

The button "Reset input" is just to turn back to zero the values of Price Change and Pool Weight.

To have access to other pages in the web app the user have to create an account and login.	

### Register
So it brings us to the **Register** page. Here the user will create a simple account with only a username and password. There are 3 inputs here:
- First is to input a Username the user want to(if available, if not will show a message when trying to register that the username was already taken).
- Second is to create a password between 4 and 8 characters. If the users input number of characters less than 4 will prompt a message to input at least 4. If the user tries to input a number greater than 8 the input will not show more than it as is blocked with `minlenght` attribute.
- Third is to confirm the password input on the step before. If both of them don't match, will appear an error to show what is wrong.

To prevent the form won't submit an empty space there are error messages to show the user if some input is empty.

### Login
If everything is right and you click on the register button, you will be redirected to the login page. Here are 2 inputs only:
- First to type your username
- Second to type your password

Here are some error messages too to prevent to not submit empty inputs, besides is another one to advise if the username and password are correct. In the footer of the login container have a link that goes to the register page if the user don't have an account or if want to create another one.

### Index(Wallet)
When clicking on sign in, the user will be redirected to his/her **Wallet**.
If it is the first time the user logged in, the wallet will be empty. So the user have to go at **Trade** page clicking on navbar with the respective name.

    
### Trade
In the **Trade** page the user can buy or sell Crypto with price updated in real time by an API provided for free by CoinMarketCap. Here are 2 inputs:
    - First the user input the Symbol of crypto he wants to buy(ex: ADA), if he wants to buy cardano.
    - Secont to input number of shares he wants to buy.

If the user let one of those inputs empty, a message will appear to show what was wrong, here are some particularities for the errors that we will list for you:
    - If the user tries to buy a Crypto the costs more than have in the wallet (The initial is $1000,00 USD - You can add funds, know how later in this README) will prompt a error "You can't afford...". So it means you will have to add more funds to your wallet.
    - If tries to sell more than he have in the wallet, will prompt "You don't have enough...". So you have to buy more stocks before selling it.
    - The shares input must be a positive integer else will promt "Should input a positive number".
    - If input a symbol that does not exist at CoinMarketCap API or is misspelled will prompt "The token did not exist on our Database". Here we reccomend to verify if the symbol was misspelled, if not this symbol does not exist on the API and you can't buy the specific one.

If the inputs are correct, when clicking on buy or sell you will be redirected to ""Wallet**'s page again, but now is not empty anymore. The wallet will show all of Crypto you have bought. In case of buying 1 and selling 1, wallet will be empty as only shows how many you have at the moment. To know about all transactions made you have to click at **History**.

### History
When clicking on **History** a table will be shown with all transactions made. Here you can know what symbol you have trade, how many shares per each trade you've bought or sold(if sold, the number will be negative), the price you bought and the date with hour when you made the trade.

    
### Quote
Another page in the web app is the **Quote**. Here you can search for the Crypto you want and as the trade page, if the Crypto you are searching for is not in our database an error message will appear. 
There are lots of good informations when searching in the **Quote** page as: 
    - Name
    - Symbol
    - Total Supply
    - Max Supply
    - Rank
    - Price
    - Market Cap

All you need to do is type the Crypto symbol(ex: symbol = BTC ; name = Bitcoin) and click on the image for search.

    
### Add Funds
The last one feature but not less important is the Add Funds that was mentioned at the beginning. The page is simple and have 1 only input to type a number of USD amount you want to add to your wallet. Remember that the MaxValue is 100000000, so if you try to add more than that will receive a message advising you the limit. To add you click in the button "Add Funds" and if you be redirected for your wallet, the funds were added successfully.

After all, if you want to stop and logout, just go at the top-right on your screen and click on the "Log Out" button. So you're going to be redirected to the Calculator page again, our first page. 

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
    
Thanks to read our tutorial, we hope you enjoy! And if you have some features you want to see, some issues when using it or want to be part and modify some parts of the project, feel free to contact-me at [GitHub](https://github.com/limaricardo).

