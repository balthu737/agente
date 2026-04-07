from db import conexcion

class Request():
    def __init__(self):
        self.summarys = ""
    def crear_tablas(self):
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
        cursor.execute(query_2)
        conn.commit()
        cursor.close()
        conn.close()
    def summary_post(self, summary, messages):
        self.summarys = summary
        self.messages = messages
        conn = conexcion()
        cursor = conn.cursor()
        query = """
        INSERT INTO summarys (summary, messages) VALUES (%s, %s)
        """
        cursor.execute(query, (self.summarys, self.messages))
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
    def experience_summary(self):
        conn = conexcion()
        cursor = conn.cursor()
        query = """
        SELECT * FROM summarys ORDER BY id DESC LIMIT 10
        """
        cursor.execute(query)
        summary = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return summary
    def experience_post(self, experience, summarys):
        conn = conexcion()
        cursor = conn.cursor()
        query = """
        INSERT INTO experiences (experience, summarys) VALUES (%s, %s) 
        """
        cursor.execute(query, (experience, summarys))
        conn.commit()
        cursor.close()
        conn.close()