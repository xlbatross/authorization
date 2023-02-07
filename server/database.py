import pymysql
import pymysql.cursors
from enum import Enum

class ResultType(Enum):
    ERROR = -1
    SUCCESS = 1
    FAILURE = 0

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

    def dbResultTemplate(self, name : str = None, isList : bool = True):
        result : dict = {"result" : ResultType.ERROR.value}
        if name is None:
            result["message"] = ""
        elif isList:
            result[name] = []
        else:
            result[name] = {}
        return result

    # 에리어 리스트 검색
    def selectAreas(self):
        conn = self.connect()
        result : dict = self.dbResultTemplate("areas")
        try:
            with conn.cursor() as cursor:
                sql = f"SELECT area_id, area_name FROM area WHERE area_active = True;"
                cursor.execute(sql)
                for row in cursor:
                    result["areas"].append(row)
            result["result"] = ResultType.SUCCESS.value
        except pymysql.err.Error as e:
            result["result"] = ResultType.ERROR.value
            result["areas"] = []
        finally:
            conn.close()
        return result
    
    # 특정 에리어 정보 검색
    def selectArea(self, areaId : int):
        conn = self.connect()
        result : dict = self.dbResultTemplate("area", isList=False)
        try:
            with conn.cursor() as cursor:
                sql = f"SELECT area_name, area_address FROM area WHERE area_id = {areaId} and area_active = True;"
                cursor.execute(sql)
                one = cursor.fetchone()
                result["area"] = one if one is None else {}
            result["result"] = ResultType.SUCCESS.value
        except pymysql.err.Error as e:
            result["result"] = ResultType.ERROR.value
            result["area"] = {}
        finally:
            conn.close()
        return result
    
    # 에리어 추가
    def insertArea(self, areaName : str, areaAddr : str):
        conn = self.connect()
        result : dict = self.dbResultTemplate()
        try:
            with conn.cursor() as cursor:
                sql = f"INSERT INTO area (area_name, area_address) VALUES ('{areaName}', '{areaAddr}');"
                result["result"] = cursor.execute(sql)
                if result["result"] == ResultType.SUCCESS.value:
                    result["message"] = "성공적으로 에리어가 추가되었습니다."
                else:
                    result["message"] = "에리어 추가에 실패했습니다."
            conn.commit()
        except pymysql.err.Error as e:
            conn.rollback()
            result["result"] = ResultType.ERROR.value
            result["message"] = e.args[1]
        finally:
            conn.close()
        return result
    
    # 특정 에리어 정보 갱신
    def updateArea(self, areaId : int, newAreaName : str, newAreaAddr : str):
        conn = self.connect()
        result : dict = self.dbResultTemplate()
        try:
            with conn.cursor() as cursor:
                sql = f"UPDATE area SET area_name = '{newAreaName}', area_address = '{newAreaAddr}' WHERE area_id = {areaId};"
                result["result"] = cursor.execute(sql)
                if result["result"] == ResultType.SUCCESS.value:
                    result["message"] = "성공적으로 수정되었습니다."
                else:
                    result["message"] = "해당 에리어가 존재하지 않습니다."
            conn.commit()
        except pymysql.err.Error as e:
            conn.rollback()
            result["result"] = ResultType.ERROR.value
            result["message"] = e.args[1]
        finally:
            conn.close()
        return result
    
    # 특정 에리어 삭제
    def deleteArea(self, areaId : int):
        conn = self.connect()
        result : dict = self.dbResultTemplate()
        try:
            with conn.cursor() as cursor:
                sql = f"UPDATE area SET area_active = False WHERE area_id = {areaId};"
                result["result"] = cursor.execute(sql)
                if result["result"] == ResultType.SUCCESS.value:
                    result["message"] = "성공적으로 삭제되었습니다."
                else:
                    result["message"] = "이미 삭제된 에리어이거나, 해당 에리어가 존재하지 않습니다."
            conn.commit()
        except pymysql.err.Error as e:
            conn.rollback()
            result["result"] = ResultType.ERROR.value
            result["message"] = e.args[1]
        finally:
            conn.close()
        return result
    
    # 보안 레벨 리스트 검색
    def selectLevels(self):
        conn = self.connect()
        result : dict = self.dbResultTemplate("levels")
        try:
            with conn.cursor() as cursor:
                sql = f"SELECT level_id, level_value FROM level;"
                cursor.execute(sql)
                for row in cursor:
                    result["levels"].append(row)
            result["result"] = ResultType.SUCCESS.value
        except pymysql.err.Error as e:
            result["result"] = ResultType.ERROR.value
            result["levels"] = []
        finally:
            conn.close()
        return result

    # 특정 에리어의 섹터 리스트 검색
    def selectSectors(self, areaId : int):
        conn = self.connect()
        result : dict = self.dbResultTemplate("sectors")
        try:
            with conn.cursor() as cursor:
                sql = f"SELECT sector_id, sector_name FROM sector WHERE area_id = {areaId} and sector_active = True;"
                cursor.execute(sql)
                for row in cursor:
                    result["sectors"].append(row)
            result["result"] = ResultType.SUCCESS.value
        except pymysql.err.Error as e:
            result["result"] = ResultType.ERROR.value
            result["sectors"] = []
        finally:
            conn.close()
        return result
    
    # 특정 섹터 검색
    def selectSector(self, sectorId : int):
        conn = self.connect()
        result : dict = self.dbResultTemplate("sector", isList=False)
        try:
            with conn.cursor() as cursor:
                sql = f"SELECT sector.sector_name, sector.level_id, level.level_value FROM sector INNER JOIN level ON sector.level_id = level.level_id WHERE sector.sector_id = {sectorId};"
                cursor.execute(sql)
                one = cursor.fetchone()
                result["sector"] = one if one is None else {}
            result["result"] = ResultType.SUCCESS.value
        except pymysql.err.Error as e:
            result["result"] = ResultType.ERROR.value
            result["sector"] = {}
        finally:
            conn.close()
        return result
    
    # 섹터 추가
    def insertSector(self, areaId : int, levelId : int, sectorName : str):
        conn = self.connect()
        result : dict = self.dbResultTemplate()
        try:
            with conn.cursor() as cursor:
                sql = f"INSERT INTO sector (area_id, level_id, sector_name) VALUES ({areaId}, {levelId}, '{sectorName}');"
                result["result"] = cursor.execute(sql)
                if result["result"] == ResultType.SUCCESS.value:
                    result["message"] = "성공적으로 섹터가 추가되었습니다."
                else:
                    result["message"] = "섹터 추가에 실패했습니다."
            conn.commit()
        except pymysql.err.Error as e:
            conn.rollback()
            result["result"] = ResultType.ERROR.value
            result["message"] = e.args[1]
        finally:
            conn.close()
        return result
    
    # 특정 섹터 정보 갱신
    def updateSector(self, sectorId : int, newLevelId : int, newSectorName : str):
        conn = self.connect()
        result : dict = self.dbResultTemplate()
        try:
            with conn.cursor() as cursor:
                sql = f"UPDATE sector SET level_id = {newLevelId}, sector_name = '{newSectorName}' WHERE sector_id = {sectorId};"
                result["result"] = cursor.execute(sql)
                if result["result"] == ResultType.SUCCESS.value:
                    result["message"] = "성공적으로 수정되었습니다."
                else:
                    result["message"] = "해당 섹터가 존재하지 않습니다."
            conn.commit()
        except pymysql.err.Error as e:
            conn.rollback()
            result["result"] = ResultType.ERROR.value
            result["message"] = e.args[1]
        finally:
            conn.close()
        return result
    
    # 특정 섹터 삭제
    def deleteSector(self, sectorId : int):
        conn = self.connect()
        result : dict = self.dbResultTemplate()
        try:
            with conn.cursor() as cursor:
                sql = f"UPDATE sector SET sector_active = False WHERE sector_id = {sectorId};"
                result["result"] = cursor.execute(sql)
                if result["result"] == ResultType.SUCCESS.value:
                    result["message"] = "성공적으로 삭제되었습니다."
                else:
                    result["message"] = "이미 삭제된 섹터거나, 해당 섹터가 존재하지 않습니다."
            conn.commit()
        except pymysql.err.Error as e:
            conn.rollback()
            result["result"] = ResultType.ERROR.value
            result["message"] = e.args[1]
        finally:
            conn.close()
        return result
    
    # 특정 에리어의 유저 리스트 검색
    def selectUsers(self, areaId : int):
        conn = self.connect()
        result : dict = self.dbResultTemplate("users")
        try:
            with conn.cursor() as cursor:
                sql = f"SELECT user_id, user_name FROM user WHERE area_id = {areaId} and user_active = True;"
                cursor.execute(sql)
                for row in cursor:
                    result["users"].append(row)
            result["result"] = ResultType.SUCCESS.value
        except pymysql.err.Error as e:
            result["result"] = ResultType.ERROR.value
            result["users"] = []
        finally:
            conn.close()
        return result
    
    # 특정 유저 검색
    def selectUser(self, userId : int):
        conn = self.connect()
        result : dict = self.dbResultTemplate("user", isList=False)
        try:
            with conn.cursor() as cursor:
                sql = f"SELECT user.user_name, user.user_image, user.user_phone, user_datetime, level.level_id, level.level_value FROM sector INNER JOIN level ON user.level_id = level.level_id WHERE user.user_id = {userId};"
                cursor.execute(sql)
                one = cursor.fetchone()
                result["user"] = one if one is None else {}
            result["result"] = ResultType.SUCCESS.value
        except pymysql.err.Error as e:
            result["result"] = ResultType.ERROR.value
            result["user"] = {}
        finally:
            conn.close()
        return result
    
    # 유저 추가
    def insertUser(self, areaId : int, levelId : int, userName : str, userImage : str, userPhone : str):
        conn = self.connect()
        result : dict = self.dbResultTemplate()
        try:
            with conn.cursor() as cursor:
                sql = f"INSERT INTO user (area_id, level_id, user_name, user_image, user_phone) VALUES ({areaId}, {levelId}, '{userName}', '{userImage}', '{userPhone}');"
                result["result"] = cursor.execute(sql)
                if result["result"] == ResultType.SUCCESS.value:
                    result["message"] = "성공적으로 유저가 추가되었습니다."
                else:
                    result["message"] = "유저 추가에 실패했습니다."
            conn.commit()
        except pymysql.err.Error as e:
            conn.rollback()
            result["result"] = ResultType.ERROR.value
            result["message"] = e.args[1]
        finally:
            conn.close()
        return result
    
    # 특정 유저 정보 수정
    def updateUser(self, userId : int, newLevelId : int, newUserName : str, newUserPhone : str):
        conn = self.connect()
        result : dict = self.dbResultTemplate()
        try:
            with conn.cursor() as cursor:
                sql = f"UPDATE user SET level_id = {newLevelId}, user_name = '{newUserName}', user_phone = '{newUserPhone}' WHERE user_id = {userId};"
                result["result"] = cursor.execute(sql)
                if result["result"] == ResultType.SUCCESS.value:
                    result["message"] = "성공적으로 수정되었습니다."
                else:
                    result["message"] = "해당 유저가 존재하지 않습니다."
            conn.commit()
        except pymysql.err.Error as e:
            conn.rollback()
            result["result"] = ResultType.ERROR.value
            result["message"] = e.args[1]
        finally:
            conn.close()
        return result
    
    # 특정 유저 삭제
    def deleteUser(self, userId : int):
        conn = self.connect()
        result : dict = self.dbResultTemplate()
        try:
            with conn.cursor() as cursor:
                sql = f"UPDATE user SET user_active = False WHERE user_id = {userId};"
                result["result"] = cursor.execute(sql)
                if result["result"] == ResultType.SUCCESS.value:
                    result["message"] = "성공적으로 삭제되었습니다."
                else:
                    result["message"] = "이미 삭제된 유저거나, 해당 유저가 존재하지 않습니다."
            conn.commit()
        except pymysql.err.Error as e:
            conn.rollback()
            result["result"] = ResultType.ERROR.value
            result["message"] = e.args[1]
        finally:
            conn.close()
        return result
    
    