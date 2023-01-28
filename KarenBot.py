#! ../env/bin/python3

import praw
import sqlalchemy as db
import re
import random as rand
from sqlalchemy import Column, String, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import praw.exceptions


reddit = praw.Reddit('KarenBot')
karenRegex = re.compile(r'a Karen', re.IGNORECASE)
botRegex = re.compile(r'a bot', re.IGNORECASE)

karenList = ["I like you as a person", "That is sweet, thank you for your honesty"]
karenSignature = "_Beep Boop, you are worthy_"


# create database connection and start it  
Base = declarative_base() # Create initial Base class from which mapped classes will be defined

engine = db.create_engine('sqlite:///roxy.sqlite3', echo=True) 
connection = engine.connect()
Base.metadata.create_all(engine)

# Create session object, which is the ORM's "handle" to the database, allowing conversation within it
# use session = Session() whenever need to talk to database
Session = sessionmaker(bind=engine)

class Comment(Base):
    __tablename__ = 'comments'

    post_title = Column(String, primary_key=True)
    comment_id = Column(String, primary_key=True)
    comment_body = Column(String)
    user_id = Column(String)

    def __repr__(self):
        return "<Comments(post_title='%s', comment_id='%s', comment_body='%s', user_id='%s')>" % (
            self.post_title, self.comment_id, self.comment_body, self.user_id)


blackList = [
    "talesfromyourserver",
    "bmw",
    "anime", 
    "asianamerican", 
    "askhistorians", 
    "askscience", 
    "askreddit", 
    "aww", 
    "chicagosuburbs", 
    "cosplay", 
    "cumberbitches", 
    "d3gf", 
    "deer", 
    "depression", 
    "depthhub", 
    "drinkingdollars", 
    "forwardsfromgrandma", 
    "geckos", 
    "giraffes", 
    "grindsmygears", 
    "indianfetish", 
    "me_irl", 
    "misc", 
    "movies", 
    "mixedbreeds", 
    "news", 
    "newtotf2", 
    "omaha", 
    "petstacking", 
    "pics", 
    "pigs", 
    "politicaldiscussion", 
    "politics", 
    "programmingcirclejerk", 
    "raerthdev", 
    "rants", 
    "runningcirclejerk", 
    "salvia", 
    "science", 
    "seiko", 
    "shoplifting", 
    "sketches", 
    "sociopath", 
    "suicidewatch", 
    "talesfromtechsupport",
    "torrent",
    "torrents",
    "trackers",
    "tr4shbros", 
    "unitedkingdom",
    "crucibleplaybook",
    "cassetteculture",
    "italy_SS",
    "DimmiOuija",
    "permission",
    "benfrick",
    "bsa",
    "futurology",
    "graphic_design",
    "historicalwhatif",
    "lolgrindr",
    "malifaux",
    "nfl",
    "toonami",
    "trumpet",
    "ps2ceres",
    "duelingcorner",
    "fuckyoukaren",
    "karen",
    "askteengirls",
    "londonontario",
    "gendercritical"
]

subreddit = reddit.subreddit("All")

# Indefinitely iterate over submissions and comments in All
for submission in subreddit.stream.submissions():
    p_compareList = []
    if submission.subreddit not in blackList:
        postTitle = submission.title # store post title in case a match is found in next loop
        for comment in subreddit.stream.comments():
            
            # store values in case match is found, so can add to Comment table
            cBody = comment.body
            cID = comment.id
            cAuthor = comment.author.name

            karenMatch = karenRegex.search(cBody)
            exceptionList = []

            if karenMatch is None:
                continue
            else:
                print('Match found')
                session = Session()
                c_compareList = []
                for instance in session.query(Comment.comment_id):
                    c_compareList.append(instance)
                for instance in session.query(Comment.post_title):
                    p_compareList.append(instance)
                if cID not in c_compareList and postTitle not in p_compareList:
                    try:
                        comment.reply(karenList[rand.randint(0,11)] + '\n\n' + karenSignature)
                        session.add( Comment(post_title=postTitle, comment_id=cID, comment_body=cBody, user_id=cAuthor))
                        print('Replying to comment')
                    except praw.exceptions.RedditAPIException as exception:
                        for subException in exception.items:
                            exceptionList.append(subException.error_type)
                            print(exceptionList)
                            
                
                session.commit()
                print(cBody)
                print(cID)
                print(cAuthor)
                print(postTitle)


