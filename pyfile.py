"""AUTHOR      : RAKSHIT KAPOOR
   INSTITUTION : NIT Jalandhar"""

import os
from flask import *
from werkzeug import secure_filename
import csv
from py2neo import *
import time

ALLOWED_EXTENSIONS = set(['csv'])
UPLOAD_FOLDER="C:/Users/R6000670/Documents/Neo4j/Ticketanalysisdb/import/"

app=Flask(__name__)
app.secret_key = 'random string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_files(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/alreadyuploaded')
def alreadyuploaded():
	return render_template('resultspage.html',contenttype=".csv",tm=0)

@app.route('/results/',methods=['post'])
def results():
	st=time.time()
	passw=request.form['pass']
	file=request.files['file']
	if file.filename=='':
		flash("No file was selected !!")
		flash("Choose your file again")
		return redirect(url_for("home"))
	elif not allowed_files(file.filename):
		flash("Invalid file (Only .csv (UTF-8) allowed)!!")
		flash("Choose your file again")
		return redirect(url_for("home"))
	else:
		gr=Graph(password=passw)
		securedfile=secure_filename(file.filename)

		if not os.path.exists(UPLOAD_FOLDER):
			os.makedirs(UPLOAD_FOLDER)

		file.save(os.path.join(app.config['UPLOAD_FOLDER'], securedfile))

		ctype=file.content_type

		rqidlist=set()
		itolist=set()
		dolist=set()

		with open('C:\\Users\\R6000670\\Documents\\Neo4j\\Ticketanalysisdb\\import\\'+securedfile) as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				tt=row['Ticket_Type']
				sv=row['Severity']
				rqid=int(row['Requester_ID'])
				rs=row['Requester_Seniority']
				fa=row["Filed_Against"]
				pr=row["Priority"]
				ito=int(row["IT_Owner_ID"])
				do=int(row["Days_Open"])
				sat=row["Satisfaction"]
				tx = gr.begin()
				a = Node("tempdata",ticket_type=tt, severity=sv, request_id=rqid, requester_seniority=rs, filed_against=fa, priority=pr, it_owner_id=ito, days_open=do,	satisfaction=sat)
				tx.merge(a)
				a=Node("RequesterID", RequesterID=rqid)
				tx.merge(a)
				rqidlist.add(rqid)
				a=Node("IT_OWNER_ID", ITOWNERID=ito)
				tx.merge(a)
				itolist.add(ito)
				a=Node("DaysOpen", DaysOpen=do)
				tx.merge(a)
				dolist.add(do)
				tx.commit()

		tx=gr.begin()
		a=Node("TicketType", TicketType='Request')
		tx.merge(a)
		a = Node("TicketType", TicketType='Issue')
		tx.merge(a)
		a = Node("Severity", Severity='0 - Unclassified')
		tx.merge(a)
		a = Node("Severity", Severity='1 - Minor')
		tx.merge(a)
		a = Node("Severity", Severity='2 - Normal')
		tx.merge(a)
		a = Node("Severity", Severity='3 - Major')
		tx.merge(a)
		a = Node("Severity", Severity='4 - Critical')
		tx.merge(a)
		a = Node("RequesterSeniority", RequesterSeniority='1 - Junior')
		tx.merge(a)
		a = Node("RequesterSeniority", RequesterSeniority='2 - Regular')
		tx.merge(a)
		a = Node("RequesterSeniority", RequesterSeniority='3 - Senior')
		tx.merge(a)
		a = Node("RequesterSeniority", RequesterSeniority='4 - Manager')
		tx.merge(a)
		a = Node("FiledAgainst", FiledAgainst='Systems')
		tx.merge(a)
		a = Node("FiledAgainst", FiledAgainst='Software')
		tx.merge(a)
		a = Node("FiledAgainst", FiledAgainst='Access/Login')
		tx.merge(a)
		a = Node("FiledAgainst", FiledAgainst='Hardware')
		tx.merge(a)
		a = Node("Priority", Priority='0 - Unassigned')
		tx.merge(a)
		a = Node("Priority", Priority='1 - Low')
		tx.merge(a)
		a = Node("Priority", Priority='2 - Medium')
		tx.merge(a)
		a = Node("Priority", Priority='3 - High')
		tx.merge(a)
		a = Node("Satisfaction", Satisfaction='0 - Unknown')
		tx.merge(a)
		a = Node("Satisfaction", Satisfaction='1 - Unsatisfied')
		tx.merge(a)
		a = Node("Satisfaction", Satisfaction='2 - Satisfied')
		tx.merge(a)
		a = Node("Satisfaction", Satisfaction='3 - Highly satisfied')
		tx.merge(a)
		tx.commit()
		gr.run("MATCH (a:tempdata),(b:Severity) WHERE a.severity = '0 - Unclassified' AND b.Severity = '0 - Unclassified' MERGE (a)-[r:Severity]->(b)")
		gr.run("MATCH (a:tempdata),(b:Severity) WHERE a.severity = '1 - Minor' AND b.Severity = '1 - Minor' MERGE (a)-[r:Severity]->(b)")
		gr.run("MATCH (a:tempdata),(b:Severity) WHERE a.severity = '2 - Normal' AND b.Severity = '2 - Normal' MERGE (a)-[r:Severity]->(b)")
		gr.run("MATCH (a:tempdata),(b:Severity) WHERE a.severity = '3 - Major' AND b.Severity = '3 - Major' MERGE (a)-[r:Severity]->(b)")
		gr.run("MATCH (a:tempdata),(b:Severity) WHERE a.severity = '4 - Critical' AND b.Severity = '4 - Critical' MERGE (a)-[r:Severity]->(b)")
		gr.run("MATCH (a:tempdata),(b:TicketType) WHERE a.ticket_type = 'Issue' AND b.TicketType = 'Issue' MERGE (a)-[r:TicketType]->(b)")
		gr.run("MATCH (a:tempdata),(b:TicketType) WHERE a.ticket_type = 'Request' AND b.TicketType = 'Request' MERGE (a)-[r:TicketType]->(b)")
		gr.run("MATCH (a:tempdata),(b:RequesterSeniority) WHERE a.requester_seniority = '1 - Junior' AND b.RequesterSeniority = '1 - Junior' MERGE (a)-[r:RequesterSeniority]->(b)")
		gr.run("MATCH (a:tempdata),(b:RequesterSeniority) WHERE a.requester_seniority = '2 - Regular' AND b.RequesterSeniority = '2 - Regular' MERGE (a)-[r:RequesterSeniority]->(b)")
		gr.run("MATCH (a:tempdata),(b:RequesterSeniority) WHERE a.requester_seniority = '3 - Senior' AND b.RequesterSeniority = '3 - Senior' MERGE (a)-[r:RequesterSeniority]->(b)")
		gr.run("MATCH (a:tempdata),(b:RequesterSeniority) WHERE a.requester_seniority = '4 - Manager' AND b.RequesterSeniority = '4 - Manager' MERGE (a)-[r:RequesterSeniority]->(b)")
		gr.run("MATCH (a:tempdata),(b:FiledAgainst) WHERE a.filed_against = 'Systems' AND b.FiledAgainst = 'Systems' MERGE (a)-[r:FiledAgainst]->(b)")
		gr.run("MATCH (a:tempdata),(b:FiledAgainst) WHERE a.filed_against = 'Software' AND b.FiledAgainst = 'Software' MERGE (a)-[r:FiledAgainst]->(b)")
		gr.run("MATCH (a:tempdata),(b:FiledAgainst) WHERE a.filed_against = 'Hardware' AND b.FiledAgainst = 'Hardware' MERGE (a)-[r:FiledAgainst]->(b)")
		gr.run("MATCH (a:tempdata),(b:FiledAgainst) WHERE a.filed_against = 'Access/Login' AND b.FiledAgainst = 'Access/Login' MERGE (a)-[r:FiledAgainst]->(b)")
		gr.run("MATCH (a:tempdata),(b:Priority) WHERE a.priority = '0 - Unassigned' AND b.Priority = '0 - Unassigned' MERGE (a)-[r:Priority]->(b)")
		gr.run("MATCH (a:tempdata),(b:Priority) WHERE a.priority = '1 - Low' AND b.Priority = '1 - Low' MERGE (a)-[r:Priority]->(b)")
		gr.run("MATCH (a:tempdata),(b:Priority) WHERE a.priority = '2 - Medium' AND b.Priority = '2 - Medium' MERGE (a)-[r:Priority]->(b)")
		gr.run("MATCH (a:tempdata),(b:Priority) WHERE a.priority = '3 - High' AND b.Priority = '3 - High' MERGE (a)-[r:Priority]->(b)")
		gr.run("MATCH (a:tempdata),(b:Satisfaction) WHERE a.satisfaction = '0 - Unknown' AND b.Satisfaction = '0 - Unknown' MERGE (a)-[r:Satisfaction]->(b)")
		gr.run("MATCH (a:tempdata),(b:Satisfaction) WHERE a.satisfaction = '1 - Unsatisfied' AND b.Satisfaction = '1 - Unsatisfied' MERGE (a)-[r:Satisfaction]->(b)")
		gr.run("MATCH (a:tempdata),(b:Satisfaction) WHERE a.satisfaction = '2 - Satisfied' AND b.Satisfaction = '2 - Satisfied' MERGE (a)-[r:Satisfaction]->(b)")
		gr.run("MATCH (a:tempdata),(b:Satisfaction) WHERE a.satisfaction = '3 - Highly satisfied' AND b.Satisfaction = '3 - Highly satisfied' MERGE (a)-[r:Satisfaction]->(b)")
		for i in rqidlist:
			gr.run("MATCH (a:tempdata),(b:RequesterID) WHERE a.request_id = " + str(i) + " AND b.RequesterID ="+ str(i) + " MERGE (a)-[r:RequesterID]->(b)")
		for i in dolist:
			gr.run("MATCH (a:tempdata),(b:DaysOpen) WHERE a.days_open = " + str(i) + " AND b.DaysOpen ="+ str(i)+ " MERGE (a)-[r:Daysopen]->(b)")
		for i in itolist:
			gr.run("MATCH (a:tempdata),(b:IT_OWNER_ID) WHERE a.it_owner_id = " + str(i) + " AND b.ITOWNERID ="+ str(i)+ " MERGE (a)-[r:ITOWNERID]->(b)")

		return render_template('resultspage.html',contenttype=ctype,tm=time.time()-st)

@app.route('/analysis/',methods=['post'])
def analysis():
	passw=request.form['password']
	gr=Graph(password=passw)
	keys=[]
	vals=[]
	txt=request.form["query"]
	properties=list(txt.split(','))
	for i in properties:
		k,v=i.split(':')
		keys.append(k)
		vals.append(v)
	props=dict(zip(keys,vals))
	print(gr.run("Match (a:tempdata"+str(props)+") return count(*)").data())
	return render_template('analysispage.html')


if __name__=='__main__':
    app.debug=True
    app.run(host="0.0.0.0",port=5000)                               # specify port value