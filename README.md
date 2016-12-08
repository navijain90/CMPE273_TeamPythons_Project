#Team: Fantastic Four

##Project : Plan My Trip

  - Plan a trip with multiple locations and this application will calculate the best optimal route with best price comparing       both Uber & Lyft
  - You can have multiple solutions with both user input route as well as optimal.
  - SMS Functionality using Twilio API is added in the application
  - User can analyse trend of comparing the Uber and Lyft from the persistant data that we have strored in Amazon RDS (MySQL)

##Technology Used:
  - Python 
  - Flask micro framework
  - MySQL
  - Bootstrap, HTML5, CSS3, JQuery, Ajax
  
##API Used:
  - Uber 
  - Lyft
  - Twilio
  - Google Map
  - Google Places
  
##Algorithm:
  - Travelling Salesman Problem

##Project Description:
On the home page of our application user needs to enter the source and destinations then click button "Get Locations". By clicking this button google map API will populate the latitude and longitude and all the locations will be shown in a map. By having this, User can check whether correct locations are selected or not.

Secondly, user need to click button "Find Cab/Taxi". By clicking this, we are calling Lyft and Uber APIs and the code for the same is written in Lyft.py and Uber.py files. We are sending all the possible permutation between the given locations so that we can have a detailed price between each permutation of the location.
Once we have recieve the prices, we form a n X n matrix , where n is the number of locations and feed this matrix into our TSP algorithm to calculate the optimal route based on price.
TSP algorithm reads each value in the matrix and calculate the best value to connect all the location according to minimum price. Output of TSP algorithm is a cordinate list. We use this cordiante to find the price from the matrix we prepared earlier.

We are storing routes and its cost into database, we have analysed those data and have shown graph representation to show which cab service is best and cost effective. So user will get basic idea which cab to book.

##Niche Feature:
We are showing optimal path that is combined of both Uber and lyft. For example user has added source location as A and destinatain locations B, C, D. Sometimes it happens like for A ==> B, Lyft is giving minimum cost. And B ==> C, Uber is giving minimum cost. So, our TSP algorithm works properly with both and shows the best route with minimum cost. This is recommended route according to us as this is the optimum route.

Lastly, we have added text message functionality. So, user will get text message for the optimum route. By having this feature, user does not require to find same route again and again.

###Output to the user given input consist of 5 sets of solution (including our recommended solution)
1) Uber solution considering user input route like  A->B->C->D->A (using only Uber)

2) Uber solution considering optimal route based on price like  A->C->D->B->A (using only Uber)

3) lyft solution considering user input route like  A->B->C->D->A (using only lyft)

4) lyft solution considering optimal route based on price like  A->C->D->B->A (using only lyft)

5) Using "Lyft - Uber" (which will show optimum route)
