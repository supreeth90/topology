import rdflib
import requests
import json
import coreapi
g=rdflib.Graph()
g.load('mini-topo.rdf')
# g.load('topo.rdf')

# for s,p,o in g:
# 	print "New entry::"
#  	print s
#  	print p
# 	print o

def delete_nodes(node_to_ref_dict):
	print("Deleting the nodes")
	for node_name in node_to_ref_dict.keys():
		print(node_to_ref_dict[node_name])	
		requests.delete(node_to_ref_dict[node_name])

def delete_ports(ports_uri):
	print("Deleting the ports")
	ports_list = coreapi.get(nodes_uri)
	for port_dict in ports_list:
		print port_dict['selfRef']
		requests.delete(port_dict['selfRef'])

		


prefix = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
	PREFIX ndl: <http://www.science.uva.nl/research/sne/ndl#> """;

query_var=prefix+"""
SELECT ?name ?interface ?connectedTo ?type ?neighbour
	WHERE {
	        ?x rdf:type ndl:Device . ?x ndl:name ?name .
		?x ndl:hasInterface ?y . ?y rdf:type ndl:Interface .
		?y ndl:name ?interface . ?y ndl:connectedTo ?connectedTo .
		OPTIONAL {
			?y ndl:connectedTo ?z .
			?z rdf:type ndl:Interface .
			?z ndl:name ?neighbour
		} . OPTIONAL {
			?y ndl:capacity ?capacity .
			?y ndl:encapsulation ?type
		} .
		
	}"""

node_only_query=prefix+"""
SELECT ?name 
WHERE {
        ?x rdf:type ndl:Device . ?x ndl:name ?name.
	OPTIONAL {
		?y ndl:connectedTo ?z .
		?z rdf:type ndl:Interface .
		?z ndl:name ?neighbour
	} . OPTIONAL {
		?y ndl:capacity ?capacity .
		?y ndl:encapsulation ?type
	} .
	
}"""
# query_var=prefix+"""
# SELECT ?name ?interfaceName ?connectedTo ?type ?neighbour
# 	WHERE {
# 	        ?y rdf:type ndl:Interface . ?y ndl:name ?interfaceName .
# 	        ?x rdf:type ndl:Interface . ?x ndl:connectedTo ?connectedTo .
# 		OPTIONAL {
# 			?y ndl:connectedTo ?z .
# 			?z rdf:type ndl:Interface .
# 			?z ndl:name ?neighbour
# 		} . OPTIONAL {
# 			?y ndl:capacity ?capacity .
# 			?y ndl:encapsulation ?type
# 		}
# 		 .
# }"""

core_routers_list = ['rtr.chic.net.internet2.edu', 'rtr.atla.net.internet2.edu', 'rtr.hous.net.internet2.edu', 'rtr.kans.net.internet2.edu', 'rtr.losa.net.internet2.edu', 'rtr.newy32aoa.net.internet2.edu', 'rtr.salt.net.internet2.edu', 'rtr.seat.net.internet2.edu', 'rtr.wash.net.internet2.edu']


# 	if row.name in core_routers_list:
# 		print row.name + " " + row.interface

routerNameToIpMap = {}
routerNameToIpMap['rtr.chic.net.internet2.edu'] = '64.57.28.241'
routerNameToIpMap['rtr.atla.net.internet2.edu'] = '64.57.28.243'
routerNameToIpMap['rtr.hous.net.internet2.edu'] = '64.57.28.244'
routerNameToIpMap['rtr.kans.net.internet2.edu'] = '64.57.28.245'
routerNameToIpMap['rtr.losa.net.internet2.edu'] = '64.57.28.248'
routerNameToIpMap['rtr.newy32aoa.net.internet2.edu'] = '64.57.28.242'
routerNameToIpMap['rtr.salt.net.internet2.edu'] = '64.57.28.246'
routerNameToIpMap['rtr.seat.net.internet2.edu'] = '64.57.28.247'
routerNameToIpMap['rtr.wash.net.internet2.edu'] = '64.57.28.249'

# r = requests.get('http://routerproxy.grnoc.iu.edu/internet2/index.cgi?fname=getResponse&args=show%20interface&cmd=show%20interface&args=&args=&args=64.57.28.241&device=64.57.28.242')
# print("Output of the router")
# print(r.text)




host_name="10.0.0.135"
port_no="8888"
uri="http://"+host_name+":"+port_no+"/"
nodes_uri=uri+"nodes"
nodes = []

for row in g.query(node_only_query):
	node = dict()
	node["$schema"]="http://unis.incntre.iu.edu/schema/20140214/node#"
	node["name"]=row.name
	ports = []
	port={'href':'instageni.illinois.edu_authority_cm_slice_idms','rel': 'full'}
	ports.append(port)
	node["ports"]=ports
	print "Node::"
	print row.name
	nodes.append(node)



print "::FINAL JSON::"
json_data = json.dumps(nodes)


print("NODE URI::"+nodes_uri)
print("JSON DATA:"+json_data)
requests.post(nodes_uri, data = json_data)

node_to_ref_dict = dict()
print "PRINTING THE STUFF\n"
nodes_list = coreapi.get(nodes_uri)

for check_node in nodes_list:
	print check_node['name']
	print check_node['selfRef']
	node_to_ref_dict[check_node['name']]=check_node['selfRef']
	print "\n"

print("Printing the map stuff")
for node_name in node_to_ref_dict.keys():
	print("Node name:"+ node_name+ " val:"+node_to_ref_dict[node_name])



# call only when needed to delete
# delete_nodes(node_to_ref_dict)


######## BUILD PORTS ###########

interface_query=prefix+"""
SELECT ?name ?interface
	WHERE {
	        ?x rdf:type ndl:Device . ?x ndl:name ?name .
		?x ndl:hasInterface ?interface 
		OPTIONAL {
			?y ndl:connectedTo ?z .
			?z rdf:type ndl:Interface .
			?z ndl:name ?neighbour
		} . OPTIONAL {
			?y ndl:capacity ?capacity .
			?y ndl:encapsulation ?type
		} .
		
	}"""

ports_uri=uri+"ports"
ports = []
print("PORTSSSSS!!!!")
for row in g.query(interface_query):
	print(row.name+" :::"+row.interface)
	temp_intf_name=row.interface
	intf_name=temp_intf_name.split("#")
	port_name_split=intf_name[1].split(":")
	port_node_name=port_name_split[0]
	port_name=port_name_split[1]
	print("PPP>>"+node_to_ref_dict[port_node_name]+">>"+port_name)
	port = dict()
	port["$schema"]="http://unis.incntre.iu.edu/schema/20140214/port#"
	port["name"]=port_name
	port["nodeRef"]=node_to_ref_dict[port_node_name]
	ipv4_addr = dict()
	ipv4_addr["type"]="ipv4"
	## TODO: Fill the actual IPv4 address or IP prefix when decided
	ipv4_addr["address"]="1.1.1.1"
	port["properties"]={"ipv4":ipv4_addr}
	ports.append(port)

print "::FINAL PORTS JSON::"
ports_json_data = json.dumps(ports)
print(ports_json_data)
print("PORTS URI::"+ports_uri)
requests.post(ports_uri, data = ports_json_data)






# for row in g.query(node_only_query):
# 	node = dict()
# 	node["$schema"]="http://unis.incntre.iu.edu/schema/20140214/node#"
# 	node["name"]=row.name
# 	node["selfRef"]=nodes_uri+row.name
# 	ports = []
# 	port={'href':'instageni.illinois.edu_authority_cm_slice_idms','rel': 'full'}
# 	ports.append(port)
# 	node["ports"]=ports
# 	print "Node::"
# 	print row.name
# 	nodes.append(node)


class Topology:
	def __init__(self):
    	self.node_to_port_dict = dict()
    	self.port_to_port_dict = dict()
    	self.node_ref_to_node = dict()
    	self.port_ref_to_port = dict()


  	def build_topology(self, rdf_url):







  	def create_nodes(self, nodes_uri, graph):
		prefix = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
		PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
		PREFIX ndl: <http://www.science.uva.nl/research/sne/ndl#> """
		node_only_query=prefix+"""
		SELECT ?name 
		WHERE {
		        ?x rdf:type ndl:Device . ?x ndl:name ?name.
			OPTIONAL {
				?y ndl:connectedTo ?z .
				?z rdf:type ndl:Interface .
				?z ndl:name ?neighbour
			} . OPTIONAL {
				?y ndl:capacity ?capacity .
				?y ndl:encapsulation ?type
			} .
			
		}"""
		
		nodes = []

		for row in graph.query(node_only_query):
			node = dict()
			node["$schema"]="http://unis.incntre.iu.edu/schema/20140214/node#"
			node["name"]=row.name
			# ports = []
			# port={'href':'instageni.illinois.edu_authority_cm_slice_idms','rel': 'full'}
			# ports.append(port)
			# node["ports"]=ports
			print "Node::"
			print row.name
			nodes.append(node)

		nodes_json_data = json.dumps(nodes)
		print("NODE URI::"+nodes_uri)
		print("NODE JSON DATA:"+nodes_json_data)
		requests.post(nodes_uri, data = nodes_json_data)

		self.build_node_ref_from_uri(uri)

	def build_node_ref_from_uri(self, uri):
		nodes_uri=uri+"nodes"
		nodes_list = coreapi.get(nodes_uri)

		for node_dict in nodes_list:
			cur_node_ref=node_dict['selfRef']
			cur_node_name=node_dict['name']
			print cur_node_ref
			print cur_node_name
			self.node_to_port_dict[cur_node_ref]=''
			self.node_ref_to_node[cur_node_ref]={'node_name':cur_node_name}
			node_to_ref_dict[check_node['name']]=check_node['selfRef']
			print "\n"

	def create_ports(self, ports_uri):
		prefix = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
		PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
		PREFIX ndl: <http://www.science.uva.nl/research/sne/ndl#> """
		interface_query=prefix+"""
		SELECT ?name ?interface
			WHERE {
			        ?x rdf:type ndl:Device . ?x ndl:name ?name .
				?x ndl:hasInterface ?interface 
				OPTIONAL {
					?y ndl:connectedTo ?z .
					?z rdf:type ndl:Interface .
					?z ndl:name ?neighbour
				} . OPTIONAL {
					?y ndl:capacity ?capacity .
					?y ndl:encapsulation ?type
				} .
				
			}"""

		ports = []
		print("PORTSSSSS!!!!")
		for row in g.query(interface_query):
			print(row.name+" :::"+row.interface)
			temp_intf_name=row.interface
			intf_name=temp_intf_name.split("#")
			port_name_split=intf_name[1].split(":")
			port_node_name=port_name_split[0]
			port_name=port_name_split[1]
			print("PPP>>"+node_to_ref_dict[port_node_name]+">>"+port_name)
			port = dict()
			port["$schema"]="http://unis.incntre.iu.edu/schema/20140214/port#"
			port["name"]=port_name
			port["nodeRef"]=node_to_ref_dict[port_node_name]
			ipv4_addr = dict()
			ipv4_addr["type"]="ipv4"
			## TODO: Fill the actual IPv4 address or IP prefix when decided
			ipv4_addr["address"]="1.1.1.1"
			port["properties"]={"ipv4":ipv4_addr}

			if node_to_port_ref_dict[port_node_name] is not None:
				current_port_ref_list=node_to_port_ref_dict[port_node_name]
				current_port_ref_list.append()
			ports.append(port)

		print "::FINAL PORTS JSON::"
		ports_json_data = json.dumps(ports)
		print(ports_json_data)
		print("PORTS URI::"+ports_uri)
		requests.post(ports_uri, data = ports_json_data)





















