import re
class RePattern(object):
	rex100_name = re.compile(r"\s*name\s*\=\s*\"([\w\s\-\']+)\"")
	rex101_dynasty = re.compile(r"\s*dynasty\s*\=\s*(\d+)")
	rex102_father = re.compile(r"\s*father\s*\=\s*(\d+)")
	rex103_mother = re.compile(r"\s*mother\s*\=\s*(\d+)")	
	rex104_religion = re.compile(r"\s*religion\s*\=\s*\"?(\w+)\"?")
	rex105_culture = re.compile(r"\s*culture\s*\=\s*\"?(\w+)\"?")
	rex106_martial = re.compile(r"\s*martial\s*=\s*(\d+)")
	rex107_give_nickname = re.compile(r"^\s*give_nickname\s*=\s*\"?([\w\-]+)\"?")

	rex200_add_lover = re.compile(r"^\s*add_lover\s*=\s*(\d+)")
	rex201_wealth = re.compile(r"^\s*wealth\s*=\s*(\d+)")

	rex301_clr_character_flag = re.compile(r"^\s*clr_character_flag\s*\=\s*\"?([\w\-]+)\"?")
	rex302_clear_global_event_target = re.compile(r"^\s*clear_global_event_target\s*\=\s*\"?([\w\-]+)\"?")
	rex303_remove_consort = re.compile(r"^\s*remove_consort\s*\=\s*(\d+)")
	rex304_add_rival = re.compile(r"^\s*add_rival\s*=\s*(\d+)")
	rex305_add_friend = re.compile(r"^\s*add_friend\s*=\s*(\d+)")
	rex306_give_minor_title = re.compile(r"^\s*give_minor_title\s*=\s*\"?([\w\-]+)\"?")
	rex307_remove_nickname = re.compile(r"^\s*remove_nickname\s*=\s*yes")
	rex308_set_global_flag = re.compile(r"^\s*set_global_flag\s*=\s*\"?([\w\-]+)\"?")
	rex309_clr_global_flag = re.compile(r"^\s*clr_global_flag\s*=\s*\"?([\w\-]+)\"?")
	rex310_give_job_title = re.compile(r"^\s*give_job_title\s*=\s*\"?([\w\-]+)\"?")
	rex311_if_limit_not = re.compile(r"^\s*if\s*=\s*\{\s*limit\s*=\s*\{\s*NOT\s*=\s*\{\s*has_dlc\s*=\s*\"(\w+)\"\s*\}\s*\}\s*add_trait\s*=\s*(\w+)\s*\}\s*")
	rex312_if_limit = re.compile(r"^\s*if\s*=\s*\{\s*limit\s*=\s*\{\s*has_dlc\s*=\s*\"(\w+)\"\s*\}\s*add_trait\s*=\s*(\w+)\s*\}\s*")
	
	rex401_set_special_character_title = re.compile(r"^\s*set_special_character_title\s*=\s*\"?([\w\-]+)*\"?")
	rex402_add_character_modifier = re.compile(r"^\s*add_character_modifier\s*=\s*\{\s*modifier\s*=\s*([\w_]+)\s*duration\s*=\s*(-?\d+)\s*\}")
	rex403_c_character_id = re.compile(r"^\s*c_(\d+)\s*=\s*\{")
	
	rex501_province = re.compile(r"^\s*province\s*\=\s*(\d+)\s*\#*")
	rex502_owner = re.compile(r"^\s*owner\s*\=\s*(ROOT)")
	rex503_leader = re.compile(r"^\s*leader\s*\=\s*(ROOT)")
	rex504_attrition = re.compile(r"^\s*attrition\s*=\s*(\d+\.\d+)")

	rex601_add_alliance = re.compile(r"^\s*add_alliance\s*=\s*\{\s*who\s*=\s*ROOT\s*years\s*=\s*(\d+)\s*\}")
	rex602_modifier = re.compile(r"^\s*modifier\s*=\s*([\w\-]+)")


