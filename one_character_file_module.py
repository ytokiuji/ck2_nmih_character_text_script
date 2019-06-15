import collections as cl
import json
import re
import pprint
import strategy
import datetime
from pathlib import Path
from character_talbe_module import CharacterTalbe

DEBUG_PRINT_LEVEL = 0

class TextFileCounter:
	def __init__(self):
		self.current_character_id = 0
		self.date_string_count = 0
		self.effect_if_count = 0
		self.line_count = 0
		self.line_scope_level = 0
		self.toplevel_trait_count = 0
		self.the_number_of_people = 0
		self.rename_count = 0
		self.rename_count_max = 0
		self.line_datescope_flag = False
		self.line_deathscope_flag = False
		self.line_effectscope_flag = False
		self.line_one_character_flag = False
		self.current_character_key = ""
		self.date_string = ""
		self.effect_scope_stack = list()
		self.effect_even_if_dead_scope_stack = list()
		self.current_character_id = list()
	def all_reset(self):
		self.current_character_id = 0
		self.date_string_count = 0
		self.effect_if_count = 0
		self.line_count = 0
		self.line_scope_level = 0
		self.toplevel_trait_count = 0
		self.the_number_of_people = 0
		self.rename_count = 0
		self.rename_count_max = 0
		self.line_datescope_flag = False
		self.line_deathscope_flag = False
		self.line_effectscope_flag = False
		self.line_one_character_flag = False
		self.current_character_key = ""
		self.date_string = ""
		self.effect_scope_stack.clear()
		self.effect_even_if_dead_scope_stack.clear()

class CK2CharacterTextFile:
	def __init__(self, filefullpath, mod_version, commitid, name_mapping_controller):
		self.path = filefullpath
		self.pre_json = cl.OrderedDict( {"file_name": str(filefullpath.name), "version": mod_version, "commitid": commitid, "createdate": str(datetime.date.today()) ,"character": {} } )
		self.character_list = [[None]*CharacterTalbe.get_column_len()]
		self.counter = TextFileCounter()
		self.name_mapping_controller = name_mapping_controller
		try:
			print("ファイルの読み込みはじめ：", filefullpath)
			with filefullpath.open(encoding="cp1252") as f:
				self.texts = f.readlines()
		except UnicodeEncodeError:
			print(filefullpath)
		else:
			#print(lines)
			print("ファイルの読み込みおわり：", filefullpath)
			f.close()
	def output_json(self):
		fw = open(str(self.path.name) + ".json", 'w')
		json.dump(self.pre_json, fw, indent=4)
		print("JSON出力完了：", fw.name)
		fw.close()
	def convert_texts_to_json(self):
		line_one_character_flag = False
		line_datescope_flag = False
		line_deathscope_flag = False
		line_effectscope_flag = False
		line_scope_level = 0
		
		self.counter.all_reset()
		
		line_count = 1
		current_character_id = -1
		toplevel_trait_count = 0
		date_string_count = 0
		effect_if_count = 0
		date_string = ""
		effect_scope_stack = list()
		effect_even_if_dead_scope_stack = list()
		print("Python辞書型データへの変換開始：", self.path)
		for line in self.texts:
			strategy.test_roop(line, self.counter, self.pre_json, self.character_list, self.name_mapping_controller)
		
