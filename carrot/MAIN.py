from carrot.DBmethod import *



db_con = CRUD()


db_con.inputWebcrp('testfile/carrot_table.csv', 'carrot')
db_con.inputWebcrp('testfile/product_table.csv', 'product')
db_con.inputWebcrp('testfile/region_table.csv', 'region')




del db_con



