import sys

act_path = '/Users/haoyu/lessons/CSC3170/Project/Data/Actors_info_utf8.csv'
award_path = '/Users/haoyu/lessons/CSC3170/Project/Data/Actors_awards_utf8.csv'
award_out_path = '/Users/haoyu/lessons/CSC3170/Project/Data/Actors_awards_final1.csv'
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

		act_dict[tmp[2]] = int(tmp[0])
		index += 1

index = 0
out_award = ''
f_award_final = open(award_out_path, 'w')
with open(award_path) as f_award:
	while True:
		if index % 1000 == 0:
			print(index, end=' ')
		tmp = f_award.readline()
		if not tmp:
			break
		else:
			tmp = tmp.split(',')

		if index == 0:
			tmp = 'Aid,届数,年份,电影节,奖项名称,Mid\n'
			f_award_final.write(tmp)
			index += 1
			continue
		else:
			name = tmp[1]
			year = tmp[2]
			mov_name = tmp[-1].replace('\n', '')
			award_name = tmp[3]
			number = filter(str.isdigit,  award_name)
			number = ''.join(list(number))
			if len(number) > 2 or len(number) < 1:
				continue
			award_name = award_name[len(number)+2:]
			if mov_name not in mid_dict and mov_name != '':
				continue
			elif mov_name == '':
				mid = ''
			else:
				mid = mid_dict[mov_name]
			if name in act_dict:
				aid = act_dict[name]
			else:
				continue

			tmp = [str(aid)] + [number] + [year] + [award_name] + tmp[4:-1] + [str(mid)+'\n']
			tmp = ','.join(tmp)
			f_award_final.write(tmp)

			index += 1

f_award_final.close()



