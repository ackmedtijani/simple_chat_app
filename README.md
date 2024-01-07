# simple_chat_app
Simple_chat_app

###

A chat app API that is used to send peer-to-peer messages. 
Users who communicate have to do so in a room. The users need to obtain a room.id by calling a specific endpoint to get a room.id. The room id is then used to connect to a specific websocket route. 
The APP has a read-receipt feature. An separate endpoint is used to send the read-receipt status of a message to another peer. 

For you to create a room and access the websockets endpoints, an api token is needed. A unique email is needed to create an api token. 

### Endpoints: 

### HTTP

CREATE ROOM ENDPOINT:

localhost/create_room/ POST request
token is passed in the header. and room_name is sent as a body of the request.  

room id is given as the response. 

localhost/create_token/ POST request
email is passed as the body of the request. api token gotten from the response

### Websockets. 

localhost/ws/chat/ROOM_ID/API_TOKEN/
Websockets route that would used to make a peer-to-peer connection to send and receive messages. 

localhost/ws/read_receipt/API_TOKEN/
Websockets route that would be used to make a peer-to-peer connection to send and receive read_receipt status. 


