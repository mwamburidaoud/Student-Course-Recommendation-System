import mysql.connector
import networkx as nx
import matplotlib.pyplot as plt

# connect to the database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="school",
  auth_plugin='mysql_native_password'

# create a cursor
cursor = cnx.cursor()

# execute a query to fetch the required and taken courses for a specific student
student_id = 1
query = """
    SELECT c.name, rc.required, rc.taken
    FROM courses c
    JOIN requirement_courses rc ON c.id = rc.course_id
    JOIN requirements r ON rc.requirement_id = r.id
    LEFT JOIN (
        SELECT *
        FROM student_courses
        WHERE student_id = %s
    ) sc ON c.id = sc.course_id
    ORDER BY r.name
"""
cursor.execute(query, (student_id,))
rows = cursor.fetchall()

# create a directed graph to represent the courses and their prerequisites
G = nx.DiGraph()
for name, required, taken in rows:
    G.add_node(name, required=required, taken=taken)
    for pre_req in taken.split(","):
        if pre_req != "":
            G.add_edge(pre_req.strip(), name)

# create two sets of nodes: one for the courses the student should take, and one for the courses they shouldn't take
should_take = set()
shouldnt_take = set()
for name in G.nodes:
    node = G.nodes[name]
    if node["required"] == "Yes" and node["taken"] == "No":
        should_take.add(name)
    else:
        shouldnt_take.add(name)


    

# plot the graph
pos = nx.spring_layout(G, k=0.15)
nx.draw_networkx_nodes(G, pos, nodelist=should_take, node_color="g")
nx.draw_networkx_nodes(G, pos, nodelist=shouldnt_take, node_color="r")
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, font_size=8)
plt.axis("off")
plt.show()

# close the connection to the database
mydb.close()
