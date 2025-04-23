import requests
from config import Config

class LotteryChecker:
    def __init__(self):
        self.cfg = Config()

    def get_lottery_result(self, issue=None):
        """获取彩票开奖结果"""
        api_url = "https://api.tanshuapi.com/api/caipiao/v1/query"
        params = {
            "key": self.cfg.api_key ,  # 你的 API Key
            "caipiaoid": self.cfg.LOTTERY_TYPE ,  # 彩票类型，
            "issueno": "",  # 期号，为空则查询最新一期
        }

        # 发送请求
        response = requests.get(api_url, params=params)

        print("接口查询结果：", response)

        # 处理响应
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 1:  # 假设 code=0 表示请求成功
                return data.get("data")  # 返回查询信息
            else:
                print(f"请求失败：{data.get('msg')}")
        else:
            print(f"请求失败，状态码：{response.status_code}")
        return None

    def compare_dlt(self, user_numbers, prize_front, prize_back):
        """检查中奖情况"""
        user_front = ' '.join(user_numbers[:5])
        user_back = ' '.join(user_numbers[-2:])
        print("user_front:",set(user_front.split()))
        print("user_back:",set(user_back.split()))
        print("prize_front:",set(prize_front.split()))
        print("prize_back:",set(prize_back.split()))

        #prize_front = set(winning_numbers[:5])
        #prize_back = winning_numbers[5]

        # 比对前区和后区号码
        front_match = len(set(user_front.split()) & set(prize_front.split()))  # 前区匹配数量
        back_match = len(set(user_back.split()) & set(prize_back.split()))    # 后区匹配数量

        # 判断中奖等级
        if front_match == 5 and back_match == 2:
            return "一等奖"
        elif front_match == 5 and back_match == 1:
            return "二等奖"
        elif front_match == 5:
            return "三等奖"
        elif front_match == 4 and back_match == 2:
            return "四等奖"
        elif front_match == 4 and back_match == 1:
            return "五等奖"
        elif front_match == 3 and back_match == 2:
            return "六等奖"
        elif front_match == 4:
            return "七等奖"
        elif (front_match == 3 and back_match == 1) or (front_match == 2 and back_match == 2):
            return "八等奖"
        elif (front_match == 3) or (front_match == 1 and back_match == 2) or (front_match == 2 and back_match == 1) or (back_match == 2):
            return "九等奖"
        else:
            return "未中奖"

    def check_winning(self):
        """检查所有用户号码的中奖情况"""
        results = []
        for entry in self.cfg.USER_NUMBERS:
            result = self.get_lottery_result(entry["issue"])
            print(result)
            winning_numbers = result["number"] +" "+ result["refernumber"]
            #print(winning_numbers)
            if result:
                print("比对函数输入：",entry["numbers"], result["number"], result["refernumber"])
                winning_level = self.compare_dlt(entry["numbers"], result["number"], result["refernumber"])
                results.append({
                    "issue": result["issueno"],
                    "opendate":result["opendate"],
                    "user_numbers": entry["numbers"],
                    "winning_numbers": winning_numbers,
                    "winning_level": winning_level,
                    "prize":result["prize"]
                })
                #print(results)
        return results