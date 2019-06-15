class CharacterTalbe(object):
    """CSV出力するキャラクター一覧を操作するクラス"""

    header = list(["id",
				  "dynasty_id",
				 "dynasty_name", 
				 "dynasty_name_jp", 
				 "name_count", 
				 "name1", 
				 "name1_jp", 
				 "full_name1", 
				 "name2_date", 
				 "name2", 
				 "name2_jp", 
				 "name3_date", 
				 "name3", 
				 "name3_jp", 
				 "name4_date", 
				 "name4", 
				 "name4_jp", 
				 "name5_date", 
				 "name5", 
				 "name5_jp", 
				 "name6_date", 
				 "name6", 
				 "name6_jp", 
				 "father_count", 
				 "father1_date", 
				 "father1_id", 
				 "father1_name", 
				 "father1_name_ja", 
				 "father2_date", 
				 "father2_id",
				 "father2_name",
				 "father2_name_ja", 
				 "father3_date", 
				 "father3_id", 
				 "father3_name", 
				 "father3_name_ja", 
				 "real_father_id", 
				 "real_father_name", 
				 "real_father_name_jp", 
				 "mother_id", 
				 "mother_name", 
				 "mother_name_jp", 
				 "female", 
				 "martial", 
				 "diplomacy", 
				 "intrigue",
				 "stewardship", 
				 "learning", 
				 "religion", 
				 "culture", 
				 "birth", 
				 "death", 
				 "random_traits", 
				 "occluded", 
				 "dna", 
				 "properties", 
				 "file", 
				 "wiki", 
				 "comment", 
				 "comment2"
				])
    def __init__(self):
        self.characters_list = list()
    @classmethod
    def get_header_column_index(self, column):
        if column not in CharacterTalbe.header:
            return(False)
        return(CharacterTalbe.header.index(column))
    @classmethod
    def get_column_len(self):
        return(len(CharacterTalbe.header))