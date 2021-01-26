# NCCU GPA Calculator
This is an open source project for calculating NCCU (National Chengchi University) students' GPA (Grade Point Average), <br>
including cumulative, major and last 60 GPA.<br>
The goal of this project is to benefit those students of NCCU who need these GPA information but can only use online GPA calculators which you have to type in <br>
course names, credits, and scores all by yourself which is very inconvenient!<br>
Feel free to fork this project and produce your own GPA calculator for your school!<br>
歡迎fork這個專案，並開發成符合自己學校格式的GPA計算器。

**Website**: https://nccu-gpa-calculator.herokuapp.com

## Deployment

### Deploy Locally

All the deployment is done in one line. Visit `localhost:5000` to see the results.

```
docker-compose up -d
```

If you would like to build and parse all the articles from scratch, set `BUILD_FROM_SCRATCH` to `True` in the `settings.py` file. Building from scratch takes around a minute.


### Deploy on Heroku
```
heroku apps:create ptt-studyabroad-api
heroku addons:create heroku-postgresql:hobby-dev
heroku stack:set container
git push heroku master 
```

## Tech Stack

* [Flask] (https://flask.palletsprojects.com/en/1.1.x/) - a micro web framework written in Python
* [docker-compose](https://docs.docker.com/compose/) - For multi-container Docker applications
* [heroku.yml](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml) - New feature from Heroku to build Docker Images with self defined manifest

## Contributor
* [Yen Ting](https://github.com/yentim0519)

