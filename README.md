#FIRST TEST FOR THE BLOG !

## RUN SERVER 
flask --app hello run
( if the file is named app.py or wsgi.py, you don’t have to use --app.)
DEBUG : flask --app hello --debug run

## ENDPOINTS 

### REGISTER : 

/api/auth/register // POST // name - email - password

### LOGIN : 

/api/auth/login // POST // email - password

### CREATE UNIVERSE :

/api/universe // POST // if the user is logged : can create an universer (id - titleUniverse - backgroundUniverse - descriptionUniverse)

### GET ALL UNIVERSE :

/api/universe // GET // can see all universes (id - titleUniverse - backgroundUniverse - descriptionUniverse)

### GET 1 UNIVERSE :

/api/universe/<int:id> // GET // if the user is logged : can see his universe and another person's world (id - titleUniverse - backgroundUniverse - descriptionUniverse)

### UPDATE UNIVERSE :

/api/universe/<int:id> // PUT // if the user is logged : can modify his universe (id - titleUniverse - backgroundUniverse - descriptionUniverse)

### POST :

/api/posts // POST / if the user is logged : can post (title - image - imageTitle - content - link)

### GET POST :

/api/posts/<int:user_id> // GET / if the user is logged : can see posts (id - title - image - imageTitle - content - link - user_id) 

### DELETE 1 POST :

/api/posts/<int:post_id> // DELETE // if the user is logged : can delete his post (id - user_id)

### ADD POSTS FROM ANOTHER UNIVERSE : 

/api/posts/<int:post_id>/copy_to_universe/<int:universe_id> // POST // if the user is logged : can add posts to his universe from another one (id - posts_id - universe_id) 

### POST COMMENT :

/api/comments/<int:posts_id> // POST // if the user is logged : can post a comment on a post (user_name - user_id - posts_id - contentComments)

### GET COMMENT :

/api/comments/<int:posts_id> // GET // if the user is logged : can see comments on a post (id - user_name - contentComments - posts_id)

### ADD LIKES :

/api/posts/<int:posts_id>/likes // POST // if the user is logged : can add like on a post (posts_id - likes_count)

### GET COUNT LIKES :

/api/posts/<int:posts_id>/likes // GET // if the user is logged : can see the number of likes per post (posts_id - likes_count)

________________________________________________

# BODY IN POSTMAN : (don't judge the content aha)

{
    "name": "lou",
    "email": "loulou@gmail.com",
    "password": "lou",
    "titleUniverse": "my super universe",
    "backgroundUniverse": "image",
    "descriptionUniverse": "it's an amazing universe",
    "title": "dolphins everywhere",
    "image": "image",
    "imageTitle": "dolphin, yes",
    "content": "Dolphins are highly intelligent marine mammals and are part of the family of toothed whales that includes orcas and pilot whales.",
    "link": "hohohohohohoho",
    "contentComments" : "yoooooo, j'adore trop et encore plus"
}








