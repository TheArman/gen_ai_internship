user_schema = {
    'type': 'object',
    'properties': {
        'full_name': {'type': 'string'},
        'email': {'type': 'string', 'format': 'email'},
        'password': {'type': 'string'},
        'role': {'type': 'string', 'enum': ['new', 'standard', 'banned', 'admin']}
    },
    'required': ['email', 'password']
}
