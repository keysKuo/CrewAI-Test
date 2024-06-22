from langchain_community.utilities import SQLDatabase

mysql_uri = "mysql+mysqlconnector://root:9952811@localhost:3306/ManageTest"
db = SQLDatabase.from_uri(mysql_uri, sample_rows_in_table_info = 3)

# print(db.dialect)
# print(db.table_info)
# print(db.get_usable_table_names())
# output = db.run("SELECT * FROM User LIMIT 10;")

# print(output)