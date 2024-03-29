``` mermaid
flowchart LR
OauthProviders(Goole/yandex) 
subgraph Architecture [ ]

    direction LR
    style Architecture fill:#F9F8F8,alignment:left

    User
    Admin
    UsersAdmin
    ETL([ETL service])

    subgraph AuthService [ ]
        style AuthService fill:#DEFDFC

        flask-api(flask \n api \n backend)
        auth-service("AUTH USER #nbsp; #nbsp;")
        user-role-service("USER ROLE #nbsp; #nbsp;")
        token-service(TOKEN CHECK)
        pgusers[(users and \n roles db)]
        redis[(db of invalid\n tokens)]
        checksig("CHECK SIGNATURE")
        checkinvalid("CHECK INVALID")
        oauth-service("OAUTH USER")
        roles-service("MANAGE ROLES")

    end

    subgraph MoviesService [ ]
        fast-api-app(fast api backend)
        fast-api-backend(find movies)
        fast-api-checkcache(Check movies in cache)
        fast-api-cache(Redis cache)
        fast-api-elastic(elasticsearch \n db)
        fast-api-incache{exists}
    end

    subgraph MoviesAdmin [ ]
        style MoviesAdmin fill:#FDE4DE
        django-admin(django admin interface)
        pgfilms[(films \n databasea\n\n)]
    end


    %% user register flow
    User --login/register--> flask-api %%0
    flask-api --> oauth-service
    oauth-service --authorize user in provider--> OauthProviders
    oauth-service --get/create user data--> pgusers
    flask-api --> auth-service
    auth-service --get/create user data--> pgusers

    %%manage roles
    UsersAdmin --manage roles--> flask-api
    flask-api --> roles-service
    roles-service --create/edit/delete roles--> pgusers

    %%manage user roles
    UsersAdmin --manage user roles--> flask-api
    flask-api -->user-role-service
    user-role-service --change user role--> pgusers

    %%check tokens
    flask-api-->token-service
    token-service-->checksig
    checksig-->checkinvalid
    checkinvalid --get invalid--> redis

    %%get films
    User --search/get/list films--> fast-api-app
    fast-api-app --vaildate token--> flask-api
    fast-api-app --> fast-api-backend
    fast-api-backend --> fast-api-checkcache
    fast-api-checkcache --> fast-api-incache
    fast-api-incache --get from cache--> fast-api-cache
    fast-api-incache --get from elastic--> fast-api-elastic
    fast-api-elastic --put to cache--> fast-api-cache

    %%manage films
    Admin --manage films--> django-admin
    django-admin --update films--> pgfilms

    %%ETL
    ETL --get new/changed films--> pgfilms
    ETL --put/update films --> fast-api-elastic


end
    linkStyle 0,1,2,3,4,5 stroke-width:2px,fill:none,stroke:red;
    linkStyle 6,7,8 stroke-width:2px,fill:none,stroke:blue;
    linkStyle 9,10,11 stroke-width:2px,fill:none,stroke:yellow;
    linkStyle 12,13,14,15,17 stroke-width:2px,fill:none,stroke:green;
    linkStyle 26,27 stroke-width:2px,fill:none,stroke:orange;

```