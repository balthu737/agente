from app.db import conexcion

class Request():
    def crear_tablas():
        conn = conexcion()
        cursor = conn.cursor()
        query = """
CREATE TABLE IF NOT EXISTS summarys (
    id INT AUTO_INCREMENT PRIMARY KEY,
    summary TEXT NOT NULL,
    messages JSON NOT NULL 
) 
"""
        query_2 = """
CREATE TABLE IF NOT EXISTS experiences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    experience TEXT NOT NULL,
    summarys JSON NOT NULL
)
        """
        cursor.execute(query)
        conn.commit()
        cursor.excute(query_2)
        conn.commit()
        cursor.close()
        conn.close()
