Войти в контейнер
docker exec -it 9e2bdaeb0dcf bash

curl --header "Content-Type: application/json" --request POST --data '{"flower":"1,2,3,7"}' http://localhost:5000/iris_post/

curl.exe --header 'Content-Type: application/json' --request POST http://localhost:5000/iris_post/ --data '{\"flower\":\"12,2,3,7\"}'