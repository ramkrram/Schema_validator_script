from datetime import datetime

import pdb
#pdb.set_trace()

def build_path(path, key):
    #pdb.set_trace()
    return key if len(path) == 0 else path + '.' + key


def validate_array(schema, src_file_schema, path):
    #pdb.set_trace()
    result = []
    for i in range(len(src_file_schema)):
        result += validate(schema, src_file_schema[i], path + '[{}]'.format(i))
    return result


def validate_type(value, type_str):
    #pdb.set_trace()
    print('Schema : "{}" Schema type: "{}"'.format(value, type_str))
    
    if type_str == "string":
        return type(value) is str
    elif type_str == 'bool':
        return type(value) is bool
    elif type_str == "int":
        return type(value) is int
    elif type_str == 'ObjectId':
        return type(value) is int
    elif type_str == 'float':
        return type(value) is float
    elif type_str == 'date':
        return type(value) is datetime
    elif type_str == 'null':
        return value is None
    elif type_str == 'number':
        return type(value) in [int, float]
    elif type_str == 'object':
        return type(value) is dict
    elif type_str == 'any':
        return True
    else:
        raise Exception('Schema Type is not valid')
        print(value)

def get_default_value(m_key):
    #pdb.set_trace()
    if type(m_key) is list and type(m_key[0]) is dict:
        return []

    if type(m_key) is dict:
        res = {}
        for key in m_key.keys():
            res[key] = get_default_value(m_key[key])
        return res

    return m_key[1]


def validate(schema, src_file_schema, path=''):
    #pdb.set_trace()
    result = []

    if type(src_file_schema) is not dict:
        raise Exception('Document passed to "validate" function must be a dictionary')

    for field in src_file_schema:
        if field not in schema.keys():
            fullpath = build_path(path, field)
            field_type = type(src_file_schema[field]).__name__
            result.append({
                'msg': '[+] Extra field: "{}" having type: "{}"'.format(fullpath, field_type),
                'type': 'extra_field',
                'path': fullpath,
                'field_type': field_type
            })
            # log()

    for key in schema:
        if key not in src_file_schema:
            # log()
            fullpath = build_path(path, key)
            result.append({
                'msg': '[-] Missing field: "{}"'.format(fullpath),
                'type': 'missing_field',
                'path': fullpath,
                'default_value': get_default_value(schema[key])
            })
            continue

        if type(schema[key]) is list and type(schema[key][0]) is dict:
            result += validate_array(schema[key], src_file_schema[key], build_path(path, key))
            continue

        if type(schema[key]) is dict:
            result += validate(schema[key], src_file_schema[key], build_path(path, key))
            continue

        if type(schema[key]) is list and type(schema[key]) is str:
            res = any(validate_type(src_file_schema[key], cur_type) for cur_type in schema[key])
            if not res:
                log()
                fullpath = build_path(path, key)
                expected = schema[key]
                found = type(src_file_schema[key]).__name__
                result.append({
                    'msg': '[*] "{}" has wrong type. Expected one of: "{}", found: "{}"'.format(fullpath, expected,found),
                    'type': 'wrong_type',
                    'path': fullpath,
                    'expected': expected,
                    'found': found,
                })
            continue

        res = None
        try:
            res = validate_type(src_file_schema[key], schema[key])
        except Exception as e:
            raise Exception('Schema is not valid: "{}" has incorrect type: "{}"'.format(key, schema[key]))
        if not res:
            # log()
            fullpath = build_path(path, key)
            expected = schema[key]
            found = type(src_file_schema[key]).__name__
            result.append({
                'msg': '[*] "{}" has wrong type. Expected: "{}", found: "{}"'.format(fullpath, expected, found),
                'type': 'wrong_type',
                'path': fullpath,
                'expected': expected,
                'found': found,
            })
    return result
