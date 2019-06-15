import re
import pprint
import one_character_file_module
from regular_expression_module import RePattern
from character_talbe_module import CharacterTalbe

# 抽象戦略
class LineToDictionaryStrategy:
	def __init__(self, submit_func, counter, character_dic, line, character_list, name_mapping_controller=None):
		self.on_submit = submit_func
		self.counter = counter
		self.character_dic = character_dic
		self.line = line
		self.character_list = character_list
		self.name_mapping_controller = name_mapping_controller

def character_scope_start_line_to_dictionary_strategy(self):
	"""
	 char_id = { が来た時の具象戦略
	"""
	self.counter.current_character_id = int(re.match(r"\d+", self.line).group())
	self.counter.current_character_key = "c_" + str(self.counter.current_character_id)
	self.character_dic["character"][self.counter.current_character_key] = {}
	self.character_dic["character"][self.counter.current_character_key]["history"] = {}
	self.character_dic["character"][self.counter.current_character_key]["id"] = self.counter.current_character_id
	self.counter.line_one_character_flag = True
	self.counter.line_scope_level += 1
	self.counter.the_number_of_people += 1
	self.character_list.append([None]*CharacterTalbe.get_column_len())
	self.character_list[self.counter.the_number_of_people][CharacterTalbe.get_header_column_index("id")] = self.counter.current_character_id

def character_id_line_to_dictionary_strategy(self):
	"""
	 char_id = が来た時の具象戦略
	"""
	self.counter.current_character_id = int(re.match(r"\d+", self.line).group())
	self.counter.current_character_key = "c_" + self.counter.current_character_id
	self.character_dic["character"][self.counter.current_character_key] = {}
	self.character_dic["character"][self.counter.current_character_key]["history"] = {}
	self.character_dic["character"][self.counter.current_character_key]["id"] = self.counter.current_character_id
	self.counter.line_one_character_flag = True
	self.counter.the_number_of_people += 1
	self.character_list.append([None]*CharacterTalbe.get_column_len())
	self.character_list[self.counter.the_number_of_people][CharacterTalbe.get_header_column_index("id")] = self.counter.current_character_id

def curly_bracket_end_strategy(self):
	"""
	中括弧閉じ「}」が来た時の具象戦略
	"""
	self.counter.line_scope_level -= 1
	if len(self.counter.effect_scope_stack) > 1:
		self.counter.effect_scope_stack.pop()
	if len(self.counter.effect_even_if_dead_scope_stack) > 1:
		self.counter.effect_even_if_dead_scope_stack.pop()

def name_line_to_dictionary_strategy(self):
	"""
	キャラクタースコープ直下で（年月日スコープ内ではない）name = 行が来た時の具象戦略
	"""

	#name4 = "".join(re.match(r"\"(.+)\"", re.sub(r'name\s*=\s*', "", str.strip(self.line))).groups())
	name5 = str("".join(RePattern.rex100_name.match(self.line).groups()))

	self.character_dic["character"][self.counter.current_character_key]["name"] = name5
	self.character_list[self.counter.the_number_of_people][CharacterTalbe.get_header_column_index("name1")] = name5
	name1_jp = str(self.name_mapping_controller.get_localization_name(self.name_mapping_controller.ID_TYPE_CHARACTER, self.counter.current_character_id, name5))
	self.character_dic["character"][self.counter.current_character_key]["name1_jp"] = name1_jp
	self.character_list[self.counter.the_number_of_people][CharacterTalbe.get_header_column_index("name1_jp")] = name1_jp
	self.counter.rename_count += 1

def dynasty_line_to_dictionary_strategy(self):
	"""
	キャラクタースコープ直下で（年月日スコープ内ではない） \tdynasty= が来た時の具象戦略
	# if DEBUG_PRINT_LEVEL >= 1 : print("■はじめに出てくる氏族名です", str.strip(line))
	"""
	dynasty_name = ""
	dynasty1 = RePattern.rex101_dynasty.match(self.line).groups()
	self.character_dic["character"][self.counter.current_character_key]["dynasty_id"] = int("".join(dynasty1))
	self.character_list[self.counter.the_number_of_people][CharacterTalbe.get_header_column_index("dynasty_id")] = int("".join(dynasty1))
	if int("".join(dynasty1)) != 0:
		dynasty_name_jp = str(self.name_mapping_controller.get_localization_name(self.name_mapping_controller.ID_TYPE_DYNASTY, int("".join(dynasty1))))
		self.character_dic["character"][self.counter.current_character_key]["dynasty_name_jp"] = dynasty_name_jp
		self.character_list[self.counter.the_number_of_people][CharacterTalbe.get_header_column_index("dynasty_name_jp")] = dynasty_name_jp
		dynasty_name = str(self.name_mapping_controller.get_dynasty_name(int("".join(dynasty1))))
		self.character_dic["character"][self.counter.current_character_key]["dynasty_name"] = dynasty_name
		self.character_list[self.counter.the_number_of_people][CharacterTalbe.get_header_column_index("dynasty_name")] = dynasty_name
	if "name" in self.character_dic["character"][self.counter.current_character_key]:
		self.character_list[self.counter.the_number_of_people][CharacterTalbe.get_header_column_index("full_name1")] = dynasty_name + ' ' + self.character_dic["character"][self.counter.current_character_key]["name"]

def test_roop(line, counter, character_dic, character_list, name_mapping_controller):
	if re.match(r"^\s*$", line):
		pass
	#
	# 中括弧スコープはじめ
	#
	elif re.match(r"^\s*{\s*\#*", line):
		translate = LineToDictionaryStrategy(scope_level_increment, counter, character_dic,line, character_list)
		translate.on_submit(translate)
	#
	# 中括弧スコープおわり
	#
	elif re.match(r"^\s*}\s*\#*", line):
		translate = LineToDictionaryStrategy(curly_bracket_end_strategy, counter, character_dic, line, character_list)
		translate.on_submit(translate)
	#
	# コメント行
	#
	elif re.match(r"^\s*#", line):
		#print("■コメント行です")
		pass
	#
	# 1.キャラクタースコープはじめ
	#
	elif (not counter.line_datescope_flag) and re.match(r"^\d+\s*\=\s*\{", line):
		translate = LineToDictionaryStrategy(character_scope_start_line_to_dictionary_strategy, counter, character_dic, line, character_list)
		translate.on_submit(translate)
	elif (not counter.line_datescope_flag) and re.match(r"^\d+\s*\=\s*(?!\{)", line):
		translate = LineToDictionaryStrategy(character_id_line_to_dictionary_strategy, counter, character_dic, line, character_list)
		translate.on_submit(translate)
	#
	# 1.キャラクタースコープ直下
	#
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and RePattern.rex100_name.match(line):
		translate = LineToDictionaryStrategy(name_line_to_dictionary_strategy, counter, character_dic, line, character_list, name_mapping_controller)
		translate.on_submit(translate)
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and RePattern.rex101_dynasty.match(line):
		translate = LineToDictionaryStrategy(dynasty_line_to_dictionary_strategy, counter, character_dic, line, character_list, name_mapping_controller)
		translate.on_submit(translate)
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and RePattern.rex102_father.match(line):
		# if DEBUG_PRINT_LEVEL >= 1 : print("■はじめに出てくる父親キャラクターIDです")
		father1 =  RePattern.rex102_father.match(line).groups()
		character_dic["character"][counter.current_character_key]["father_id"] = int("".join(father1))
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("father1_id")] = int("".join(father1))
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and RePattern.rex103_mother.match(line):
		# if DEBUG_PRINT_LEVEL >= 1 : print("■",line_count,"はじめに出てくる母親キャラクターIDです")
		mother1 = RePattern.rex103_mother.match(line).groups()
		character_dic["character"][counter.current_character_key]["mother_id"] = int("".join(mother1))
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("mother_id")] = int("".join(mother1))
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and RePattern.rex104_religion.match(line):
		# if DEBUG_PRINT_LEVEL >= 1 : print("■はじめに出てくる宗教コードです", str.strip(line))
		religion1 = RePattern.rex104_religion.match(line).groups()
		character_dic["character"][counter.current_character_key]["religion_code"] = "".join(religion1)
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("religion")] = "".join(religion1)
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and RePattern.rex105_culture.match(line):
		# if DEBUG_PRINT_LEVEL >= 1 : print("■はじめに出てくる文化コードです")
		culture1 = RePattern.rex105_culture.match(line).groups()
		character_dic["character"][counter.current_character_key]["culture_code"] = "".join(culture1)
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("culture")] = "".join(culture1)
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and re.match(r"\s*disallow_random_traits\s*\=\s*yes", line):
		# if DEBUG_PRINT_LEVEL >= 1 : print("■はじめに出てくるランダム特質不許可フラグです")
		character_dic["character"][counter.current_character_key]["disallow_random_traits"] = True
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("random_traits")] = True
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and re.match(r"\s*add_trait\s*\=", line):
		# if DEBUG_PRINT_LEVEL >= 1 : print("■はじめに出てくる特質追加です")
		counter.toplevel_trait_count += 1
		addtrait1 = re.match(r"\s*add_trait\s*\=\s*\"?(\w+)\"?" ,line).groups()
		character_dic["character"][counter.current_character_key]["trait_code" + str(counter.toplevel_trait_count)] = "".join(addtrait1)
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and re.match(r"\s*trait\s*\=", line):
		# if DEBUG_PRINT_LEVEL >= 1 : print("■", line_count, "はじめに出てくる特質追加です", str.strip(line))
		counter.toplevel_trait_count += 1
		trait1 = re.match(r"\s*trait\s*\=\s*\"?(\w+)\"?" ,line).groups()
		character_dic["character"][counter.current_character_key]["trait_code" + str(counter.toplevel_trait_count)] = "".join(trait1)
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and re.match(r"\s*female\s*\=\s*yes", line):
		# if DEBUG_PRINT_LEVEL >= 1 : print("■はじめに出てくる女性フラグです")
		character_dic["character"][counter.current_character_key]["female"] = True
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("female")] = True
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and RePattern.rex106_martial.match(line):
		# if DEBUG_PRINT_LEVEL >= 1 : print("■", counter.line_count, "はじめに出てくる軍事能力値です", str.strip(line))
		martial1 = RePattern.rex106_martial.match(line).groups()
		character_dic["character"][counter.current_character_key]["martial"] = int("".join(martial1))
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("martial")] = int("".join(martial1))
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and re.match(r"\s*diplomacy\s*\=", line):
		diplomacy1 = re.match(r"\s*diplomacy\s*\=\s*(\d+)" ,line).groups()
		character_dic["character"][counter.current_character_key]["diplomacy"] = int("".join(diplomacy1))
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("diplomacy")] = int("".join(diplomacy1))
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and re.match(r"\s*intrigue\s*\=", line):
		intrigue1 = re.match(r"\s*intrigue\s*\=\s*(\d+)" ,line).groups()
		character_dic["character"][counter.current_character_key]["intrigue"] = int("".join(intrigue1))
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("intrigue")] = int("".join(intrigue1))
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and re.match(r"\s*stewardship\s*\=", line):
		stewardship1 = re.match(r"\s*stewardship\s*\=\s*(\d+)" ,line).groups()
		character_dic["character"][counter.current_character_key]["stewardship"] = int("".join(stewardship1))
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("stewardship")] = int("".join(stewardship1))
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and re.match(r"\s*learning\s*\=", line):
		# if DEBUG_PRINT_LEVEL >= 1 : print("■はじめに出てくる学習能力値です")
		learning1 = re.match(r"\s*learning\s*\=\s*(\d+)" ,line).groups()
		character_dic["character"][counter.current_character_key]["learning"] = int("".join(learning1))
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("learning")] = int("".join(learning1))
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and re.match(r"^\s*effect\s*=\s*\{\s*set_character_flag\s*=\s*\w+\s*\}", line):
		pass
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and RePattern.rex107_give_nickname.match(line):
		temp_give_nickname = RePattern.rex107_give_nickname.match(line).groups()
		character_dic["character"][counter.current_character_key]["give_nickname"] = "".join(temp_give_nickname)
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and re.match(r"\s*properties\s*\=", line):
		"""
		properties
		"""
		properties1 = re.match(r"\s*properties\s*\=\s*\"?(\w+)\"?" ,line).groups()
		character_dic["character"][counter.current_character_key]["properties"] = "".join(properties1)
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("properties")] = "".join(properties1)
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and re.match(r"\s*dna\s*\=", line):
		"""
		dna
		"""
		dna1 = re.match(r"\s*dna\s*\=\s*\"?(\w+)\"?" ,line).groups()
		character_dic["character"][counter.current_character_key]["dna"] = "".join(dna1)
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("dna")] = "".join(dna1)
	#
	# 2．年月日スコープ内容
	#
	elif counter.line_one_character_flag and (not counter.line_datescope_flag) and re.match(r"^\s*\d{1,4}\.\d{1,2}\.\d{1,2}\s*=\s*\{", line):
		counter.line_datescope_flag = True
		counter.line_scope_level += 1
		counter.date_string_count += 1
		# if DEBUG_PRINT_LEVEL >= 1 : print("■DATEスコープはじめ（はじめ中括弧あり）: ", counter.line_scope_level)
		date1 = re.match(r"^\s*(\d{1,4}\.\d{1,2}\.\d{1,2})\s*\=\s*\{" ,line).groups()
		counter.date_string = "".join(date1)
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)] = {}
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["date"] = counter.date_string
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*birth\s*\=\s*yes", line):
		"""
		生年月日1
		"""
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["birth"] = True
		character_dic["character"][counter.current_character_key]["birth_date"] = counter.date_string
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("birth")] = counter.date_string
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*birth\=\s*\"\d{1,4}\.\d{1,2}\.\d{1,2}\"", line):
		"""
		生年月日2
		"""
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["birth"] = True
		character_dic["character"][counter.current_character_key]["birth_date"] = counter.date_string
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("birth")] = counter.date_string
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*death\s*\=\s*yes", line):
		"""
		没年月日1
		"""
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["death"] = True
		character_dic["character"][counter.current_character_key]["death_date"] = counter.date_string
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("death")] = counter.date_string
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*death\=\s*\"\d{1,4}\.\d{1,2}\.\d{1,2}\"", line):
		"""
		没年月日2
		"""
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["death"] = True
		character_dic["character"][counter.current_character_key]["death_date"] = counter.date_string
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("death")] = counter.date_string
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*death\s*\=\s*\{\s*.+\s*\}", line):
		"""
		没年月日3
		"""
		counter.line_deathscope_flag = True
		# if DEBUG_PRINT_LEVEL >= 1 : print("■DEATHスコープはじめ（はじめ＆おわり中括弧あり）: ", counter.line_scope_level)
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["death"] = True
		character_dic["character"][counter.current_character_key]["death_date"] = counter.date_string
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("death")] = counter.date_string
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*death\s*\=\s*\{", line):
		"""
		没年月日スコープはじめ
		"""
		counter.line_scope_level += 1
		counter.line_deathscope_flag = True
		# if DEBUG_PRINT_LEVEL >= 1 : print("■DEATHスコープはじめ（はじめ中括弧あり）: ", counter.line_scope_level)
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["death"] = True
		character_dic["character"][counter.current_character_key]["death_date"] = counter.date_string
		character_list[counter.the_number_of_people][CharacterTalbe.get_header_column_index("death")] = counter.date_string
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*death_reason\s*\=\s*", line):
		"""
		死因
		"""
		death_reason1 = re.match(r"^\s*death_reason\s*\=\s*\"?(\w+)\"?" ,line).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["death_reason"] = "".join(death_reason1)
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*killer\s*\=\s*", line):
		"""
		殺害者
		"""
		killer1 = re.match(r"^\s*killer\s*\=\s*(\d+)" ,line).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["killer"] = int("".join(killer1))
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*give_nickname\=\s*", line):
		give_nickname1 = re.match(r"^\s*give_nickname\s*\=\s*\"?(\w+)\"?" ,line).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["give_nickname"] = "".join(give_nickname1)
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*add_spouse\s*\=\s*", line):
		add_spouse1 = re.match(r"^\s*add_spouse\s*\=\s*(\d+)" ,line).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["add_spouse"] = int("".join(add_spouse1))
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*remove_spouse\s*\=\s*", line):
		remove_spouse1 = re.match(r"^\s*remove_spouse\s*\=\s*(\d+)" ,line).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["remove_spouse"] = int("".join(remove_spouse1))
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*employer\s*\=\s*", line):
		employer1 = re.match(r"^\s*employer\s*\=\s*(\d+)" ,line).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["employer"] = int("".join(employer1))
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*dynasty\s*\=\s*", line):
		dynasty2 = re.match(r"^\s*dynasty\s*\=\s*(\d+)" ,line).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["dynasty"] = int("".join(dynasty2))
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*(add_)?trait\s*=\s*", line):
		if counter.line_scope_level > 2 : raise Exception("△年月日スコープ直下より下のスコープレベルで該当しました") # 年月日スコープ直下以外
		add_trait2 = re.match(r"^\s*(add_)?trait\s*=\s*\"?(\w+)\"?" ,line).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["add_trait"] = "".join(add_trait2[1])
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*remove_trait\s*=\s*", line):
		remove_trait2 = re.match(r"^\s*remove_trait\s*=\s*\"?(\w+)\"?" ,line).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["remove_trait"] = "".join(remove_trait2)
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*culture\s*=\s*", line):
		if counter.line_scope_level > 2 : raise Exception("△年月日スコープ直下より下のスコープレベルで該当しました") # 年月日スコープ直下以外
		temp_culture = re.match(r"^\s*culture\s*=\s*\"?(\w+)\"?" ,line).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["culture_code"] = "".join(temp_culture)
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*religion\s*=\s*\"?(\w+)\"?", line):
		if counter.line_scope_level > 2 : raise # 年月日スコープ直下以外
		temp_religion = re.match(r"^\s*religion\s*=\s*\"?(\w+)\"?" ,line).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["religion_code"] = "".join(temp_religion)
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*(add|remove)_claim\s*=\s*\"?(\w+)\"?", line):
		temp_add_claim = re.match(r"^\s*(add|remove)_claim\s*=\s*\"?(\w+)\"?" ,line).groups()
		if len(counter.effect_scope_stack) > 0:
			character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"][temp_add_claim[0] + "_claim"] = temp_add_claim[1]
		else:
			character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)][temp_add_claim[0] + "_claim"] = temp_add_claim[1]
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*add_matrilineal_spouse\s*=\s*(\d+)", line):
		temp_add_matrilineal_spouse = re.match(r"^\s*add_matrilineal_spouse\s*=\s*(\d+)" ,line).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["add_matrilineal_spouse"] = int("".join(temp_add_matrilineal_spouse))
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*name\s*=\s*\"?([\w\-\s]+)\"?", line):
		temp_name = re.match(r"^\s*name\s*=\s*\"?([\w\-\s]+)\"?" ,line).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["name"] = "".join(temp_name)
		counter.rename_count += 1
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*add_consort\s*=\s*(\d+)", line):
		temp_add_consort = re.match(r"^\s*add_consort\s*=\s*(\d+)" ,line).groups()
		if len(counter.effect_scope_stack) > 0:
			character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["add_consort"] = int("".join(temp_add_consort))
		else:
			character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["add_consort"] = int("".join(temp_add_consort))
	## remove_nickname 一行完結スコープなし
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 0 and RePattern.rex307_remove_nickname.match(line):
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["remove_nickname"] = True
	## add_lover
	elif counter.line_one_character_flag and counter.line_datescope_flag and RePattern.rex200_add_lover.match(line):
		temp_add_lover = RePattern.rex200_add_lover.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["add_lover"] = int("".join(temp_add_lover))
	## mother
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 0 and RePattern.rex103_mother.match(line):
		temp_mother = RePattern.rex103_mother.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["mother_id"] = int("".join(temp_mother))
	## wealth
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 0 and RePattern.rex201_wealth.match(line):
		temp_wealth = RePattern.rex201_wealth.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["wealth"] = int("".join(temp_wealth))
	#
	# 2.年月日スコープ直下　Effectスコープ一行完結もの
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*effect\s*=\s*\{\s*remove_nickname\s*=\s*yes\s*\}", line):
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"] = {"remove_nickname" : True}
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*effect\s*=\s*\{\s*add_consort\s*=\s*\d+\s*\}", line):
		add_consort1 = re.match(r"^\s*effect\s*=\s*\{\s*add_consort\s*=\s*(\d+)\s*\}" ,str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"] = {"add_consort" : int("".join(add_consort1))}
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*effect\s*=\s*\{\s*break_betrothal\s*=\s*\d+\s*\}", line):
		break_betrothal1 = re.match(r"^\s*effect\s*=\s*\{\s*break_betrothal\s*=\s*(\d+)\s*\}" ,str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"] = {"break_betrothal" : int("".join(break_betrothal1))}
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*effect\s*=\s*\{\s*add_betrothal\s*=\s*\d+\s*\}", line):
		add_betrothal1 = re.match(r"^\s*effect\s*=\s*\{\s*add_betrothal\s*=\s*(\d+)\s*\}" ,str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"] = {"add_betrothal" : int("".join(add_betrothal1))}
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*effect\s*=\s*\{\s*c_\d+\s*=\s*\{\s*add_lover\s*=\s*ROOT\s*\}\s*\}", line):
		add_lover1 = re.match(r"^\s*effect\s*=\s*\{\s*c_(\d+)\s*=\s*\{\s*add_lover\s*=\s*ROOT\s*\}\s*\}" ,str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"] = {"add_lover" : int("".join(add_lover1))}
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*effect\s*=\s*\{\s*add_lover\s*=\s*\d+\s*\}", line):
		add_lover1 = re.match(r"^\s*effect\s*=\s*\{\s*add_lover\s*=\s*(\d+)\s*\}" ,str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"] = {"add_lover" : int("".join(add_lover1))}
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*effect\s*=\s*\{\s*c_\w+\s*=\s*\{\s*ROOT\s*=\s*\{\s*capital\s*=\s*PREV\s*\}\s*\}\s*\}", line):
		capital1 = re.match(r"^\s*effect\s*=\s*\{\s*(c_\w+)\s*=\s*\{\s*ROOT\s*=\s*\{\s*capital\s*=\s*PREV\s*\}\s*\}\s*\}" ,str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"] = {"capital" : "".join(capital1)}
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*effect\s*=\s*\{\s*clr_character_flag\s*=\s*\"?\w+\"?\s*\}", line):
		clr_character_flag1 = re.match(r"^\s*effect\s*=\s*\{\s*clr_character_flag\s*=\s*\"?(\w+)\"?\s*\}" ,str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"] = {"clr_character_flag" : "".join(clr_character_flag1)}
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*effect\s*=\s*\{\s*set_character_flag\s*=\s*\w+\s*\}", line):
		set_character_flag1 = re.match(r"^\s*effect\s*=\s*\{\s*set_character_flag\s*=\s*\"?(\w+)\"?\s*\}" ,str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"] = {"set_character_flag" : "".join(set_character_flag1)}
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*effect\s*=\s*\{\s*c_\d+\s*=\s*\{\s*ROOT\s*=\s*\{\s*set_real_father\s*=\s*PREV\s*\}\s*\}\s*\}", line):
		set_real_father1 = re.match(r"^\s*effect\s*=\s*\{\s*c_(\d+)\s*=\s*\{\s*ROOT\s*=\s*\{\s*set_real_father\s*=\s*PREV\s*\}\s*\}\s*\}" , str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"] = {"set_real_father" : int("".join(set_real_father1))}
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*effect\s*=\s*\{\s*c_\d+\s*=\s*\{\s*add_consort\s*=\s*ROOT\s*\}\s*\}", line):
		add_consort1 = re.match(r"^\s*effect\s*=\s*\{\s*c_(\d+)\s*=\s*\{\s*add_consort\s*=\s*ROOT\s*\}\s*\}" , str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"] = {"add_consort" : int("".join(add_consort1))}
	#
	# 3. effect_even_if_deadスコープはじめ
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 0 and re.match(r"^\s*effect_even_if_dead\s*=\s*\{", line):
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect_even_if_dead"] = {}
		counter.line_scope_level += 1
		counter.effect_even_if_dead_scope_stack.append("effect_even_if_dead")
	#
	# 4. set_special_character_title一行完結スコープなし
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_even_if_dead_scope_stack) == 1 and RePattern.rex401_set_special_character_title.match(line):
		temp_set_special_character_title = RePattern.rex401_set_special_character_title.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect_even_if_dead"]["set_special_character_title"] = "".join(temp_set_special_character_title)
	#
	# 4. add_character_modifier 一行完結スコープあり
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_even_if_dead_scope_stack) == 1 and RePattern.rex402_add_character_modifier.match(line):
		temp_add_character_modifier = RePattern.rex402_add_character_modifier.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect_even_if_dead"]["add_character_modifier"] = {"modifier" : temp_add_character_modifier[0], "duration": int(temp_add_character_modifier[1])}
	#
	# 3.Effectスコープはじめ
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*effect\s*\=\s*\{", line):
		counter.line_scope_level += 1
		counter.line_effectscope_flag = True
		# if DEBUG_PRINT_LEVEL >= 1 : print("■EFECTスコープはじめ（はじめ中括弧あり）: ", counter.line_scope_level)
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"] = {}
		counter.effect_scope_stack.append("effect") # 名前付きスコープのスタック
	#
	# 3.Effectスコープ内容
	#
	## 
	elif counter.line_one_character_flag and counter.line_datescope_flag and RePattern.rex312_if_limit.match(line):
		counter.effect_if_count += 1
		if_limit = RePattern.rex312_if_limit.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["if_" + str(counter.effect_if_count)] = {"limit" : {}}
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["if_" + str(counter.effect_if_count)]["limit"] = {"has_dlc" : "".join(if_limit[0])}
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["if_" + str(counter.effect_if_count)]["add_trait"] = "".join(if_limit[1])
				
	## if={limit = {NOT={has_dlc="Reapers"}}add_trait = ill}
	elif counter.line_one_character_flag and counter.line_datescope_flag and RePattern.rex311_if_limit_not.match(line):
		counter.effect_if_count += 1
		if_limit_not = RePattern.rex311_if_limit_not.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["if_" + str(counter.effect_if_count)] = {"limit" : {"NOT" : {}}}
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["if_" + str(counter.effect_if_count)]["limit"]["NOT"]["has_dlc"] = "".join(if_limit_not[0])
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["if_" + str(counter.effect_if_count)]["add_trait"] = "".join(if_limit_not[1])
	## 養子一行完結
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and re.match(r"^\s*c_\d+\s*=\s*\{\s*ROOT\s*=\s*\{\s*set_real_father\s*=\s*PREV\s*\}\s*\}", line):
		# if DEBUG_PRINT_LEVEL >= 1 : print("■養子設定句（はじめおわり中括弧あり）: ", counter.line_scope_level)
		set_real_father1 = re.match(r"^\s*c_(\d+)\s*=\s*\{\s*ROOT\s*=\s*\{\s*set_real_father\s*=\s*PREV\s*\}\s*\}" , str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["set_real_father"] = int("".join(set_real_father1))
	## 婚約一行完結
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and re.match(r"^\s*add_betrothal\s*\=\s*", line):
		add_betrothal1 = re.match(r"^\s*add_betrothal\s*\=\s*(\d+)" ,line).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["add_betrothal"] = int("".join(add_betrothal1))
	## 婚約破棄一行完結
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and re.match(r"^\s*break_betrothal\s*\=\s*", line):
		break_betrothal1 = re.match(r"^\s*break_betrothal\s*\=\s*(\d+)" ,line).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["break_betrothal"] = int("".join(break_betrothal1))
	## 首都指定一行完結
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and re.match(r"^\s*[bcdke]_[a-zA-Z_\-]+\s*\=\s*\{\s*ROOT\s*\=\s*\{\s*capital\s*\=\s*PREV\s*\}\s*\}", line):
		x_title_scope = re.match(r"^\s*([bcdke]_[a-zA-Z_\-]+)\s*=\s*\{\s*ROOT\s*=\s*\{\s*capital\s*=\s*PREV\s*\}\s*\}" ,str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["capital"] = "".join(x_title_scope)
		# if DEBUG_PRINT_LEVEL >= 1 : print("■首都指定句（はじめおわり中括弧あり）: ", counter.line_scope_level)
	## 第一タイトル指定一行完結
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and re.match(r"^\s*[bcdke]_[a-zA-Z_\-]+\s*=\s*\{\s*make_primary_title\s*=\s*yes\s*\}", line):
		xx_title_scope = re.match(r"^\s*([bcdke]_[a-zA-Z_\-]+)\s*=\s*\{\s*make_primary_title\s*=\s*yes\s*\}" ,str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["make_primary_title"] = "".join(xx_title_scope)
	## キャラクターフラグセット一行完結スコープなし
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and re.match(r"^\s*set_character_flag\s*=\s*", line):
		temp_set_character_flag = re.match(r"^\s*set_character_flag\s*=\s*\"?([\w_\-]+)\"?" ,str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["set_character_flag"] = "".join(temp_set_character_flag)
	## タイトル削除一行完結スコープなし
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and re.match(r"^\s*remove_title\s*=\s*\"?([\w\-]+)\"?", line):
		temp_remove_title = re.match(r"^\s*remove_title\s*=\s*\"?([\w\-]+)\"?" ,str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["remove_title"] = "".join(temp_remove_title)
	## 一行完結スコープなし
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and re.match(r"^\s*save_global_event_target_as\s*\=\s*\"?([\w\-]+)\"?", line):
		temp_save_global_event_target_as = re.match(r"^\s*save_global_event_target_as\s*\=\s*\"?([\w\-]+)\"?" ,str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["save_global_event_target_as"] = "".join(temp_save_global_event_target_as)
	## アーティファクト追加一行完結スコープなし
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and re.match(r"^\s*add_artifact\s*\=\s*\"?([\w\-]+)\"?", line):
		temp_add_artifact = re.match(r"^\s*add_artifact\s*\=\s*\"?([\w\-]+)\"?" ,str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["add_artifact"] = "".join(temp_add_artifact)
	## clr_character_flag一行完結スコープなし
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and RePattern.rex301_clr_character_flag.match(line):
		temp_clr_character_flag = RePattern.rex301_clr_character_flag.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["clr_character_flag"] = "".join(temp_clr_character_flag)
	## clear_global_event_target一行完結スコープなし
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and RePattern.rex302_clear_global_event_target.match(line):
		temp_clear_global_event_target = RePattern.rex302_clear_global_event_target.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["clear_global_event_target"] = "".join(temp_clear_global_event_target)
	## remove_consort 一行完結スコープなし
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and RePattern.rex303_remove_consort.match(line):
		temp_remove_consort = RePattern.rex303_remove_consort.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["remove_consort"] = int("".join(temp_remove_consort))
	## add_rival 一行完結スコープなし
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and RePattern.rex304_add_rival.match(line):
		temp_add_rival = RePattern.rex304_add_rival.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["add_rival"] = int("".join(temp_add_rival))
	## add_friend 一行完結スコープなし
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and RePattern.rex305_add_friend.match(line):
		temp_add_friend = RePattern.rex305_add_friend.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["add_friend"] = int("".join(temp_add_friend))
	## give_minor_title 一行完結スコープなし
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and RePattern.rex306_give_minor_title.match(line):
		temp_give_minor_title = RePattern.rex306_give_minor_title.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["give_minor_title"] = "".join(temp_give_minor_title)
	## remove_nickname 一行完結スコープなし
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and RePattern.rex307_remove_nickname.match(line):
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["remove_nickname"] = True
	## set_global_flag 一行完結スコープなし
	elif counter.line_one_character_flag and counter.line_datescope_flag and (len(counter.effect_scope_stack) == 1 or len(counter.effect_even_if_dead_scope_stack) == 1) and RePattern.rex308_set_global_flag.match(line):
		temp_set_global_flag = RePattern.rex308_set_global_flag.match(str.strip(line)).groups()
		if len(counter.effect_scope_stack) == 1:
			character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["set_global_flag"] = "".join(temp_set_global_flag)
		elif len(counter.effect_even_if_dead_scope_stack) == 1:
			character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect_even_if_dead"]["set_global_flag"] = "".join(temp_set_global_flag)
		else:
			raise Exception("想定されていない行です", str.strip(line))
	### clr_global_flag 一行完結スコープなし
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and RePattern.rex309_clr_global_flag.match(line):
		temp_clr_global_flag = RePattern.rex309_clr_global_flag.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["clr_global_flag"] = "".join(temp_clr_global_flag)
	### give_job_title 一行完結スコープなし
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and RePattern.rex310_give_job_title.match(line):
		temp_give_job_title = RePattern.rex310_give_job_title.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["give_job_title"] = "".join(temp_give_job_title)
	#
	# 4. spawn_unit スコープはじめ
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and re.match(r"^\s*spawn_unit\s*\=\s*\{$", line):
		counter.line_scope_level += 1
		# if DEBUG_PRINT_LEVEL >= 1 : print("■SPAWN_UNITスコープはじめ（はじめ中括弧あり）: ", counter.line_scope_level)
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["spawn_unit"] = {}
		counter.effect_scope_stack.append("spawn_unit")
	#
	# 5. province 一行完結スコープなし
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 2 and counter.effect_scope_stack[1] == "spawn_unit" and RePattern.rex501_province.match(line):
		temp_province_id = RePattern.rex501_province.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["spawn_unit"]["province"] = int("".join(temp_province_id))
	#
	# 5. owner 一行完結スコープなし
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 2 and counter.effect_scope_stack[1] == "spawn_unit" and RePattern.rex502_owner.match(line):
		temp_owner_code = RePattern.rex502_owner.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["spawn_unit"]["owner"] = "".join(temp_owner_code)
	#
	# 5. leader 一行完結スコープなし
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 2 and counter.effect_scope_stack[1] == "spawn_unit" and RePattern.rex503_leader.match(line):
		temp_leader_code = RePattern.rex503_leader.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["spawn_unit"]["leader"] = "".join(temp_leader_code)
	#
	# 5. troops スコープはじめ
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 2 and counter.effect_scope_stack[1] == "spawn_unit" and re.match(r"^\s*troops\s*\=\s*\{", line):
		counter.line_scope_level += 1
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["spawn_unit"]["troops"] = {}
		counter.effect_scope_stack.append("troops")
		# if DEBUG_PRINT_LEVEL >= 1 : print("■TROOPSスコープはじめ（はじめ中括弧あり）: ", counter.line_scope_level)
	#
	# 6. light_infantry|light_cavalry|archers 一行完結スコープあり
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 3 and counter.effect_scope_stack[2] == "troops" and re.match(r"^\s*(light_infantry|light_cavalry|archers)\s*=\s*\{\s*(\d+)\s*(\d+)\s*\}", line):
		temp_troopsclass = re.match(r"^\s*(light_infantry|light_cavalry|archers)\s*=\s*\{\s*(\d+)\s*(\d+)\s*\}", str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["spawn_unit"]["troops"][temp_troopsclass[0]] = [int(temp_troopsclass[1]), int(temp_troopsclass[2])]
	#
	# 5. attrition 一行完結スコープなし
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) >= 2 and counter.effect_scope_stack[1] == "spawn_unit" and RePattern.rex504_attrition.match(line):
		temp_attrition = RePattern.rex504_attrition.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["spawn_unit"]["attrition"] = float("".join(temp_attrition))
	#
	# 4. Cキャラクタースコープはじめ
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and RePattern.rex403_c_character_id.match(line):
		counter.line_scope_level += 1
		temp_c_character_id = RePattern.rex403_c_character_id.match(str.strip(line)).groups()
		temp_str_c_character_id = "".join(temp_c_character_id)
		counter.effect_scope_stack.append(int(temp_str_c_character_id))
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["c_" + temp_str_c_character_id] = {}
	#
	# 5. opinionスコープはじめ
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 2 and re.match(r"^\s*opinion\s*=\s*\{", line):
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["c_" + str(counter.effect_scope_stack[1])]["opinion"] = {}
		counter.line_scope_level += 1
		counter.effect_scope_stack.append("opinion")
	#
	# 6. who = ROOT 一行完結スコープなし
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) >= 3 and counter.effect_scope_stack[2] == "opinion" and re.match(r"^\s*who\s*=\s*ROOT", line):
		if len(counter.effect_scope_stack) == 4:
			character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["c_" + str(counter.effect_scope_stack[1])]["opinion"] = { "character_id" : counter.effect_scope_stack[1], "modifier" : counter.effect_scope_stack[3]}
			counter.effect_scope_stack.pop()
		else:
			counter.effect_scope_stack.append("ROOT")
	#
	# 6. modifier 一行完結スコープなし
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) >= 3 and counter.effect_scope_stack[2] == "opinion" and RePattern.rex602_modifier.match(line):
		temp_modifier = RePattern.rex602_modifier.match(str.strip(line)).groups()
		if len(counter.effect_scope_stack) == 4:
			character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["c_" + str(counter.effect_scope_stack[1])]["opinion"] = { "character_id" : counter.effect_scope_stack[1], "modifier" : "".join(temp_modifier)}
			counter.effect_scope_stack.pop()
		else:
			counter.effect_scope_stack.append("".join(temp_modifier))
	#
	# 4.タイトルスコープはじめ
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 1 and re.match(r"^\s*([bcdke]_[a-zA-Z\-_]+)\s*=\s*\{", line):
		counter.line_scope_level += 1
		# if DEBUG_PRINT_LEVEL >= 1 : print("■C_スコープはじめ（はじめ中括弧あり）: ", counter.line_scope_level)
		x_title_scope = re.match(r"^\s*([bcdke]_[\w\-]+)\s*=\s*\{" ,str.strip(line)).groups()
		counter.effect_scope_stack.append("".join(x_title_scope)) # 名前付きスコープのスタック
	#
	# 5. holder_scope スコープはじめ <4.タイトルスコープ以下>
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 2 and re.match(r"^\s*holder_scope\s*=\s*\{", line):
		counter.line_scope_level += 1
		counter.effect_scope_stack.append("holder_scope")
	#
	# 6. break_alliance=FROM 一行完結スコープなし
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 3 and len(counter.effect_scope_stack) == 3 and re.match(r"^\s*break_alliance\s*=\s*FROM", line):
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["break_alliance"] = { "title": counter.effect_scope_stack[1] }
	#
	# 6. add_alliance 一行完結スコープあり
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and len(counter.effect_scope_stack) == 3 and len(counter.effect_scope_stack) == 3 and RePattern.rex601_add_alliance.match(line):
		temp_add_alliance = RePattern.rex601_add_alliance.match(str.strip(line)).groups()
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"]["add_alliance"] = { "title": counter.effect_scope_stack[1], "years" : int("".join(temp_add_alliance)) }
	#
	# 5.ROOTスコープはじめ
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*ROOT=\s*\{", line):
		character_dic["character"][counter.current_character_key]["history"]["date" + str(counter.date_string_count)]["effect"][ counter.effect_scope_stack.pop() ] = { "ROOT" : {} }
		counter.line_scope_level += 1
		counter.effect_scope_stack.append("ROOT") # 名前付きスコープのスタック
		# if DEBUG_PRINT_LEVEL >= 1 : print("■ROOTスコープはじめ（はじめ中括弧あり）: ", counter.line_scope_level)
	#
	# 6. ROOTスコープ内容
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*capital\s*=\s*PREV$", line):
		pass
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*set_real_father\s*=\s*PREV", line):
		pass
	#
	#
	#
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*father\s*=\s*", line):
		pass
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*[bcdke]_[\w\-]+\s*=\s*\{\s*make_primary_title\s*=\s*yes\s*\}$", line):
		# if DEBUG_PRINT_LEVEL >= 1 : print("■第一称号指定句（はじめおわり中括弧あり）: ", counter.line_scope_level)
		# if DEBUG_PRINT_LEVEL >= 1 : print("■第一称号指定句（はじめおわり中括弧あり）: ", counter.line_scope_level)
		pass
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*opinion\s*=\s*\{.+\}", line):
		pass
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*[bcdke]_[\w\-]+\s*=\s*\{", line):
		counter.line_scope_level += 1
		# if DEBUG_PRINT_LEVEL >= 1 : print("■タイトルスコープ（はじめ中括弧あり）: ", counter.line_scope_level)
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*raise_levies\s*=\s*\{$", line):
		counter.line_scope_level += 1
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*location\s*=\s*\d+", line):
		pass
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*force_mult\s*=\s*\d+", line):
		pass
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*(heavy_infantry|pikemen)\s*=\s*\{\s*\d+\s*\d+\s*\}$", line):
		pass
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*dismiss\s*=\s*yes$", line):
		pass
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*disband_event_forces\s*=\s*yes", line):
		pass
	elif counter.line_one_character_flag and counter.line_datescope_flag and re.match(r"^\s*capital\s*=\s*\"?(\w|-)+\"?$", line):
		pass
	else:
		print("[L", counter.line_count , "] ", line)
	if counter.line_scope_level == 0:
		# 一人分のデータループがおわり
		counter.line_one_character_flag = False
		counter.line_datescope_flag = False
		counter.line_deathscope_flag = False
		counter.line_effectscope_flag = False
		counter.toplevel_trait_count = 0
		counter.date_string_count = 0
		if counter.rename_count_max < counter.rename_count :
			counter.rename_count_max = counter.rename_count
		counter.rename_count = 0
	elif counter.line_scope_level == 1:
		# 年月日スコープがおわり
		counter.line_datescope_flag = False
	elif counter.line_scope_level == 2:
		# Effectスコープなどおわり
		counter.line_effectscope_flag = False
		counter.effect_if_count = 0
		counter.effect_scope_stack.clear()
	elif counter.line_scope_level == 3:
		# effect > c_0000 スコープなどおわり
		pass
	counter.line_count += 1