#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 12:47:13 2018

@author: alex
"""
from PCATParser import *
import json, os

class ProfileManager(object):
    
    def __init__(self):
        #identify the Profile
        try:
            self.cik_name = json.loads(open("data/profilemanager/data/cik_to_name.json", "r").read())
            self.name_cik = json.loads(open("data/profilemanager/data/name_to_cik.json", "r").read())
            self.name_alias = {}
        except Exception as e:
            print("Error reading in one of the profile indentifier files " + str(e))
        #sic <---> naics transforms
        try:
            self.naics_description = json.loads(open("data/profilemanager/data/naics2017_to_naics2017_title.json", "r").read())
            self.sic_description = json.loads(open("data/profilemanager/data/sic_to_description.json", "r").read())
            self.naics_sic = json.loads(open("data/profilemanager/data/naics_to_sic.json", "r").read())
            self.sic_naics = json.loads(open("data/profilemanager/data/sic_to_naics.json", "r").read())
        except Exception as e:
            print("Error reading in one of the SIC <---> NAICS Transforms " + str(e))
        
    def __contains__(self, key):
        if key in self.cik_name:
            return True
        elif key in self.name_cik:
            return True
        else:
            for i in range(len(self.name_aliases.values())):
                for alias in self.name_aliases.values()[i]:
                    if key == alias:
                        return True
    
    def __getitem(self, key):
        if key in self.cik_name:
            return json.loads(open(os.path.join("data/profilemanager/profiles", "{}.json".format(key)), "r").read())
        elif key in self.name_cik:
            return json.loads(open(os.path.join("data/profilemanager/profiles", "{}.json".format(self.name_cik[key])), "r").read())
            #open name_cik[key]
        else:
            for i in range(len(self.name_aliases.values())):
                for alias in self.name_aliases.values()[i]:
                    if key == alias:
                        return json.loads(open(os.path.join("data/profilemanager/profiles", "{}.json".format(self.name_cik[name_aliases.keys()[i]])), "r").read())
                        # open name_cik[name_aliases.keys()[i]]
        
    def __iter__(self):
        for cik in self.cik_name.keys():
            yield self.get(cik)
        
    def __len__(self):
        return len(self.cik_name)
        
    def __repr__(self):
        return json.dumps(self.cik_name, sort_keys = True, indent = 4)
        
    def __str__(self):
        return json.dumps(self.cik_name, sort_keys = True, indent = 4)
    
    #def alias_to_cik(self, alias):
    
    def cik_to_alias(self, cik):
        return self.name_alias[self.cik_name[cik]]
        
    def cik_to_naics(self, cik):
        return self.get(cik).naics
        
    def cik_to_name(self, cik):
        return self.cik_name(cik)
    
    def cik_to_sic(self, cik):
        return self.cik_sic[cik]
        
    def cik_to_description(self, cik):
        return self.naics_description[self.get(cik).naics] + self.sic_description[self.get(cik).sic]
        
    def cik_to_name(self, cik):
        return self.cik_name[cik]
        
    def generate_profiles(self):
        cik_to_sic = json.loads(open(os.path.join("data/profilemanager/data", "cik_to_sic.json"), "r").read())
        sic_to_naics = json.loads(open(os.path.join("data/profilemanager/data", "sic_to_naics.json"), "r").read())
        thicc_edgar = json.loads(open(os.path.join("data/profilemanager/data", "edgardata.json"), "r").read())
        for cik in self.cik_name:
            this = {}
            this['cik'] = cik
            this['name'] = self.cik_to_name(cik)
            this['sic'] = cik_to_sic[cik]
            try:
                this['naics'] = sic_to_naics[this['sic'].pop()]
            except:
                this['naics'] = None
            this['subsidiaries'] = None
            try:
                this['ten_ks'] = thicc_edgar[cik]["10K"]
                remove_queue = []
                for elem in this['ten_ks']:
                    if elem['url'] == "":
                        remove_queue.append(elem)
                for elem in remove_queue:
                    this['ten_ks'].remove(elem)
            except Exception as e:
                print(str(e))
                this['ten_ks'] = None
            try:
                if len(this['ten_ks']) == 0:
                    this['ten_ks'] = None
                else:
                    for elem in this['ten_ks']:
                        elem['txt'] = parse_single_page(elem['url'])
                        print("Parsed {}".format(elem['url']))
            except:
                pass
            try:
                this['eight_ks'] = thicc_edgar[cik]["8K"]
                remove_queue = []
                for elem in this['eight_ks']:
                    if elem['url'] == "":
                        remove_queue.append(elem)
                for elem in remove_queue:
                    this['eight_ks'].remove(elem)
            except Exception as e:
                print(str(e))
                this['eight_ks'] = None
            try:
                if len(this['eight_ks']) == 0:
                    this['eight_ks'] = None
                else:
                    for elem in this['eight_ks']:
                        elem['txt'] = eightk_parser(elem['url'])
                        print("Parsed {}".format(elem['url']))
            except:
                pass
            try:
                this['EX21s'] = thicc_edgar[cik]["EX21"]
                remove_queue = []
                for elem in this['EX21s']:
                    if elem['url'] == "":
                        remove_queue.append(elem)
                for elem in remove_queue:
                    this['EX21s'].remove(elem)
            except Exception as e:
                print(str(e))
                this['EX21s'] = None
            try:
                if len(this['EX21s']) == 0:
                    this['EX21s'] = None
                else:
                    for elem in this['EX21s']:
                        elem['txt'] = eightk_parser(elem['url'])
                        print("Parsed {}".format(elem['url']))
            except:
                pass
            this['website'] = None
            open(os.path.join("data/profilemanager/profiles", "{}.json".format(cik)), "w").write(json.dumps(this, sort_keys = True, indent = 4)) 
        
    def get(self, key):
        if key in self.cik_name:
            return json.loads(open(os.path.join("data/profilemanager/profiles", "{}.json".format(key)), "r").read())
        elif key in self.name_cik:
            return json.loads(open(os.path.join("data/profilemanager/profiles", "{}.json".format(self.name_cik[key])), "r").read())
            #open name_cik[key]
        else:
            for i in range(len(self.name_aliases.values())):
                for alias in self.name_aliases.values()[i]:
                    if key == alias:
                        return json.loads(open(os.path.join("data/profilemanager/profiles", "{}.json".format(self.name_cik[name_aliases.keys()[i]])), "r").read())
                        # open name_cik[name_aliases.keys()[i]]
    
    def naics_to_description(self, naics):
        return self.naics_description[naics]
    
    def naics_to_sic(self, naics):
        return self.naics_sic[naics]
    
    def name_to_aliases(self, name):
        return self.name_alias[name]
    
    def name_to_cik(self, name):
        return self.name_cik[name]
    
    def name_to_description(self, name):
        return self.naics_description[self.get(name).naics] + self.sic_description[self.get(name).sic]
        
def main():
    pm = ProfileManager()
    pm.generate_profiles()
    
if __name__ == "__main__" :
    main()