import os

# SingleStore Database Configuration
SINGLESTORE_CONFIG = {
    'host': os.getenv('SINGLESTORE_HOST', 'svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.co'),
    'user': os.getenv('SINGLESTORE_USER', 'roshan-a8a10'),
    'password': os.getenv('SINGLESTORE_PASSWORD', 'OkgTtGzGafIOkZgo6nD8lAhl65Io933T'),
    'database': os.getenv('SINGLESTORE_DB', 'db_roshan_7e420'),
}
