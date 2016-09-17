# coding: utf8

import pymongo

from pymongo import MongoClient
client = MongoClient()

# Удалить БД, если она существует
# connection.drop_database("test_database")

# Выбираем БД
db = client.test_database
# либо: db = client['test-database']

# Удалить коллекцию
db.drop_collection('users')

collection = db.test_collection
# or: collection = db['test-collection']

post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"]}

print post

posts = db.posts
post_id = posts.insert_one(post).inserted_id
print post_id

# Добавление документов в колекцию 'users'
db.users.save( { 'name':'user 1', 'level':1 } )
db.users.save( { 'name':'user 2', 'level':2 } )
db.users.insert( { 'name':'user 3', 'level':3 } )

# # Полное имя колекции
print db.users.full_name

# # Получить все документы
for user in db.users.find():
    print user

# Выбрать конкретные атрибуты
users = db.users.find({},{ 'login':1, 'name':1 })

# Получить один документ по условию
user = db.users.find_one({'name':'user 1'})

# Получить/установить значение
print user['level']
user['level'] = 7

# Сохранить документ
db.users.save(user)

# Удалить документ
db.users.remove(user)

# Установить значение в документе
db.users.update({ 'name':'user 2' }, { "$set": { 'level':5 } })

# Кол-во документов
print 'Count',db.users.count()
print 'Count lvl=2',db.users.find({'level':2}).count()

# Сортировка
print "SORT"
for user in db.users.find().sort('level'):
    print user
# в обратном порядке: .sort('level',pymongo.DESCENDING)
# Сортировка по нескольким атрибутам
    db.users.find({}).sort( [('status',1),('level',-1)] )

# Ограничение выборки, пропустить один документ и выбрать не более двух
for user in db.users.find().skip(1).limit(2):
    print user

# Условия
print "ASDKASLDKALSDK"
for user in db.users.find().where('this.name == "user 2" || this.level>3'):
    print user

# Выбрать неповторяющиеся записи
for user in db.users.distinct('level'):
    print user

# Поиск регулярным выражением
import re
regex = re.compile('^us', re.I | re.U) 
result = db.collection.find({ 'name':regex })