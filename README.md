#FIRST TEST FOR THE BLOG !

## RUN SERVER 
flask --app hello run
( if the file is named app.py or wsgi.py, you don’t have to use --app.)
DEBUG : flask --app hello --debug run

## ENDPOINTS 
REGISTER
______________________REGISTER____________________________

1. /api/auth/register - POST
Request Body:

{
    "name": "user_name",
    "email": "user_email",
    "password": "user_password"
}
Response:

{
    "message": "User registered successfully"
}
Status Code: 201 Created

_______________________LOGIN___________________________

2. /api/auth/login - POST
Request Body:

{
    "email": "user_email",
    "password": "user_password"
}
Response:

{
    "token": "jwt_token"
}
Status Code: 200 OK or 401 Unauthorized with message Invalid email or password

________________________POST UNIVERSE__________________________


3. /api/universe - POST
Request Body:

{
    "titleUniverse": "universe_title",
    "backgroundUniverse": "universe_background",
    "descriptionUniverse": "universe_description"
}
Response:

{
    "message": "This is your universe"
}
Status Code: 201 Created

________________________GET ALL UNIVERSE__________________________

4. /api/universe - GET
Response:

[
    {
        "id": universe_id,
        "titleUniverse": "universe_title",
        "descriptionUniverse": "universe_description",
        "backgroundUniverse": "base64_encoded_background"
    },
    ...
]
Status Code: 200 OK or 404 Not Found with message No universes found

________________________GET 1 UNIVERSE__________________________

5. /api/universe/<int:id> - GET
Response:

{
    "id": universe_id,
    "titleUniverse": "universe_title",
    "descriptionUniverse": "universe_description",
    "backgroundUniverse": "base64_encoded_background"
}
Status Code: 200 OK or 404 Not Found with message No universes found

________________________UPDATE 1 UNIVERSE__________________________

6. /api/universe/<int:id> - PUT
Request Body:

{
    "titleUniverse": "new_title",
    "backgroundUniverse": "new_background",
    "descriptionUniverse": "new_description"
}
Response:

{
    "message": "Mise à jour de l'univers réussie"
}
Status Code: 200 OK, 403 Forbidden with message Vous n'êtes pas autorisé à mettre à jour cet univers, or 404 Not Found with message Utilisateur introuvable

________________________POST A POST__________________________

7. /api/posts - POST
Request Body:

{
    "title": "post_title",
    "imageUrl": "post_image_url",
    "imageTitle": "post_image_title",
    "content": "post_content",
    "link": "post_link"
}
Response:

{
    "message": "Posted !"
}
Status Code: 201 Created

________________________GET POST__________________________

8. /api/posts/<int:user_id> - GET
Response:

{
    "user_id": user_id,
    "posts": [
        {
            "id": post_id,
            "title": "post_title",
            "image": "base64_encoded_image",
            "imageTitle": "post_image_title",
            "content": "post_content",
            "link": "post_link"
        },
        ...
    ]
}
Status Code: 200 OK or 404 Not Found with message No posts found for user with ID {user_id}

_______________________DELETE MY POST___________________________

9. /api/posts/<int:post_id> - DELETE
Response:

{
    "message": "Post deleted successfully"
}
Status Code: 200 OK, 403 Forbidden with message you cannot delete this post, or 404 Not Found with message Post not found

__________________ADD POST TO MY UNIVERSE FROM ANOTHER ONE ____________________

10. /api/posts/<int:post_id>/copy_to_universe/<int:universe_id> - POST
Response:

{
    "message": "Post copied to universe successfully"
}
Status Code: 200 OK or 404 Not Found with messages Source post not found, Target universe not found, or User not found

_______________________COMMENTS___________________________

11. /api/comments/<int:posts_id> - POST
Request Body:

{
    "contentComments": "comment_content"
}
Response:

{
    "message": "Commentaire posté !"
}
Status Code: 201 Created

______________________GET COMMENTS____________________________

12. /api/comments/<int:posts_id> - GET
Response:

[
    {
        "id": comment_id,
        "user_name": "comment_author",
        "contentComments": "comment_content"
    },
    ...
]
Status Code: 200 OK or 404 Not Found with message No comments found for post with ID {posts_id}

_______________________ADD LIKE___________________________

13. /api/posts/<int:posts_id>/likes - POST
Response:

{
    "message": "Post liked successfully"
}
Status Code: 200 OK or 404 Not Found with message Post not found

_________________________GET LIKES OF 1 POST_________________________

4. /api/posts/<int:posts_id>/likes - GET
Response:

{
    "post_id": posts_id,
    "like_count": like_count
}
Status Code: 200 OK


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








