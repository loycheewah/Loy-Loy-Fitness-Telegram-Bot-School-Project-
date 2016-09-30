import math
import time as Time
import os
import datetime
import xml.etree.ElementTree as ET
import asyncio
import telepot.aio
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from dotenv import load_dotenv, find_dotenv

class MessageCounter(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count_i = self._count_j = self._count_k = 0
        self._user_id = 0
        self._firstname = ""
        self._filename = ""
        self._age = 0
        self._gender = ""
        self._height = 0
        self._weight = 0.0
        self._filestring = ""
        self._list1 = []
        self._list2 = []
        self._list3 = []
        self._list4 = []
        self._elementnumber = 0
        self._exercisename = ""
        self._exercisecalories = 0.0
        self._exercisetime = 0.0

    async def on_chat_message(self, msg):
        print("Received from id ", msg['from']['id'], " ", msg['chat']['type'], " : ", msg['text'])

        self._user_id = msg['from']['id']
        self._firstname = msg['from']['first_name']
        self._filename = str(self._user_id) + '.xml'


        '''''
        Basic interaction with user
        '''''
        # Basic interfacing with user_start
        if(msg['text'] == "Okay! Let's start :)"):
            if(os.path.isfile(self._filename)):
                self._count_i = 1
                self._count_k = 0
            else:
                self._count_j = 1
                self._count_k = 0
        elif(self._count_i == self._count_j == 0 and self._count_k == 1):
            await self.sender.sendMessage("Uh no... Please try again!\nHint: Press the given *button*")
        else:
            pass

        if(self._count_i == 2 and self._count_j == self._count_k == 0):
            if(msg['text'] == "Record food intake"):
                self._count_i = 3
            elif(msg['text'] == "Record physical activity"):
                self._count_i = 4
            elif(msg['text'] == "Get daily report"):
                self._count_i = 5
            elif(msg['text'] == "Get weekly report"):
                self._count_i = 6
            else:
                self._count_k = 1
        else:
            pass

        if(self._count_i == 3 and self._count_j == 1 and self._count_k == 0):
            if(msg['text'] == 'Meals'):
                self._count_j = 2
            elif(msg['text'] == 'Snacks'):
                self._count_j = 3
            else:
                self._count_k = 1

        if(self._count_i == 0 and self._count_j == 0 and self._count_k == 0):
            keyboard_button = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Okay! Let's start :)")]], resize_keyboard=True, one_time_keyboard=True)
            await self.sender.sendMessage("Hello! My name is *Loy Loy*.\n\nI am a tiny little bot that is able to be your _health and fitness companion_ by keeping track of your *food intake* and your *physical activity*. \n\nI'm sure you will be glad to use me. \nShall we *start*? \n\n(Hint: Press the given button)", parse_mode='Markdown', reply_markup=keyboard_button)
        elif(self._count_i == 0 and self._count_j == 1 and self._count_k == 0):
            keyboard_button = ReplyKeyboardHide()
            await self.sender.sendMessage("Hello *" + self._firstname + "*!\nYou're a *first time* user! I would require some of your *information*.", parse_mode = 'Markdown', reply_markup=keyboard_button)
            await self.sender.sendMessage("What's your age (just the numbers)? (eg: 21)")
            self._count_k +=1
        elif(self._count_i == 0 and self._count_j == 1 and self._count_k == 1):
            try:
                self._age = math.floor(float(msg['text']))

                keyboard_button = ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text='Guy')],
                    [KeyboardButton(text='Girl')]
                                                      ], resize_keyboard=True, one_time_keyboard=True)
                await self.sender.sendMessage("Are you a *guy* or a *girl*?\n\n(Hint: Use the *button* given)", parse_mode='Markdown', reply_markup=keyboard_button)

                self._count_k += 1
            except ValueError:
                await self.sender.sendMessage("Wrong input. Please try again.\nHint: just the numbers (eg: 21)")
        elif(self._count_i == 0 and self._count_j == 1 and self._count_k == 2):
            if(msg['text'] == "Guy"):
                self._gender = "male"
                keyboard_button = ReplyKeyboardHide()
                await self.sender.sendMessage("*Great!* Now enter your *height* in *cm* (eg: 165)", parse_mode='Markdown', reply_markup=keyboard_button)
                self._count_k += 1
            elif(msg['text'] == "Girl"):
                self._gender = "female"
                keyboard_button = ReplyKeyboardHide()
                await self.sender.sendMessage("*Great!* Now enter your *height* in *cm* (eg: 151)", parse_mode='Markdown', reply_markup=keyboard_button)
                self._count_k += 1
            else:
                await self.sender.sendMessage("Wrong input. Please try again.\nHint: Use the *button* given", parse_mode='Markdown')
        elif(self._count_i == 0 and self._count_j == 1 and self._count_k == 3):
            try:
                self._height = math.floor(float(msg['text']))
                await self.sender.sendMessage("Thank you. Now enter your *weight* in *kg* (eg: 65.4)", parse_mode='Markdown')
                self._count_k += 1
            except ValueError:
                await self.sender.sendMessage("Wrong input. Please try again.\nHint: do not include cm (eg:160)")
        elif(self._count_i == 0 and self._count_j == 1 and self._count_k == 4):
            try:
                self._weight = float(msg['text'])

                self._filestring = '<?xml version="1.0" ?>' + '\n' +\
                    '<profile>' + '\n' +\
                    '   <information>' + '\n' + \
                    '      <age>' + str(self._age) + '</age>' + '\n' +\
                    '      <gender>' + self._gender + '</gender>' + '\n' +\
                    '      <weight>' + str(self._weight) + '</weight>' + '\n' +\
                    '      <height>' + str(self._height) + '</height>' + '\n' +\
                    '   </information>' + '\n' + \
                    '   <meals>' + '\n' + '   </meals>' + '\n' +\
                    '   <snacks>' + '\n' + '   </snacks>' + '\n' +\
                    '   <exercise>' + '\n' + '   </exercise>' + '\n' +\
                    '</profile>' + '\n'
                file = open(self._filename, "w",encoding='utf8')
                file.write(self._filestring)
                file.close()

                self._count_i = 1
                self._count_j = self._count_k = 0

                keyboard_button = ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text='Record food intake'), KeyboardButton(text='Record physical activity')],
                    [KeyboardButton(text='Get daily report'), KeyboardButton(text='Get weekly report')]
                ], resize_keyboard=True, one_time_keyboard=True)
                await self.sender.sendMessage("Welcome *" + self._firstname + "*!\n\nWhat do you _want_ me to do now?", parse_mode='Markdown', reply_markup=keyboard_button)
                self._count_i += 1

            except ValueError:
                await self.sender.sendMessage("Wrong input. Please try again.\nHint: do not include kg (eg: 65.4)")
            except:
                await self.sender.sendMessage("Uhh no... Some strange error occured.")
        elif(self._count_i == 1 and self._count_j == self._count_k == 0):
            keyboard_button = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='Record food intake'), KeyboardButton(text='Record physical activity')],
                [KeyboardButton(text='Get daily report'), KeyboardButton(text='Get weekly report')]
            ], resize_keyboard=True, one_time_keyboard=True)
            await self.sender.sendMessage("Welcome *" + self._firstname + "*!\n\nWhat do you _want_ me to do now?", parse_mode='Markdown', reply_markup=keyboard_button)
            self._count_i += 1

        elif(self._count_i == 2 and self._count_j == 0 and self._count_k == 1):
            await self.sender.sendMessage("Uh no... Please try again!\nHint: Use the given *button*", parse_mode='Markdown')
            self._count_k = 0
            # Basic interfacing with user_end


            '''''
            Record food intake routine. User can classify under meals or snacks.
            '''''
            # Record Food Intake_Start
        elif(self._count_i == 3 and self._count_j == 0 and self._count_k == 0):
            keyboard_button = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='Meals')],[KeyboardButton(text='Snacks')]
            ], resize_keyboard=True, one_time_keyboard=True)
            await self.sender.sendMessage("Do you want to record a *meal* or a *snack*?", parse_mode='Markdown', reply_markup=keyboard_button)
            self._count_j += 1

        elif(self._count_i == 3 and self._count_j == 1 and self._count_k == 1):
            await self.sender.sendMessage("Uh no... Wrong input. Please try again!\nHint: Use the given *button*", parse_mode='Markdown')
            self._count_k = 0

        elif(self._count_i == 3 and self._count_j == 2 and self._count_k == 0):
            keyboard_button = ReplyKeyboardHide()
            await self.sender.sendMessage("Great! Give me the *name* of the *meal*", parse_mode='Markdown', reply_markup=keyboard_button)
            self._count_k = 1

        elif(self._count_i == 3 and self._count_j == 2 and self._count_k == 1):
            url = "http://www.myfitnesspal.com/food/search?search=" + quote(msg['text'])
            content = urlopen(url).read()
            soup = BeautifulSoup(content, "html.parser")

            if(soup.find('ul',{"class":"food_search_results"}) is None or soup.find('ul',{"class":"food_search_results"}).findAll('div', {"class": "food_description"}).__len__() < 6):
                await self.sender.sendMessage("Uh oh...\nNo results found from web database!\nSorry...")

                keyboard_button = ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text='Record food intake'), KeyboardButton(text='Record physical activity')],
                    [KeyboardButton(text='Get daily report'), KeyboardButton(text='Get weekly report')]
                ], resize_keyboard=True, one_time_keyboard=True)
                await self.sender.sendMessage("Welcome *" + self._firstname + "*!\n\nWhat do you _want_ me to do now?", parse_mode='Markdown', reply_markup=keyboard_button)

                self._filestring = ""
                self._list1 = []
                self._list2 = []
                self._list3 = []
                self._list4 = []
                self._elementnumber = 0
                self._exercisename = ""
                self._exercisecalories = 0.0
                self._exercisetime = 0.0

                self._count_i = 2
                self._count_j = self._count_k = 0
            else:
                result = soup.find('ul', {"class": "food_search_results"}).findAll('div', {"class": "food_description"})
                result2 = soup.find('ul',{"class":"food_search_results"}).findAll('div',{"class":"nutritional_info"})
                for x in range(6):
                    self._list1.append(result[x].find('a').text + " (" + result[x].find('a',{"class":"brand"}).text + ")")
                    self._list2.append(result2[x].getText(strip=True).split(',Calories:')[0].split(':')[1])
                    self._list3.append(result2[x].getText(strip=True).split(',Calories:')[1].split(',')[0])
                keyboard_button = ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text= self._list1[0]),KeyboardButton(text= self._list1[1])],
                    [KeyboardButton(text= self._list1[2]),KeyboardButton(text= self._list1[3])],
                    [KeyboardButton(text= self._list1[4]),KeyboardButton(text= self._list1[5])]
                ], resize_keyboard=True, one_time_keyboard=True)
                await self.sender.sendMessage("Which one?",reply_markup=keyboard_button)
                self._count_k += 1

        elif(self._count_i == 3 and self._count_j == 2 and self._count_k == 2):
            if(msg['text'] == self._list1[0] or msg['text'] == self._list1[1] or msg['text'] == self._list1[2] or msg['text'] == self._list1[3]or msg['text'] == self._list1[4] or msg['text'] == self._list1[5]):
                if(msg['text'] == self._list1[0]):
                    self._elementnumber = 0
                    keyboard_button = ReplyKeyboardHide()
                    await self.sender.sendMessage(self._list1[0] + "\n" + "*1 serving: *" + self._list2[0] + "\n\n" + "How many servings did you consume?", parse_mode='Markdown', reply_markup=keyboard_button)
                elif(msg['text'] == self._list1[1]):
                    self._elementnumber = 1
                    keyboard_button = ReplyKeyboardHide()
                    await self.sender.sendMessage(self._list1[1] + "\n" + "*1 serving: *" + self._list2[1] + "\n\n" + "How many servings did you consume?", parse_mode='Markdown', reply_markup=keyboard_button)
                elif(msg['text'] == self._list1[2]):
                    self._elementnumber = 2
                    keyboard_button = ReplyKeyboardHide()
                    await self.sender.sendMessage(self._list1[2] + "\n" + "*1 serving: *" + self._list2[2] + "\n\n" + "How many servings did you consume?", parse_mode='Markdown', reply_markup=keyboard_button)
                elif(msg['text'] == self._list1[3]):
                    self._elementnumber = 3
                    keyboard_button = ReplyKeyboardHide()
                    await self.sender.sendMessage(self._list1[3] + "\n" + "*1 serving: *" + self._list2[3] + "\n\n" + "How many servings did you consume?", parse_mode='Markdown', reply_markup=keyboard_button)
                elif(msg['text'] == self._list1[4]):
                    self._elementnumber = 4
                    keyboard_button = ReplyKeyboardHide()
                    await self.sender.sendMessage(self._list1[4] + "\n" + "*1 serving: *" + self._list2[4] + "\n\n" + "How many servings did you consume?", parse_mode='Markdown', reply_markup=keyboard_button)
                else:
                    self._elementnumber = 5
                    keyboard_button = ReplyKeyboardHide()
                    await self.sender.sendMessage(self._list1[5] + "\n" + "*1 serving: *" + self._list2[5] + "\n\n" + "How many servings did you consume?", parse_mode='Markdown', reply_markup=keyboard_button)
                self._count_k += 1
            else:
                await self.sender.sendMessage("Invalid input. I don't understand!\nHint: Use the given *button*", parse_mode='Markdown')

        elif(self._count_i == 3 and self._count_j == 2 and self._count_k == 3):
                try:
                    portion = float(msg['text'])
                    if(portion >= 0):
                        food_name = self._list1[self._elementnumber]
                        food_calories = portion * float(self._list3[self._elementnumber])

                        file = open(self._filename,"r",encoding='utf8')
                        self._filestring = file.read()
                        file.close()
                        date = '{:%B_%d_%Y}'.format(datetime.datetime.today())

                        first_delimiter = '   </meals>'
                        first_split_string1 = self._filestring.split(first_delimiter)[0]
                        first_split_string2 = first_delimiter + self._filestring.split(first_delimiter)[1]

                        if(date in first_split_string1):
                            second_delimiter = '      </' + date + '>'
                            second_split_string1 = first_split_string1.split(second_delimiter)[0]
                            second_split_string2 = second_delimiter + first_split_string1.split(second_delimiter)[1]

                            string_to_insert = '         <entry>' + '\n' + \
                                               '            <name>' + food_name + '</name>' + '\n' + \
                                               '            <serving>' + str(portion) + ' serving(s) of ' + self._list2[self._elementnumber] + '</serving>' + '\n' +\
                                               '            <calories>' + str(food_calories) + '</calories>' + '\n' + \
                                               '         </entry>' + '\n'
                            self._filestring = second_split_string1 + string_to_insert + second_split_string2 + first_split_string2
                            file = open(self._filename, "w", encoding='utf8')
                            file.write(self._filestring)
                            file.close()
                        else:
                            string_to_insert = '      <' + date + '>' + '\n' + \
                                               '         <entry>' + '\n' + \
                                               '            <name>' + food_name + '</name>' + '\n' + \
                                               '            <serving>' + str(portion) + ' serving(s) of ' + self._list2[self._elementnumber] + '</serving>' + '\n' + \
                                               '            <calories>' + str(food_calories) + '</calories>' + '\n' + \
                                               '         </entry>' + '\n' + \
                                               '      </' + date + '>' + '\n'
                            self._filestring = first_split_string1 + string_to_insert + first_split_string2
                            file = open(self._filename, "w", encoding='utf8')
                            file.write(self._filestring)
                            file.close()

                        await self.sender.sendMessage("*" + food_name + "*\n*" + str(portion) + "* serving(s) of " + self._list2[self._elementnumber] + " \n*" + str(food_calories) + "* calories.\n\nYour meal intake has been recorded.\nThank you!", parse_mode='Markdown')

                        keyboard_button = ReplyKeyboardMarkup(keyboard=[
                            [KeyboardButton(text='Record food intake'), KeyboardButton(text='Record physical activity')],
                            [KeyboardButton(text='Get daily report'), KeyboardButton(text='Get weekly report')]
                        ], resize_keyboard=True, one_time_keyboard=True)
                        await self.sender.sendMessage("Welcome *" + self._firstname + "*!\n\nWhat do you _want_ me to do now?", parse_mode='Markdown', reply_markup=keyboard_button)

                        self._filestring = ""
                        self._list1 = []
                        self._list2 = []
                        self._list3 = []
                        self._list4 = []
                        self._elementnumber = 0
                        self._exercisename = ""
                        self._exercisecalories = 0.0
                        self._exercisetime = 0.0

                        self._count_i = 2
                        self._count_j = self._count_k = 0
                    else:
                        await self.sender.sendMessage("Invalid. Please try again.")

                except ValueError:
                    await self.sender.sendMessage("Invalid input!\nHint: Just the *numbers with decimal points* if necessary.", parse_mode='Markdown')

        elif (self._count_i == 3 and self._count_j == 3 and self._count_k == 0):
            keyboard_button = ReplyKeyboardHide()
            await self.sender.sendMessage("Great! Give me the *name* of the *snack*", parse_mode='Markdown', reply_markup=keyboard_button)
            self._count_k = 1

        elif (self._count_i == 3 and self._count_j == 3 and self._count_k == 1):
            url = "http://www.myfitnesspal.com/food/search?search=" + quote(msg['text'])
            content = urlopen(url).read()
            soup = BeautifulSoup(content, "html.parser")

            if (soup.find('ul',{"class":"food_search_results"}) is None or soup.find('ul',{"class":"food_search_results"}).findAll('div', {"class": "food_description"}).__len__() < 6):
                await self.sender.sendMessage("Uh oh...\nNo results found from web database!\nSorry...")

                keyboard_button = ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text='Record food intake'), KeyboardButton(text='Record physical activity')],
                    [KeyboardButton(text='Get daily report'), KeyboardButton(text='Get weekly report')]
                ], resize_keyboard=True, one_time_keyboard=True)
                await self.sender.sendMessage("Welcome *" + self._firstname + "*!\n\nWhat do you _want_ me to do now?", parse_mode='Markdown', reply_markup=keyboard_button)

                self._filestring = ""
                self._list1 = []
                self._list2 = []
                self._list3 = []
                self._list4 = []
                self._elementnumber = 0
                self._exercisename = ""
                self._exercisecalories = 0.0
                self._exercisetime = 0.0

                self._count_i = 2
                self._count_j = self._count_k = 0
            else:
                result = soup.find('ul', {"class": "food_search_results"}).findAll('div', {"class": "food_description"})
                result2 = soup.find('ul', {"class": "food_search_results"}).findAll('div', {"class": "nutritional_info"})
                for x in range(6):
                    self._list1.append(result[x].find('a').text + " (" + result[x].find('a', {"class": "brand"}).text + ")")
                    self._list2.append(result2[x].getText(strip=True).split(',Calories:')[0].split(':')[1])
                    self._list3.append(result2[x].getText(strip=True).split(',Calories:')[1].split(',')[0])
                keyboard_button = ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text=self._list1[0]),KeyboardButton(text=self._list1[1])],
                    [KeyboardButton(text=self._list1[2]),KeyboardButton(text=self._list1[3])],
                    [KeyboardButton(text=self._list1[4]),KeyboardButton(text=self._list1[5])]
                ], resize_keyboard=True, one_time_keyboard=True)
                await self.sender.sendMessage("Which one?", reply_markup=keyboard_button)
                self._count_k += 1

        elif (self._count_i == 3 and self._count_j == 3 and self._count_k == 2):
            if (msg['text'] == self._list1[0] or msg['text'] == self._list1[1] or msg['text'] == self._list1[2] or msg['text'] == self._list1[3] or msg['text'] == self._list1[4] or msg['text'] == self._list1[5]):
                if (msg['text'] == self._list1[0]):
                    self._elementnumber = 0
                    keyboard_button = ReplyKeyboardHide()
                    await self.sender.sendMessage(self._list1[0] + "\n" + "*1 serving: *" + self._list2[0] + "\n\n" + "How many servings did you consume?", parse_mode='Markdown', reply_markup=keyboard_button)
                elif (msg['text'] == self._list1[1]):
                    self._elementnumber = 1
                    keyboard_button = ReplyKeyboardHide()
                    await self.sender.sendMessage(self._list1[1] + "\n" + "*1 serving: *" + self._list2[1] + "\n\n" + "How many servings did you consume?", parse_mode='Markdown', reply_markup=keyboard_button)
                elif (msg['text'] == self._list1[2]):
                    self._elementnumber = 2
                    keyboard_button = ReplyKeyboardHide()
                    await self.sender.sendMessage(self._list1[2] + "\n" + "*1 serving: *" + self._list2[2] + "\n\n" + "How many servings did you consume?", parse_mode='Markdown', reply_markup=keyboard_button)
                elif (msg['text'] == self._list1[3]):
                    self._elementnumber = 3
                    keyboard_button = ReplyKeyboardHide()
                    await self.sender.sendMessage(self._list1[3] + "\n" + "*1 serving: *" + self._list2[3] + "\n\n" + "How many servings did you consume?", parse_mode='Markdown', reply_markup=keyboard_button)
                elif (msg['text'] == self._list1[4]):
                    self._elementnumber = 4
                    keyboard_button = ReplyKeyboardHide()
                    await self.sender.sendMessage(self._list1[4] + "\n" + "*1 serving: *" + self._list2[4] + "\n\n" + "How many servings did you consume?", parse_mode='Markdown', reply_markup=keyboard_button)
                else:
                    self._elementnumber = 5
                    keyboard_button = ReplyKeyboardHide()
                    await self.sender.sendMessage(self._list1[5] + "\n" + "*1 serving: *" + self._list2[5] + "\n\n" + "How many servings did you consume?", parse_mode='Markdown', reply_markup=keyboard_button)
                self._count_k += 1
            else:
                await self.sender.sendMessage("Invalid input. I don't understand!\nHint: Use the given *button*", parse_mode='Markdown')

        elif (self._count_i == 3 and self._count_j == 3 and self._count_k == 3):
                try:
                    portion = float(msg['text'])
                    if(portion >= 0):
                        food_name = self._list1[self._elementnumber]
                        food_calories = portion * float(self._list3[self._elementnumber])

                        file = open(self._filename, "r", encoding='utf8')
                        self._filestring = file.read()
                        file.close()
                        date = '{:%B_%d_%Y}'.format(datetime.datetime.today())

                        first_delimiter = '   </meals>'
                        first_split_string1 = self._filestring.split(first_delimiter)[0] + first_delimiter
                        first_split_string2 = self._filestring.split(first_delimiter)[1]
                        second_delimiter = '   </snacks>'
                        second_split_string1 = first_split_string2.split(second_delimiter)[0]
                        second_split_string2 = second_delimiter + first_split_string2.split(second_delimiter)[1]
                        if (date in second_split_string1):
                            third_delimiter = '      </' + date + '>'
                            third_split_string1 = second_split_string1.split(third_delimiter)[0]
                            third_split_string2 = third_delimiter + second_split_string1.split(third_delimiter)[1]

                            string_to_insert = '         <entry>' + '\n' + \
                                               '            <name>' + food_name + '</name>' + '\n' + \
                                               '            <serving>' + str(portion) + ' serving(s) of ' + self._list2[self._elementnumber] + '</serving>' + '\n' + \
                                               '            <calories>' + str(food_calories) + '</calories>' + '\n' + \
                                               '         </entry>' + '\n'
                            self._filestring = first_split_string1 + third_split_string1 + string_to_insert + third_split_string2 + second_split_string2
                            file = open(self._filename,"w", encoding='utf8')
                            file.write(self._filestring)
                            file.close()
                        else:
                            string_to_insert = '      <' + date + '>' + '\n' + \
                                               '         <entry>' + '\n' + \
                                               '            <name>' + food_name + '</name>' + '\n' + \
                                               '            <serving>' + str(portion) + ' serving(s) of ' + self._list2[self._elementnumber] + '</serving>' + '\n' + \
                                               '            <calories>' + str(food_calories) + '</calories>' + '\n' + \
                                               '         </entry>' + '\n' + \
                                               '      </' + date + '>' + '\n'
                            self._filestring = first_split_string1 + second_split_string1 + string_to_insert + second_split_string2
                            file = open(self._filename,"w", encoding = 'utf8')
                            file.write(self._filestring)
                            file.close()

                        await self.sender.sendMessage("*" + food_name + "*\n*" + str(portion) + "* serving(s) of " + self._list2[self._elementnumber] + " \n*" + str(food_calories) + "* calories.\n\nYour snack intake has been recorded.\nThank you!", parse_mode='Markdown')

                        keyboard_button = ReplyKeyboardMarkup(keyboard=[
                            [KeyboardButton(text='Record food intake'), KeyboardButton(text='Record physical activity')],
                            [KeyboardButton(text='Get daily report'), KeyboardButton(text='Get weekly report')]
                        ], resize_keyboard=True, one_time_keyboard=True)
                        await self.sender.sendMessage("Welcome *" + self._firstname + "*!\n\nWhat do you _want_ me to do now?", parse_mode='Markdown', reply_markup=keyboard_button)

                        self._filestring = ""
                        self._list1 = []
                        self._list2 = []
                        self._list3 = []
                        self._list4 = []
                        self._elementnumber = 0
                        self._exercisename = ""
                        self._exercisecalories = 0.0
                        self._exercisetime = 0.0

                        self._count_i = 2
                        self._count_j = self._count_k = 0
                    else:
                        await self.sender.sendMessage("Invalid input. Please try again.")
                except ValueError:
                    await self.sender.sendMessage("Invalid input!\nHint: Just the *numbers with decimal points* if necessary.", parse_mode='Markdown')
                        # Record Food Intake_End


                '''''
                Record Physical Activity Routine!
                '''''
            # Record Physical Activity_Start
        elif (self._count_i == 4 and self._count_j == 0 and self._count_k == 0):
            await self._sender.sendMessage("Give me a moment to retrieve the list of physical activity from the web.")
            driver = webdriver.PhantomJS()
            driver.get("http://www.mydr.com.au/tools/calories-burned-calculator")
            Time.sleep(1)

            activity = Select(driver.find_element_by_id('activity'))
            for x in activity.options:
                self._list4.append(x.text)
            driver.quit()

            string_to_send = "These are the activities that I found.\nWhich one?" + "\n\n"
            string_to_send2 = ""
            string_to_send3 = ""
            for x in range(1,math.floor(self._list4.__len__()/3)):
                string_to_send += str(x) + ".\t" + self._list4[x] + "\n"
            for x in range(math.floor(self._list4.__len__()/3), math.floor(self._list4.__len__()/3*2)):
                string_to_send2 += str(x) + ".\t" + self._list4[x] + "\n"
            for x in range(math.floor(self._list4.__len__()/3*2), self._list4.__len__()):
                string_to_send3 += str(x) + ".\t" + self._list4[x] + "\n"
            string_to_send3 += "\nPlease reply with the serial number of the physical activity."

            keyboard_button = ReplyKeyboardHide()
            await self.sender.sendMessage("Great!\n" + string_to_send, reply_markup=keyboard_button)
            await self.sender.sendMessage(string_to_send2, reply_markup=keyboard_button)
            await self.sender.sendMessage(string_to_send3, reply_markup=keyboard_button)


            self._count_j += 1

        elif(self._count_i == 4 and self._count_j == 1 and self._count_k == 0):
            try:
                self._exercisename = int(msg['text'])
                if(self._exercisename < 1 or self._exercisename >= self._list4.__len__()):
                    await self.sender.sendMessage("Item not found! Please try again!")
                else:
                    self._exercisename = self._list4[self._exercisename]
                    await self.sender.sendMessage("Great!\n\nHow long is your *" + self._exercisename + "* in *minutes*?", parse_mode='Markdown')
                    self._count_j += 1

            except ValueError:
                await self.sender.sendMessage("Invalid input. Please try again.\nHint: Enter only the *serial number* of the physical activity.", parse_mode='Markdown')

        elif(self._count_i == 4 and self._count_j == 2 and self._count_k == 0):
            try:
                if(float(msg['text']) >= 0):
                    self._exercisetime = float(msg['text'])
                    await self.sender.sendMessage("Give me a moment. Calculating your calories...")
                    
                    driver = webdriver.PhantomJS()
                    driver.get("http://www.mydr.com.au/tools/calories-burned-calculator")
                    Time.sleep(1)

                    tree = ET.parse(self._filename)
                    if(tree.getroot().find('information').find('gender').text == 'male'):
                        driver.find_element_by_id('sm').click()
                    else:
                        driver.find_element_by_id('sf').click()

                    height = driver.find_element_by_id('h')
                    height.send_keys(tree.getroot().find('information').find('height').text)

                    weight = driver.find_element_by_id('w')
                    weight.send_keys(tree.getroot().find('information').find('weight').text)

                    age = driver.find_element_by_id('a')
                    age.send_keys(tree.getroot().find('information').find('age').text)

                    activity = Select(driver.find_element_by_id('activity'))
                    activity.select_by_visible_text(self._exercisename)

                    time = driver.find_element_by_id('time')
                    time.send_keys(str(self._exercisetime))

                    button = driver.find_element_by_css_selector('.btngreenbutton.add_top')
                    button.click()

                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    driver.quit()

                    self._exercisecalories = soup.find(id="res").getText(strip=True).split(' kcal')[0]

                    file = open(self._filename, "r", encoding='utf8')
                    self._filestring = file.read()
                    file.close()

                    date = '{:%B_%d_%Y}'.format(datetime.datetime.today())

                    first_delimiter = '   </snacks>'
                    first_split_string1 = self._filestring.split(first_delimiter)[0] + first_delimiter
                    first_split_string2 = self._filestring.split(first_delimiter)[1]
                    second_delimiter = '   </exercise>'
                    second_split_string1 = first_split_string2.split(second_delimiter)[0]
                    second_split_string2 = second_delimiter + first_split_string2.split(second_delimiter)[1]

                    if (date in second_split_string1):
                        third_delimiter = '      </' + date + '>'
                        third_split_string1 = second_split_string1.split(third_delimiter)[0]
                        third_split_string2 = third_delimiter + second_split_string1.split(third_delimiter)[1]

                        string_to_insert = '         <entry>' + '\n' + \
                                           '            <name>' + self._exercisename + '</name>' + '\n' + \
                                           '            <calories>' + str(self._exercisecalories) + '</calories>' + '\n' + \
                                           '         </entry>' + '\n'
                        self._filestring = first_split_string1 + third_split_string1 + string_to_insert + third_split_string2 + second_split_string2
                        file = open(self._filename, "w", encoding='utf8')
                        file.write(self._filestring)
                        file.close()
                    else:
                        string_to_insert = '      <' + date + '>' + '\n' + \
                                           '         <entry>' + '\n' + \
                                           '            <name>' + self._exercisename + '</name>' + '\n' + \
                                           '            <calories>' + str(self._exercisecalories) + '</calories>' + '\n' + \
                                           '         </entry>' + '\n' + \
                                           '      </' + date + '>' + '\n'
                        self._filestring = first_split_string1 + second_split_string1 + string_to_insert + second_split_string2
                        file = open(self._filename, "w", encoding='utf8')
                        file.write(self._filestring)
                        file.close()

                    await self.sender.sendMessage("*" + self._exercisename + "*\n*" + str(self._exercisecalories) + "* calories.\n\nYour physical activity has been recorded.\nThank you!", parse_mode='Markdown')

                    keyboard_button = ReplyKeyboardMarkup(keyboard=[
                        [KeyboardButton(text='Record food intake'), KeyboardButton(text='Record physical activity')],
                        [KeyboardButton(text='Get daily report'), KeyboardButton(text='Get weekly report')]
                    ], resize_keyboard=True, one_time_keyboard=True)
                    await self.sender.sendMessage("Welcome *" + self._firstname + "*!\n\nWhat do you _want_ me to do now?", parse_mode='Markdown', reply_markup=keyboard_button)

                    self._filestring = ""
                    self._list1 = []
                    self._list2 = []
                    self._list3 = []
                    self._list4 = []
                    self._elementnumber = 0
                    self._exercisename = ""
                    self._exercisecalories = 0.0
                    self._exercisetime = 0.0

                    self._count_i = 2
                    self._count_j = self._count_k = 0

                else:
                    await self.sender.sendMessage("Invalid input. Please try again.")

            except ValueError:
                await self.sender.sendMessage("Invalid input. Please try again.\nHint: Enter only the *numbers* with *decimal point* if necessary..", parse_mode='Markdown')
                # Record Physical Activity_End


            '''''
            Daily report of yesterday and today (2 separate reports).
            '''''
            # Daily Report_Start
        elif(self._count_i == 5 and self._count_j == self._count_k == 0):
            tree = ET.parse(self._filename)
            meals_list_yesterday = []
            snacks_list_yesterday = []
            exercise_list_yesterday = []
            meals_list_today = []
            snacks_list_today = []
            exercise_list_today = []

            date = '{:%B_%d_%Y}'.format(datetime.datetime.today() - datetime.timedelta(days=1))
            if(type(tree.getroot().find('meals').find(date)) == type(None)):
                pass
            else:
                for x in tree.getroot().find('meals').find(date).findall('entry'):
                    meals_list_yesterday.append(x[0].text)
                    meals_list_yesterday.append(x[1].text)
                    meals_list_yesterday.append(x[2].text)
            if(type(tree.getroot().find('snacks').find(date)) == type(None)):
                pass
            else:
                for x in tree.getroot().find('snacks').find(date).findall('entry'):
                    snacks_list_yesterday.append(x[0].text)
                    snacks_list_yesterday.append(x[1].text)
                    snacks_list_yesterday.append(x[2].text)
            if(type(tree.getroot().find('exercise').find(date)) == type(None)):
                pass
            else:
                for x in tree.getroot().find('exercise').find(date).findall('entry'):
                    exercise_list_yesterday.append(x[0].text)
                    exercise_list_yesterday.append(x[1].text)

            date = '{:%B_%d_%Y}'.format(datetime.datetime.today())
            if(type(tree.getroot().find('meals').find(date)) == type(None)):
                pass
            else:
                for x in tree.getroot().find('meals').find(date).findall('entry'):
                    meals_list_today.append(x[0].text)
                    meals_list_today.append(x[1].text)
                    meals_list_today.append(x[2].text)
            if(type(tree.getroot().find('snacks').find(date)) == type(None)):
                pass
            else:
                for x in tree.getroot().find('snacks').find(date).findall('entry'):
                    snacks_list_today.append(x[0].text)
                    snacks_list_today.append(x[1].text)
                    snacks_list_today.append(x[2].text)
            if(type(tree.getroot().find('exercise').find(date)) == type(None)):
                pass
            else:
                for x in tree.getroot().find('exercise').find(date).findall('entry'):
                    exercise_list_today.append(x[0].text)
                    exercise_list_today.append(x[1].text)
            if(meals_list_yesterday == meals_list_today == snacks_list_yesterday == snacks_list_today == exercise_list_yesterday == exercise_list_today == []):
                keyboard_button = ReplyKeyboardHide()
                await self.sender.sendMessage("I'm sorry. You did not log any food intake or physical activity for yesterday or today.",reply_markup=keyboard_button)
            else:

                if(meals_list_yesterday == snacks_list_yesterday == exercise_list_yesterday == []):
                    pass
                else:
                    message_string = "Daily Report for yesterday.\n\n\n"
                    message_string += '{:%A, %d %B %Y}'.format(datetime.datetime.today() - datetime.timedelta(days=1))
                    message_string += "\n\n\n*Meals*\n\n"
                    if(meals_list_yesterday == []):
                        message_string += "Sorry. you did not log any meals intake for yesterday!\n\n"
                    else:
                        for (i, x) in enumerate(meals_list_yesterday):
                            if(i%3 == 0):
                                message_string += x + '\n'
                            elif(i%3 == 1):
                                message_string += x + '\n'
                            else:
                                message_string += "Calories intake: " + x + '\n\n'
                    message_string += "*Snacks*\n\n"
                    if (snacks_list_yesterday == []):
                        message_string += "Sorry. you did not log any snacks intake for yesterday!\n\n"
                    else:
                        for (i, x) in enumerate(snacks_list_yesterday):
                            if(i%3 == 0):
                                message_string += x + '\n'
                            elif(i%3 == 1):
                                message_string += x + '\n'
                            else:
                                message_string += "Calories intake: " + x + '\n\n'
                    message_string += "*Physical activities*\n\n"
                    if (exercise_list_yesterday == []):
                        message_string += "Sorry. you did not log any physical activity for yesterday!\n\n"
                    else:
                        for (i, x) in enumerate(exercise_list_yesterday):
                            if (i % 2 == 0):
                                message_string += x + '\n'
                            else:
                                message_string += "Calories burnt: " + x + '\n\n'
                    message_string += "\n"
                    resting_metabolic_rate = 0.0
                    net_calories_of_day = 0.0
                    self._age = int(tree.getroot().find('information')[0].text)
                    self._gender = tree.getroot().find('information')[1].text
                    self._weight = float(tree.getroot().find('information')[2].text)
                    self._height = int(tree.getroot().find('information')[3].text)
                    if(self._gender == 'male'):
                        resting_metabolic_rate = 1.2 * (88.362 + (4.799 * self._height) + (13.397 * self._weight) - (5.677 * self._age))
                    else:
                        resting_metabolic_rate = 1.2 * (447.593 + (3.098 * self._height) + (9.247 * self._weight) - (4.33 * self._age))
                    if(meals_list_yesterday == []):
                        pass
                    else:
                        for (i, x) in enumerate(meals_list_yesterday):
                            if(i%3 == 0 or i%3 == 1):
                                pass
                            else:
                                net_calories_of_day += float(x)
                    if (snacks_list_yesterday == []):
                        pass
                    else:
                        for (i, x) in enumerate(snacks_list_yesterday):
                            if (i % 3 == 0 or i%3 == 1):
                                pass
                            else:
                                net_calories_of_day += float(x)
                    if (exercise_list_yesterday == []):
                        pass
                    else:
                        for (i, x) in enumerate(exercise_list_yesterday):
                            if (i % 2 == 0):
                                pass
                            else:
                                net_calories_of_day -= float(x)
                    calories_deficit = resting_metabolic_rate - net_calories_of_day
                    kilogram_deficit = calories_deficit * 35 / 7700
                    message_string += "If everyday were like this, you'll weigh *" + str(round(self._weight - kilogram_deficit, 1)) + "* " + "kg in 5 weeks!"

                    keyboard_button = ReplyKeyboardHide()
                    await self.sender.sendMessage(message_string,parse_mode='Markdown', reply_markup=keyboard_button)

                if(meals_list_today == snacks_list_today == exercise_list_today == []):
                    pass
                else:
                    message_string = "Daily Report for today.\n\n\n"
                    message_string += '{:%A, %d %B %Y}'.format(datetime.datetime.today())
                    message_string += "\n\n\n*Meals*\n\n"
                    if(meals_list_today == []):
                        message_string += "Sorry. you did not log any meals intake for today!\n\n"
                    else:
                        for (i, x) in enumerate(meals_list_today):
                            if(i%3 == 0):
                                message_string += x + '\n'
                            elif(i%3 == 1):
                                message_string += x + '\n'
                            else:
                                message_string += "Calories intake: " + x + '\n\n'
                    message_string += "*Snacks*\n\n"
                    if (snacks_list_today == []):
                        message_string += "Sorry. you did not log any snacks intake for today!\n\n"
                    else:
                        for (i, x) in enumerate(snacks_list_today):
                            if(i%3 == 0):
                                message_string += x + '\n'
                            elif(i%3 == 1):
                                message_string += x + '\n'
                            else:
                                message_string += "Calories intake: " + x + '\n\n'
                    message_string += "*Physical activities*\n\n"
                    if (exercise_list_today == []):
                        message_string += "Sorry. you did not log any physical activity for today!\n\n"
                    else:
                        for (i, x) in enumerate(exercise_list_today):
                            if (i % 2 == 0):
                                message_string += x + '\n'
                            else:
                                message_string += "Calories burnt: " + x + '\n\n'
                    message_string += "\n"
                    resting_metabolic_rate = 0.0
                    net_calories_of_day = 0.0
                    self._age = int(tree.getroot().find('information')[0].text)
                    self._gender = tree.getroot().find('information')[1].text
                    self._weight = float(tree.getroot().find('information')[2].text)
                    self._height = int(tree.getroot().find('information')[3].text)
                    if(self._gender == 'male'):
                        resting_metabolic_rate = 1.2 * (88.362 + (4.799 * self._height) + (13.397 * self._weight) - (5.677 * self._age))
                    else:
                        resting_metabolic_rate = 1.2 * (447.593 + (3.098 * self._height) + (9.247 * self._weight) - (4.33 * self._age))
                    if(meals_list_today == []):
                        pass
                    else:
                        for (i, x) in enumerate(meals_list_today):
                            if(i%3 == 0 or i%3 == 1):
                                pass
                            else:
                                net_calories_of_day += float(x)
                    if (snacks_list_today == []):
                        pass
                    else:
                        for (i, x) in enumerate(snacks_list_today):
                            if (i%3 == 0 or i%3 == 1):
                                pass
                            else:
                                net_calories_of_day += float(x)
                    if (exercise_list_today == []):
                        pass
                    else:
                        for (i, x) in enumerate(exercise_list_today):
                            if (i % 2 == 0):
                                pass
                            else:
                                net_calories_of_day -= float(x)
                    calories_deficit = resting_metabolic_rate - net_calories_of_day
                    kilogram_deficit = calories_deficit * 35 / 7700
                    message_string += "If you were to continue this everyday, you'll weigh *" + str(round(self._weight - kilogram_deficit, 1)) + "* " + "kg in 5 weeks!"

                    keyboard_button = ReplyKeyboardHide()
                    await self.sender.sendMessage(message_string,parse_mode='Markdown', reply_markup=keyboard_button)

            keyboard_button = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='Record food intake'), KeyboardButton(text='Record physical activity')],
                [KeyboardButton(text='Get daily report'), KeyboardButton(text='Get weekly report')]
            ], resize_keyboard=True, one_time_keyboard=True)
            await self.sender.sendMessage("Welcome *" + self._firstname + "*!\n\nWhat do you _want_ me to do now?", parse_mode='Markdown', reply_markup=keyboard_button)

            self._filestring = ""
            self._list1 = []
            self._list2 = []
            self._list3 = []
            self._list4 = []
            self._elementnumber = 0
            self._exercisename = ""
            self._exercisecalories = 0.0
            self._exercisetime = 0.0

            self._count_i = 2
            self._count_j = self._count_k = 0
            # Daily Report_End


            '''''
            Weekly Report will give user a report of his week up to yesterday.
            '''''
            # Weekly Report_Start
        elif(self._count_i == 6 and self._count_j == self._count_k == 0):
            tree = ET.parse(self._filename)
            meals_list_week = []
            snacks_list_week = []
            exercise_list_week = []
            for x in range(7,0,-1):
                date = '{:%B_%d_%Y}'.format(datetime.datetime.today() - datetime.timedelta(days=x))
                if (type(tree.getroot().find('meals').find(date)) == type(None)):
                    pass
                else:
                    for y in tree.getroot().find('meals').find(date).findall('entry'):
                        meals_list_week.append(y[0].text)
                        meals_list_week.append(y[1].text)
                if (type(tree.getroot().find('snacks').find(date)) == type(None)):
                    pass
                else:
                    for y in tree.getroot().find('snacks').find(date).findall('entry'):
                        snacks_list_week.append(y[0].text)
                        snacks_list_week.append(y[1].text)
                if (type(tree.getroot().find('exercise').find(date)) == type(None)):
                    pass
                else:
                    for y in tree.getroot().find('exercise').find(date).findall('entry'):
                        exercise_list_week.append(y[0].text)
                        exercise_list_week.append(y[1].text)
            if (meals_list_week == snacks_list_week == exercise_list_week == []):
                keyboard_button = ReplyKeyboardHide()
                await self.sender.sendMessage("I'm sorry. You did not log any food intake or physical activity for the past week.", reply_markup=keyboard_button)
            else:
                message_string = "Weekly Report.\n\n\n"
                message_string += '{:%A, %d %B %Y}'.format(datetime.datetime.today() - datetime.timedelta(days=7))
                message_string += " – "
                message_string += '{:%A, %d %B %Y}'.format(datetime.datetime.today() - datetime.timedelta(days=1))
                message_string += "\n\n\n*Meals*\n\n"
                if (meals_list_week == []):
                    message_string += "Sorry. you did not log any meals for the past week!\n\n"
                else:
                    for (i, x) in enumerate(meals_list_week):
                        if (i % 2 == 0):
                            message_string += x + '\n'
                        else:
                            message_string += "Calories intake: " + x + '\n\n'
                message_string += "*Snacks*\n\n"
                if (snacks_list_week == []):
                    message_string += "Sorry. you did not log any snacks intake for the past week!\n\n"
                else:
                    for (i, x) in enumerate(snacks_list_week):
                        if (i % 2 == 0):
                            message_string += x + '\n'
                        else:
                            message_string += "Calories intake: " + x + '\n\n'
                message_string += "*Physical activities*\n\n"
                if (exercise_list_week == []):
                    message_string += "Sorry. you did not log any physical activity for the past week!\n\n"
                else:
                    for (i, x) in enumerate(exercise_list_week):
                        if (i % 2 == 0):
                            message_string += x + '\n'
                        else:
                            message_string += "Calories burnt: " + x + '\n\n'
                message_string += "\n"
                resting_metabolic_rate_week = 0.0
                net_calories_of_week = 0.0
                self._age = int(tree.getroot().find('information')[0].text)
                self._gender = tree.getroot().find('information')[1].text
                self._weight = float(tree.getroot().find('information')[2].text)
                self._height = int(tree.getroot().find('information')[3].text)
                if (self._gender == 'male'):
                    resting_metabolic_rate_week = 1.2 * 7 * (88.362 + (4.799 * self._height) + (13.397 * self._weight) - (5.677 * self._age))
                else:
                    resting_metabolic_rate_week = 1.2 * 7 * (447.593 + (3.098 * self._height) + (9.247 * self._weight) - (4.33 * self._age))
                if (meals_list_week == []):
                    pass
                else:
                    for (i, x) in enumerate(meals_list_week):
                        if (i%3 == 0 or i%3 == 1):
                            pass
                        else:
                            net_calories_of_week += float(x)
                if (snacks_list_week == []):
                    pass
                else:
                    for (i, x) in enumerate(snacks_list_week):
                        if (i%3 == 0 or i%3 == 1):
                            pass
                        else:
                            net_calories_of_week += float(x)
                if (exercise_list_week == []):
                    pass
                else:
                    for (i, x) in enumerate(exercise_list_week):
                        if (i%3 == 0 or i%3 == 1):
                            pass
                        else:
                            net_calories_of_week -= float(x)
                calories_deficit = resting_metabolic_rate_week - net_calories_of_week
                kilogram_deficit = calories_deficit * 5 / 7700
                message_string += "If you were to continue this every week, you'll weigh *" + str(
                    round(self._weight - kilogram_deficit, 1)) + "* " + "kg in 5 weeks!"

                keyboard_button = ReplyKeyboardHide()
                await self.sender.sendMessage(message_string, parse_mode='Markdown', reply_markup=keyboard_button)

            keyboard_button = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='Record food intake'), KeyboardButton(text='Record physical activity')],
                [KeyboardButton(text='Get daily report'), KeyboardButton(text='Get weekly report')]
            ], resize_keyboard=True, one_time_keyboard=True)
            await self.sender.sendMessage("Welcome *" + self._firstname + "*!\n\nWhat do you _want_ me to do now?", parse_mode='Markdown', reply_markup=keyboard_button)

            self._filestring = ""
            self._list1 = []
            self._list2 = []
            self._list3 = []
            self._list4 = []
            self._elementnumber = 0
            self._exercisename = ""
            self._exercisecalories = 0.0
            self._exercisetime = 0.0

            self._count_i = 2
            self._count_j = self._count_k = 0
            # Weekly Report_End


load_dotenv(find_dotenv())
TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = telepot.aio.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=300),
])

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())
print('Listening ...')

loop.run_forever()
