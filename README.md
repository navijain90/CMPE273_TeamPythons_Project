CMPE273: Fantastic Four Project

Project Definition: Trip Planner using Uber vs Lyft's Price Estimation

  - You can plan a trip which consists of a set of places and estimate the total cost between Uber and Lyft.
  - You can have multiple solutions for the given route.
  
  
When we run the project, main.py will be executed and refer.html file will be opened. User need to write source and destination locations in the given text fields. User can add multiple destinations.

Firstly, user need to click button "Get Locations". By clicking this button google map API will populate the latitude and longitude and all the locations will be shown in a map. By having this, User can check whether correct locations are selected or not.

Secondly, user need to click button "Find Cab/Taxi". By clicking this, we are calling Lyft and Uber APIs and the code for the same is written in Lyft.py and Uber.py files.In each file we have written code to calculate price according the user route. To find cost optimum path, we have written code into BusinessLogic.py and try_tsp.py files.
We have used Travel Salesman Algorithm to find cost effective route (which give the best route according to the cost).
We have shown cost effective route only using Uber and Lyft too.

We are storing routes and its cost into database, we have analysed those data and have shown graph representation to show which cab service is best and cost effective. So user will get basic idea which cab to book.

Niche Feature: We are showing mixed solution. For ex user have added source location as A and destinatain locations B, C, D. Sometimes it happens like for A ==> B, Lyft is giving minimum cost. And B ==> C, Uber is giving minimum cost. So, our TSP algorithm works properly with both and shows the best route with minimum cost. This is recommended route according to us as this is the optimum route.

Lastly, we have added text message functionality. So, user will get text message for the optimum route. By having this feature, user does not require to find same route again and again.

So, we have shown routes 
1) Using Uber which is added by user
2) Using Lyft which is added by user
3) Using Uber according to our TSP algorithm (which will show cost effective solution)
4) Using Lyft according to our TSP algorithm (which will show cost effective solution)
5) Using "Lyft - Uber" (which will show optimum route)
