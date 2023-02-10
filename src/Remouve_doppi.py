def remouve_doppi (result):
    for i in range(len(result)-1):
        if result[i].text == result[i+1].text:
            result.pop(i)
