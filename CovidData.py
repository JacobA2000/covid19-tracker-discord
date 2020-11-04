#REFER TO https://coronavirus.data.gov.uk/developers-guide FOR DETAILS ON THE API
from requests import get

class colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'

def get_data(url):
    response = get(url, timeout=10)
    
    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: { response.text }')
        
    return response.json()

def generate_url(areaType, area, getAreas=False, daily=False, sevenDay=False):
    url = ""

    if getAreas == True:
        url = (
            'https://api.coronavirus.data.gov.uk/v1/data?'
            f'filters=areaType={areaType}&'
            'latestBy=date&'
            'structure={"area":"areaName"}'
        )
    elif daily == True:
        url = (
            'https://api.coronavirus.data.gov.uk/v1/data?'
            f'filters=areaType={areaType};areaName={area}&'
            'latestBy=date&'
            'structure={"date":"date","newCases":"newCasesByPublishDate","totalCases":"cumCasesByPublishDate", "rate":"newCasesBySpecimenDateRollingRate"}'
        )
    elif sevenDay == True:
        url = (
            'https://api.coronavirus.data.gov.uk/v1/data?'
            f'filters=areaType={areaType};areaName={area}&'
            'latestBy=newCasesBySpecimenDateRollingRate&'
            'structure={"date":"date","newCases":"newCasesBySpecimenDateRollingSum","rate":"newCasesBySpecimenDateRollingRate"}'
        )
    
    return url