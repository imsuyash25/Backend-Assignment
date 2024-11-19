## Installation

To install and set up the Web App, follow these steps:
Clone the repository: 
``` sh
git clone <repository_url>
``` 

* Install the required dependencies 
``` sh
pip install -r requirements.txt
```

## Set up the database

* Run migrations
``` sh
python manage.py makemigrations
python manage.py migrate
```

* Start the development server

```sh
python manage.py runserver
```

# Sample Output

* Create Collection

- API: http://127.0.0.1:8000/collection/

Request Payload
```sh
{
  "title":"First Collection",
  "description":"description",
  "movies":[
    {
      "title":"first movie",
      "description":"description",
      "genres":"comedy",
      "uuid":"123e4567-e89b-12d3-a456-426614174143"
    },
    {
      "title":"second movie",
      "description":"description",
      "genres":"action",
      "uuid":"123e4567-e89b-12d3-a456-426614174242"
    }
    ]
}
```

Response 

``` sh
Status: 201 Created
{
  "collection_uuid": "d3d65338-860d-419b-9bef-9e4384744aaa"
}
```

* Collection Update

- API: http://127.0.0.1:8000/collection/af8e4674-78ef-4c05-9976-d05a6bd61366/

Request Payload

``` sh
{
  "title":"favour6678",
  "description":"updated",
  "movies":[
    {
      "title":"first movie",
      "description":"description",
      "genres":"comedy",
      "uuid":"123e4567-e89b-12d3-a456-426614174323"
    },
    {
      "title":"second movie",
      "description":"description",
      "genres":"action",
      "uuid":"123e4567-e89b-12d3-a456-426614174444"
    }]
}
```

Response 

``` sh
Status: 200 OK
{
  "title": "favour6678",
  "description": "updated",
  "movies": [
    {
      "title": "first movie",
      "description": "description",
      "genres": "comedy",
      "uuid": "123e4567-e89b-12d3-a456-426614174323"
    },
    {
      "title": "second movie",
      "description": "description",
      "genres": "action",
      "uuid": "123e4567-e89b-12d3-a456-426614174444"
    }
  ]
}
```

* Collection Get

- API: http://127.0.0.1:9000/collection/af8e4674-78ef-4c05-9976-d05a6bd61366/

Response 

``` sh
Status: 200 OK
{
  "title": "favour6678",
  "description": "updated",
  "movies": [
    {
      "title": "first movie",
      "description": "description",
      "genres": "comedy",
      "uuid": "123e4567-e89b-12d3-a456-426614174323"
    },
    {
      "title": "second movie",
      "description": "description",
      "genres": "action",
      "uuid": "123e4567-e89b-12d3-a456-426614174444"
    }
  ]
}
```
* Collection Delete

- API: http://127.0.0.1:9000/collection/af8e4674-78ef-4c05-9976-d05a6bd61366/

Response: Success

* Collection Get

- API : http://127.0.0.1:8000/collection/

Response 
```
{
  "is_success": true,
  "data": {
    "collections": [
      {
        "title": "First Collection",
        "uuid": "08d0e86d-104a-4f19-99fb-f8936379a2ab",
        "description": "Description"
      },
      {
        "title": "sixth",
        "uuid": "15d9ffb1-b54f-4c23-b02c-4d567884dd85",
        "description": "description"
      },
      {
        "title": "favour5",
        "uuid": "472b57b8-d5d0-4441-82b7-763cdd503022",
        "description": "description"
      }
    ],
    "favourite_genres": [
      "comedy",
      "action"
    ]
  }
}
```