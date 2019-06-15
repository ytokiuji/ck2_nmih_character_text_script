import sqlite3
import os
import csv
import pprint
import argparse
import sys

DATABASE_FILE_NAME = 'name_mapping.db'
CSV_ENCODING = 'utf_8_sig'
CHARACTER_TABLE_NAME = 'character_name_japan'
DYNASY_TABLE_NAME = 'dynasty_name_japan'

class NameMappingController(object):
    """description of class"""
    ID_TYPE_CHARACTER = 'character'
    ID_TYPE_DYNASTY = 'dynasty'

    def __init__(self, char_name_path=None, dynasty_name_path=None):
        self.database = NameMappingDB()
        self.char_name_path = char_name_path
        self.dynasty_name_path = dynasty_name_path
        self.char_name_list = list()
        self.dynasty_name_list = list()
        if char_name_path == None and dynasty_name_path == None:
            pass
        elif char_name_path != None and dynasty_name_path != None:
            self.read_csv(char_name_path, self.char_name_list)
            self.database.create_table(CHARACTER_TABLE_NAME, self.char_name_list)
            self.read_csv(dynasty_name_path, self.dynasty_name_list)
            self.database.create_table(DYNASY_TABLE_NAME, self.dynasty_name_list)
        elif char_name_path != None and dynasty_name_path == None:
            self.read_csv(char_name_path, self.char_name_list)
            self.database.create_table(CHARACTER_TABLE_NAME, self.char_name_list)
			#print(self.get_localization_name(self.ID_TYPE_CHARACTER, 103, "Takasue"))
        elif char_name_path == None and dynasty_name_path != None:
            self.read_csv(dynasty_name_path, self.dynasty_name_list)
            self.database.create_table(DYNASY_TABLE_NAME, self.dynasty_name_list)
        else:
            print(char_name_path, dynasty_name_path)
            raise Exception(self)
        #print(self.get_localization_name(self.ID_TYPE_DYNASTY, 3, "Onodera"))
        
    def read_csv(self, csv_path, name_list):
        """
        gitlab.com:nmihteam/nmih-japanese-name-mapping-table.git
        CSVファイルを読み込みます
        """
        with open(csv_path, newline='', encoding=CSV_ENCODING) as f:
            data_reader = csv.reader(f)
            for row in data_reader:
                name_list.append(row)

    def get_localization_name(self, id_type, id, name=None, date=None):
        """
        ID種類、ID、name、dateを受け取って翻訳後名前を返す

		Parameters
		----------
		id_type : string
			ID_TYPE_CHARACTER または ID_TYPE_DYNASTY。
		id : string
			キャラクターID または Dynasty ID。
		name : string
			キャラクター名または Dynasty 名
		date : string
			キャラクターファイルの年月日（任意）。
        """
        cur = self.database.conn.cursor()
        if id_type == NameMappingController.ID_TYPE_CHARACTER and date == None:
            #sql_str = 'select name_jp from ' + CHARACTER_TABLE_NAME + ' where id = \'' + str(id) + '\' and name = \"' + name + '\";'
            sql_str = 'select name_jp from ' + CHARACTER_TABLE_NAME + ' where id = ? and name = ?;'
            cur.execute(sql_str, (str(id), name))
        elif id_type == NameMappingController.ID_TYPE_CHARACTER and date != None:
            sql_str = 'select name_jp from ' + CHARACTER_TABLE_NAME + ' where id = ? and name = ? and date = ? ;'
            cur.execute(sql_str, (str(id), name, date))
        elif id_type == NameMappingController.ID_TYPE_DYNASTY:
            sql_str = 'select name_jp from ' + DYNASY_TABLE_NAME + ' where id = ? ;'
            cur.execute(sql_str, (str(id),))
        else:
            raise Exception(ID種類または引数が違います)
        name_jp = cur.fetchone()
        temp1 = None
        if name_jp != None:
            temp1 = ''.join(map(str, name_jp))
        return(temp1)

    def get_dynasty_name(self, id):
        """
        DynastyID を受け取って翻訳前名前を返す

		Parameters
		----------
		id : string
			Dynasty ID。
        """
        cur = self.database.conn.cursor()
        sql_str = 'select name from ' + DYNASY_TABLE_NAME + ' where id = ? ;'
        cur.execute(sql_str, (str(id),))
        name = cur.fetchone()
        cur.close()
        temp1 = None
        if name != None:
            temp1 = ''.join(map(str, name))
        return(temp1)

class NameMappingDB(object):
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_FILE_NAME)

    def create_table(self, tabale_name, create_data_list):
        """
        既存のテーブルを削除し、新しくテーブルを作成し、受け取ったリストデータをすべてインサートする。
        """
        cur = self.conn.cursor()
        cur.execute('drop table if exists %s;' % tabale_name)
        cur.execute("create table if not exists " + tabale_name + " (" + ", ".join(create_data_list[0]) + ")")
        for row in create_data_list[1:]:
            sql_incert = "insert into %s values (" + str('?,' * len(row)).rstrip(', ') + ')'
            cur.execute(sql_incert % tabale_name, (row))
        self.conn.commit()
        cur.execute("select name_jp, id, name from %s" % tabale_name)
        cur.close()

def arg_parser():
	parser = argparse.ArgumentParser(description='このスクリプトは Crusader Kings II の MOD である Nova Monumenta Iaponiae Historica (NMIH) の日本語名対応表が記載されたCSVファイルをデータベース（SQLite）に格納するスクリプトです。')
	parser.add_argument('-cjn', '--char-jp-name', help='キャラクター名日本語対応表CSVを指定します', nargs='+')
	parser.add_argument('-djn', '--dynasty-jp-name', help='氏族名日本語対応表CSVを指定します', nargs='+')
	return parser.parse_args()

def main():
	if len(sys.argv) < 2:
		raise Exception('引数が指定されていません')
		exit(1)
	args = arg_parser()
	name_mapping_controller = NameMappingController(str(args.char_jp_name), str(args.dynasty_jp_name))
	sys.exit(0)

if __name__=='__main__':
	main()
	#name_mapping_controller = NameMappingController()
	#print(name_mapping_controller.get_dynasty_name(2))