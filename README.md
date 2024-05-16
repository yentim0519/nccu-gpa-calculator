# NCCU GPA Calculator
This is an open source project for calculating NCCU (National Chengchi University) students' GPA (Grade Point Average), including cumulative, major and last 60 GPA.<br>
<br>
The goal of this project is to benefit those students of NCCU who need these GPA information but can only use online GPA calculators which users have to type in 
course names, credits, and scores all by themselves, which is very inconvenient.<br>
<br>
Feel free to fork this project and developed a GPA calculator for your school or make a PR (Pull Request) to make this project better! (The file test_transcript is provided for people who can't access NCCU transcript html file for testing)<br>
<br>
歡迎fork這個專案，並開發成符合自己學校格式的GPA計算器，或者可以提交PR (Pull Request)幫助改善此專案!（test_transcript提供給無法獲取政大成績html檔的人做測試）

**Website**: https://nccu-gpa-calculator-new-version.vercel.app/
<br>
<br>
**Demo Video**
![image](https://github.com/yentim0519/nccu-gpa-calculator/blob/master/nccu-gpa-calculator-demo-video.gif)

## Deploy Locally
Install pipenv and clone this project to your computer.
```
pip install pipenv
```
Go to the directory you clone and run the command from below.
```
// install the packages in Pipfile in your virtual enviornment
pipenv install 

// activate the virtual enviornment (After running this command, you are in the virtual enviorment)
pipenv shell 

// check the packages you install form Pipfile (you may see from here, it's different than your local pip3 list)
pip3 list 

// Run the Flask project (After clicking the link that come up, you should be able to access the website)
python3 application.py 

//Exit from the virtual enviornment when you are done.
exit
```
If you are not a student from NCCU, you can play around the website with the file "test_trascript" in this repository. 
<br>

## Tech Stack

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - a micro web framework written in Python.
* [Vercel](https://vercel.com/) - a Frontend Cloud.

## Contributor
* [Yen Ting](https://github.com/yentim0519)

