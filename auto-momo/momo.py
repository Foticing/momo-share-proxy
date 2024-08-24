# encoding:utf-8
from os import environ
from ip import listIP, getheaders, ip_main
from asyncio import create_task, wait, Semaphore, run
from aiohttp import ClientSession, ClientTimeout

global n  # 记录访问成功次数
link = 'https://www.maimemo.com/page?sid=7a9e30670b28730d0ebb5219dedfb4eb&uid=19253996&pid=2cfaa018e3403c2daadb212e3a941b49&tid=52e66ba0ff3fc8263abdb6661f966a0b&view_time=1724504670&bind_user=0&create_user=0&oauth=wechat_wx6a4680fa1ef1b496&unionid=o6IDit3i0oc7OvR85vMQFTdWB0CE&token=580857d6dca812bed7391ac883d525dc506aa4a49406f23ab67fda093123df85&expired_time=2025-08-24T21:04:30%2008:00'  # 设置link

# 如果检测到程序在 github actions 内运行，那么读取环境变量中的登录信息
if environ.get('GITHUB_RUN_ID', None):
    link = environ['link']


async def create_aiohttp(url, proxy_list):
    global n
    n = 0
    async with ClientSession() as session:
        # 生成任务列表
        task = [create_task(web_request(url, proxy, session)) for proxy in proxy_list]
        await wait(task)


# 网页访问
async def web_request(url, proxy, session):
    # 并发限制
    async with Semaphore(5):
        try:
            async with await session.get(url=url, headers=await getheaders(), proxy=proxy,
                                         timeout=ClientTimeout(total=10)) as response:
                # 返回字符串形式的相应数据
                page_source = await response.text()
                await page(page_source)
        except Exception:
            pass


# 判断访问是否成功
async def page(page_source):
    global n
    if "学习天数" in page_source:
        n += 1


def main():
    ip_main()  # 抓取代理
    run(create_aiohttp(link, listIP))
    print(f"墨墨分享链接访问成功{n}次。")


if __name__ == '__main__':
    main()
