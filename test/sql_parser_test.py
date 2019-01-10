from sql import sql_parser

def run():
    print(sql_parser.parse('Select From document;'))