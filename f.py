import peewee as pw
import datetime

def create_db(table):
   db.connect()
   table.drop_table()
   table.create_table()
   db.close()

db = pw.MySQLDatabase('calories_meter', host = 'localhost', port = 3306, user = 'root', password = 'Vobdim4008')

class BaseModel(pw.Model):
    class Meta:
        database = db

class Users(BaseModel):
   teleId = pw.IntegerField()
   username = pw.TextField()

class products(BaseModel):
       
   title = pw.TextField(unique = True, null = False)
   protein = pw.FloatField(null = False)
   fat = pw.FloatField(null = False)
   carbs = pw.FloatField(null = False)
   calories = pw.IntegerField()
   uid = pw.IntegerField()

class todays_meal(BaseModel):
       
   product = pw.ForeignKeyField(products, backref='todays_products')
   weight = pw.IntegerField(null = False)
   meal_date = pw.DateField()
   uid = pw.IntegerField()
      
class weight(BaseModel):
       
   weight = pw.FloatField()
   measure_date = pw.DateField()
   user_id = pw.IntegerField()
   
def select_products(tuser_id):
   s = ""
   q = Users.select().where(Users.teleId == tuser_id)
   for row in q:
      s = row.id
   sp = ""
   q = products.select().where(products.uid == s)
   for row in q:
        sp = sp + ("ID:{}. {} (Б:{} Ж:{} У:{} ККал:{})".format(row.id, row.title, row.protein, row.fat, row.carbs, row.calories)) + '\n'
   q.execute()
   return sp

def select_weight(tuser_id):
   q = Users.select().where(Users.teleId == tuser_id)
   wid = ''
   for row in q:
      wid= row.id
   s = ''   
   q = weight.select().where(weight.user_id == wid)
   for row in q:
      s = s + ("ID {}, Вес {}, Дата {}".format(row.id, row.weight, row.measure_date)) + '\n'
   q.execute()
   if (s == ""):
     s = "Записей о весе нет, добавьте новую"
   return s

def add_products(ttitle, p, f, c, tuser_id):
   #rows = [{"title":title, "protein":p, "fat":f, "carbs":c}] 
   q = Users.select().where(Users.teleId == tuser_id)
   s = ''
   for row in q:
      s = row.id
   products.create(title = ttitle, protein = p, fat = f, carbs = c, calories =(float(p)*4*0.845 + float(f)*9*0.94 + float(c)*3.75*0.956), uid = s)     

def user_select(telebot_id):
   q = Users.select().where(Users.teleId == telebot_id)
   s = ''
   for row in q:
      s = row.teleId
   return s

def new_user(telebot_id, username):
   a = Users(teleId = telebot_id, username = username)
   a.save()

def weight_insert(tweight, tuser_id):
   q = Users.select().where(Users.teleId == tuser_id)
   s = ''
   for row in q:
      s = row.id
   a = weight(weight = tweight, measure_date = datetime.date.today(), user_id = s)
   a.save()
   
def dbweight_delete(tid, tuser_id):
   q = Users.select().where(Users.teleId == tuser_id)
   s = ''
   for row in q:
      s = row.id
   qry = weight.delete().where((weight.user_id == s)&(weight.id == tid))
   qry.execute()
   
def dbproducts_delete(tid, tuser_id):
   q = Users.select().where(Users.teleId == tuser_id)
   s = ''
   for row in q:
      s = row.id
   qry = products.delete().where((products.uid == s)&(products.id == tid))
   qry.execute()
   
def select_status(tuser_id):
   q = Users.select().where(Users.teleId == tuser_id)
   s = ''
   for row in q:
      s = row.id
   q = (todays_meal
        .select()
        .join(products)
        .where(
            (todays_meal.uid == s)&
            (todays_meal.meal_date == datetime.date.today())&
            (products.uid == s))
         .order_by(todays_meal.id))
   s = ""
   t_p = 0
   t_f= 0
   t_carb = 0
   t_cal = 0
   for today in q:
      comp = today.weight/100
      s = s + ("ID {}. {} {} гр. (б {}) (ж {}) (у {}) (калл {})".format(today.id, today.product.title, today.weight, comp * today.product.protein, comp * today.product.fat, comp * today.product.carbs, comp * today.product.calories)) + '\n'
   
      t_p += comp * today.product.protein
      t_f += comp * today.product.fat
      t_carb += comp * today.product.carbs
      t_cal += comp * today.product.calories
   s += '\n' + '\n'+"Белки: {}".format(int(t_p)) + '\n'+ 'Жиры: {}'.format(int(t_f)) + '\n' +'Углеводы: {}'.format(int(t_carb)) + '\n' + 'Каллории: {}'.format(int(t_cal))
   if (s == ""):
     s = "Записей о сегодняшних продуктах нет, добавьте новую"
   return s

def dbtoday_add(title, tweight, tuser_id):
   ret = ""
   pid = ""
   q = Users.select().where(Users.teleId == tuser_id)
   s = ''
   for row in q:
      s = row.id
   q = products.select().where((products.uid == s) & (products.title == title))
   for row in q:
      pid = row.id
   if (pid == ""):
      ret = "Такого продукта нет, добавьте продукт через Меню:Продукты->Добавить"
      return ret
   else:
      ret = "Успешно добавлено"
   todays_meal.create(product = pid, weight = tweight, meal_date = datetime.date.today(), uid = s)
   return ret

def dbtoday_delete(tid, tuser_id):
   q = Users.select().where(Users.teleId == tuser_id)
   s = ''
   for row in q:
      s = row.id
   qry = todays_meal.delete().where((todays_meal.uid == s)&(todays_meal.id == tid))
   qry.execute()
#create_db(products)
#create_db(todays_meal)
# create_db(weight)



