
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, Character, Group, db
from auth import requires_auth, AuthError


class tableTopStuffTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):

        pass

    def test_characters(self):
        res = self.client().get('/characters')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['characters'])
    
    def test_character_id(self):
        res = self.client().get('/characters/23')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['character'])

    def test_OOR_character_id(self):
        ##Character ID Out Of Range 
        res = self.client().get('/characters/9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_character_post_Admin(self):
        #Admin Role
        info = {"gender": "male","job": "Warlock","name": "Timmy","player_name": "Francis","race": "Doggo"}
        res = self.client().post('/characters', data=json.dumps(info), headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFBQmtVOWhCQndTNmc0ZEhvRjd0USJ9.eyJpc3MiOiJodHRwczovL3N0ZWVwLXRyZWUtMTg2My5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTI1NzUyMzg5Mzc1ODg3ODUzMzEiLCJhdWQiOiJGU05ELUNhcHN0b25lIiwiaWF0IjoxNTg4NzAzNDY0LCJleHAiOjE1ODg3ODk4NjQsImF6cCI6IkZDNC01eHM2RWliSGRJZmptakdZRmgxaWhDS2kzaXpCIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2hhcmFjdGVyIiwiZGVsZXRlOmdyb3VwIiwicGF0Y2g6Y2hhcmFjdGVyIiwicGF0Y2g6Z3JvdXAiLCJwb3N0OmNoYXJhY3RlciIsInBvc3Q6Z3JvdXAiXX0.I47_s5z3FDWNmpiBgIFUyt5go7fIbDiMVTnj8Lb9Gc_Jgzr1YR8AdMeQUwy0juYB59zpWPbUAiX4bfuc-PSVVT4VF10NJWSnBm8n1dHlMMhXtwUBs1Gg1HIn5ZiJZjF4bEzAvdvvImmNZIx_phaCkYTRwKKOh3bF-g00EEvtPTojRvEZxiui1bYdh8UUDcTGWFzejNFZfIHpPO7Hh9y_BV6cMCrBg3bskrbHgcIjl4V8STnpdsKPupI2yHtnaB18F2icPleMsO4Maf-Rga2TTS4vU4q2JyBUTAkV_rpjHb5bTCjQ1uh2nJiDbi3yWg417hUrhEC56NCU-ZNjEXVCug'})
        data = json.loads(res.data)

        character = data['character']
        character_ID = character['id']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_character_post_NA(self):
        ##No Authorization
        info = {"gender": "male","job": "Warlock","name": "Timmy","player_name": "Francis","race": "Doggo"}
        res = self.client().post('/characters', data=json.dumps(info), headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '})
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 401)
        
    def test_character_patch_Player(self):
        #Player Role
        info = {"currency": "0", "gender": "male", "group": None, "id": 23, "job": "Wizard", "lvl": 1, "name": "Taako (from TV)", "player_name": "Justin", "race": "Elf"}
        res = self.client().patch('/characters/23', data=json.dumps(info), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFBQmtVOWhCQndTNmc0ZEhvRjd0USJ9.eyJpc3MiOiJodHRwczovL3N0ZWVwLXRyZWUtMTg2My5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhMDUxOTM3OWI2NGUwY2Y0MDU1MzU0IiwiYXVkIjoiRlNORC1DYXBzdG9uZSIsImlhdCI6MTU4ODcyMTUwNSwiZXhwIjoxNTg4ODA3OTA1LCJhenAiOiJGQzQtNXhzNkVpYkhkSWZqbWpHWUZoMWloQ0tpM2l6QiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmNoYXJhY3RlciIsInBhdGNoOmNoYXJhY3RlciIsInBvc3Q6Y2hhcmFjdGVyIl19.sTaNAzf5TdU5nZPri71_zk2gioGD23pqV8uzyxOzKechG39WJvNjNcKhTc-xZRnI_nNvhNNqWC0cYPveB-o23eP_ZhqzdpFGW8aD1UR3die1Ftu5jCm8X7MJ75gecRCW2Ioi0gWqri-MsVEFPz8SzdGs_kAF3Gp_G4kW-DTnrXVqcB1Py_klRaMxqQXdKWDMdtUzPxcIurXibZHD-N7nVMeBgt4brH6MGc1AKkMnhjnSzGA8OJonEqNBLIwF_60dbT0xxCAEwS1e1VE38heAJJbHAWZXUX7hxAbVaRMNkQmRJ4zB4VJ97og_JIFP8dREZ8-Eg5ARWuDRtpVfbat9aw'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['character_id'])

    def test_character_patch_DM(self):
        #DM Role
        info = {"currency": "0", "gender": "male", "group": None, "id": 23, "job": "Wizard", "lvl": 1, "name": "Taako (from TV)", "player_name": "Justin", "race": "Elf"}
        res = self.client().patch('/characters/23', data=json.dumps(info), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFBQmtVOWhCQndTNmc0ZEhvRjd0USJ9.eyJpc3MiOiJodHRwczovL3N0ZWVwLXRyZWUtMTg2My5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhMDg3YjJkOTAyMTYwYzkyOTcxOTQxIiwiYXVkIjoiRlNORC1DYXBzdG9uZSIsImlhdCI6MTU4ODcyMjczOSwiZXhwIjoxNTg4ODA5MTM5LCJhenAiOiJGQzQtNXhzNkVpYkhkSWZqbWpHWUZoMWloQ0tpM2l6QiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmdyb3VwIiwicGF0Y2g6Z3JvdXAiLCJwb3N0Omdyb3VwIl19.dUZKxzmk4sL1C-QZAWJphDW20rl2DuOgRaH5kJ0WNp7_1tWsdY5d8O1iV-Wkx5Hzd2lWjh8K8PWzinNzkeb_-T096A2nvCB_fvbN7RUypQ1F1wfSvkHPjm53dZcmQz51NQTkQLuhbmhAfa_Jsm7A5vCU6b3wkaSOEbv4ixREsTkHr7kfHCYi8bXM66VjWlrOO0h5bCXpa8O5-fFBCFsiQsqg8mh6NaLdDqIT8IufIfywSttuBKtzKjeuWedOwgZ7bdlJ7OvA8bcUmnO6WI8fLbyuH_F4il6QCCI1H3JD4bB4lWG4d0_TONd8F91M7IF6EZeVqooguKqOjwGSb13fzQ'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_character_delete(self):
        obj = Character.query.order_by(Character.id.desc()).first()
        id = obj.id
        res = self.client().delete('/characters/' + str(id), data=json.dumps(None), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFBQmtVOWhCQndTNmc0ZEhvRjd0USJ9.eyJpc3MiOiJodHRwczovL3N0ZWVwLXRyZWUtMTg2My5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhMDUxOTM3OWI2NGUwY2Y0MDU1MzU0IiwiYXVkIjoiRlNORC1DYXBzdG9uZSIsImlhdCI6MTU4ODcyMTUwNSwiZXhwIjoxNTg4ODA3OTA1LCJhenAiOiJGQzQtNXhzNkVpYkhkSWZqbWpHWUZoMWloQ0tpM2l6QiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmNoYXJhY3RlciIsInBhdGNoOmNoYXJhY3RlciIsInBvc3Q6Y2hhcmFjdGVyIl19.sTaNAzf5TdU5nZPri71_zk2gioGD23pqV8uzyxOzKechG39WJvNjNcKhTc-xZRnI_nNvhNNqWC0cYPveB-o23eP_ZhqzdpFGW8aD1UR3die1Ftu5jCm8X7MJ75gecRCW2Ioi0gWqri-MsVEFPz8SzdGs_kAF3Gp_G4kW-DTnrXVqcB1Py_klRaMxqQXdKWDMdtUzPxcIurXibZHD-N7nVMeBgt4brH6MGc1AKkMnhjnSzGA8OJonEqNBLIwF_60dbT0xxCAEwS1e1VE38heAJJbHAWZXUX7hxAbVaRMNkQmRJ4zB4VJ97og_JIFP8dREZ8-Eg5ARWuDRtpVfbat9aw'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['character_id'])
    
    def test_character_OOR_delete(self):
        res = self.client().delete('/characters/9999', data=json.dumps(None), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFBQmtVOWhCQndTNmc0ZEhvRjd0USJ9.eyJpc3MiOiJodHRwczovL3N0ZWVwLXRyZWUtMTg2My5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhMDUxOTM3OWI2NGUwY2Y0MDU1MzU0IiwiYXVkIjoiRlNORC1DYXBzdG9uZSIsImlhdCI6MTU4ODcyMTUwNSwiZXhwIjoxNTg4ODA3OTA1LCJhenAiOiJGQzQtNXhzNkVpYkhkSWZqbWpHWUZoMWloQ0tpM2l6QiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmNoYXJhY3RlciIsInBhdGNoOmNoYXJhY3RlciIsInBvc3Q6Y2hhcmFjdGVyIl19.sTaNAzf5TdU5nZPri71_zk2gioGD23pqV8uzyxOzKechG39WJvNjNcKhTc-xZRnI_nNvhNNqWC0cYPveB-o23eP_ZhqzdpFGW8aD1UR3die1Ftu5jCm8X7MJ75gecRCW2Ioi0gWqri-MsVEFPz8SzdGs_kAF3Gp_G4kW-DTnrXVqcB1Py_klRaMxqQXdKWDMdtUzPxcIurXibZHD-N7nVMeBgt4brH6MGc1AKkMnhjnSzGA8OJonEqNBLIwF_60dbT0xxCAEwS1e1VE38heAJJbHAWZXUX7hxAbVaRMNkQmRJ4zB4VJ97og_JIFP8dREZ8-Eg5ARWuDRtpVfbat9aw'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    ### GROUP TESTS ####
    def test_groups(self):
        res = self.client().get('/groups')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['groups'])

    def test_group_id(self):
        res = self.client().get('/groups/20')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['group'])

    def test_OOR_group_id(self):
        res = self.client().get('/groups/9999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
    
    def test_groups_post_Admin(self):
        #Admin Role
        info = {"name": "Three who pee when happy","player_name": "TheOneWhoFeedsTheDoggos"}
        res = self.client().post('/groups', data=json.dumps(info), headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFBQmtVOWhCQndTNmc0ZEhvRjd0USJ9.eyJpc3MiOiJodHRwczovL3N0ZWVwLXRyZWUtMTg2My5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTI1NzUyMzg5Mzc1ODg3ODUzMzEiLCJhdWQiOiJGU05ELUNhcHN0b25lIiwiaWF0IjoxNTg4NzAzNDY0LCJleHAiOjE1ODg3ODk4NjQsImF6cCI6IkZDNC01eHM2RWliSGRJZmptakdZRmgxaWhDS2kzaXpCIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2hhcmFjdGVyIiwiZGVsZXRlOmdyb3VwIiwicGF0Y2g6Y2hhcmFjdGVyIiwicGF0Y2g6Z3JvdXAiLCJwb3N0OmNoYXJhY3RlciIsInBvc3Q6Z3JvdXAiXX0.I47_s5z3FDWNmpiBgIFUyt5go7fIbDiMVTnj8Lb9Gc_Jgzr1YR8AdMeQUwy0juYB59zpWPbUAiX4bfuc-PSVVT4VF10NJWSnBm8n1dHlMMhXtwUBs1Gg1HIn5ZiJZjF4bEzAvdvvImmNZIx_phaCkYTRwKKOh3bF-g00EEvtPTojRvEZxiui1bYdh8UUDcTGWFzejNFZfIHpPO7Hh9y_BV6cMCrBg3bskrbHgcIjl4V8STnpdsKPupI2yHtnaB18F2icPleMsO4Maf-Rga2TTS4vU4q2JyBUTAkV_rpjHb5bTCjQ1uh2nJiDbi3yWg417hUrhEC56NCU-ZNjEXVCug'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_groups_post_NA(self):
        ##No Authorization
        info = {"name": "Three who pee when happy","player_name": "TheOneWhoFeedsTheDoggos"}
        res = self.client().post('/groups', data=json.dumps(info), headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_group_patch_DM(self):
        #DM Role
        info = {"characters": [{"id": 23},{"id": 24},{"id": 25}],"group": {"id": 20,"master": {"player_name": "Griffin"},"name": "Tres Horny Boys"}}
        res = self.client().patch('/groups/20', data=json.dumps(info), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFBQmtVOWhCQndTNmc0ZEhvRjd0USJ9.eyJpc3MiOiJodHRwczovL3N0ZWVwLXRyZWUtMTg2My5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhMDg3YjJkOTAyMTYwYzkyOTcxOTQxIiwiYXVkIjoiRlNORC1DYXBzdG9uZSIsImlhdCI6MTU4ODcyMjczOSwiZXhwIjoxNTg4ODA5MTM5LCJhenAiOiJGQzQtNXhzNkVpYkhkSWZqbWpHWUZoMWloQ0tpM2l6QiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmdyb3VwIiwicGF0Y2g6Z3JvdXAiLCJwb3N0Omdyb3VwIl19.dUZKxzmk4sL1C-QZAWJphDW20rl2DuOgRaH5kJ0WNp7_1tWsdY5d8O1iV-Wkx5Hzd2lWjh8K8PWzinNzkeb_-T096A2nvCB_fvbN7RUypQ1F1wfSvkHPjm53dZcmQz51NQTkQLuhbmhAfa_Jsm7A5vCU6b3wkaSOEbv4ixREsTkHr7kfHCYi8bXM66VjWlrOO0h5bCXpa8O5-fFBCFsiQsqg8mh6NaLdDqIT8IufIfywSttuBKtzKjeuWedOwgZ7bdlJ7OvA8bcUmnO6WI8fLbyuH_F4il6QCCI1H3JD4bB4lWG4d0_TONd8F91M7IF6EZeVqooguKqOjwGSb13fzQ'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['group_id'])

    def test_group_patch_Player(self):
        #Player Role
        info = {"characters": [{"id": 23},{"id": 24},{"id": 25}],"group": {"id": 20,"master": {"player_name": "Griffin"},"name": "Tres Horny Boys"}}
        res = self.client().patch('/groups/20', data=json.dumps(info), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFBQmtVOWhCQndTNmc0ZEhvRjd0USJ9.eyJpc3MiOiJodHRwczovL3N0ZWVwLXRyZWUtMTg2My5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhMDUxOTM3OWI2NGUwY2Y0MDU1MzU0IiwiYXVkIjoiRlNORC1DYXBzdG9uZSIsImlhdCI6MTU4ODcyMTUwNSwiZXhwIjoxNTg4ODA3OTA1LCJhenAiOiJGQzQtNXhzNkVpYkhkSWZqbWpHWUZoMWloQ0tpM2l6QiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmNoYXJhY3RlciIsInBhdGNoOmNoYXJhY3RlciIsInBvc3Q6Y2hhcmFjdGVyIl19.sTaNAzf5TdU5nZPri71_zk2gioGD23pqV8uzyxOzKechG39WJvNjNcKhTc-xZRnI_nNvhNNqWC0cYPveB-o23eP_ZhqzdpFGW8aD1UR3die1Ftu5jCm8X7MJ75gecRCW2Ioi0gWqri-MsVEFPz8SzdGs_kAF3Gp_G4kW-DTnrXVqcB1Py_klRaMxqQXdKWDMdtUzPxcIurXibZHD-N7nVMeBgt4brH6MGc1AKkMnhjnSzGA8OJonEqNBLIwF_60dbT0xxCAEwS1e1VE38heAJJbHAWZXUX7hxAbVaRMNkQmRJ4zB4VJ97og_JIFP8dREZ8-Eg5ARWuDRtpVfbat9aw'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_group_delete(self):
        obj = Group.query.order_by(Group.id.desc()).first()
        id = obj.id
        res = self.client().delete('/groups/' + str(id), data=json.dumps(None), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFBQmtVOWhCQndTNmc0ZEhvRjd0USJ9.eyJpc3MiOiJodHRwczovL3N0ZWVwLXRyZWUtMTg2My5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhMDg3YjJkOTAyMTYwYzkyOTcxOTQxIiwiYXVkIjoiRlNORC1DYXBzdG9uZSIsImlhdCI6MTU4ODcyMjczOSwiZXhwIjoxNTg4ODA5MTM5LCJhenAiOiJGQzQtNXhzNkVpYkhkSWZqbWpHWUZoMWloQ0tpM2l6QiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmdyb3VwIiwicGF0Y2g6Z3JvdXAiLCJwb3N0Omdyb3VwIl19.dUZKxzmk4sL1C-QZAWJphDW20rl2DuOgRaH5kJ0WNp7_1tWsdY5d8O1iV-Wkx5Hzd2lWjh8K8PWzinNzkeb_-T096A2nvCB_fvbN7RUypQ1F1wfSvkHPjm53dZcmQz51NQTkQLuhbmhAfa_Jsm7A5vCU6b3wkaSOEbv4ixREsTkHr7kfHCYi8bXM66VjWlrOO0h5bCXpa8O5-fFBCFsiQsqg8mh6NaLdDqIT8IufIfywSttuBKtzKjeuWedOwgZ7bdlJ7OvA8bcUmnO6WI8fLbyuH_F4il6QCCI1H3JD4bB4lWG4d0_TONd8F91M7IF6EZeVqooguKqOjwGSb13fzQ'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['group_id'])

    def test_group_OOR_delete(self):
        obj = Group.query.order_by(Group.id.desc()).first()
        id = obj.id
        res = self.client().delete('/groups/9999', data=json.dumps(None), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFBQmtVOWhCQndTNmc0ZEhvRjd0USJ9.eyJpc3MiOiJodHRwczovL3N0ZWVwLXRyZWUtMTg2My5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhMDg3YjJkOTAyMTYwYzkyOTcxOTQxIiwiYXVkIjoiRlNORC1DYXBzdG9uZSIsImlhdCI6MTU4ODcyMjczOSwiZXhwIjoxNTg4ODA5MTM5LCJhenAiOiJGQzQtNXhzNkVpYkhkSWZqbWpHWUZoMWloQ0tpM2l6QiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmdyb3VwIiwicGF0Y2g6Z3JvdXAiLCJwb3N0Omdyb3VwIl19.dUZKxzmk4sL1C-QZAWJphDW20rl2DuOgRaH5kJ0WNp7_1tWsdY5d8O1iV-Wkx5Hzd2lWjh8K8PWzinNzkeb_-T096A2nvCB_fvbN7RUypQ1F1wfSvkHPjm53dZcmQz51NQTkQLuhbmhAfa_Jsm7A5vCU6b3wkaSOEbv4ixREsTkHr7kfHCYi8bXM66VjWlrOO0h5bCXpa8O5-fFBCFsiQsqg8mh6NaLdDqIT8IufIfywSttuBKtzKjeuWedOwgZ7bdlJ7OvA8bcUmnO6WI8fLbyuH_F4il6QCCI1H3JD4bB4lWG4d0_TONd8F91M7IF6EZeVqooguKqOjwGSb13fzQ'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

if __name__ == "__main__":
    unittest.main()