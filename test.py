def get_correct_page_range(primary_category, length):
    page_list = []
    if primary_category == "Talmud":
        last_num = 0
        for num in range(2, int(length+2)//2+1):
            last_num = num
            page_list.append(str(num)+'a')
            page_list.append(str(num) + 'b')
        if length % 2 != 0:
            page_list.append(str(last_num+1) + 'a')

        print(len(page_list))


get_correct_page_range("Talmud", 125)