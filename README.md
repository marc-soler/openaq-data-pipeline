# Open Air Quality Data Pipeline


docker run -it -p 6789:6789 -v $(pwd):/home/src -e USER_CODE_PATH=/home/src/traffic-collision  mageai/mageai /app/run_app.sh mage start traffic-collision

docker run -it -p 6789:6789 -v $(pwd):/home/src -e USER_CODE_PATH=/home/src/traffic-collision -e KAGGLE_USERNAME=[USERNAME] -e KAGGLE_KEY=[KEY] mageai/mageai /app/run_app.sh mage start traffic-collision