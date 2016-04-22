

import re

class RouteInfo:

	def __init__(self):
		self.prefix = None
		self.from_ip = None
		self.from_as = None
		self.as_path_list = []
		self.next_hop = None
		self.origin = None
		self.view = None
		self.sequence = None
		self.med = None
		self.local_pref = None
		self.community = None
		self.status = None

	def display(self):
		print("PREFIX:"+self.prefix)
		print("from_ip:"+self.from_ip)
		print("from_as:"+self.from_as)
		print("next_hop:"+self.next_hop)
		print("AS PATH LIST:")
		print(self.as_path_list)
		print("origin: ",self.origin)
		print("view: ",self.view)
		print("sequence: ",self.sequence)
		print("MULTI_EXIT_DISC: ",self.med)
		print("local_pref: ",self.local_pref)
		print("community: ",self.community)
		print("status: ",self.status)

class Prefix:
	
	def __init__(self, rib_file_name = None):
		self.prefix_to_route = dict()
		if rib_file_name is not None:
			self.rib_file = open(rib_file_name, "r")
		else:
			self.rib_file = None

	def display_prefix(self):

		for prefix in self.prefix_to_route.keys():
			print("\n\n=======PREFIX: "+prefix+"=========\n")
			route_info_list = self.prefix_to_route[prefix]
			for route_info in route_info_list:
				print("\n")
				route_info.display()

	def build_prefix(self):

		route_info = self.build_route_info()
		while (route_info is not None):
			## Add to the list only if route_info is a valid one
			if route_info.prefix is not None and route_info.from_ip is not None:
				current_prefix = route_info.prefix
				if current_prefix != "":
					if current_prefix in self.prefix_to_route.keys():
						current_route_info_list = self.prefix_to_route[current_prefix]
						current_route_info_list.append(route_info)
					else:
						new_route_info_list = []
						new_route_info_list.append(route_info)
						self.prefix_to_route[current_prefix] = new_route_info_list
			route_info = self.build_route_info()


	def build_route_info(self):
		print("In build_route_info")
		route_info = None
		line = self.rib_file.readline()
		while (line):
			print("ENTERED WHILE")
			if "TIME:" in line: 
				print("TIME match")
				if route_info is None:
					print("START")
					route_info = RouteInfo()
				else:
					print("END")
					return route_info
			if "TYPE:" in line:
				print("TYPE match")
				if route_info is None:
					print("START")
					print("RouteInfo created")
					route_info = RouteInfo()
			if "PREFIX" in line:
				print("PREFIX match")
				matchObj = re.match( r'PREFIX: (.*)', line, re.M|re.I)
				route_info.prefix = matchObj.group(1)
			if "FROM" in line:
				print("FROM match")
				matchObj = re.match( r'FROM: (.*) AS(.*)', line, re.M|re.I)
				route_info.from_ip = matchObj.group(1)
				route_info.from_as = matchObj.group(2)
			if "ASPATH" in line:
				print("ASPATH match")
				matchObj = re.match( r'ASPATH: (.*)', line, re.M|re.I)
				as_path_string = matchObj.group(1)
				route_info.as_path_list = as_path_string.split(" ")
			if "NEXT_HOP" in line:
				print("NEXT_HOP match")
				matchObj = re.match( r'NEXT_HOP: (.*)', line, re.M|re.I)
				route_info.next_hop = matchObj.group(1)
			if "ORIGIN:" in line:
				print("ORIGIN match")
				matchObj = re.match( r'ORIGIN: (.*)', line, re.M|re.I)
				route_info.origin = matchObj.group(1)
			if "VIEW" in line:
				print("VIEW match")
				matchObj = re.match( r'VIEW: (.*)', line, re.M|re.I)
				route_info.view = matchObj.group(1)
			if "SEQUENCE:" in line:
				print("SEQUENCE match")
				matchObj = re.match( r'SEQUENCE: (.*)', line, re.M|re.I)
				route_info.sequence = matchObj.group(1)
			if "MULTI_EXIT_DISC:" in line:
				print("MULTI_EXIT_DISC match")
				matchObj = re.match( r'MULTI_EXIT_DISC: (.*)', line, re.M|re.I)
				route_info.med = matchObj.group(1)
			if "LOCAL_PREF:" in line:
				print("LOCAL_PREF match")
				matchObj = re.match( r'LOCAL_PREF: (.*)', line, re.M|re.I)
				route_info.local_pref = matchObj.group(1)
			if "COMMUNITY:" in line:
				print("COMMUNITY match")
				matchObj = re.match( r'COMMUNITY: (.*)', line, re.M|re.I)
				route_info.community = matchObj.group(1)
			if "STATUS:" in line:
				print("STATUS match")
				matchObj = re.match( r'STATUS: (.*)', line, re.M|re.I)
				route_info.status = matchObj.group(1)
			line = self.rib_file.readline()
			print("NEW LINE READ:"+line)
		return route_info




prefix_obj = Prefix('rib_data')
prefix_obj.build_prefix()
prefix_obj.display_prefix()

