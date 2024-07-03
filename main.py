import time
# 将config中的信息进行导入
from config import *
# 代码用到了requests模块，进行导入
import requests
# B站使用了brotli（br）加密方式，因此需要导入brotli（如果不导入，请求会报错）
import brotli


# 该函数传入user_list（种子用户列表）
# 其作用是，查找每个用户关注的up，将up的信息保存到f_list，进行去重后返回；
# 同时将该用户user_dict中的read属性设置为1，表示该用户已被查询过，避免后续重复查询；
def following(fo_list: list) -> list:
    # 创建一个列表，把所有用户的关注者信息保存到列表中
    f_list = []
    # n用于计数
    n = 0
    # 遍历user_list
    for user in fo_list:
        n += 1
        # 调用B站接口，获取用户关注的up信息;(返回信息是json才能用.json()方法)
        data = requests.get(following_url.format(user, 1), headers=request_headers).json()
        # 若接口返回code为0，代表请求成功
        if data['code'] == 0:
            temp_list = data['data']['list']
            # 将该用户关注up的用户id和用户名全部保存到f_list
            f_list.extend([(str(j['mid']), j['uname']) for j in temp_list])
            # 判断用户关注数是否大于50，如果大于50则再发起一次请求，获取第二页数据
            if data['data']['total'] > 50:
                data2 = requests.get(following_url.format(user, 2), headers=request_headers).json()
                f_list.extend([(str(j['mid']), j['uname']) for j in data2['data']['list']])
            print('{}, 用户{}关注列表已查询'.format(n, user))
        # 返回其它，则可能是用户设置隐私，禁止其他人查看关注列表
        else:
            print('{}, 用户{}已设置隐私，无法查看'.format(n, user))
        # 需要先判断指定用户是否在fo_dict中，如果不进行判断会带来很麻烦的KeyError
        if user in user_dict:
            # 将指定用户user_dict的read属性改为1，表示该用户已被查询过，避免后续重复查询；
            user_dict[user]['read'] = 1
            # 查询完一个用户信息后，暂停1秒，再去查询下一个用户的信息；这里很重要，避免被系统认定为恶意爬虫，直接ban id或者ip
        time.sleep(1)
    # 用set()将f_list转为集合，从而进行去重；再用list()重新转换为列表
    return list(set(f_list))


# 传入2个参数，w_num用于计数；w_list是用户信息列表；
# 遍历w_list，如果元素在user_dict中，则不处理；不在字典中，则调用B站接口爬取指定用户的数据；
# 最终返回更新后的user_dict
def writedata(w_num: int, w_list: list) -> dict:
    for user in w_list:
        w_num += 1
        # w_list里的每个元素是一个元组，元组第一个元素是用户id，第二个元素是用户名
        # 如果用户还未记录在w_dict中，则调用接口获取用户的粉丝量，并把相关信息记录在w_dict
        if user[0] not in user_dict:
            follower_num = requests.get(stat_url.format(user[0]), headers=request_headers).json()['data']['follower']
            user_dict[user[0]] = {'uname': user[1], 'follower_num': follower_num}
            print('{},{},{}插入到字典中'.format(w_num, user[0], user[1]))
            # 查询完一个用户信息后，暂停1秒，再去查询下一个用户的信息；这里很重要，避免被系统认定为恶意爬虫，直接ban id或者ip
            time.sleep(0.3)
        # 如果用户已记录在w_dict中，则无需进行操作
        else:
            print('{},{},{}已在字典中'.format(w_num, user[0], user[1]))
    # 返回结果是更新后的user_dict
    return user_dict


if __name__ == '__main__':
    t1 = time.time()
    user_dict = {}
    test_user_list = ['1969187'] # 该id是UP自己的用户id
    # test_user_list = ['1440869598']
    num = 0
    filename = '0710'

    try:
        # 用following()函数，获取test_user_list中所有用户的关注列表，保存到following_list
        following_list = following(test_user_list)
        print(following_list)
        # 用writedata()函数，获取following_list中所有用户的粉丝量，然后把信息更新到user_dict中
        user_dict = writedata(num, following_list)
        # 把user_dict中粉丝量介于800到1000的用户筛选出来
        result_list = [(user_dict[i]['follower_num'], i) for i in user_dict if 800 < user_dict[i]['follower_num'] < 1000]
        # 如果result_list不为空，则打印对应用户的粉丝量和个人主页链接
        if len(result_list) > 0:
            for user in result_list:
                print('粉丝量{}, https://space.bilibili.com/{}'.format(user[0], user[1]))
        else:
            print('没有符合条件的用户')
        # 把user_dict保存为py文件（方便后续再次调用，直接import即可）
        with open(filename + '_result' + '.py', 'w', newline='') as f:
            f.write('user_dict = ' + str(user_dict))
        # 把result_list中用户的粉丝量和个人主页链接信息，保存为txt文档
        with open(filename + '_url' + '.txt', 'w', newline='') as f:
            for user in result_list:
                f.write('粉丝量{}, https://space.bilibili.com/{}\n'.format(user[0], user[1]))

    # 如果在执行中出现任何错误，那么会把关键信息打印、保存。
    # 当然我这个写法过于暴力（没有枚举任何错误类型），仅供参考
    except:
        print(user_dict)
        result_list = [(user_dict[i]['follower_num'], i) for i in user_dict if 800 < user_dict[i]['follower_num'] < 1000]
        if len(result_list) > 0:
            for user in result_list:
                print('粉丝量{}, https://space.bilibili.com/{}'.format(user[0], user[1]))
        else:
            print('没有符合条件的用户')
        with open(filename + '_result' + '.py', 'w', newline='') as f:
            f.write('user_dict = ' + str(user_dict))
        with open(filename + '_url' + '.txt', 'w', newline='') as f:
            for user in result_list:
                f.write('粉丝量{}, https://space.bilibili.com/{}\n'.format(user[0], user[1]))

    print("代码执行完毕，用时{}秒".format(round(time.time() - t1, 2)))
