# 
export $(cat .env | xargs)

docker compose up --build
