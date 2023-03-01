import mysql.connector

class MysqlService:
    def __init__(self) -> None:
        self.db = mysql.connector.connect(
            host="192.168.1.120",
            user="root",
            password="dIAFaceRecognition2020",
            )

        self.mycursor = self.db.cursor()

    def update(self, img_name):
        # sql = "UPDATE face_recognition.faces_current SET camera_draw_image = 'https://192.168.1.120/images/test.jpg' WHERE camera_code = 'CAMERA3'"
        sql = f"UPDATE face_recognition.faces_current SET camera_draw_image = 'https://192.168.1.120/images/{img_name}' WHERE camera_code = 'CAMERA3'"
        self.mycursor.execute(sql)
        self.db.commit()