import pymysql
import pymysql.cursors
from templates import ResultType

class Database:
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.user = "root"
        self.passwd = "iotiotiot"
        self.dbname = "authorization"
        self.charset = "utf8"

    def connect(self):
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.dbname,
            charset=self.charset,
            cursorclass=pymysql.cursors.DictCursor
        )
    
    # 에리어 추가
    def insertArea(self, areaName : str):
        conn = self.connect()
        result : dict = {"result" : ResultType.NONE.value, "message" : ""}
        try:
            with conn.cursor() as cursor:
                sql = f"INSERT INTO area (area_name) VALUES ('{areaName}');"
                cursor.execute(sql)
            conn.commit()
            result["result"] = ResultType.SUCCESS.value
        except pymysql.err.Error as e:
            conn.rollback()
            result["result"] = ResultType.FAILURE.value
            result["message"] = e.args[1]
        finally:
            conn.close()
        return result
    
    # 에리어 리스트
    def selectAreas(self):
        conn = self.connect()
        result : dict = {"result" : ResultType.NONE.value, "areas" : []}
        try:
            with conn.cursor() as cursor:
                sql = f"SELECT area_id, area_name FROM area WHERE area_active = True;"
                cursor.execute(sql)
                for row in cursor:
                    result["areas"].append(row)
            result["result"] = ResultType.SUCCESS.value
        except pymysql.err.Error as e:
            result["result"] = ResultType.FAILURE.value
            result["areas"] = []
        finally:
            conn.close()
        return result
    
    def updateArea(self, areaId : int, newAreaName : str):
        conn = self.connect()
        result : dict = {"result" : ResultType.NONE.value, "message" : ""}
        try:
            with conn.cursor() as cursor:
                sql = f"UPDATE area SET area_name = '{newAreaName}' WHERE area_id = {areaId};"
                cursor.execute(sql)
            conn.commit()
            result["result"] = ResultType.SUCCESS.value
        except pymysql.err.Error as e:
            conn.rollback()
            result["result"] = ResultType.FAILURE.value
            result["message"] = e.args[1]
        finally:
            conn.close()
        return result
    
    def deleteArea(self, areaId : int):
        conn = self.connect()
        result : dict = {"result" : ResultType.NONE.value, "message" : ""}
        try:
            with conn.cursor() as cursor:
                sql = f"UPDATE area SET area_active = False WHERE area_id = {areaId};"
                cursor.execute(sql)
            conn.commit()
            result["result"] = ResultType.SUCCESS.value
        except pymysql.err.Error as e:
            conn.rollback()
            result["result"] = ResultType.FAILURE.value
            result["message"] = e.args[1]
        finally:
            conn.close()
        return result
    
    

    
    # def getPropertyList(self, money):
    #     conn = self.connect()
    #     result : list[Property] = []
    #     try:
    #         with conn.cursor() as cursor:
    #             sql = f"SELECT * FROM property WHERE property_entitlement + property_deposit <= {money}"
    #             cursor.execute(sql)
    #             for row in cursor:
    #                 result.append(Property(row))
    #     except:
    #         conn.rollback()
    #     finally:
    #         conn.close()
    #     return result
    
    # def getPlaceList(self, latitude, longitude):
    #     conn = self.connect()
    #     result : list[Place] = []
    #     try:
    #         with conn.cursor() as cursor:
    #             sql = f"SELECT * FROM place WHERE place_latitude BETWEEN {latitude - (0.0091 / 2)} AND {latitude + (0.0091 / 2)} AND place_longitude BETWEEN {longitude - (0.0113 / 2)} and {longitude + (0.0113 / 2)}"
    #             print(sql)
    #             cursor.execute(sql)
    #             for row in cursor:
    #                 result.append(Place(row))
    #     finally:
    #         conn.close()
    #     return result

    # def getPlaceCategoryList(self, latitude, longitude):
    #     conn = self.connect()
    #     result : list[PlaceCategory] = []
    #     try:
    #         with conn.cursor() as cursor:
    #             sql = f"""SELECT place_category, count(*) as count, 
    #             (CASE WHEN place_category = "음식점" THEN (CASE WHEN count(*) >= 50 THEN 50 ELSE floor(count(*) / 10) * 10 END) * -1
    #             ELSE sum(place_weight) END) as weight FROM place 
    #             WHERE place_latitude BETWEEN {latitude - (0.0091 / 2)} AND {latitude + (0.0091 / 2)} AND place_longitude BETWEEN {longitude - (0.0113 / 2)} AND {longitude + (0.0113 / 2)} 
    #             GROUP BY place_category"""
    #             print(sql)
    #             cursor.execute(sql)
    #             for row in cursor:
    #                 result.append(PlaceCategory(row))
    #     finally:
    #         conn.close()
    #     return result

    # def getPopulation(self, neighborhood : str):
    #     conn = self.connect()
    #     result : int = 0
    #     try:
    #         with conn.cursor() as cursor:
    #             sql = f"SELECT population_count FROM population WHERE population_name = '{neighborhood}'"
    #             print(sql)
    #             cursor.execute(sql)
    #             result = cursor.fetchone()['population_count']
    #     finally:
    #         conn.close()
    #     return result

    # def insertPlaceList(self, placeDataList : list[PlaceData]):
    #     conn = self.connect()
    #     result : bool = True
    #     try:
    #         with conn.cursor() as cursor:
    #             for placeData in placeDataList:
    #                 sql = f"INSERT INTO place (place_name, place_address, place_latitude, place_longitude, place_category, place_weight, update_date) VALUES ('{placeData.placeName}', '{placeData.placeAddress}', {placeData.placeLatitude}, {placeData.placeLongitude}, '{placeData.placeCategory}', {placeData.placeWeight}, curdate())"
    #                 cursor.execute(sql)
    #         conn.commit()
    #     except Exception as e:
    #         conn.rollback()
    #         print(e)
    #         result = False
    #     finally:
    #         conn.close()
    #     return result