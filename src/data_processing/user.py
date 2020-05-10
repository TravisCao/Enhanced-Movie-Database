comm_path = "/Users/haoyu/lessons/CSC3170/Project/Data/comment.csv"
user_out_path = "/Users/haoyu/lessons/CSC3170/Project/Data/user_final.csv"


users = []
index = 0
c = 0
with open(comm_path) as f_comm:
    while True:
        tmp = f_comm.readline()
        if not tmp:
            break
        else:
            tmp = tmp.split(",")
        if index == 0:
            index += 1
            continue
        if len(tmp) != 7:
            continue

        user = tmp[5]
        users.append(user)

        index += 1

f_user = open(user_out_path, "w")
f_user.write("Uid,name,pwd,mail\n")
for index, name in enumerate(users):
    tmp = [
        str(index + 1),
        name,
        str(hash(str(index + 1))),
        str(index + 1) + "@movdata.com\n",
    ]
    tmp = ",".join(tmp)
    f_user.write(tmp)
f_user.close()
