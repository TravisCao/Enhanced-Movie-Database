import sys


comm_path = '/Users/haoyu/lessons/CSC3170/Project/Data/comment.csv'
comm_user_out_path = '/Users/haoyu/lessons/CSC3170/Project/Data/comm_user_final1.csv'
mov_path  = '/Users/haoyu/lessons/CSC3170/Project/Data/movie0.csv'
mov1_path = '/Users/haoyu/lessons/CSC3170/Project/Data/movie1.csv'
mid_path = '/Users/haoyu/lessons/CSC3170/Project/Data/mov.csv'


mid_dict = {}
index = 0
with open(mid_path) as f_mid:
	while True:
		tmp = f_mid.readline()
		if not tmp:
			break
		else:
			tmp = tmp.split(',')
		if index == 0:
			index += 1
			continue
		mov_name = tmp[0].split(' ')[0]
		mov_id = index-1
		if mov_name not in mid_dict:
			mid_dict[mov_name] = mov_id
		index += 1


index = 0
mov_dict = {}
with open(mov_path) as f_mov:
	while True:
		tmp = f_mov.readline()
		if not tmp:
			break
		else:
			tmp = tmp.split(',')
		if index == 0:
			index += 1
			continue
		if len(tmp) != 3:
			print(tmp)
			continue
		mov_id = tmp[0]
		name   = tmp[1]
		mov_dict[mov_id] = name

index = 0
with open(mov1_path) as f_mov1:
	while True:
		tmp = f_mov1.readline()
		if not tmp:
			break
		else:
			tmp = tmp.split(',')
		if index == 0:
			index += 1
			continue
		if len(tmp) != 3:
			print(tmp)
			continue			
		mov_id = tmp[0]
		name   = tmp[1]
		mov_dict[mov_id] = name



users = []
index = 0
c = 0
with open(comm_path) as f_comm:
	while True:
		tmp = f_comm.readline()
		if not tmp:
			break
		else:
			tmp = tmp.split(',')
		if index == 0:
			index += 1
			continue
		if len(tmp) != 7:
			continue

		user = tmp[5]	
		users.append(user)

		index += 1

user_dict = {}

for index, name in enumerate(users):
	user_dict[name] = index+1

cid = 1
index = 0
f_comm_user = open(comm_user_out_path, 'w')
f_comm_user.write('Cid,时间,Uid,Mid,评分,内容\n')
with open(comm_path) as f_comm:
	while True:
		tmp = f_comm.readline()
		if not tmp:
			break
		else:
			tmp = tmp.split(',')
		if index == 0:
			index += 1
			continue
		if len(tmp) != 7:
			continue
		if tmp[1][:2] != '20':
			continue

		user   = tmp[5]	
		time   = tmp[1][:4]
		mov_ID    = tmp[2]
		rating = tmp[3]
		con    = tmp[4]
		user_id = user_dict[user]
		if mov_ID not in mov_dict:
			continue
		mov = mov_dict[mov_ID]
		if mov not in mid_dict:
			continue
		mov = mid_dict[mov]

		out = [str(cid), time, str(user_id), str(mov), str(rating), con+'\n']
		out = ','.join(out)
		f_comm_user.write(out)
		cid += 1

		index += 1

f_comm_user.close()


