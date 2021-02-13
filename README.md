# theatre-api
## Steps to run a local server

1. Make migrations
```shell
python manage.py makemigrations
```
2. Apply migrations
```shell
python manage.py migrate
```
3. Run server
```shell
python manage.py runserver
```

## API Info

### 1. Occupy a seat - [Endpoint URL - /occupy/ ]
This endpoint will be given the person's name and ticket ID (this should be a UUID field, tickets will not contain information about the seat number beforehand) as input and outputs the seat number which will be occupied.

If the seating is full, the appropriate error message is returned.

#### Example
```shell
curl -v -H "Content-Type: application/json" -X POST -d '{"name":"Foobar","ticketID":"91d5a57c-052b-47e8-8c63-0d77557dcb00"}' http://127.0.0.1:8000/seat/occupy/
```

### 2. Vacate a seat - [Endpoint URL - /vacate/ ]
This endpoint takes the seat number which the person will be vacating and frees that slot up to be used by other people.

#### Example
```shell
curl -v -H "Content-Type: application/json" -X DELETE -d '{"seatNum":2}' http://127.0.0.1:8000/seat/vacate/
```
### 3. Get information of a person/seat - [Endpoint URL - /get_info/\<NAME or SEATNUM or TICKETID\> ]
This endpoint can take either the seat number or person’s name or ticket ID for the input and returns the person’s name, ticket ID, and slot number.

#### Examples
1. Get information using a seat number
```shell
curl -i -H "Accept: application/json" 'http://127.0.0.1:8000/seat/get_info/1'
```

2. Get information using a person's name
```shell
curl -i -H "Accept: application/json" 'http://127.0.0.1:8000/seat/get_info/Foobar'
```

3. Get information using a ticket ID
```shell
curl -i -H "Accept: application/json" 'http://127.0.0.1:8000/seat/get_info/91d5a57c-052b-47e8-8c63-0d77557cbaa1'
```
