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

                                                                                      #get data from csv file to neo4j database
with open('C:\\Users\\R6000670\\Documents\\Neo4j\\pracneo\\import\\dataset.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tt=row['Ticket_Type']
        sv=row['Severity']
        rqid=row['Requester_ID']
        rs=row['Requester_Seniority']
        fa=row["Filed_Against"]
        pr=row["Priority"]
        ito=row["IT_Owner_ID"]
        do=row["Days_Open"]
        sat=row["Satisfaction"]
        tx = gr.begin()
        a = Node("data",ticket_type=tt, severity=sv, request_id=rqid, requester_seniority=rs, filed_against=fa, priority=pr, it_owner_id=ito, days_open=do,satisfaction=sat)
        tx.merge(a)
        tx.commit()
	
