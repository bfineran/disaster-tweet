import phonenumbers

x = phonenumbers.parse("my number is 2155949300 shit", "US")
numberstr = str(x)
idx = numberstr.find("National Number: ")
realnumber = numberstr[(idx+17):(idx+17+10)]

print realnumber