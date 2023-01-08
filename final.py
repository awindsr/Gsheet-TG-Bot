import telegram
import requests
import json
from telegram.ext import Application, CommandHandler
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Credentials
# Replace TOKEN with your bot's API token
tok = "5846355924:AAG00YOmBunjEs9jWNSwQBkf6zX_3b3maII"
bot = telegram.Bot(token=tok)

#student's list according to roll number
namelist = "1.Adithya P Binu, 2.Adithya Raj, 3.ADITHYAN BIJU, 4.ADVAIT ARJIT S, 5.AGNUS JOSE, 6.ALAN K B, 7.ALAN LEEJOY, 8.ALEENA V SUNIL, 9.ALEN JOJIMON10, 10.Alen Siju Mudakodil, 11.ALENE ELSA JOSE, 12.ALTHAF RAHMAN, 13.ALWIN JIMMY THOMAS, 14.Amal Joy, 15.ANITA MARY JOSEPH, 16.Anumol V S, 17.Anush S Kumar, 18.AwinDas R, 19.BAINA ELSA BIJU, 20.Basil Vazhathottathil, 21.Bijal T Benny, 22.CHRIS REJI KURIAKOSE, 23.Devika Rajeev, 24.Diya Benny, 25.DONEY SIBY, 26.Elna S Bijo, 27.Emitta Mathew, 28.FAHAD RASHEED, 29.FELIX JOBI, 30.GITHIN CIRIL, 31.Gowrikrishna C, 32.JEEVA GEORGE SEBASTIAN, 33.Jeswin Jose, 34.Jeswin sabu, 35.Jibin Gigi, 36.JISMI SAJU, 37.JO SAJI, 38.Jose Thomas, 39.Kevin Biju Kulangara, 40.LIDIYA REJU, 41.Manu Emmanuel, 42.Maria Rose Alex, 43.Muhammed farhan, 44.NAGARAJ MENON K S, 45.Nandagopan L, 46.Naveen Ajesh, 47.Neha Maria Joji, 48.Nikita Ajay, 49.NYGIL JOHNS JOY, 50.Parvathi KB, 51.PRAPANCH J, 52.Praveen Rajan, 53.REVATHY BIJU, 54.RICHARD M MATHEW, 55.Rony Sebastian Tomson, 56.Sarya Sajeev, 57.Sharon Sell Norbert, 58.SHRAYA S SANTHOSH, 59.Siya Varghese, 60.Stephin Mathew, 61.STEVE MARAUTHOOR THOMAS, 62.THOMAS MATHEW, 63.THOMAS VARGHESE"
entry = namelist.split(", ")


# Set up the Google Sheets API client
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet
sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1IYtdwxk0QN8YVFY-01BWUBQ3uiFYw76nbj-RjrVRsOY/edit#gid=2009057025').sheet1

chatidlist = [576071770]
value_list = []
def getValues():
    response = requests.get("https://api.telegram.org/bot5846355924:AAG00YOmBunjEs9jWNSwQBkf6zX_3b3maII/getUpdates")
    update_Dict = json.loads(response.text)
    chatid = update_Dict["result"][-1]["message"]["from"]["id"]
    username = update_Dict["result"][-1]["message"]["from"]["username"]
    text = update_Dict["result"][-1]["message"]["text"]
    value_list = [chatid, username, text]
    return value_list


def accesscontrol():
    values = getValues()
    chat_id = values[0]
    if chat_id in chatidlist:
        return True
    else:
        requests.get(url=f"https://api.telegram.org/bot5846355924:AAG00YOmBunjEs9jWNSwQBkf6zX_3b3maII/sendMessage?chat_id={chat_id}&text=Unauthorised Access")
        return False

def extractupdateID(url, bot):
    url = "" #extract text from telegram bot's update URL

    if accesscontrol() == True:
        values = getValues()
        text = values[2]
        chat_id = values[0]
        username = values[1]
        message =f'Hi, {username} \n 🔹Use "/add row col data" to add data \n 🔹use "/list" to list all student names with roll number \n 🔹use "/check rollnumber" to list the entries of a student. \n'
        requests.get(url=f"https://api.telegram.org/bot5846355924:AAG00YOmBunjEs9jWNSwQBkf6zX_3b3maII/sendMessage?chat_id={chat_id}&text={message}")
        return text
    else:
        return

def handle_text(bot, text):
    # Get the input text and split it into the cell coordinates and the cell value
    if accesscontrol() == True:
        url = ""
        values = getValues()
        input_text = values[2]
        chat_id = values[0]

        input_parts = input_text.split(' ')

        row = int(input_parts[1]) + 1
        col = int(input_parts[2])
        data = input_parts[3]
        val = sheet.cell(row, 1).value
        studentName = val
        
        print(row, col, data)
        # Write the value to the specified cell
        sheet.update_cell(row, col, data)

        # Send a confirmation message
        msg_text = f"Successfully updated {studentName}'s data."
        send_message = requests.get(url=f"https://api.telegram.org/bot5846355924:AAG00YOmBunjEs9jWNSwQBkf6zX_3b3maII/sendMessage?chat_id={chat_id}&text={msg_text}")
    else:
        return
def checkEntry(num, rownum): #Get details about a student
    if accesscontrol() == True:
        url = ""
        values = getValues()
        input_text = values[2]
        chat_id = values[0]
        input_parts = input_text.split(' ')
        row = int(input_parts[1]) + 1
        studentEntries = sheet.row_values(row)
        entry_list = []
        for i in range(1, len(studentEntries)):
            name = studentEntries[0]
            entry = studentEntries[i]
            entry_list.append(entry)
        print(entry_list)
        entry_line = "\n".join(entry_list)
        student_details = f'{name} \n{entry_line}'
        send_message = requests.get(url=f"https://api.telegram.org/bot5846355924:AAG00YOmBunjEs9jWNSwQBkf6zX_3b3maII/sendMessage?chat_id={chat_id}&text={student_details}")
    else: 
        return

def rollList(list, rolllist): #get roll number list
    if accesscontrol() == True:
        values = getValues()
        chat_id = values[0]
        rolllist = "\n".join(entry)
        send_message = requests.get(url=f"https://api.telegram.org/bot5846355924:AAG00YOmBunjEs9jWNSwQBkf6zX_3b3maII/sendMessage?chat_id={chat_id}&text={rolllist}")
    else:
        return
# # Set the bot to listen for messages that start with the '/add' command
application = Application.builder().token(tok).build()
application.add_handler(CommandHandler('start', extractupdateID))
application.add_handler(CommandHandler('add', handle_text))
application.add_handler(CommandHandler('list', rollList))
application.add_handler(CommandHandler('check', checkEntry))
application.run_polling()