multiplier = 10000
symbol = "CUS"
newLine = []
deli = ""
symbol_name = ""
fin_month = ""
fin_year = ""
fin_day = ""
final_message = ""
year = ""
inst_code = ""
put_call = ""
output = 0

with open("input.txt") as f:
    try:
        for line in f:
            deli = line.split("|")
            for x in deli:
                if '202' in x:
                    y = x.split("=")
                    if y[0] == '202':
                        # print(y[0], y[1])
                        strike_p = y[1]
                        strike_price = float(strike_p)
                        output = strike_price * multiplier
                        output1 = int(output)
                        output2 = str(output1)
                        fin_output = output / 100
                        fin_output = int(fin_output)
                        fin_output = str(fin_output)
                        # print("fin", fin_output)
                if '55' in x:
                    z = x.split("=")
                    if z[0] == '55':
                        # print(z[0], z[1])
                        symbol_name = z[1];
                        symbol_name = str(symbol_name)
                        # print(symbol_name)
                if '201' in x:
                    b = x.split("=")
                    if b[0] == '201':
                        put_call = b[1]
                        if put_call == '1':
                            put_call = "CE"
                            if put_call == "CE":
                                put_call1 = "C"
                        elif put_call == '0':
                            put_call = "PE"
                            if put_call == "PE":
                                put_call1 = "P"
                        else:
                            print("data not found")
                    # print(b[0], put_call)
                if '541' in x:
                    c = x.split("=")
                    if c[0] == '541':
                        # print(c[0], c[1])
                        expiry_date = c[1]
                        n = 4
                        year = [(expiry_date[i:i + n]) for i in range(0, len(expiry_date), n)]
                        fin_year = year[0]
                        year_digit = [(fin_year[i:i + n]) for i in range(2, len(fin_year), n)]
                        year_digit1 = year_digit[0]
                        # print(year_digit1)
                        # print("year:-", fin_year)
                        n = 2
                        month = [(expiry_date[i:i + n]) for i in range(4, len(expiry_date), n)]
                        fin_month = month[0]
                        fin_month = str(fin_month)
                        if fin_month == '01':
                            fin_month = 'JAN'
                        elif fin_month == '02':
                            fin_month = 'FEB'
                        elif fin_month == '03':
                            fin_month = 'MAR'
                        elif fin_month == '04':
                            fin_month = 'APR'
                        elif fin_month == '05':
                            fin_month = 'MAY'
                        elif fin_month == '06':
                            fin_month = 'JUN'
                        elif fin_month == '07':
                            fin_month = 'JUL'
                        elif fin_month == '08':
                            fin_month = 'AUG'
                        elif fin_month == '09':
                            fin_month = 'SEP'
                        elif fin_month == '10':
                            fin_month = 'OCT'
                        elif fin_month == '11':
                            fin_month = 'NOV'
                        elif fin_month == '12':
                            fin_month = 'DEC'
                        else:
                            print("Month not found")
                    fin_day = month[1]
                    fin_day = str(fin_day)
                    # print("mon day", fin_month, fin_day)

                if '48' in x:
                    d = x.split("=")
                    if d[0] == '48':
                        # print(d[0], d[1])
                        inst_code = d[1]
                        # print("int code",inst_code)
                        final_message = symbol_name + year_digit1 + fin_month + output2 + put_call
                        detail = fin_year + put_call1 + fin_output
                        file1 = open("myfile.txt", 'a')
                        print("1,", final_message, ",", symbol, " OPT ", fin_month, " ", detail, ",HKEX,", inst_code,
                              ",", multiplier, ",262=CUS OPT ", fin_month, " ", detail,
                              "|263=1|264=0|265=1|266=Y|267=3|269=0|269=1|269=2|146=1|55=CUS|48=", inst_code,
                              "|207=HKEX|,", file=file1, sep='')
                        file1.close()

    except:
        pass
