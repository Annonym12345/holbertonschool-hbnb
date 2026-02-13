```mermaid

classDiagram

class User {
  +UUID id
  +String email
  +String password
  +String first_name
  +String last_name
  +DateTime created_at
  +DateTime updated_at
  +login()
  +logout()
}

class Place {
  +UUID id
  +String name
  +String description
  +Integer number_rooms
  +Integer number_bathrooms
  +Integer max_guest
  +Float price_by_night
  +String city_id
  +String user_id
  +DateTime created_at
  +DateTime updated_at
  +update_availability()
}

class Review {
  +UUID id
  +String text
  +String user_id
  +String place_id
  +DateTime created_at
  +DateTime updated_at
  +editReview()
}

class Amenity {
  +UUID id
  +String name
  +DateTime created_at
  +DateTime updated_at
  +addAmenity()
}

User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : has
Place "0..*" --> "0..*" Amenity : includes
