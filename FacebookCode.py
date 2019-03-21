# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 12:44:46 2018

@author: neal8
"""

import requests
import pandas as pd
from dateutil.parser import parse


def fb_crawler(token,fb_id,n):  #n為總共要爬幾則貼文
    t=0
    columns = ['發文時間', '文章內容', '分享內容', '留言數', '分享數','發文類型' ,
               'likes','love','haha','wow','sad','angry','total','留言']
    posts = []
    res = requests.get('https://graph.facebook.com/v2.9/{}/posts?limit=20&access_token={}'.format(fb_id, token),headers={'Connection':'close'})    
    while 'paging' in res.json(): 
            
        for post in res.json()['data']:
            try:
                p_res = requests.get(
                        'https://graph.facebook.com/v2.9/{}?'.format(post['id']) +
                        'fields=comments.limit(0).summary(true),likes.limit(0).summary(true),shares,reactions.type(LOVE).limit(0).summary(total_count).as(reactions_love),reactions.type(HAHA).limit(0).summary(total_count).as(reactions_haha),reactions.type(WOW).limit(0).summary(total_count).as(reactions_wow),reactions.type(SAD).limit(0).summary(total_count).as(reactions_sad),reactions.type(ANGRY).limit(0).summary(total_count).as(reactions_angry),reactions.type(NONE).limit(0).summary(total_count).as(reactions_none),type&' +
                        'access_token={}'.format(token),headers={'Connection':'close'})
    # 留言數
                if 'comments' in p_res.json():
                    comments = p_res.json()['comments']['summary'].get('total_count')
                else:
                    comments = 0
    # 按讚數
                if 'likes' in p_res.json():
                    likes = p_res.json()['likes']['summary'].get('total_count')
                else:
                    likes = 0
    # 分享數
                if 'shares' in p_res.json():
                    shares = p_res.json()['shares'].get('count')
                else:
                    shares = 0
                
                if 'reactions_love' in p_res.json():
                    love = p_res.json()['reactions_love']['summary'].get('total_count')
                else:
                    love = 0
                
                if 'reactions_haha' in p_res.json():
                    haha = p_res.json()['reactions_haha']['summary'].get('total_count')
                else:
                    haha = 0
        
                if 'reactions_wow' in p_res.json():
                    wow = p_res.json()['reactions_wow']['summary'].get('total_count')
                else:
                    wow = 0
                
                if 'reactions_sad' in p_res.json():
                    sad = p_res.json()['reactions_sad']['summary'].get('total_count')
                else:
                    sad = 0
                
                if 'reactions_angry' in p_res.json():
                    angry = p_res.json()['reactions_angry']['summary'].get('total_count')
                else:
                    angry = 0
                
                if 'reactions_none' in p_res.json():
                    total = p_res.json()['reactions_none']['summary'].get('total_count')
                else:
                    total = 0
                
                if 'type' in p_res.json():
                    ty = p_res.json().get('type')
                else:
                    ty='none'
                
                comm=fb_crawler_comments_sec(token,post['id'])

                posts.append([(str(parse(post['created_time']).date()))+" "+(str(parse(post['created_time']).time())),
                      post.get('message'),
                      post.get('story'),
                      comments,
                      shares,
                      ty,
                      likes,
                      love,
                      haha,
                      wow,
                      sad,
                      angry,
                      total,
                      comm])
        
            except ConnectionError:
                print(post['id']+' post got ConnectionError error')
                
            t=t+1
            print(t)
            if t>2700:
                break
        if t>2700:
            break
            
        if 'next' in res.json()['paging']:
            res = requests.get(res.json()['paging']['next'],headers={'Connection':'close'})

        else:
            break
    df = pd.DataFrame(posts, columns=columns)
    df.to_csv('M:\\playstation0429.csv',index=False)

def fb_crawler_comments_sec(token,fb_post_id):
    comment = []
    com_res = requests.get('https://graph.facebook.com/'+fb_post_id+'/comments?access_token='+token,headers={'Connection':'close'})
    while 'paging' in com_res.json(): 
        
        for com in com_res.json()['data']:

            comment.append(com.get('message'))
        if 'next' in com_res.json()['paging']:
            try:
                com_res = requests.get(com_res.json()['paging']['next'],headers={'Connection':'close'})
            except ConnectionError:
                print(fb_post_id+'  got ConnectionError error') 
        else:
            break
    return comment

a='EAAaFYjWejrIBAApkrz07vldcq96CmFcR5OaebEPmB7zJv8JFz5QyeGehg4rzhO5gumC2cpte7nkZASm5X3eZBwb5ZBiHIwaDroGudvxowsMZCr0sL8xfANZCjeZANoqzmA1SkRnHqWBVugx2eOQ0ZB5YmIJLfOdLKoZD'    #長期權杖
b='14104316802'

fb_crawler(a,b,5)