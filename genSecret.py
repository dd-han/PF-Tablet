import pyotp
import pyqrcode

secretKeyComment = "Hakurei"

secretKey = pyotp.random_base32()
print("Your Securet Key is "+secretKey)

url = pyqrcode.create('otpauth://totp/'+secretKeyComment+'?secret='+secretKey)
print(url.terminal(quiet_zone=1))

