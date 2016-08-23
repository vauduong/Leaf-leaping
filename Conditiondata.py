import picamera 
from gpiozero import Button
from PIL import Image
import os, sys
import math
import Adafruit_DHT
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart



other = 0
orange = 0
leafRatio= 0.0
temp = 0
humid =0
timesRun = 0
button = Button(5)
toAdd = ""
haveLeavesStatus = ""
tooColdStatus = ""
tooDampStatus = ""

#rgb to hsv conversion from Michael Fogleman on activestate code
def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:

        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v

def pictureAnalysis():
    camera = picamera.PiCamera()
    camera.resolution=(120,120)
    camera.capture('/home/pi/BUILDIT/unmodified.jpg')

    print ("Unmodified image captured")

    img = Image.open('/home/pi/BUILDIT/unmodified.jpg')
    img = img.convert("RGBA")

    datas = img.getdata()

    global orange
    global other
    global leafRatio
    global haveLeavesStatus
   
    #Modified "Using pil to make all white pixels transparent" code from cr333 on stackoverflow, shows which pixels are orange in new image called Modified.jpg
    newData = []
    for item in datas:
        if (((rgb2hsv(item[0], item[1], item[2]))[0]) <70)  and (((rgb2hsv(item[0], item[1], item[2]))[2])>0.7):
            newData.append((255, 255, 255, 0))
            orange = orange + 1
        else:
            newData.append((0,0,0,0))
            other = other + 1

    img.putdata(newData)
    img.save("/home/pi/BUILDIT/modified.jpg", "JPEG")

    print("modified image created")
    leafRatio = float(orange/other)
    if (leafRatio > 0.3):
        haveLeavesStatus = "YES"
    else:
        haveLeavesStatus = "NO"
        

    print ("orange =" + str(orange))
    print ("other =" + str(other))
    print ("leafRatio =" + str(leafRatio))
    print ("haveLeaves =" + str(haveLeavesStatus))


def temperatureAnalysis():
    global temp
    global humid
    global tooColdStatus
    global tooDampStatus
    print("getting DHT")
    #Humidity code from Adafruit website

    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)

    # Un-comment the line below to convert the temperature to Fahrenheit.
    # temperature = temperature * 9/5.0 + 32

    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).  
    # If this happens try again!

    if humidity is not None and temperature is not None:
            print 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
            temp = float(temperature)
            humid = float(humidity)
            if(temp> 20.0):
                tooColdStatus = "NO"
            else:
                tooColdStatus = "YES"

            if(humid> 50.0):
                tooDampStatus = "YES"
            else:
                tooDampStatus = "NO"

            print("Too cold? " + tooColdStatus)
            print("Too Damp? " + tooDampStatus)
    else:
            print 'Failed to get reading. Try again!'

    


#sending email code modified from Gaven MacDonald on youtube and user1292828 on stackoverflow
def sendEmail():
    global orange
    global other
    global toAdd
    global tooColdStatus
    global tooDampStatus
    global leafRatio
    global haveLeavesStatus
    smtpUser = 'wyleafleapers@gmail.com'
    smtpPass = '***************************'
         
    fromAdd = smtpUser

    subject = 'Leaf Data'
    header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
    body = 'Concentration data:' + '\n' + "orange =" + str(orange) + '\n' + "other =" + str(other) + '\n' + "leaf ratio =" + str(leafRatio) + '\n' + "temp= " + str(temp) + " humidity=" + str(humid) + '\n' + "Enough Leaves? " + str(haveLeavesStatus) + '\n' + "Too cold? " + str(tooColdStatus) + '\n' + "Too damp? " + str(tooDampStatus)
    

    msg = MIMEMultipart()
    text = MIMEText(str(body))
    msg.attach(text)
    img_data= open('/home/pi/BUILDIT/modified.jpg', 'rb').read()
    image = MIMEImage(img_data, name=os.path.basename('/home/pi/BUILDIT/modified.jpg'))
    msg.attach(image)
    img_data = open('/home/pi/BUILDIT/unmodified.jpg', 'rb').read()
    image2 = MIMEImage(img_data, name=os.path.basename('/home/pi/BUILDIT/unmodified.jpg'))
    msg.attach(image2)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    print("Sent Email to: " + str(toAdd))

    s.ehlo()
    s.starttls()
    s.ehlo()

    s.login(smtpUser, smtpPass)
    s.sendmail(fromAdd, toAdd, msg.as_string())

    s.quit()

def action():      
    orange = 0
    other = 0
    global button
    print ("waiting for press")

    button.wait_for_press()
    print ("Scanning...")
    pictureAnalysis()
    temperatureAnalysis()
    sendEmail()

def restart():
    global timesRun
    global toAdd
    restart = raw_input("would you like to run again? Press y if so or n to exit."  + '\n')
    if restart == "n":
       sys.exit("Goodbye, thank you!")
    if restart == "y":
        timesRun = timesRun + 1 
        script()
    else:
        print("please type y or n")
        restart()
        
def script():
    global toAdd
    global timesRun
    if(timesRun < 1):
        toAdd = str(raw_input("Please enter email address: "))
        action()
    else:
        address = raw_input("Same email? Press y if so or n to enter new email." + '\n')
        if address == "n":
            toAdd = str(raw_input("Please enter email address: "))
        action()

    restart()
       
            
    



script()
input("press any key to close the window")
