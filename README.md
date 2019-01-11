----------------------
URLTester for sitemap
----------------------

Load the sitemap of your website and verify if the pages are up and running.

Prerequisite:
-------------------
- virtualenv
- python 3.6.4 

Install
---------------------
1. Install libraries

    If you are using virtualenv, make sure you are in your environment. 

        pip install -r requirements.txt
    
2.  Setup database
    
        python manage.py makemigrations
        python manage.py migrate

    
3. Setup static files
 
        python manage.py collectstatic
        
4. Run the http server 

        python manage.py runserver

