# office-api-test-task

## Test task
It is necessary to make an API for the office. Let's say we have a website where there is an office at some address, there are different rooms, and there are seats in each room. It is necessary to implement all the necessary CRUD operations in order to occupy places there for some time. Show available, look at the employee when and where he was sitting, and so on.

The task specifically says little information to test the candidate's ability to find solutions on his own and ask questions

## Installation Guide  
1. Clone git repository
2. Install a Virtual Environment
3. Install the dependencies
```
python pip install -r requirements.txt
```
4. Apply migrations:
```
python manage.py migrate
```
5. Create superuser:
```
python manage.py createsuperuser
```
6. Run the server:
```
python manage.py runserver
```

## RESTful API
### Structure
In our case, we have four resources, Office, Room, Seat, History.

| Resources   | Endpoint                 | HTTP Method  | CRUD Method | Result                       |
|:------------|:-------------------------|:------------:|:-----------:|:-----------------------------|
| **Office**  | api/v1/office/           |     GET      |    READ     | Get all offices              |
|             | api/v1/office/           |     POST     |   CREATE    | Create new office            |
|             | api/v1/office/:id/       |     GET      |    READ     | Get definite office          |
|             | api/v1/office/:id/       | PUT / PATCH  |   UPDATE    | Update definite office       |
| **Room**    | api/v1/room/             |     GET      |    READ     | Get all rooms                |
|             | api/v1/room/             |     POST     |   CREATE    | Create new room              |
|             | api/v1/room/available/   |     GET      |    READ     | Get room with free seats     |
|             | api/v1/room/:id/         |     GET      |    READ     | Get definite room            |
|             | api/v1/room/:id/         | PUT / PATCH  |   UPDATE    | Update definite room         |
| **Seat**    | api/v1/room/:id/seat/    |     GET      |    READ     | Get seats in definite room   |
|             | api/v1/room/:id/seat/    |     POST     |   CREATE    | Create seat in definite room |
|             | api/v1/seat/             |     GET      |    READ     | Get all seats                |
|             | api/v1/seat/             |     POST     |   CREATE    | Create new seat              |
|             | api/v1/seat/available/   |     POST     |   CREATE    | Get free seats               |
|             | api/v1/seat/:id/         |     GET      |    READ     | Get definite seat            |
|             | api/v1/seat/:id/         |     PUT      |   UPDATE    | Update definite seat         |
|             | api/v1/seat/:id/         |    DELETE    |   DELETE    | Delete definite seat         |
| **History** | api/v1/user/:id/history/ |     GET      |    READ     | Get User history             |

