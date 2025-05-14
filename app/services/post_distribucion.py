import os, smtplib
from email.message import EmailMessage
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import SessionLocal
from app.core.config import settings
import pandas as pd
import mimetypes

SMTP_HOST = settings.SMTP_HOST
SMTP_PORT = settings.SMTP_PORT
SMTP_USER = settings.SMTP_USER
SMTP_PASS = settings.SMTP_PASS

def generar_csvs_y_enviar(id_usuarios: list[int]):
    db: Session = SessionLocal()

    for id_usuario in id_usuarios:
        correo = db.execute(
            text("SELECT correo_usuario FROM tbl_usuarios WHERE id_usuario = :id"),
            {"id": id_usuario}
        ).scalar()

        if not correo:
            continue

        registros = db.execute(
            text("""
                SELECT * FROM tbl_distri_mutaciones 
                WHERE id_usuario = :id AND fecha_distribucion = CURRENT_DATE
            """),
            {"id": id_usuario}
        ).fetchall()

        if not registros:
            continue

        filename = f"mutaciones_gestionar_{id_usuario}.xlsx"
        filepath = os.path.join("temp", filename)
        os.makedirs("temp", exist_ok=True)

        # Convertir registros a DataFrame y guardar como Excel
        df = pd.DataFrame([dict(row._mapping) for row in registros])
        df.to_excel(filepath, index=False)

        """
        filename = f"mutaciones_gestionar_{id_usuario}.csv"
        filepath = os.path.join("temp", filename)
        os.makedirs("temp", exist_ok=True)

        with open(filepath, "w", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(registros[0]._mapping.keys())     # encabezados
            for row in registros:
                writer.writerow(row._mapping.values())        # valores
        """


        enviar_email(correo, filepath, id_usuario)

    db.close()


def enviar_email(destinatario, archivo_adj, id_usuario):
    db: Session = SessionLocal()
    total_registros = db.execute(
        text("""
            SELECT COUNT(*) FROM tbl_distri_mutaciones 
            WHERE id_usuario = :id AND fecha_distribucion = CURRENT_DATE
        """),
        {"id": id_usuario}
    ).scalar()
    
    datos_naturaleza = db.execute(
        text("""
            SELECT cod_naturaleza_juridica, naturaleza_juridica, COUNT(*) as cantidad
            FROM tbl_distri_mutaciones
            WHERE id_usuario = :id AND fecha_distribucion = CURRENT_DATE
            GROUP BY cod_naturaleza_juridica, naturaleza_juridica
            ORDER BY cantidad DESC
        """),
        {"id": id_usuario}
    ).fetchall()

    tabla_datos = ""
    for fila in datos_naturaleza:
        tabla_datos += f"<tr><td style='border: 1px solid #ccc; padding: 8px;'>{fila.cod_naturaleza_juridica}</td>"
        tabla_datos += f"<td style='border: 1px solid #ccc; padding: 8px;'>{fila.naturaleza_juridica}</td>"
        tabla_datos += f"<td style='border: 1px solid #ccc; padding: 8px; text-align: center;'>{fila.cantidad}</td></tr>"

    db.close()

    cuerpo_html = f"""
    <html>
    <body>
        <table align="center" width="600" style="font-family: Arial, sans-serif; border-collapse: collapse; border: 1px solid #ccc;">
            <tr>
                <td style="background-color: #00a8e8; padding: 15px; text-align: center;">
                    <table align="center" style="border-collapse: collapse;">
                        <tr>
                            <td style="vertical-align: middle; padding-right: 10px;">
                                <img src="https://cdnwordpresstest-f0ekdgevcngegudb.z01.azurefd.net/es/wp-content/themes/theme_alcaldia/logos/logo_footer.png" 
                                    alt="Logo" width="60" height="50">
                            </td>
                            <td style="vertical-align: middle;">
                                <a href="https://www.medellin.gov.co/es/secretaria-gestion-y-control-territorial/" 
                                style="color: #0033cc; font-size: 18px; text-decoration: none; font-weight: bold;">
                                    Secretaria de Gestión y Control Territorial
                                </a>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr>
                <td style="padding: 20px; text-align: left;">
                    <p style="font-size: 16px;"><a href="#" style="text-decoration: underline;">Hola!</a></p>
                    <p>Adjunto encontrarás el archivo con las matrículas que debes gestionar.</p>
                    <p><a href="#" style="text-decoration: underline;">Total</a> registros: {total_registros}</p>

                    <br>
                    <p style="font-size: 16px;"><strong>Registros por Naturaleza Jurídica</strong></p>
                    <table width="100%" style="border-collapse: collapse; font-family: Arial, sans-serif; font-size: 14px;">
                        <thead>
                            <tr style="background-color: #f2f2f2;">
                                <th style="border: 1px solid #ccc; padding: 8px;">Código</th>
                                <th style="border: 1px solid #ccc; padding: 8px;">Naturaleza Jurídica</th>
                                <th style="border: 1px solid #ccc; padding: 8px;">Cantidad Registros</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tabla_datos}
                        </tbody>
                    </table>
                </td>
            </tr>
            <tr>
                <td style="background:#333333;color:white;padding:10px;text-align:center;font-size:10px;">
                    Equipo de Apoyo a los Sistemas de Información Catastral<br>
                    Business Plaza, Calle 44a No 55-44, Piso 14<br>
                    Subsecretaría de Catastro
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    cuerpo_html_old = f"""
    <html>
    <body>
        <table align="center" width="600" style="font-family: Arial, sans-serif; border-collapse: collapse; border: 1px solid #ccc;">
            <tr>
                <td style="background-color: #00a8e8; padding: 15px; text-align: center;">
                    <table align="center" style="border-collapse: collapse;">
                        <tr>
                            <td style="vertical-align: middle; padding-right: 10px;">
                                <img src="https://cdnwordpresstest-f0ekdgevcngegudb.z01.azurefd.net/es/wp-content/themes/theme_alcaldia/logos/logo_footer.png" 
                                    alt="Logo" width="60" height="50">
                            </td>
                            <td style="vertical-align: middle;">
                                <a href="https://www.medellin.gov.co/es/secretaria-gestion-y-control-territorial/" 
                                style="color: #0033cc; font-size: 18px; text-decoration: none; font-weight: bold;">
                                    Secretaria de Gestión y Control Territorial
                                </a>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr>
                    <td style="padding: 20px; text-align: left;">
                    <p style="font-size: 16px;"><a href="#" style="text-decoration: underline;">Hola!</a></p>
                    <p>Adjunto encontrarás el archivo con las matrículas que debes gestionar.</p>
                    <p><a href="#" style="text-decoration: underline;">Total</a> registros: {total_registros}</p>
                </td>
            </tr>
            <tr>
                <td style="background:#333333;color:white;padding:10px;text-align:center;font-size:10px;">
                    Equipo de Apoyo a los Sistemas de Información Catastral<br>
                    Business Plaza, Calle 44a No 55-44, Piso 14<br>
                    Subsecretaría de Catastro
                </td>
            </tr>
        </table>
    </body>
    </html>
""" 

    msg = EmailMessage()
    msg["Subject"] = f"Mutaciones asignadas - Usuario {id_usuario}"
    msg["From"] = settings.SMTP_USER
    msg["To"] = destinatario #"nancymaya80@gmail.com"

    msg.set_content("Este correo contiene información en formato HTML.")
    msg.add_alternative(cuerpo_html, subtype="html")

    with open(archivo_adj, "rb") as f:
        contenido = f.read()
        mime_type, _ = mimetypes.guess_type(archivo_adj)
        maintype, subtype = mime_type.split("/")
        msg.add_attachment(contenido, maintype=maintype, subtype=subtype, filename=os.path.basename(archivo_adj))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)

 