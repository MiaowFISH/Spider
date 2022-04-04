for i in range(1, ):
    url = 'http://images.dmzj1.com/b/别当欧尼酱了/第21话_1543049755/{:0>2d}.jpg'.format(i)
    page = url[-22: -18]
    if os.path.exists('D:\\Miaow\\Documents\\wwwroot\\buka\\img\\{}_{:0>4d}.jpg'.format(page, i)):
        print('{}_{:0>4d}.jpg exits'.format(page, i))
    else:
        r = requests.get(url)
        print(url, r.status_code)
        if r.status_code == 200:
            file = 'D:\\Miaow\\Documents\\wwwroot\\buka\\img\\{}_{:0>4d}.jpg'.format(page, i)
            data = r.content
            with open(file, 'wb') as f:
                f.write(data)
        else:
            print(f'共{i - 1}话')
            break
