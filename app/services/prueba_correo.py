import yagmail

yag = yagmail.SMTP(user='equipocatastroapp@gmail.com', password='augamwpnyffiixsn')

cuerpo_html = f"""
<html>
<body>
</body>
</html>
"""
archivo_adj=""
yag.send(
    to="john_goez82192@elpoli.edu.co",
    subject="Perrito",
    contents=[cuerpo_html, archivo_adj]
)
