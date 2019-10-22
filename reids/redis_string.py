from redis import StrictRedis


if __name__ == '__main__':
    # 创建StrictRedis对象，链接redis数据库
    try:
        sr = StrictRedis()
        # 添加一个key，为name, value, focusdroid
        res = sr.set('name', 'focusdroidss')

        res = sr.set('name', 'nangong')
        # 获取name的值
        rss = sr.get('name')
        print(rss)

        ## 删除
        resdel = sr.delete('name')
        print(resdel)
    except Exception as e:
        pass
