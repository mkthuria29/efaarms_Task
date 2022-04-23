# efaarms_Task
#### Steps for running the project:

1. for running server - `docker-compose up`
2. for shell `docker-compose run --service-ports web bash`


#### Steps need to be done initially:

1. do - `docker-compose up`
2. then run `sudo chown -R 1001:1001 data` in the project base directory
3. exec into postgres container and create a database with name `efarms_assignment`
   1. `docker exec -ti efarms_postgres bash`
   2. `psql -U user_name -W password`
   3. `create database efarms_assignment;`
4. then run - `docker-compose up` again all containers should work now
