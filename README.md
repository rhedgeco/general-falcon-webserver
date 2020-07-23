# general_falcon_webserver
A wrapper for the falcon api that allows for creating websites in a simpler way.

Automatically does all routing and handling for serving html pages and 404 handling.
Adds an api for easily dealing with Sqlite databases and connecting them to your website.

Example Static Webpage.
```python
from general_falcon_webserver import WebApp, SqliteDatabase

app = WebApp('frontend') # Specify the folder with index.html and all frontend resources

# Databases can be added with this command
# db = SqliteDatabase('example-database-name')

# Routes for api calls can be added as such
# This automatically concatenates /api/ to the beginning of the path
# app.add_route('resource_path', Resource)

app.launch_webserver()
```