from smbus import SMBus
import time
import sqlite3 as sqlite

# I2C globals
ADDR = 0x27
bus = SMBus(1)


deg = u'\N{DEGREE SIGN}'

# sqlite config
# CREATE TABLE temp_humidity(id INTEGER primary key, datetime DATETIME DEFAULT CURRENT_TIMESTAMP, temp_c REAL NOT NULL, temp_f REAL NOT NULL, humidity INTEGER NOT NULL);
sqliteCon = sqlite.connect('temp.db')


# Main loop
while True:
    # Get the current system date and time
    datetime = time.strftime('%m/%d/%Y %H:%M:%S')

    # Read data from sensor
    bus.write_byte(ADDR, 0x00)
    ans = bus.read_i2c_block_data(ADDR, 0x00, 4)

    # Convert to human readable humdidity
    humidity = ((ans[0] & 0x3f) << 8) + ans[1]
    humidity = humidity * float('6.10e-3')
    humidity = '{:.0f}'.format(humidity)

    # Convert to human readable temperature
    tempC = (ans[2] << 8) + ans[3]
    tempC = tempC >> 2
    tempC = (tempC * float('1.007e-2')) - 40
    tempF = (tempC * 1.8) + 32

    #insert into SQLITE database
    cursor = sqliteCon.cursor()
    cursor.execute("INSERT INTO temp_humidity (datetime, temp_c, temp_f, humidity) VALUES (?, ?, ?, ?)", (time.strftime('%Y-%m-%dT%H:%M:%S'), tempC, tempF, humidity))
    sqliteCon.commit()

    tempC_formatted = '{:.1f}'.format(tempC)
    tempF_formatted = '{:.1f}'.format(tempF)



    # print
    print datetime
    print 'Temperature: ' + str(tempC_formatted) + deg + 'C'
    print 'Temperature: ' + str(tempF_formatted) + deg + 'F'
    print 'Humidity: ' + str(humidity) + '%'
    print ''

    time.sleep(60)

