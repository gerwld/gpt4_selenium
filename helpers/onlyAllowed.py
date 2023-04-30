values = list(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")


def onlyAllowed(my_string=""):
    for item in my_string:
        if item not in values:
            my_string = my_string.replace(item, "")
    return my_string
