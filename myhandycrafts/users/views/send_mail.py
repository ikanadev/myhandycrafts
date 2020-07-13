
from rest_framework.views import APIView

import logging
import re
import os
import json
import datetime
import time
import email.message
import smtplib



class UserUserViewSet(APIView):

    def get(self):

                emailToSend = []
                emailToSend.append('example@gmail.com')
                emailToSend.append('example@gmail.com')
                emailToSend.append('example@gmail.com')
                try:
                    msg = email.message.Message()
                    msg['From'] = "<contacto@midominio.com>"
                    msg['To'] = ",".join(emailToSend)
                    msg['Subject'] = "FORMULARIO DE MI SITIO WEB"
                    body = """
                                <html>
                                    <head>
                                        <link href="https://fonts.googleapis.com/css?family=Goudy+Bookletter+1911|Share+Tech" rel="stylesheet">
                                    </head>
                                    <body style="margin: auto;
                                        width: fit-content!important;">
                                        <div style="padding: 10px;
                                        background: #1862ac;
                                        border-radius: 17px;">
                                        <div style="background-color: #fff; padding: 20px; border-radius: 10px;">
                                        <img style="text-align: center; max-width: 100%; border-radius: 30px; display: block; margin-left: auto; margin-right: auto;" src="https://cristopherav.files.wordpress.com/2015/10/email-icon.png"/>
                                        <h4 style="font-weight: 400;">
                                        Acabas de recibir un nuevo mensaje de contacto desde Mi Sitio Web con el siguiente contenido:
                                        </h4>
                                            <table style="width: 100%;">
                                                <tbody>
                                                   
                                                </tbody>
                                            </table>
                                            <p style="text-align: center;">--------------------------</p>
                                            <p style="text-align: center; font-size:12px">Mi sitio Web 2020 Derechos reservados.<br/><br/>
                                            Este correo es informativo, favor no responder a esta direccion de correo, ya que no se encuentra habilitada para recibir mensajes.</p>
                                        </div>
                                        </div> 
                                    </body>
                                </html>
                            """

                    msg.add_header('Content-Type', 'text/html')
                    msg.set_payload(body)

                    server = smtplib.SMTP("email-smtp.us-east-1.amazonaws.com", 587)
                    server.starttls()
                    server.login("usuario", "contraseña")
                    server.sendmail(msg['From'], emailToSend, msg.as_string())
                    server.quit()
                except Exception as e:
                    pass
                    # logger.error(e)

        content = {
            "success": True,
            "message": "OK.",
            "requestDate": datetime.datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S')
        }

        response = {
            "isBase64Encoded": False,
            "statusCode": 200,
            "body": json.dumps(content),
            "headers": {
                'content-Type': 'application/json',
                'charset': 'utf8',
                'Access-Control-Allow-Origin': '*'
            }
        }

        return response


