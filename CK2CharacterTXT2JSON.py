import argparse
from character_files_controller_module import CharacterFilesController
from name_mapping_module import NameMappingController


def arg_parser():
	parser = argparse.ArgumentParser(description='このスクリプトは Crusader Kings II の MOD である Nova Monumenta Iaponiae Historica (NMIH) のキャラクターデータが記載されたテキストファイルを操作するスクリプトです。')
	parser.add_argument('infolder', help='入力するキャラクターテキストファイルがあるフォルダを指定します')
	parser.add_argument('-o', '--output', help='出力ファイルの位置を指定します')
	parser.add_argument('-sv', '--set-version', help='MODのバージョンを指定します')
	parser.add_argument('-sc', '--set-commitid', help='ファイルのコミットIDを指定します')
	parser.add_argument('-cjn', '--char-jp-name', help='キャラクター名日本語対応表CSVを指定します')
	parser.add_argument('-djn', '--dynasty-jp-name', help='氏族名日本語対応表CSVを指定します')
	return parser.parse_args()

def main():
	args = arg_parser()
	char_files = CharacterFilesController(args.infolder, args.output, args.set_version, args.set_commitid, args.char_jp_name, args.dynasty_jp_name)
	char_files.read_txt()
	char_files.convert_dictionary()
	char_files.output_json()
	char_files.output_connexion_json()
	char_files.output_connexion_csv()


if __name__=='__main__':
	#
	#スクリプト引数見本
	#D:\lin\Repository\nova-monumenta-iaponiae-historica\NMIH\history\characters -sv 0.8.8 -sc 18b3778 -cjn D:\lin\Repository\nmih-japanese-name-mapping-table\character_name_japan.csv -djn D:\lin\Repository\nmih-japanese-name-mapping-table\dynasty_name_japan.csv
	main()
