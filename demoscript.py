from flask import Flask, render_template, request
app = Flask(__name__, template_folder='templates')
import pymongo

@app.route('/')
def home():
   return render_template('home.html')
   
@app.route('/create')
def create():
   return render_template('create.html')

@app.route('/createdisplay',methods = ['POST', 'GET']) 
def createdisplay():
   if request.method == 'POST':
      result2={}
      result = request.form
      for i in result:
        result2[i]=result[i]
        
      result2['Total'] = int(result['Physics']) + int(result['Chemistry']) + int(result['Maths'])
      result2['Percentage'] = int(result2['Total'])/3
      
      
      ### Mongo DB ###
      client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.wonbr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
      db = client['myFirstDatabase']
      collection = db["Workshop"]
      collection.insert_one(result2)

      
      return render_template("create_submit.html",result = result2)
      
   
@app.route('/read')
def read():
   return render_template('read.html')
   
        
@app.route('/readdisplay', methods = ['POST', 'GET'])
def readdisplay():
   if request.method == 'POST':
      result2={}
      result = request.form
      for i in result:
        result2[i]=result[i]
        
      ### Mongo DB ###
      client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.wonbr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
      db = client['myFirstDatabase']
      collection = db["Workshop"]
      result = collection.find_one({"Name":result2["Name"]})
      return render_template("read_submit.html",result = result)
   
@app.route('/update')
def update():
   return render_template('update.html')
   
@app.route('/updatedisplay',  methods = ['POST', 'GET'])
def updatedisplay():
    if request.method == 'POST':
          result2={}
          result = request.form
          for i in result:
            result2[i]=result[i]
            
          result2['Total'] = int(result['Physics']) + int(result['Chemistry']) + int(result['Maths'])
          result2['Percentage'] = int(result2['Total'])/3
          
          
          ### Mongo DB ###
          client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.wonbr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
          db = client['myFirstDatabase']
          collection = db["Workshop"]
          
          myquery = { "Name": result2["Name"] }
          newvalues = { "$set": { "Physics": result2["Physics"], "Chemistry": result2["Chemistry"], "Maths": result2["Maths"], "Percentage": result2["Percentage"], "Total": result2["Total"], } }

          collection.update_one(myquery, newvalues)
          result = collection.find_one({"Name":result2["Name"]})
          

          
          return render_template("update_submit.html",result = result)
   

   
@app.route('/delete')
def delete():
   return render_template('delete.html')
   
   
@app.route('/deletedisplay',  methods = ['POST', 'GET'])
def updatedelete():
    if request.method == 'POST':
          result2={}
          result = request.form
          for i in result:
            result2[i]=result[i]
          
          ### Mongo DB ###
          client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.wonbr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
          db = client['myFirstDatabase']
          collection = db["Workshop"]
          
          myquery = { "Name": result2["Name"] }

          collection.delete_one(myquery)

          return render_template("delete_submit.html",result = result2  )
   
if __name__ == '__main__':
   app.run(debug = True)