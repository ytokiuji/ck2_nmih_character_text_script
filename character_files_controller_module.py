import datetime
import json
import pprint
import csv
from pathlib import Path
from one_character_file_module import CK2CharacterTextFile
from character_talbe_module import CharacterTalbe
from name_mapping_module import NameMappingController

OUTPUT_CSV_ENCODING = 'utf_8_sig'
OUTPUT_CSV_FILE_NAME = str(datetime.date.today()) + '.csv'

class CharacterStatistics():
	"""
	すべてのキャラクターに関係する統計値を保持する。

	Attributes
	----------
	the_number_of_people : int
		キャラクター総数を集計する。
	rename_count_max : int
		全キャラクターの内、改名回数が最大のもの。
	"""
	def __init__(self):
		self.the_number_of_people = 0
		self.rename_count_max = 0
	def reset_all(self):
		self.the_number_of_people = 0
		self.rename_count_max = 0
	def increment_one_file(self, the_number_of_people):
		"""
		キャラクター人数を集計
		"""
		self.the_number_of_people += the_number_of_people
	def update_rename_count_max(self, count_max):
		"""
		改名回数最大を更新する
		"""
		if self.rename_count_max < count_max :
			self.rename_count_max = count_max

class CharacterFilesController():
	def __init__(self, input_folder_path, output_folder_path, mod_version, commitid, char_name_path=None, dynasty_name_path=None):
		"""
		キャラクターテキストファイルを読み込むための準備をする。

		Parameters
		----------
		input_folder_path : string
			読み込むフォルダのパス。
		output_folder_path : string
			出力するフォルダのパス（任意）。
		mod_version : string
			読み込むテキストファイルのMODバージョン（任意）。
		commitid : string
			読み込むテキストファイルのリポジトリのコミットID（任意）。
		"""
		self.input_folder_path = input_folder_path
		self.output_folder_path = output_folder_path
		self.mod_version = mod_version
		self.commitid = commitid
		self.txtfilepathlist = list()
		self.text_file_object_list = list() # 一つのキャラクターファイルを表すオブジェクトが入った配列
		self.all_character_date_dic = dict()
		self.all_character_date_list = list()
		self.counter = CharacterStatistics()
		self.name_mapping_controller = NameMappingController(char_name_path, dynasty_name_path)

	def read_txt(self):
		"""
		キャラクターテキストファイルを読み込み、python3辞書型データに格納する。
		"""
		input_folder = Path(self.input_folder_path)
		txtfilelist = list(input_folder.glob('**/*.txt'))
		
		for t in txtfilelist:
			self.txtfilepathlist.append(Path(t))

		for path in self.txtfilepathlist:
			self.text_file_object_list.append(CK2CharacterTextFile(path, self.mod_version, self.commitid, self.name_mapping_controller))

		print(len(self.text_file_object_list),"個のファイルを読み込みました。")

	def convert_dictionary(self):
		"""
		すべてのキャラクターファイルをPythonの辞書型データに変換し保存する。
		すべてのキャラクターファイルをPythonのリスト型データに変換し保存する。
		"""
		for text_one_file in self.text_file_object_list:
			text_one_file.convert_texts_to_json()
			self.counter.increment_one_file(text_one_file.counter.the_number_of_people)
			self.counter.update_rename_count_max(text_one_file.counter.rename_count_max)
	def output_json(self):
		"""
		すべてのキャラクターファイル辞書型データを各ファイルごとにJSON変換し保存する。
		"""
		for text_one_file in self.text_file_object_list:
			text_one_file.output_json()
			self.all_character_date_dic[str(text_one_file.path.name)] = text_one_file.pre_json
			self.all_character_date_list.append(text_one_file.character_list)
	def output_connexion_json(self):
		"""
		すべてのキャラクターファイル辞書型データを連結したものを一つのJSONに変換し保存する。
		"""
		fw = open(str(datetime.date.today()) + ".json", 'w')
		json.dump(self.all_character_date_dic, fw, indent=4)
		print("JSON出力完了：", fw.name)
		fw.close()
		print("総人数：", self.counter.the_number_of_people)
		print("改名回数最大：", self.counter.rename_count_max)
	def output_connexion_csv(self):
		"""
		すべてのキャラクターファイルリストデータを一つに連結する。
		"""
		with open(OUTPUT_CSV_FILE_NAME, 'w', encoding=OUTPUT_CSV_ENCODING, newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(CharacterTalbe.header)
			for one_file in self.all_character_date_list:
				for row in one_file:
					if row[CharacterTalbe.get_header_column_index("id")]:
						writer.writerow(row)