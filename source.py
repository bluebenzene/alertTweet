import gtts
import subprocess
def play(file_name):
    proc = subprocess.Popen(["play", f"alert_sound/{file_name}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate()
text ='DECRYPT: Bitcoin Tipping Service Damus Gets Booted From Apple App Store'
sound = gtts.gTTS(text,lang='en',tld='us')
sound.save("alert_sound/textaudio.mp3")
file_name = 'textaudio.mp3'
play(file_name)
