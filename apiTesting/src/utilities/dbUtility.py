import pymysql
import logging as logger
from apiTesting.src.utilities.credentialsUtility import CredentialsUtility

class DBUtility(object):

    def __init__(self):
        creds_helper = CredentialsUtility()
        self.creds = creds_helper.get_db_credentials()
        self.host = 'localhost'
        self.port = 10005

    def create_connection(self):
        connection = pymysql.connect(host=self.host, user=self.creds['db_user'],
                                     password=self.creds['db_password'], port=self.port)

        return connection

    def execute_select(self, sql):
        conn = self.create_connection()

        try:
            logger.debug(f"Executing sql: {sql}")
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute(sql)
            rs_dict = cur.fetchall()
            cur.close()

        except Exception as e:
            raise Exception(f"Failed running sql: {sql} \n Error: {str(e)}")
        finally:
            cur.close()

        return rs_dict