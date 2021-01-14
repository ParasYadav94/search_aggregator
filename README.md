#NAUGE-  search_aggregator

ABOUT 

Search Aggregator


Assignment
  You have been provided with three Shopping site APIs (Paytm, Shopclues and TataCliq) – the
  requirement is to:
    • Build a Django Application that would display a Search Text field and Search Icon button
    • When user enters the search string and clicks on search, then
      -> Search all the three API providers simultaneously (use multi-threading or any other
          strategy) – one API may respond faster than other so you need to display results as
          soon as they arrive – no more and no less than 50 records in a page or all the
          results if less than 50 records returned for APIs combined.
      -> Display Product Name, URL, Image and Price from the API results
      -> Aggregate results into your local database – Product Name, URL, Image and Price are
          the mandatory fields
      -> These APIs use pagination, so you need to ensure all records are retrieved
      -> If the results already exist in local database, update existing records
      -> Display matching records from your local database (first time nothing would be
            there) – You may expose it as another API provider, if required.
You may use any database of your choice and appropriate code in the frontend to optimize the user
experience which is typical of a shopping site.


Commands to run -

1) for creating a virtual enviornment
    ->  python -m venv <env_name>
      
2) Activate the virtual envionrment
    ->  <env_name>\Scripts\activate
      
3) Run migratiosns commands - 
   ->  python manage.py makemigrations
   ->  python manage.py migrate
    
 4) To start the server
   ->  python manage.py runserver   
   
   
 
