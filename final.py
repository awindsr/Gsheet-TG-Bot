import telegram
import requests
import json
from telegram.ext import Application, CommandHandler
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Credentials
# Replace TOKEN with your bot's API token
tok = ""
bot = telegram.Bot(token=tok)

#student's list according to roll number
namelist = ""
entry = namelist.split(", ")


# Set up the Google Sheets API client
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('./credentials.json', scope)
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
        message =f'Hi, {username} \n 🔹Use "/add row col data" to add data \n 🔹use "/list" to list all student names with roll number \n 🔹use "/check rollnumber" to list the entries of a student \n 🔹use "/del row col" to delete the data of a student \n 🔹use "/total collected col" to get total amount collected for a specific need.'
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

def delete(row, col):
    if accesscontrol() == True:
        values = getValues()
        input_text = values[2]
        chat_id = values[0]

        input_parts = input_text.split(' ')

        row = int(input_parts[1]) + 1
        col = int(input_parts[2])
        val = sheet.cell(row, 1).value
        col_head = sheet.cell(1, col).value
        studentName = val
        sheet.update_cell(row, col, '')

        msg = f"Successfully deleted {studentName}'s entry of {col_head}."
        send_message = requests.get(url=f"https://api.telegram.org/bot5846355924:AAG00YOmBunjEs9jWNSwQBkf6zX_3b3maII/sendMessage?chat_id={chat_id}&text={msg}")

def total(row, col):
    values = getValues()
    input_text = values[2]
    chat_id = values[0]

    input_parts = input_text.split(' ')
    row = 65
    col = int(input_parts[2])
    val = sheet.cell(row, col).value
    col_head = sheet.cell(1, col).value
    msg = f'total amount collected till now for {col_head} is Rs: {val}.'
    send_message = requests.get(url=f"https://api.telegram.org/bot5846355924:AAG00YOmBunjEs9jWNSwQBkf6zX_3b3maII/sendMessage?chat_id={chat_id}&text={msg}")

# # Set the bot to listen for messages that start with the '/add' command
application = Application.builder().token(tok).build()
application.add_handler(CommandHandler('start', extractupdateID))
application.add_handler(CommandHandler('add', handle_text))
application.add_handler(CommandHandler('list', rollList))
application.add_handler(CommandHandler('check', checkEntry))
application.add_handler(CommandHandler('del', delete))
application.add_handler(CommandHandler('total', total))
application.run_polling()