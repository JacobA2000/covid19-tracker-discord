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
            'structure={"newCases":"newCasesBySpecimenDateRollingSum","rate":"newCasesBySpecimenDateRollingRate"}'
        )
    
    return url
    

    

if __name__ == '__main__':
    #REFER TO https://coronavirus.data.gov.uk/developers-guide FOR DETAILS ON THE API
    AREA = "Bristol, city of"
    AREA_TYPE = "utla"
    
    dailyURL = (
        'https://api.coronavirus.data.gov.uk/v1/data?'
        f'filters=areaType={AREA_TYPE};areaName={AREA}&'
        'latestBy=date&'
        'structure={"date":"date","newCases":"newCasesByPublishDate","totalCases":"cumCasesByPublishDate", "rate":"newCasesBySpecimenDateRollingRate"}'
    )

    sevenDayURL = (
        'https://api.coronavirus.data.gov.uk/v1/data?'
        f'filters=areaType={AREA_TYPE};areaName={AREA}&'
        'latestBy=newCasesBySpecimenDateRollingRate&'
        'structure={"newCases":"newCasesBySpecimenDateRollingSum","rate":"newCasesBySpecimenDateRollingRate"}'
    )
    
    dailyData = get_data(dailyURL)
    sevenDayData = get_data(sevenDayURL)

    print(f"""
    {colors.GREEN}{AREA.upper()} - COVID STATS{colors.ENDC}

    {colors.YELLOW}Total Cases: {dailyData["data"][0]['totalCases']}{colors.ENDC}

    {colors.CYAN}DAILY:{colors.ENDC}
    {colors.YELLOW}Data Date: {dailyData["data"][0]['date']}
    New Cases: {dailyData["data"][0]['newCases']}{colors.ENDC}

    {colors.CYAN}PAST 7 DAYS:{colors.ENDC}
    {colors.YELLOW}Cases: {sevenDayData["data"][0]['newCases']}
    Rate: {sevenDayData["data"][0]['rate']}{colors.ENDC}
    """)