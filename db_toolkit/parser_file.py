import os
def make_temporal(arr) :
    dict_arr = []
    for item in arr :
        table_name = item.get('name')
        field_name = item.get('primary_key')
        dict_arr.append({'table_name': table_name, 'field': field_name})
    inkrement = 'GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 )'
    temporal_table = {'name': 'time', 
                      'primary_key': 'time_id', 
                      'fields': [{'field_name': 'time_id', 
                                  'field_type': 'integer', 
                                  'field_specials': ['not_null', inkrement], 
                                  'field_pointers': dict_arr}, 
                                 {'field_name': 'current_time', 
                                  'field_type': 'timestamptz', 
                                  'field_specials': ['not_null'], 
                                  'field_pointers': []}]}
    arr.append(temporal_table)
    return arr

def parse_schema(file_path) :
    file = open(file_path, 'r')
    text = file.read()
    file.close()
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    text = text.replace(' ', '')
    text = text.replace('(', '|')
    text = text.replace('[', '|#')
    text = text.replace('<', '|')
    text = text.replace('"', '|*')
    text = text.replace(')', '')
    text = text.replace(']', '')
    text = text.replace('>', '')
    if '$temporal$' in text :
        text = text.replace('$temporal$', '')
        temporal_mode = True
    else :
        temporal_mode = False
    commands = text.split(';')
    commands.pop()
    result = []
    for command in commands :
        command = command.replace('}', '')
        arr = command.split('{')
        lexem = arr[0].split('|')
        name = lexem[0]
        primary_key = lexem[1]
        fields = arr[1].split(',')
        parsed_fields = []
        for field in fields :
            field_arr = field.split('|')
            field_name = field_arr[0]
            field_type = field_arr[1]
            pointer_arr = []
            field_specials = []
            for character in field_arr[2:] :
                if '#' in character :
                    field_pointer = character[1:].split('&')
                    for pointer in field_pointer :
                        pointer_command = pointer.split(':')
                        pointer_arr.append({'table_name':pointer_command[0], 
                                            'field':pointer_command[1]})
                if '*' in character and character != '*':
                    field_specials = character[1:].split('+') 
            parsed_fields.append({'field_name':field_name, 
                                'field_type':field_type,
                                'field_specials':field_specials,
                                'field_pointers':pointer_arr}) 
        result.append({'name':name,
                       'primary_key':primary_key,
                       'fields':parsed_fields})
    if temporal_mode == True :
        result = make_temporal(result) 
    return result, temporal_mode

def table_priority(schema) :
    schema_mask = []
    for table in schema :
        table_arr = []
        name = table.get('name')
        fields = table.get('fields')
        for field in fields :
            pointers = field.get('field_pointers')
            for pointer in pointers :
                table_name = pointer.get('table_name')
                table_arr.append(table_name)
        schema_mask.append({'table_name': name, 'pointer_names': table_arr})
    priority_mask = []
    for table_mask in schema_mask :
        if len(table_mask.get('pointer_names')) == 0:
            priority_mask.append(table_mask)
    i = 0
    while True :
        if i >= len(schema_mask) :
            i = 0
        if len(priority_mask) == len(schema_mask) :
            break
        else :
            pointer_names = schema_mask[i].get('pointer_names')
            approved = True
            pointer_mask = schema_mask[i].get('table_name')
            priority_names =[]
            for mask in priority_mask :
                priority_names.append(mask.get('table_name'))
            if ((not set(pointer_names).issubset(priority_names)
                and pointer_mask in priority_names)
                or len(pointer_names) == 0) :
                approved = False
            if approved == True :
                priority_mask.append(schema_mask[i])
            i+=1
    sorted_tables = []
    for sorted_mask in priority_mask :
        mask_name = sorted_mask.get('table_name')
        for value in schema :
            if mask_name == value.get('name') :
                sorted_tables.append(value)
                break
    return sorted_tables
    
def get_query(parsed_command) :
    file = open(f'{os.path.dirname(__file__)}/schema.txt', 'r')
    template_text = file.read()
    file.close()
    primary_field = parsed_command.get('primary_key')
    primary_key = f'CONSTRAINT {primary_field}_pkey PRIMARY KEY ({primary_field}),\n'
    table_name = parsed_command.get('name')
    fields = parsed_command.get('fields')
    create_field = ''
    foreign = ''
    j=0
    for field in fields :
        field_name = field.get('field_name') 
        field_type = field.get('field_type')
        field_specials = field.get('field_specials')
        pointer_arr = field.get('field_pointers')
        default = 'COLLATE pg_catalog."default"'
        not_null = 'NOT NULL'
        inkrement = 'GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 )'
        more = ' '.join(field_specials)
        more = more.replace('default', default)
        more = more.replace('not_null', not_null)
        more = more.replace('auto_inkrement', inkrement)
        create_field = create_field + f'"{field_name}" {field_type} {more},\n'
        #more == через + дополнительные в ""
        for i in range(len(pointer_arr)) :
            foreign = foreign + f'''CONSTRAINT {pointer_arr[i].get('table_name')}_fkey FOREIGN KEY ("{field_name}")
                    REFERENCES public.{pointer_arr[i].get('table_name')} ({pointer_arr[i].get('field')}) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION'''
            if i + 1 != len(pointer_arr) :
                foreign = foreign +',\n'
        if j + 1 != len(fields) and len(pointer_arr) > 0:
                foreign = foreign +',\n'
        j+=1
    if foreign == '' :
            primary_key = primary_key.replace(',', '')
    else :
        if foreign[len(foreign)-2] == ',' :
            foreign = foreign[:len(foreign)-2] + '\n'
    template_text = template_text.replace('table_name', table_name)
    template_text = template_text.replace('create_field', create_field)
    template_text = template_text.replace('primary_key', primary_key)
    template_text = template_text.replace('foreign', foreign)
    return template_text
#this_field - поле, от которого ссылка
# В <> primary key

def set_limitations(schema) :
    file = open(f'{os.path.dirname(__file__)}/limitations_query.txt', 'r')
    template_text = file.read()
    file.close()
    result = ''
    limits = ''
    for table in schema :
        name = table.get('name')
        if name != 'time' :
            base_query = f'CREATE TRIGGER {name}_audit\nAFTER INSERT ON "{name}"\nFOR EACH ROW EXECUTE PROCEDURE process_table_audit();'
            result = result + base_query + '\n'
        limit_1 = f'CREATE RULE {name}_rl_del AS ON DELETE TO public.{name}\nDO INSTEAD NOTHING;'
        limit_2 = f'CREATE RULE {name}_rl_up AS ON UPDATE TO public.{name}\nDO INSTEAD NOTHING;'
        limits = limits + f'{limit_1}\n{limit_2}\n'
    template_text = template_text.replace('tables_audit', result + limits)
    return template_text