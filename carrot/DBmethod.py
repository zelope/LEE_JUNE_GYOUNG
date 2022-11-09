import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from pprint import pprint

class Database():
    def __init__(self, host ='dataproject.czsp7v9awfy0.ap-northeast-2.rds.amazonaws.com'
                 , dname= 'carrotdb', user = 'jkmanager', password = 'jkdavin12', port = 5432):
        """

        :param host: str host 명
        :param dname: str 사용할 Database 명 아마 carrrot으로 고정일듯
        :param user: str 사용할 user 명
        :param password: str 사용하는 user password
        :param port: int 사용할 포트번호
        """
        self.host = host
        self.dname = dname
        self.user = user
        self.password = password
        self.port = port
        self.db = psycopg2.connect(
            host= self.host, dbname= self.dname,
            user=self.user, password=self.password,
            port=self.port)


        self.cursor = self.db.cursor()



    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.cursor.commit()


class CRUD(Database):
    def __init__(self):
        super(CRUD, self).__init__()

    def create_table(self, table,columinfo):
        """
        해당 table이 없는 경우에만 실행,public Schemas에 저장
        :param table: str
        :param columinfo:str
        colum1이름 columTYPE 부가정보(pk 등), ...... 양식으로 작성
        :return: void

        """
        sql = f'CREATE TABLE IF NOT EXISTS {table} ({columinfo});'
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(" insert DB err ", e)

    def readDB(self, table, colum):
        """
        해당 테이블 가져오기

        :param table: 필요 table 뿐 아니라 from 뒤에 올수 있는 모든 요소,
        즉 groupby, where, orderby, rollup, 서브쿼리등도 인식가능
        :param colum: 필요한 coulum (*포함) 뿐 아니라 집계함수도 인식가능능
       :return: list형태이며 각 행은 tuple형태로 묶임
        """
        sql = f" SELECT {colum} from {table}"


        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            result = (" read DB err", e)

        return result

    def showtable(self, table, colum):
        """
        해당테이블을 보여주기만 함. return void
        :param table: str
        :param colum: str
        :return: void
        """
        whatshow = self.readDB(table, colum)
        pprint(whatshow)

    def insertDB(self, table, data=None, colum = None):
        """
        총 3개지 경우가 있다.
        colum = None이면 우리가 일반적으로 생각하는 insert
        data = None 인 경우 다른 테이블에서 가져와야 함으로
        table 에 tablename select columName from tableName2의 형태로 작성
        둘 다 None이 아닌경우 특정 colum에만 값 입력
        :param table: str
        :param data: str 단 char[]인 경우 이중 str
        :param colum: str
        :return: void
        """
        if (colum==None):
            sql = f" INSERT INTO {table} VALUES ({data}) ;"
        elif(data == None):
            sql = f" INSERT INTO {table};"
        else:
            sql = f" INSERT INTO {table}({colum}) VALUES ('{data}') ;"


        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(" insert DB err ", e)

    def updateDB(self, table, colum, value, condition = None):
        """

        :param table: str update할 table
        :param colum: str update할 colum
        :param value: str update할 값
        :param condition: str update할 것들을 찾는 condition 보통 pk
        :return: void
        """
        if condition == None:
            sql = f" UPDATE {table} SET {colum}='{value}' ; "
        else:
            sql = f" UPDATE {table} SET {colum}='{value}' WHERE {condition} ; "


        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(" update DB err", e)

    def deleteDB(self, table, condition):
        """

        :param table: str 삭제할 table
        :param condition: str 삭제할 것을 찾을 conditon, 주로 pk
        :return: void
        """
        sql = f" delete from {table} where {condition} ; "
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("delete DB err", e)

    def addFKcolum(self, table, colum, refer):
        """

        :param table: str colum 추가할 table
        :param colum: str columName columTYPE
        :param refer: str tableName(columName)
        :return: void
        """

        sql =  f" alter table {table} ADD column {colum} REFERENCES {refer}; "
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("delete DB err", e)

    #나중에 다중 join 필요하면 리스트도 받아서 for문으로 돌리자
    def innerjoinDB(self, tableA, tableB, condition, colum):
        """
        INNER JOIN

        :param tableA: str tableA A
        :param tableB:str table B
        :param join: str A.columName = B.columName
        특정열 (where)또한 여기에 추가로 입력
        :param colum: str A.~, B.~
        :return:
        """
        sql = f" select {colum} from {tableA} inner join {tableB} on {condition}; "
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("delete DB err", e)

    def outLjoinDB(self, tableA, tableB, condition, colum):
        """
        left JOIN

        :param tableA: str tableA A
        :param tableB:str table B
        :param join: str A.columName = B.columName
        특정열 (where)또한 여기에 추가로 입력
        :param colum: str A.~, B.~
        :return:
        """
        sql = f" select {colum} from {tableA} left outer join  {tableB} on {condition}; "
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("delete DB err", e)

    def outRjoinDB(self, tableA, tableB, condition, colum):
        """
        right JOIN

        :param tableA: str tableA A
        :param tableB:str table B
        :param join: str A.columName = B.columName
        특정열 (where)또한 여기에 추가로 입력
        :param colum: str A.~, B.~
        :return: void
        """
        sql = f" select {colum} from {tableA} right outer join  {tableB} on {condition}; "
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("delete DB err", e)

    def inputWebcrp(self, data,title):
        """
        웹크롤링으로 받은 csv을 업로드 해줌.
        :param data:str csv data. 단 실행시키는 파이썬파일과 같은 경로에 있어야한다
        :param title: str 만들 table 이름
        :return: void
        """

        df = pd.read_csv(data,index_col = 0)
        if not (data in '.csv'):
            index = data.find('.')
            data = data[0:index]+'.csv'
            df.to_csv(data, mode='w')


        df.columns = [c.lower() for c in df.columns]
        posaddress = "postgresql://" + self.user + ":" + self.password + "@" \
                     + self.host + ":"+str(self.port) + "/"+self.dname
        engine = create_engine(posaddress)


        df.to_sql(name = title, con=engine, index=False, if_exists='replace')
