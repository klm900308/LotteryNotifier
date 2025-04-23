from apscheduler.schedulers.blocking import BlockingScheduler
from lottery import LotteryChecker
from notification import send_email
from datetime import datetime
from xml.dom import minidom
import json

def job():
    print(f"开始执行检查任务: {datetime.now()}")
    checker = LotteryChecker()
    results = checker.check_winning()
    #data = results[0]
    #print(results)
    #print(data['prize'])
    #print(results['prize'])
    #print(data['user_numbers'],data['winning_numbers'])
    # 解析 XML
    #dom = minidom.parseString(results['prize'])
    # 格式化输出
    #pretty_xml = dom.toprettyxml(indent="  ")
    formatted_json = json.dumps(results[0]['prize'], indent=4, ensure_ascii=False)

    for result in results:
        email_content = f"""
        彩票类型: 大乐透
        开奖期号: {result['issue']}
        开奖时间:{result['opendate']}
        中奖情况: {result['winning_level']}
        你的号码: {', '.join(result['user_numbers'][:5])} | {', '.join(result['user_numbers'][-2:])}
        开奖号码: {', '.join(result['winning_numbers'].split()[:5])} | {', '.join(result['winning_numbers'].split()[-2:])}
        开奖情况：{formatted_json}
        """

        subject = f"大乐透{result['issue']}期开奖结果 - {result['winning_level']}"
        send_email(subject, email_content)

# 测试邮件发送代码
#if __name__ == "__main__":
#    # 测试邮件发送
#    send_email("彩票中奖通知", "这是一封测试邮件")

# 正式代码...
if __name__ == "__main__":
    # 创建定时任务
    scheduler = BlockingScheduler()

    #正式任务
    # 每周二、四、日8:00执行（大乐透开奖时间为周一、三、六）
    #scheduler.add_job(job, 'cron', hour=8, minute=00, day_of_week='tue,thu,sun')

    #测试任务
    scheduler.add_job(job, 'interval', seconds=10)

    print("彩票开奖通知服务已启动，等待执行...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("服务已停止")