# Decisions for new service (store and retrive user likes, bookmarks, comments)

## Service strategy
We considered two options:
- extend existing service

Proc|Cons
----|----
re-use auth|more complicated webserver logic
re-use webserver|less overall relaibility, if webserver down - both services unavailable
less overhead for logs collections| -
load generated by new features disdainfully small compare to film timestamp service (in worst case +3 requests to ~7000 requests per 1 film|-

- implemet new service

Proc|Cons
----|----
more simpler webserver logic|re-implementation of auth
-|extra auth requests
-|extra logging


Based on proc and cons above, decided to go with existing service expansion to have benifits of re-using already implemeted auth meckanithm, reducing auth requets. Both services not the most high relable, so relability can be sacrifed. Added load seems to be disdainfully small