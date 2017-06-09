from py2neo import *
gr=Graph(host="localhost",password="XXXyour passXXX",user="neo4j")

"""gr=Graph(password="XXXyour passXXXX")"""                                             #will also do as only authentication is required

gr.run("merge (someone:masterchef{name:'someone',city:'chandigarh',age:22})")           #your query here

"""listofdict=gr.data("matCh (n:masterchef) return n.name, n.age")"""                  # display data from database, returns list of dictionaries
                                                                                       # n.age, n.name restricts the data to be displayed 
             #------------OR------------
listofdict=gr.run("matCh (n:masterchef) return n.name, n.age").data()                  

for i in listofdict:
	print(i)

gr.run("match (k:masterchef{age:22}) detach delete k")
