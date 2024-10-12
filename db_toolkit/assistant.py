from huggingface_hub import InferenceClient
import os
import db_toolkit.db as db

class LLMAssistant() :
	def __init__(self, key, name, description) :
		self.__db_name = name
		if os.path.isfile(f'{name}.txt') :
			print("Shema is already exists")
		else :
			client = InferenceClient(api_key=key)
			model3 = "google/gemma-1.1-7b-it"

			with open(f'{os.path.dirname(__file__)}/promt.txt', 'r') as file :
				text = file.read()
				text = text.replace('[Topic]', name)
				text = text.replace('[Overview]', description)
			messages = [
				{ "role": "user", "content": text }
			]
			output = client.chat.completions.create(
				model=model3,
				messages=messages, 
				stream=True, 
				temperature=0.7,
				max_tokens=2000,
				top_p=0.7
			)
			with open('description.txt', 'w') as f :
				for chunk in output:
					f.write(chunk.choices[0].delta.content)
			with open('description.txt', 'r') as f :
					query = f.read()
			os.remove('description.txt')

			with open(f'{os.path.dirname(__file__)}/llm_task.txt', 'r') as file :
				text = file.read()
				text = text.replace('user_query', query)
			messages = [
				{ "role": "user", "content": text }
			]

			output = client.chat.completions.create(
				model=model3,
				messages=messages, 
				stream=True, 
				temperature=0.5,
				max_tokens=2000,
				top_p=0.7
			)
			with open(f'{name}.txt', 'w') as f :
				for chunk in output:
					f.write(chunk.choices[0].delta.content)

			with open(f'{name}.txt', 'r') as f :
				text = f.read()
				text = text.replace('## Social Network Database Schema', '')
				text = text.replace('```sql', '')
				text = text.replace('```', '')
				text = text.replace("auto_increment", 'auto_inkrement')
				text = text.replace('(datetime)', '(timestamp)')
			with open(f'{name}.txt', 'w') as f :
				f.write(text)
	def set_db(self, password, dev_mode=False, user="postgres", host="localhost") :
		shema_file = f'{self.__db_name}.txt'
		result_name = self.__db_name.lower().replace(' ', '_')
		db.DB_Creator(result_name, password, shema_file, dev_mode, user, host)