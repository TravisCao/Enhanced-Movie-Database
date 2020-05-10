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
		mov_id = index
		if mov_name not in mid_dict:
			mid_dict[mov_name] = mov_id
		index += 1

print(mid_dict)
