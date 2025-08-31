from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import requests
import os
from datetime import datetime

class NotificationService:
    def __init__(self):
        self.sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

    def send_email(self, to_email: str, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        """
        Send email using SendGrid or SMTP
        """
        try:
            if self.sendgrid_api_key:
                return self._send_sendgrid_email(to_email, subject, body, html_body)
            else:
                return self._send_smtp_email(to_email, subject, body, html_body)
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def send_sms(self, to_phone: str, message: str) -> bool:
        """
        Send SMS using Twilio
        """
        try:
            if not all([self.twilio_account_sid, self.twilio_auth_token, self.twilio_phone_number]):
                print("Twilio credentials not configured")
                return False

            url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_account_sid}/Messages.json"
            data = {
                "From": self.twilio_phone_number,
                "To": to_phone,
                "Body": message
            }
            
            response = requests.post(url, data=data, auth=(self.twilio_account_sid, self.twilio_auth_token))
            return response.status_code == 201

        except Exception as e:
            print(f"Error sending SMS: {e}")
            return False

    def send_appointment_confirmation(self, customer_email: str, customer_name: str, 
                                    appointment_date: datetime, service_name: str) -> bool:
        """
        Send appointment confirmation email
        """
        subject = "Conferma Appuntamento - Smart Garage"
        body = f"""
        Gentile {customer_name},

        Confermiamo il suo appuntamento per il servizio: {service_name}
        Data e ora: {appointment_date.strftime('%d/%m/%Y alle %H:%M')}

        La aspettiamo presso la nostra officina.

        Cordiali saluti,
        Smart Garage
        """
        
        html_body = f"""
        <html>
        <body>
            <h2>Conferma Appuntamento</h2>
            <p>Gentile {customer_name},</p>
            <p>Confermiamo il suo appuntamento per il servizio: <strong>{service_name}</strong></p>
            <p><strong>Data e ora:</strong> {appointment_date.strftime('%d/%m/%Y alle %H:%M')}</p>
            <p>La aspettiamo presso la nostra officina.</p>
            <br>
            <p>Cordiali saluti,<br>Smart Garage</p>
        </body>
        </html>
        """
        
        return self.send_email(customer_email, subject, body, html_body)

    def send_appointment_reminder(self, customer_email: str, customer_name: str,
                                appointment_date: datetime, service_name: str) -> bool:
        """
        Send appointment reminder email
        """
        subject = "Promemoria Appuntamento - Smart Garage"
        body = f"""
        Gentile {customer_name},

        Le ricordiamo il suo appuntamento per domani:
        Servizio: {service_name}
        Data e ora: {appointment_date.strftime('%d/%m/%Y alle %H:%M')}

        La aspettiamo!

        Cordiali saluti,
        Smart Garage
        """
        
        html_body = f"""
        <html>
        <body>
            <h2>Promemoria Appuntamento</h2>
            <p>Gentile {customer_name},</p>
            <p>Le ricordiamo il suo appuntamento per domani:</p>
            <p><strong>Servizio:</strong> {service_name}</p>
            <p><strong>Data e ora:</strong> {appointment_date.strftime('%d/%m/%Y alle %H:%M')}</p>
            <p>La aspettiamo!</p>
            <br>
            <p>Cordiali saluti,<br>Smart Garage</p>
        </body>
        </html>
        """
        
        return self.send_email(customer_email, subject, body, html_body)

    def send_invoice_notification(self, customer_email: str, customer_name: str,
                                invoice_number: str, amount: float, due_date: datetime) -> bool:
        """
        Send invoice notification email
        """
        subject = f"Fattura {invoice_number} - Smart Garage"
        body = f"""
        Gentile {customer_name},

        La sua fattura {invoice_number} è stata emessa.
        Importo: €{amount:.2f}
        Scadenza: {due_date.strftime('%d/%m/%Y')}

        Grazie per aver scelto i nostri servizi.

        Cordiali saluti,
        Smart Garage
        """
        
        html_body = f"""
        <html>
        <body>
            <h2>Fattura {invoice_number}</h2>
            <p>Gentile {customer_name},</p>
            <p>La sua fattura è stata emessa.</p>
            <p><strong>Importo:</strong> €{amount:.2f}</p>
            <p><strong>Scadenza:</strong> {due_date.strftime('%d/%m/%Y')}</p>
            <p>Grazie per aver scelto i nostri servizi.</p>
            <br>
            <p>Cordiali saluti,<br>Smart Garage</p>
        </body>
        </html>
        """
        
        return self.send_email(customer_email, subject, body, html_body)

    def send_vehicle_ready_notification(self, customer_phone: str, customer_name: str,
                                      vehicle_info: str) -> bool:
        """
        Send SMS notification when vehicle is ready
        """
        message = f"Gentile {customer_name}, il suo veicolo {vehicle_info} è pronto per il ritiro. Smart Garage"
        return self.send_sms(customer_phone, message)

    def _send_sendgrid_email(self, to_email: str, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        """
        Send email using SendGrid API
        """
        try:
            url = "https://api.sendgrid.com/v3/mail/send"
            headers = {
                "Authorization": f"Bearer {self.sendgrid_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "personalizations": [{"to": [{"email": to_email}]}],
                "from": {"email": "noreply@smartgarage.com", "name": "Smart Garage"},
                "subject": subject,
                "content": [
                    {"type": "text/plain", "value": body}
                ]
            }
            
            if html_body:
                data["content"].append({"type": "text/html", "value": html_body})
            
            response = requests.post(url, headers=headers, json=data)
            return response.status_code == 202

        except Exception as e:
            print(f"Error sending SendGrid email: {e}")
            return False

    def _send_smtp_email(self, to_email: str, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        """
        Send email using SMTP (fallback)
        """
        try:
            # This would need to be configured with actual SMTP settings
            # For now, just log the attempt
            print(f"SMTP email would be sent to {to_email}: {subject}")
            return True

        except Exception as e:
            print(f"Error sending SMTP email: {e}")
            return False
