
import json, requests
from typing import List
from decorators import log_exceptions

@log_exceptions()
class SmsSender:
    def __init__(self, id, company_code, from_phone):
        self.id = id
        self.company_code = company_code
        self.from_phone = from_phone

    def send_sms (self, phone_numbers:List[str], message:str, api_url):
        converted_sms_data = json.dumps ([
            { "usercode": self.id, "deptcode" : self.company_code, "to": phone_number, "reqphone": self.from_phone, "text" : message } 
            for phone_number in phone_numbers])
        waittime = 300
        response = requests.post(api_url, headers={'Content-Type': 'application/json'}, data=converted_sms_data, verify=False, timeout=waittime) 
        send_results:List[dict] = response.json()['results']
        need_cash = any('fail_need_cash' in send_result.values() for send_result in send_results)
        
        return "잔액 부족" if need_cash else "SMS 전송 완료"