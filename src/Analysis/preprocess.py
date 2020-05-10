import os
import xlrd
import xlwt

# 检验是否含有中文字符
def isContainChinese(s):
    for c in s:
        if "\u4e00" <= c <= "\u9fa5":
            return True
    return False


# 检验是否全是中文字符
def isAllChinese(s):
    for c in s:
        if not ("\u4e00" <= c <= "\u9fa5"):
            return False
    return True


def containenglish(str0):
    import re

    return bool(re.search("[a-z]", str0))


def process_data():
    import xlwt

    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding="utf-8")
    workbook_award = xlwt.Workbook(encoding="utf-8")
    workbook_best_five = xlwt.Workbook(encoding="utf-8")

    # 创建一个worksheet
    worksheet = workbook.add_sheet("My Worksheet")
    worksheet.write(0, 0, label="中文姓名")
    worksheet.write(0, 1, label="英文姓名")
    worksheet.write(0, 2, label="性别")
    worksheet.write(0, 3, label="出生国家")
    worksheet.write(0, 4, label="出生省份")
    worksheet.write(0, 5, label="出生城市")
    worksheet.write(0, 6, label="星座")
    worksheet.write(0, 7, label="职业")
    worksheet.write(0, 8, label="更多外文名")
    worksheet.write(0, 9, label="imdb编号")
    worksheet.write(0, 10, label="官方网站")
    worksheet.write(0, 11, label="现任配偶")
    # create worksheet for award
    worksheet_award = workbook_award.add_sheet("My Worksheet")
    worksheet_award.write(0, 0, label="中文姓名")
    worksheet_award.write(0, 1, label="英文姓名")
    worksheet_award.write(0, 2, label="年份")
    worksheet_award.write(0, 3, label="电影节")
    worksheet_award.write(0, 4, label="奖项名称")
    worksheet_award.write(0, 5, label="获奖电影名称")
    # create worksheet for bestfive
    worksheet_best_five = workbook_best_five.add_sheet("My Worksheet")
    worksheet_best_five.write(0, 0, label="中文姓名")
    worksheet_best_five.write(0, 1, label="英文名称")
    worksheet_best_five.write(0, 2, label="电影年份")
    worksheet_best_five.write(0, 3, label="电影名称")
    actor_info_index = 1
    actor_award_index = 1
    actor_best_index = 1

    with open("/Users/hm_cai/Desktop/归档/record_info_index.txt", "r") as read_recording:
        index_record_lists = read_recording.readlines()

    for dir_root, _, fnames in os.walk(
        "/Users/hm_cai/Desktop/CSC3170爬虫/celebrity/dataset"
    ):
        for fname in sorted(fnames):
            if fname + "\n" in index_record_lists:
                print("passing {}".format(fname))
                pass
            else:
                f_path = dir_root + "/" + fname
                with open(f_path, "r") as data_input:
                    print(
                        "processing file : {} ,  line_index : {}".format(
                            f_path, actor_info_index
                        )
                    )
                    index_record = []
                    data = data_input.readlines()
                    for i in range(len(data)):
                        data[i] = data[i].lstrip().rstrip()
                        if data[i] == "":
                            index_record.append(i)

                    # preprocess data
                    index_record.sort(reverse=True)
                    for index in index_record:
                        del data[index]

                    if len(data) < 5:
                        pass
                    else:
                        # obtain basic info
                        data_strcture = {
                            "姓名:": "Null",
                            "性别:": "Null",
                            "星座:": "Null",
                            "出生日期:": "Null",
                            "出生地:": "Null",
                            "职业:": "Null",
                            "更多外文名:": "Null",
                            "家庭成员:": "Null",
                            "imdb编号:": "Null",
                            "官方网站:": "Null",
                        }  # , '代表影片:':'Null', 'Awards:':'Null'}

                        data_strcture["姓名:"] = data[0][data[0].index(":") + 1 :]

                        index_record_2 = []
                        for i in range(len(data)):
                            data_content = data[i]
                            if data_content in data_strcture and (i < len(data) - 1):
                                data_strcture[data_content] = data[i + 1]
                                index_record_2.append(i)
                                index_record_2.append(i + 1)
                        if len(index_record_2) == 0:
                            index_record_2.append(0)

                        # process family member
                        famiy_member = data_strcture["家庭成员:"]
                        data_strcture["现任配偶:"] = "Null"
                        if famiy_member == "Null":
                            pass
                        elif "/" in famiy_member:
                            famiy_member_split = famiy_member.split("/")
                            print(famiy_member_split)
                            for member in famiy_member_split:
                                if "前夫" in member or "前妻" in member:
                                    pass
                                elif "夫" in member:
                                    data_strcture["现任配偶:"] = member[
                                        : member.index("夫") - 1
                                    ]
                                elif "妻" in member:
                                    data_strcture["现任配偶:"] = member[
                                        : member.index("妻") - 1
                                    ]
                        del data_strcture["家庭成员:"]

                        # process more name
                        if "(本名)" in data_strcture["更多外文名:"]:
                            index = data_strcture["更多外文名:"].index("(本名)")
                            data_strcture["更多外文名:"] = data_strcture["更多外文名:"][:index]

                        # process english and chinese name
                        data_strcture["中文姓名:"] = "Null"
                        data_strcture["英文姓名:"] = "Null"
                        actor_name = data_strcture["姓名:"]
                        if isContainChinese(actor_name) and containenglish(actor_name):
                            split_name = actor_name.split(" ")
                            chinese_name = split_name[0]
                            english_name = data_strcture["姓名:"][
                                len(chinese_name) :
                            ].lstrip()
                            data_strcture["中文姓名:"] = chinese_name
                            data_strcture["英文姓名:"] = english_name
                        elif isContainChinese(actor_name) and not containenglish(
                            actor_name
                        ):
                            chinese_name = actor_name
                            data_strcture["中文姓名:"] = chinese_name
                        elif not isContainChinese(actor_name) and containenglish(
                            actor_name
                        ):
                            english_name = actor_name
                            data_strcture["英文姓名:"] = english_name
                        else:
                            assert "something wrong"
                        del data_strcture["姓名:"]

                        # process birhplace
                        data_strcture["出生国家:"] = "Null"
                        data_strcture["出生省份:"] = "Null"
                        data_strcture["出生城市:"] = "Null"
                        birth_location = data_strcture["出生地:"]
                        if birth_location == "Null":
                            pass
                        elif "," in birth_location:
                            birth_location_split = birth_location.split(",")
                            if len(birth_location_split) == 3:
                                data_strcture["出生国家:"] = birth_location_split[0]
                                data_strcture["出生省份:"] = birth_location_split[1]
                                data_strcture["出生城市:"] = birth_location_split[2]
                            elif len(birth_location_split) == 2:
                                data_strcture["出生国家:"] = birth_location_split[0]
                                data_strcture["出生城市:"] = birth_location_split[1]
                            else:
                                assert "more than 3 elements in birthplace"
                        else:
                            data_strcture["出生国家:"] = birth_location
                        del data_strcture["出生地:"]

                        # 写入excel
                        # 参数对应 行, 列, 值
                        worksheet.write(
                            actor_info_index, 0, label=data_strcture["中文姓名:"]
                        )
                        worksheet.write(
                            actor_info_index, 1, label=data_strcture["英文姓名:"]
                        )
                        worksheet.write(actor_info_index, 2, label=data_strcture["性别:"])
                        worksheet.write(
                            actor_info_index, 3, label=data_strcture["出生国家:"]
                        )
                        worksheet.write(
                            actor_info_index, 4, label=data_strcture["出生省份:"]
                        )
                        worksheet.write(
                            actor_info_index, 5, label=data_strcture["出生城市:"]
                        )
                        worksheet.write(actor_info_index, 6, label=data_strcture["星座:"])
                        worksheet.write(actor_info_index, 7, label=data_strcture["职业:"])
                        worksheet.write(
                            actor_info_index, 8, label=data_strcture["更多外文名:"]
                        )
                        worksheet.write(
                            actor_info_index, 9, label=data_strcture["imdb编号:"]
                        )
                        worksheet.write(
                            actor_info_index, 10, label=data_strcture["官方网站:"]
                        )
                        worksheet.write(
                            actor_info_index, 11, label=data_strcture["现任配偶:"]
                        )
                        if actor_info_index % 100 == 0:
                            workbook.save("/Users/hm_cai/Desktop/归档/Actors_info.xlsx")
                        actor_info_index += 1

                        data = data[index_record_2[-1] + 1 :]
                        """ process award and best five """

                        awards_index = data.index("Awards:")
                        awards_list = data[awards_index:]
                        best_five_list = data[:awards_index]
                        years_list = [
                            "1900",
                            "1901",
                            "1902",
                            "1903",
                            "1904",
                            "1905",
                            "1906",
                            "1907",
                            "1908",
                            "1909",
                            "1910",
                            "1911",
                            "1912",
                            "1913",
                            "1914",
                            "1915",
                            "1916",
                            "1917",
                            "1918",
                            "1919",
                            "1920",
                            "1921",
                            "1922",
                            "1923",
                            "1924",
                            "1925",
                            "1926",
                            "1927",
                            "1928",
                            "1929",
                            "1930",
                            "1931",
                            "1932",
                            "1933",
                            "1934",
                            "1935",
                            "1936",
                            "1937",
                            "1938",
                            "1939",
                            "1940",
                            "1941",
                            "1942",
                            "1943",
                            "1944",
                            "1945",
                            "1946",
                            "1947",
                            "1948",
                            "1949",
                            "1950",
                            "1951",
                            "1952",
                            "1953",
                            "1954",
                            "1955",
                            "1956",
                            "1957",
                            "1958",
                            "1959",
                            "1960",
                            "1961",
                            "1962",
                            "1963",
                            "1964",
                            "1965",
                            "1966",
                            "1967",
                            "1968",
                            "1969",
                            "1970",
                            "1971",
                            "1972",
                            "1973",
                            "1974",
                            "1975",
                            "1976",
                            "1977",
                            "1978",
                            "1979",
                            "1980",
                            "1981",
                            "1982",
                            "1983",
                            "1984",
                            "1985",
                            "1986",
                            "1987",
                            "1988",
                            "1989",
                            "1990",
                            "1991",
                            "1992",
                            "1993",
                            "1994",
                            "1995",
                            "1996",
                            "1997",
                            "1998",
                            "1999",
                            "2000",
                            "2001",
                            "2002",
                            "2003",
                            "2004",
                            "2005",
                            "2006",
                            "2007",
                            "2008",
                            "2009",
                            "2010",
                            "2011",
                            "2012",
                            "2013",
                            "2014",
                            "2015",
                            "2016",
                            "2017",
                            "2018",
                            "2019",
                            "2020",
                            "2021",
                        ]
                        if len(awards_list) == 1:
                            pass
                        else:
                            for i in range(1, len(awards_list)):
                                if awards_list[i] in years_list:
                                    try:
                                        worksheet_award.write(
                                            actor_award_index,
                                            0,
                                            label=data_strcture["中文姓名:"],
                                        )
                                        worksheet_award.write(
                                            actor_award_index,
                                            1,
                                            label=data_strcture["英文姓名:"],
                                        )
                                        worksheet_award.write(
                                            actor_award_index, 2, label=awards_list[i]
                                        )
                                        worksheet_award.write(
                                            actor_award_index,
                                            3,
                                            label=awards_list[i + 1],
                                        )
                                        worksheet_award.write(
                                            actor_award_index,
                                            4,
                                            label=awards_list[i + 2],
                                        )
                                        try:
                                            worksheet_award.write(
                                                actor_award_index,
                                                5,
                                                label=awards_list[i + 3],
                                            )
                                        except:
                                            pass

                                        actor_award_index += 1
                                    except:
                                        pass

                        if actor_info_index % 100 == 0:
                            workbook_award.save(
                                "/Users/hm_cai/Desktop/归档/Actors_awards.xlsx"
                            )

                        # process best five
                        if len(best_five_list) == 0:
                            pass
                        else:
                            for i in range(0, len(best_five_list)):
                                if best_five_list[i] in years_list:
                                    try:
                                        worksheet_best_five.write(
                                            actor_best_index,
                                            0,
                                            label=data_strcture["中文姓名:"],
                                        )
                                        worksheet_best_five.write(
                                            actor_best_index,
                                            1,
                                            label=data_strcture["英文姓名:"],
                                        )
                                        worksheet_best_five.write(
                                            actor_best_index, 2, label=best_five_list[i]
                                        )
                                        worksheet_best_five.write(
                                            actor_best_index,
                                            3,
                                            label=best_five_list[i + 1],
                                        )
                                        actor_best_index += 1
                                    except:
                                        pass
                            if actor_info_index % 100 == 0:
                                workbook_best_five.save(
                                    "/Users/hm_cai/Desktop/归档/Actors_best_five.xlsx"
                                )

                        with open(
                            "/Users/hm_cai/Desktop/归档/record_info_index.txt", "a"
                        ) as recording:
                            recording.write("{}\n".format(fname))


if __name__ == "__main__":
    process_data()
