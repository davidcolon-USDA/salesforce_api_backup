import sys
sys.path.append('/home/ec2-user/.local/lib/python3.11/site-packages')

from simple_salesforce import Salesforce
import json

# Replace these values with your actual Salesforce credentials
USERNAME = 'api@usdaccuat.gov'
PASSWORD = 'OneOcx72125'
SECURITY_TOKEN = 'ta26M2cvGjSHByIOiyn7jd2Qp'
DOMAIN = 'oneusdacontactcenter--ccuat.sandbox.my'
API_URL = 'https://oneusdacontactcenter--ccuat.sandbox.my.salesforce.com/'
API_VERSION = '64.0'

def connect_salesforce():
    try:
        sf = Salesforce(
            username=USERNAME,
            password=PASSWORD,
            security_token=SECURITY_TOKEN,
            domain=DOMAIN,
            version=API_VERSION
        )
        print("✅ Connected to Salesforce.")
        return sf
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return None

def query_accounts(sf):
    query = "SELECT Id, FirstName, LastName, Email FROM Contact LIMIT 10"
    results = sf.query(query)
    for acc in results['records']:
        print(f"{acc}")

if __name__ == '__main__':
    sf = connect_salesforce()
    print(f"Salesforce instance URL: https://{sf.sf_instance}")
    if sf:
        query_accounts(sf)
