from sqlmodel import create_engine

# Con mysql-connector
mysql_url = "mysql+mysqlconnector://root:1234@localhost:3306/mi_base"

# Si usas pymysql, sería:
# mysql_url = "mysql+pymysql://root:1234@localhost:3306/mi_base"

engine = create_engine(mysql_url, echo=True)