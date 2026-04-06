from api_db_memoria.db import conexcion

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
    def summary_post(self, summary, messages):
        self.summary = summary
        self.messages = messages
        conn = conexcion()
        cursor = conn.cursor()
        query = """
        INSERT INTO summarys (summary, messages) VALUES (%S, %S)
        """
        cursor.execute(query, (self.summary, self.messages))
        conn.commit()
        cursor.close()
        conn.close()
    def summary_count(self):
        conn = conexcion()
        cursor = conn.cursor()
        query = """
        SELECT COUNT(*) FROM summarys 
        """
        cursor.execute(query)
        count = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return count