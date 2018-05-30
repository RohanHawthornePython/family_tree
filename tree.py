import model
from datetime import datetime

class Person():
	def __init__(self, id, fullname, gender, dob):
		self.id = id
		self.fullname = fullname
		self.gender = gender
		self.dob = dob
		self.spouse = []
		self.children = {}

	def __cmp__(self, other):
		me = datetime.strptime(self.dob, '%d/%m/%Y')
		them = datetime.strptime(other.dob, '%d/%m/%Y')
		return cmp(me, them)
        
	def __eq__(self, other):
		return other.id == self.id
		
	def __lt__(self, other):
		me = datetime.strptime(self.dob, '%d/%m/%Y')
		them = datetime.strptime(other.dob, '%d/%m/%Y')
		return me < them

def pdiv(p):
	return "<div class='"+p.gender+"' ondrop='drop_person(event)' ondragover='allowDrop(event)'>"+p.fullname+"</div>\n"
	
def mdiv(m):
	if not m.divorced:
		return "<div class='divorced'><img src='/static/divorced.jpg'/></div>\n"
	else:
		return "<div class='married'><img src='/static/married.jpg'/></div>\n"
		
def build_tree(person, p, t):
	
	print_tree = "<li>"
	# print the root
	print_tree += pdiv(person)
	
	# print the spouse
	for s in person.spouse:
		print_tree += pdiv(s)
		# recurse the children from the marriages
		for marriage in children.keys():
			for child in marriage:
				
				print_tree += "<li>\n"
				print_tree += build_tree(child, p, t+1)
				print_tree += "</li>\n"
			
	print_tree += "</li>"
	return print_tree
	

def draw_tree(p):
	# start tree
	html = "<div class='tree' id='FamilyTreeDiv'>\n"
	html += "<ul>"
	
	# get root
	root = min(p)
	
	# build the tree recursively
	html += build_tree(root, p, 1)
	
	# end tree	
	html += "</ul>"
	html += "</div>\n"
	return html
	
def get_tree():

	db = model.get_db()
	cur = db.cursor()
	
	persons = []
		
	# get all the people
	cur.execute("SELECT * FROM person")
	records = cur.fetchall()
	for record in records:
		persons.append(Person(record[0],record[1],record[2],record[3]))

	# add the spouses
	for p in persons:
		cur.execute("SELECT id, bride FROM marriage WHERE groom = ? UNION SELECT id, groom FROM marriage WHERE bride = ?",[p.id,p.id])
		records = cur.fetchall()
		for record in records:
			spouse_id = record[1]
			spouse = [per for per in persons if per.id == spouse_id]
			p.spouse.append(spouse)
			
			# get marriages and their children
			marriage = record[0]
			cur.execute("SELECT id, child FROM child WHERE marriage = ?", [marriage])
			records = cur.fetchall()
			for rec in recs:
				child = [per for per in persons if per.id == rec[1]]
				p.children[rec[0]].append(child)
	
	if len(persons):
		return draw_tree(persons)
	else:
		return "Drag an object onto the canvas to start"