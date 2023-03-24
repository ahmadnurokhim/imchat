import sqlite3
def get_id():
    conn = sqlite3.connect("data.db")
    current_conv_content_count = conn.execute("SELECT COUNT(*) FROM conversations WHERE conv_id LIKE '000000-%'").fetchone()[0]
    conn.commit()
    conn.close()
    return "000000-{:0>6}".format(f"{current_conv_content_count}")

