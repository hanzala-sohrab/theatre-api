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

1. **<details><summary><ins>Occupy seat</ins></summary>**
   
    - _Description_: 
        - The Endpoint will be given the person's name and ticket ID (this should be a UUID field, tickets will not contain information about the seat number beforehand) as input. 
        - Output is the seat number which will be occupied.
        - If the seating is full, the appropriate error message is returned 
    - POST `/api/seat/occupy/`
    
        | Parameter  | Description |
        | ------------- | ------------- |
        | `name` **(required)** | Person's name  |
        | `ticketID` **(required)** | Ticket ID (UUID)  |
    
    - **Example**
        ```shell
        # Load the schema document
        coreapi get http://127.0.0.1:8000/docs/
        
        # Interact with the API endpoint
        coreapi action occupy create -p name="Hanzala Foo" -p ticketID="c4c0b2b1-5a1c-4ad9-b643-57b7bc1c2f65"
        ```
    
    - **Result**
        ```json
        {
            "name": "Hanzala Foo",
            "seatNum": 1,
            "ticketID": "c4c0b2b1-5a1c-4ad9-b643-57b7bc1c2f65",
            "status": true
        }
        ```
    </details>


2. **<details><summary><ins>Vacate seat</ins></summary>**
   
    - _Description_: 
        - This endpoint takes the seat number which the person will be vacating and frees that slot up to be used by other people
   
    - GET `/api/seat/vacate/{seatNo}`
    - **Example**
        ```shell
        # Load the schema document
        coreapi get http://127.0.0.1:8000/docs/
        
        # Interact with the API endpoint
        coreapi action vacate delete -p seatNo=1
        ```
    - **Result**
      
        ```json
        {
            "message": "Seat number 1 is now vacant!"
        }
        ```
    </details>
    
    
3. **<details><summary><ins>Get person/seat information using a person's name</ins></summary>**
   
    - GET `/api/seat/get_info/{pName}`
    - **Example**
        ```shell
        # Load the schema document
        coreapi get http://127.0.0.1:8000/docs/
        
        # Interact with the API endpoint
        coreapi action get_info read_1 -p pName="Hanzala1"
        ```
    - **Result**
      
        ```json
        [
            {
                "name": "Hanzala1",
                "seatNum": 3,
                "ticketID": "85b5d736-829c-11eb-8dcd-0242ac130989",
                "status": true
            }
        ]
        ```
    </details>

4. **<details><summary><ins>Get person/seat information using a person's name</ins></summary>**
   
    - GET `/api/seat/get_info/{pName}`
    - **Example**
        ```shell
        # Load the schema document
        coreapi get http://127.0.0.1:8000/docs/
        
        # Interact with the API endpoint
        coreapi action get_info read_1 -p pName="Hanzala1"
        ```
    - **Result**
      
        ```json
        [
            {
                "name": "Hanzala1",
                "seatNum": 3,
                "ticketID": "85b5d736-829c-11eb-8dcd-0242ac130989",
                "status": true
            }
        ]
        ```
    </details>
    
   

5. **<details><summary><ins>Get person/seat information using a ticket ID</ins></summary>**
   
    - GET `/api/seat/get_info/{ticketNo}`
    - **Example**
        ```shell
        # Load the schema document
        coreapi get http://127.0.0.1:8000/docs/
        
        # Interact with the API endpoint
        coreapi action get_info read_0 -p ticketNo="85b5d736-829c-11eb-8dcd-0242ac130989"
        ```
    - **Result**
      
        ```json
        [
            {
                "name": "Hanzala1",
                "seatNum": 3,
                "ticketID": "85b5d736-829c-11eb-8dcd-0242ac130989",
                "status": true
            }
        ]
        ```
    </details>

## Note
The theatre's **MAX_OCCUPANCY** is initially set to 5. It can be changed in the project's settings file ``theatre/settings.py``.