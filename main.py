from datetime import datetime, timedelta
import pickle
import time
import requests
import sys

class NewsToNaver:
    def __init__(self):

        sys.stdout.write(f"\rA-RT Checker\n")
        sys.stdout.flush()
        data = '''                       @@@@@@@@@
                       @@@@@@@@@
                       @@@@@@@@@                   @@@@@@@@@@@     @@@@@@@@@@@@@
                       @@@@@@@@@                   @@@@@@@@@@@@    @@@@@@@@@@@@@
                       @@@@@@@@@                   @@@@@@@@@@@@@   @@@@@@@@@@@@@
                       @@@@@@@@@                     @@@@  @@@@@   @@@ @@@@@ @@@
                       @@@$@@@@@                     @@@@   @@@@   @@  @@@@@  @@
                      @@@@ @@@@@@                    @@@@   @@@@   @@  @@@@@  @@
                      @@@* *@@@@@      -@@@@@@!      @@@@  @@@@        @@@@@
                      @@@; ;@@@@@      -@@@@@@!      @@@@@@@@@         @@@@@
                      @@@@@@@@@@@      ,@@@@@@!      @@@@@@@@          @@@@@
                     @@@@@@@@@@@@@                   @@@@#@@@@         @@@@@
                     @@@@@@@@@@@@@                   @@@@  @@@@        @@@@@
                     @@@:   ;@@@@@                   @@@@  @@@@        @@@@@
                    @@@@.   ,@@@@@@                  @@@@   @@@@       @@@@@
                    @@@@-, .-@@@@@@                @@@@@@@  @@@@@     @@@@@@@
                  @@@@@@@; ;#@@@@@@@               @@@@@@@  @@@@@     @@@@@@@
                  @@@@@@@; ;@@@@@@@@               @@@@@@@  @@@@@     @@@@@@@
                  @@@@@@@; :@@@@@@@@                                     
                  @@@@@@@; ;@@@@@@@@           Checker by Pv(seso6430@naver.com) ver_0.0.3
                                                                     '''
        for i in data.split("\n"):
            print(i)
            time.sleep(0.1)

    def save(self, data):
        pickle.dump(data, open(f'_internal/abcld.dll', 'wb'), pickle.HIGHEST_PROTOCOL)

    def load(self):
        try:
            return pickle.load(open(f'_internal/abcld.dll', 'rb'))
        except:
            while True:
                id = input("입력된 아이디는 계속 저장됩니다.\nA-RT ID:")
                pw = input("A-RT PW:")
                data = f"{id}:{pw}"
                try:
                    self.mypage({"ID": data.split(":")[0], "PW": data.split(":")[-1]})
                    self.save(data)
                    break
                except:
                    print("\n계정을 다시 확인해주세요.")
            return data

    def login(self, data, urls):
        req = requests.get(urls)
        JSESSIONID = str(req.cookies).split("JSESSIONID=")[-1].split(" for")[0]
        WMONID = str(req.cookies).split("WMONID=")[-1].split(" for")[0]
        header = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Cookie": f"JSESSIONID={JSESSIONID}; " f"WMONID={WMONID}",
        }
        url = f"{urls}login/login-processing"
        data = f'loginType=member&username={data["ID"]}&password={data["PW"]}'
        req = requests.post(url, data=data, headers=header)
        UID = str(req.cookies).split("UID=")[-1].split(" for")[0]
        header = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Cookie": f"JSESSIONID={JSESSIONID}; " f"WMONID={WMONID}; " f"UID={UID}",
        }
        cookie = [
            {
                "name": "JSESSIONID",
                "value": JSESSIONID
            },
            {
                "name": "WMONID",
                "value": WMONID
            },
            {
                "name": "UID",
                "value": UID
            },

        ]
        return header, cookie

    def mypage(self, data):
        header, cookie = self.login(data, "https://m.grandstage.a-rt.com/")
        req = requests.get('https://m.grandstage.a-rt.com/member/member-barcode-info', headers=header)
        event = requests.get("https://m.grandstage.a-rt.com/promotion/event/list?statusType=ing")
        for i in event.json()["eventList"]:
            if "출석체크" in i["eventName"]:
                eventNo = i["eventNo"]
                break
        data = f"eventNo={eventNo}&memberNo={req.json()['memberInfo']['memberNo']}&eventTypeCode=10002&mktUseAgreeYn=N&chkSaveID=&smsRecvYn=N&emailRecvYn=N&nightSmsRecvYn=N&quizAnswer=&surveyNo="
        requests.post('https://m.grandstage.a-rt.com/promotion/event/attend/check/member/save', headers=header, data=data)

        return req.json()["memberInfo"]['memberName']

    def run(self):
        while True:
            data = self.load()
            print(data)
            name = self.mypage({"ID": data.split(":")[0], "PW": data.split(":")[-1]})
            inputtime = datetime.now()+timedelta(days=1)
            sys.stdout.write(f"\r{name}님 A-RT AIO에 오신것을 환영합니다.\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}에 금일 출석체크가 완료되었습니다.\n다음 출석체크는 24시간 이후입니다.\n")
            sys.stdout.flush()
            while True:
                sys.stdout.write(f"\r{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                sys.stdout.flush()
                if datetime.now() >= inputtime:
                    break

NewsToNaver().run()


# pyinstaller --icon=img.ico main_.py
