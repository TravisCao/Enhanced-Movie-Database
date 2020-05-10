import sys

act_path = '/Users/haoyu/lessons/CSC3170/Project/Data/Actors_info_utf8.csv'
mov_path = '/Users/haoyu/lessons/CSC3170/Project/Data/mov.csv'
mov_out_path = '/Users/haoyu/lessons/CSC3170/Project/Data/Actors_mov_final.csv'
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
		mov_name = tmp[0]
		mov_id = index-1
		if mov_name not in mid_dict:
			mid_dict[mov_name] = mov_id
		index += 1


act_dict = {}
index = 0
with open(act_path) as f_act:
	while True:
		tmp = f_act.readline()
		if not tmp:
			break
		else:
			tmp = tmp.split(',')
		if index == 0:
			index += 1
			continue
		act_dict[tmp[1]] = int(tmp[0])
		index += 1

def get_id(names):
	l = []
	names = names.split('/')
	for name in names:
		if name in act_dict:
			act_id = act_dict[name]
			l.append(act_id)
		else:
			continue
	return l


index = 0
f_act_mov = open(mov_out_path, 'w')
with open(mov_path) as f_mov:
	while True:
		tmp = f_mov.readline()
		if not tmp:
			break
		else:
			tmp = tmp.split(',')

		if index == 0:
			print(tmp)
			tmp = ['Aid', '职业', 'Mid\n']
			tmp = ','.join(tmp)
			f_act_mov.write(tmp)
			index += 1
			continue
		else:
			mov      = tmp[0] 

			director = tmp[11]
			writer   = tmp[12]
			actor    = tmp[13]
			l_director = get_id(director)
			l_writer = get_id(writer)
			l_actor = get_id(actor)

			for i in l_director:
				line = ','.join([str(i), '导演', mov+'\n'])
				f_act_mov.write(line)
			for i in l_writer:
				line = ','.join([str(i), '编剧', mov+'\n'])
				f_act_mov.write(line)
			for i in l_actor:
				line = ','.join([str(i), '演员', mov+'\n'])
				f_act_mov.write(line)

			index += 1

f_act_mov.close()


