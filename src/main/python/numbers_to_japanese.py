# https://github.com/Greatdane/Convert-Numbers-to-Japanese
# Japanese Number Converter
# currently using length functions - possible to use Recursive Functions?
# Works only up to sen man for now (9 digits)
# Now includes Kanji to arabic numbers, WIP

romaji_dict = {"0": "zero", "1": "ichi", "2": "ni", "3": "san", "4": "yon", "5": "go", "6": "roku", "7": "nana",
               "8": "hachi", "9": "kyuu", "10": "juu", "100": "hyaku", "1000": "sen", "10000": "man",
               "100000000": "oku",
               "300": "sanbyaku", "600": "roppyaku", "800": "happyaku", "3000": "sanzen", "8000": "hassen"}

kanji_dict = {"0": "零", "1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "七",
              "8": "八", "9": "九", "10": "十", "100": "百", "1000": "千", "10000": "万", "100000000": "億",
              "300": "三百", "600": "六百", "800": "八百", "3000": "三千", "8000": "八千"}

hiragana_dict = {"0": "ゼロ", "1": "いち", "2": "に", "3": "さん", "4": "よん", "5": "ご", "6": "ろく", "7": "なな",
                 "8": "はち", "9": "きゅう", "10": "じゅう", "100": "ひゃく", "1000": "せん", "10000": "まん", "100000000": "おく",
                 "300": "さんびゃく", "600": "ろっぴゃく", "800": "はっぴゃく", "3000": "さんぜん", "8000": "はっせん"}


def len_one(convert_num, requested_dict):
    # Returns single digit conversion, 0-9
    return requested_dict[convert_num]


def len_two(convert_num, requested_dict):
    # Returns the conversion, when number is of length two (10-99)
    if convert_num[0] == "0":  # if 0 is first, return len_one
        return len_one(convert_num[1], requested_dict)
    if convert_num == "10":
        return requested_dict["10"]  # Exception, if number is 10, simple return 10
    if convert_num[0] == "1":  # When first number is 1, use ten plus second number
        return requested_dict["10"] + " " + len_one(convert_num[1], requested_dict)
    elif convert_num[1] == "0":  # If ending number is zero, give first number plus 10
        return len_one(convert_num[0], requested_dict) + " " + requested_dict["10"]
    else:
        num_list = []
        for x in convert_num:
            num_list.append(requested_dict[x])
        num_list.insert(1, requested_dict["10"])
        # Convert to a string (from a list)
        output = ""
        for y in num_list:
            output += y + " "
        output = output[:len(output) - 1]  # take off the space
        return output


def len_three(convert_num, requested_dict):
    # Returns the conversion, when number is of length three (101-999)
    num_list = []
    if convert_num[0] == "1":
        num_list.append(requested_dict["100"])
    elif convert_num[0] == "3":
        num_list.append(requested_dict["300"])
    elif convert_num[0] == "6":
        num_list.append(requested_dict["600"])
    elif convert_num[0] == "8":
        num_list.append(requested_dict["800"])
    else:
        num_list.append(requested_dict[convert_num[0]])
        num_list.append(requested_dict["100"])
    if convert_num[1:] == "00" and len(convert_num) == 3:
        pass
    else:
        if convert_num[1] == "0":
            num_list.append(requested_dict[convert_num[2]])
        else:
            num_list.append(len_two(convert_num[1:], requested_dict))
    output = ""  # convert to a string (from a list)
    for y in num_list:
        output += y + " "
    output = output[:len(output) - 1]  # take off the space
    return output


def len_four(convert_num, requested_dict):
    # Returns the conversion, when number is of length four (1001-9999)
    num_list = []
    # First, check for zeros (and get deal with them)
    if convert_num == "0000":
        return ""
    while convert_num[0] == "0":
        convert_num = convert_num[1:]
    if len(convert_num) == 1:
        return len_one(convert_num, requested_dict)
    elif len(convert_num) == 2:
        return len_two(convert_num, requested_dict)
    elif len(convert_num) == 3:
        return len_three(convert_num, requested_dict)
    # If no zeros, do the calculation
    else:
        if convert_num[0] == "1":
            num_list.append(requested_dict["1000"])
        elif convert_num[0] == "3":
            num_list.append(requested_dict["3000"])
        elif convert_num[0] == "8":
            num_list.append(requested_dict["8000"])
        else:
            num_list.append(requested_dict[convert_num[0]])
            num_list.append(requested_dict["1000"])
        if convert_num[1:] == "000" and len(convert_num) == 4:
            pass
        else:
            if convert_num[1] == "0":
                num_list.append(len_two(convert_num[2:], requested_dict))
            else:
                num_list.append(len_three(convert_num[1:], requested_dict))
        output = ""
        for y in num_list:
            output += y + " "
        output = output[:len(output) - 1]
        return output


def len_x(convert_num, requested_dict):
    # Returns everything else.. (up to 9 digits!)
    num_list = []
    if len(convert_num[0:-4]) == 1:
        num_list.append(requested_dict[convert_num[0:-4]])
        num_list.append(requested_dict["10000"])
    elif len(convert_num[0:-4]) == 2:
        num_list.append(len_two(convert_num[0:2], requested_dict))
        num_list.append(requested_dict["10000"])
    elif len(convert_num[0:-4]) == 3:
        num_list.append(len_three(convert_num[0:3], requested_dict))
        num_list.append(requested_dict["10000"])
    elif len(convert_num[0:-4]) == 4:
        num_list.append(len_four(convert_num[0:4], requested_dict))
        num_list.append(requested_dict["10000"])
    elif len(convert_num[0:-4]) == 5:
        num_list.append(requested_dict[convert_num[0]])
        num_list.append(requested_dict["100000000"])
        num_list.append(len_four(convert_num[1:5], requested_dict))
        if convert_num[1:5] == "0000":
            pass
        else:
            num_list.append(requested_dict["10000"])
    else:
        return ("Not yet implemented, please choose a lower number.")
    num_list.append(len_four(convert_num[-4:], requested_dict))
    output = ""
    for y in num_list:
        output += y + " "
    output = output[:len(output) - 1]
    return output


def convert(convert_num, requested_dict):
    # Check lengths and convert accordingly
    if len(convert_num) == 1:
        convert_result = len_one(convert_num, requested_dict)
        return (convert_result)
    elif len(convert_num) == 2:
        convert_result = len_two(convert_num, requested_dict)
        return (convert_result)
    elif len(convert_num) == 3:
        convert_result = len_three(convert_num, requested_dict)
        return (convert_result)
    elif len(convert_num) == 4:
        convert_result = len_four(convert_num, requested_dict)
        return (convert_result)
    else:
        convert_result = len_x(convert_num, requested_dict)
        return (convert_result)


def remove_spaces(convert_result):
    # Remove spaces in Hirigana and Kanji results
    correction = ""
    for x in convert_result:
        if x == " ":
            pass
        else:
            correction += x
    return correction


def kanjiConvert(convert_num):
    # Converts kanji to arabic number

    if convert_num == "零":
        return 0

    # First, needs to check for MAN 万 and OKU 億 kanji, as need to handle differently, splitting up the numbers at these intervals.
    # key tells us whether we need to add or multiple the numbers, then we create a list of numbers in an order we need to multipy/add
    key = []
    numberList = []
    y = ""
    for x in convert_num:
        if x == "万" or x == "億":
            numberList.append(y)
            key.append("times")
            numberList.append(x)
            key.append("plus")
            y = ""
        else:
            y += x
    if y != "":
        numberList.append(y)

    numberListConverted = []
    baseNumber = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
    linkNumber = ["十", "百", "千", "万", "億"]

    # Converts the kanji number list to arabic numbers, using the 'base number' and 'link number' list above. For a link number, we would need to
    # link with a base number
    for noX in numberList:
        count = len(noX)
        result = 0
        skip = 1
        for x in reversed(noX):
            addTo = 0
            skip -= 1
            count = count - 1
            if skip == 1:
                continue
            if x in baseNumber:
                for y, z in kanji_dict.items():
                    if z == x:
                        result += int(y)
            elif x in linkNumber:
                if noX[count - 1] in baseNumber and count > 0:
                    for y, z in kanji_dict.items():
                        if z == noX[count - 1]:
                            tempNo = int(y)
                            for y, z in kanji_dict.items():
                                if z == x:
                                    addTo += tempNo * int(y)
                                    result += addTo
                                    skip = 2
                else:
                    for y, z in kanji_dict.items():
                        if z == x:
                            result += int(y)
        numberListConverted.append(int(result))

    result = numberListConverted[0]
    y = 0

    # iterate over the converted list, and either multiply/add as instructed in key list
    for x in range(1, len(numberListConverted)):
        if key[y] == "plus":
            try:
                if key[y + 1] == "times":
                    result = result + numberListConverted[x] * numberListConverted[x + 1]
                    y += 1
                else:
                    result += numberListConverted[x]
            except IndexError:
                result += numberListConverted[-1]
                break
        else:
            result = result * numberListConverted[x]
        y += 1

    return result


def convert_to_japanese(convert_num):
    convert_result_kanji = convert(convert_num, kanji_dict)
    convert_result_kanji = remove_spaces(convert_result_kanji)
    convert_result_hiragana = convert(convert_num, hiragana_dict)
    convert_result_hiragana = remove_spaces(convert_result_hiragana)
    return convert_result_kanji, convert_result_hiragana
    # print("Kanji: " + convert_result)
    # Hiragana
    # requested_dict = hiragana_dict
    # convert_result = convert(convert_num)
    # convert_result = remove_spaces(convert_result)
    # print("Hiragana: " + convert_result)
    # # Romaji
    # requested_dict = romaji_dict
    # print("Romaji: " + convert(convert_num))
