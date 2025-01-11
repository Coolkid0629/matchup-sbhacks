import singlestoredb as s2

# Create a connection to the database
#conn = s2.connect('admin:yRvwS48EZszpsQwpT9JOYnpfSg1Wu3HH@svc-2d85fc18-3a17-4bcf-800c-160f3fd4e87a-dml.gcp-virginia-1.svc.singlestore.com:3306')
conn = s2.connect(host='svc-2d85fc18-3a17-4bcf-800c-160f3fd4e87a-dml.gcp-virginia-1.svc.singlestore.com', port='3306', user='admin',
                  password='yRvwS48EZszpsQwpT9JOYnpfSg1Wu3HH', database='lunchLink')
# Check if the connection is open
with conn:
    with conn.cursor() as cur:
        flag = cur.is_connected()
        print(flag)