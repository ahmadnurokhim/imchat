import sqlite3
def get_new_content_id(conv_id):
    conn = sqlite3.connect("data.db")
    current_content_count = conn.execute(f"SELECT COUNT(*) FROM contents WHERE conv_id = '{conv_id}'").fetchone()[0]
    conn.commit()
    conn.close()
    return "{:0>6}".format(f"{current_content_count}")

def get_new_conv_id():
    conn = sqlite3.connect("data.db")
    current_conv_count = conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
    conn.commit()
    conn.close()
    return "{:0>6}".format(f"{current_conv_count}")

