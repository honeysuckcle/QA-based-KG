def read_file(file_name):
    res = []
    with open(file_name,"r",encoding='utf-8')  as f:
        dd = f.read().split("\n")
        if len(dd)>0:
            l = len(dd[0].split("\t"))
            for i in range(l):
                res.append([])
            for item in dd:
                stemp = item.split("\t")
                if len(stemp) == l:
                    for i in range(l):
                        if stemp[i] not in res[i]:
                            res[i].append(stemp[i])
        f.close()
    return res