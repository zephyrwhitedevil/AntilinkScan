from pymongo import MongoClient
import logging

def connect():
    client = MongoClient("mongodb+srv://filetolink:DWPEfBYWs4y1ricL@filetolink.xgmsac5.mongodb.net/?retryWrites=true&w=majority")
    db = client['linkscan']
    collection = db['whitelist_db']
    return collection,db

def add_userid(chatid,result_string):
    col,db = connect()
    data_db = check_userid(chatid,result_string)
    print(data_db)
    if data_db == False:
        ins= col.insert_one({'chat_id':str(chatid),'user_id':str(result_string)})
        return 1
    else:
        return 0



       
def remove_userid(chat_id,result_string):
    col,db = connect()
    data_db = check_userid(chat_id,result_string)
    print(data_db)
    if data_db == True:
        print("comminnn")
        try:
            rmv = col.delete_one({'chat_id':str(chat_id),"user_id":result_string})
        except Exception as e:
            print(str(e))
        print(rmv.deleted_count)
        return 1
    else:
        return 0


def check_userid(chat_id,result_string):
    col,db = connect()
    print(result_string)
    query = {'chat_id':str(chat_id),"user_id": str(result_string)}
    result = col.find(query)
    print(result.count())
    if result.count()!=0:
        return True
    return False


def add_chatid(group_name,member_count,chat_id):
    col,db=connect()
    collection = db['group_id']
    data = collection.find_one({'chat_id':chat_id})
    if data and data['members_count'] != member_count:
        collection.update_one({'chat_id': chat_id}, {'$set': {'members_count': member_count}})
    if not data:
        collection.insert_one({'chat_id':chat_id,'group_name':group_name,'members_count':member_count})
        return {"status":"Success"}
    else:
        return ''
    

def get_groupslist():
    col,db=connect()
    collection = db['group_id']
    stats_message = "Group Stats:\n"
    groups = collection.find({}, {'_id': 0, 'group_name': 1, 'chat_id': 1, 'members_count': 1})
    if groups:
        for group in groups:
            stats_message += f"{group['group_name']} (ID: {group['chat_id']}): {group['members_count']} members\n"
        return stats_message
    else:
        return None
    



