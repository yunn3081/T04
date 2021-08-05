import psycopg2

def get_data():
    myConnection = psycopg2.connect(
        host="localhost",
        database="cellline",
        user="postgres",
        password="postgres",
        port=5432)
    cur = myConnection.cursor()
    cur.execute('SELECT "No", "Product category", "Organism", "Age", "Gender", "Ethnicity", "Biopsy site", "Tissue", "Cancer type", "Growth properties", "Stock" FROM public.patient_cellline')
    cellline_data = cur.fetchall()
    cur.close
    myConnection.close
    return cellline_data