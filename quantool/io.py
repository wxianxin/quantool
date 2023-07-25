""" io utils
"""

import os
import pandas as pd
import sqlalchemy


class RDB:
    """RDB tools"""

    def __init__(self):
        pass

    def connect(
        self,
        user: str,
        password: str,
        host: str,
        port: str,
        database: str,
    ) -> None:
        """"""
        self.engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        )
        self._conn = self.engine.connect()
        return self._conn

    def disconnect(self) -> None:
        """"""
        self._conn.commit()
        self._conn.close()
        self.engine.dispose()

    def df_io(
        self,
        sql_query: str = None,
        read_sql: str = None,
        to_sql_df=None,
        table_name=None,
        if_exists="fail",
    ):
        """"""
        if sql_query is not None:
            result = self._conn.execute(sqlalchemy.text(sql_query))
            try:
                print(result.fetchone())
            except:
                print(result)
            return result

        if read_sql is not None:
            df = pd.read_sql(sqlalchemy.text(read_sql), self._conn)
            return df

        if to_sql_df is not None:
            to_sql_df.to_sql(table_name, self._conn, if_exists=if_exists)

    def db_sqlalchemy(
        self,
        user: str,
        password: str,
        host: str,
        port: str,
        database: str,
        sql_query: str = None,
        read_sql: str = None,
        to_sql_df=None,
        table_name=None,
        if_exists="fail",
    ):
        """"""

        self.connect(user, password, host, port, database)
        df = self.df_io(
            sql_query=sql_query,
            read_sql=read_sql,
            to_sql_df=to_sql_df,
            table_name=table_name,
            if_exists=if_exists,
        )
        self.disconnect()

        return df


if __name__ == "__main__":
    db = RDB()
    df = db.db_sqlalchemy(
        user="user",
        password="pwd",
        host="192.168.0.1",
        port="3306",
        database="db",
        read_sql="SELECT * FROM table;",
    )
