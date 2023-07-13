try:
    import mysql.connector as sqltor
    import PySimpleGUI as sg
    import os
    import webbrowser
    import matplotlib.pyplot as plt
    from googlesearch import search
    from Layouts import *
    from mysql_conection import *

except (ModuleNotFoundError, ImportError):
    import sys, subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PySimpleGUI"])
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "mysql-connector-python"]
    )
    import PySimpleGUI as sg
    import mysql.connector as sqltor
    import os
    import webbrowser
    import matplotlib.pyplot as plt
    from googlesearch import search

## Error handling for importing modules

sg.theme("BluePurple")

## To set theme of window

if os.path.isfile("temp.txt"):

    ## Checking for previously saved passwords

    file = open("temp.txt", "r")
    string = file.readline()
    user = string.split(":")[1]
    string = file.readline()
    password = string.split(":")[1]
    mycon, mycon = initiate_connection(user, password)
    file.close()
else:

    window1 = sg.Window(title="MYSQL Login Page", layout=Login_Layout)

    ## Using PySimpleGUI to create user interface for entering sql credentials

    while True:
        event, value = window1.read()
        if event == sg.WINDOW_CLOSED or event == "Cancel":
            quit()
        elif event == "login":
            user = value["username"]
            password = value["password"]
            if value["--SAVE--"]:
                ## if user wants to save password

                with open("temp.txt", "w") as file:
                    file.write("User:" + user + "\nPassword:" + password)
            try:
                mycon, mycur = initiate_connection(user, password)
                if mycon.is_connected():
                    break
            except (sqltor.ProgrammingError, sqltor.OperationalError) as e1:
                window1.find_element("label").Update(
                    "Can't connect to server, Check server status and credentials"
                )
        else:
            pass
    window1.close()

window2 = sg.Window(title="COVID19 User Finder/Creator", layout=layout2)
while True:
    event, value = window2.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Submit":
        data = select_data(mycon, "show databases;")
        if ("covid19",) in data:
            mycur.execute("use covid19;")
        else:
            mycur.execute("create database covid19;")
            mycur.execute("use covid19;")
        data = select_data("show tables;")
        if ("meetinginfo",) not in data:
            mycur.execute(
                "create table MeetingInfo(MeetId int primary key auto_increment,"
                "Purpose varchar(20) not null,"
                "Date Date not null);"
            )
            mycur.execute(
                "create table MeetingUser(MeetId int not null ,"
                "UserId int not null,"
                "foreign key(MeetId) references MeetingInfo(MeetId),"
                "foreign key (UserId) references user(UserId));"
            )

            ## Checks for existing table (MeetingInfo). If it does not exist, it creates one

        try:
            mycur.execute(
                "insert into meetinginfo(Purpose,Date) values('%s','%s');"
                % (value["purpose"], value["Date"])
            )

            ## inserts values entered by user into the  table

            mycur.execute("select max(MeetId) from MeetingInfo")
            for i in mycur.fetchone():
                MeetId = i
            uid = value["UIs"]
            uidlist = [(MeetId, UserID) for UserID in uid.split(",")]
            mycur.executemany(
                "insert into MeetingUser(MeetId,UserId) values(%s,%s)", uidlist
            )
            ## Insterts value into the table (MeetingUser)
            mycon.commit()
        except sqltor.Error:
            window2.find_element("MeetError").Update(
                "There was a problem logging the meet"
            )

        ## Insterts value into table(MeetingUser)

        mycon.commit()
        mycur.execute(
            'select m.meetid  from meetinguser m,user n where m.userid=n.userid and n.covidstatus="+ve";'
        )
        data = mycur.fetchall()

        ## Selecting meeting IDs of meetings in which covid +ve person was there

        data = [i for (i,) in data]
        temp = []
        for i in range(len(data)):
            mycur.execute(
                "select m.userid from meetinguser m , user n where m.userid=n.userid and m.meetid=%s"
                % data[i]
            )
            temp.append(mycur.fetchall())

        ## Selecting user IDs of the the people attending the meetings in which a covid patient was there

        mycur.execute("select userid from user where covidstatus='+ve'")
        surecases = mycur.fetchall()
        surecases = [j for (j,) in surecases]
        temp2 = []
        for i in temp:
            for (j,) in i:
                temp2.append(j)
        temp = temp2
        try:
            for i in surecases:
                temp.remove(i)
        except ValueError:
            pass
        ## Removing those who have been tested +ve for covid

        for i in temp:
            mycur.execute(
                "update user set covidstatus='prob+ve' where (userid=%s and covidstatus='-ve')"
                % i
            )

            ## Setting covid status of people who attended meeting with covid patient to prob+ve (prob+ve =  probably +ve)

        mycon.commit()

    elif event == "submit":

        ## To create new users

        data = select_data(mycon, "show databases;")
        if ("covid19",) in data:
            mycur.execute("use covid19;")
        else:
            mycur.execute("create database covid19;")
            mycur.execute("use covid19;")

        ## Checking for database covid 19 and if it doesn't exist, it creates one

        data = select_data(mycon, "show tables;")
        if ("user",) not in data:
            mycur.execute(
                "create table User(UserID int Primary key auto_increment,"
                "Name varchar(18) not null,"
                "Phone BIGINT UNIQUE not null,"
                "Address varchar(30) not null,"
                "CovidStatus varchar(8) not null check (CovidStatus in ('+ve','prob+ve','-ve')))"
            )

        ## Checks if the table User exists or not and if it doesn't exist, it creates one

        try:
            r_keys = ["+ve", "-ve"]
            mycur.execute(
                "insert into User(Name,Phone,Address,CovidStatus) values(%s,%s,%s,%s)",
                (
                    value["name"],
                    value["phone"],
                    value["address"],
                    [key for key in r_keys if value[key]][0],
                ),
            )
            mycon.commit()

        ## Inserting personal info. of users into table (User)

        except sqltor.IntegrityError:
            window2.find_element("UserError").Update(
                "A user exists with same phone number."
            )

        ## Helps to restrict duplicacy of data
    elif event == "Update":
        window2["CreateUser"].Update(visible=False)
        window2["UpdateUser"].Update(visible=True)
        window2["return"].Update(visible=True)

    ## Create user is disables and update user is enabled once update button is clicked

    elif event == "return":
        window2["CreateUser"].Update(visible=True)
        window2["UpdateUser"].Update(visible=False)
        window2["return"].Update(visible=False)

    ## Create user is enabled and update user is disabled once return button is clicked

    elif event == "update":
        option = value["l3option"]
        userid = value["UQuery"]
        Nvalue = value["NValue"]
        mycur.execute("use covid19;")
        mycur.execute(
            "update user set %s='%s' where UserID='%s'" % (option, Nvalue, userid)
        )
        mycon.commit()

    ## Updates info of the user according to the new data provided

    elif event == "search":
        searchby = value["option"]
        query = value["squery"]
        mycur.execute("use covid19;")

        if query == "":
            mycur.execute("select * from user")
        else:
            mycur.execute("select * from user where %s='%s'" % (searchby, query))
        dat = mycur.fetchall()
        window2.find_element("list").Update(dat)

        ## Searches user info according to query entered

    elif event == "hospitallist":
        pincode = sg.popup_get_text("Enter Pincode", "Chrome")
        query = "covid test centres near {}".format(pincode)
        res = [i for i in search(query, tld="co.in", num=3, stop=3, pause=2)]
        webbrowser.open_new_tab(res[0])

        ## opens a tab on the internet to show covid testing centers near the pincode entered

    elif event == "graph":
        try:
            graphdata = select_data(
                mycon,
                "select substring(Address,1,1) as Block,count(*) "
                "from user "
                "where covidstatus='+ve' "
                "group by Block "
                "order by Block;",
            )

            ## Counts number of cases per block
            blocks = []
            cases = []
            for (i, j) in graphdata:
                blocks.append(i)
                cases.append(j)

            line = plt.bar(blocks, cases)
            plt.xlabel("Blocks")
            plt.ylabel("Cases")

            for i in range(len(cases)):
                plt.annotate(
                    str(cases[i]), xy=(blocks[i], cases[i]), ha="center", va="bottom"
                )

            plt.show()

            ## plots graph of number of cases on Y axis vs Blocks on X axis

        except sqltor.Error:
            pass
    elif event == "Clear Database":
        mycur.execute("drop database covid19")
        mycon.commit()

    ## Clears existing data in database covid19

    elif event == "Delete Saved Password":
        os.remove("temp.txt")

    ## Deletes saved passwords

    elif event == "About...":
        string2 = """
        Welcome to COVID 19 Case Management Application

        This is a RDBMS based system which logs meetings
                    between Users in the RDBMS

        To start,you need to create users in the Create
        Users section.You can add as many users you want
        and search them in the Search Section

        Once a covid +ve person is logged in a meeting with
        a non COVID person,The covid -ve person is marked as
        prob+ve.You can update any info by clicking the
        update button

        You can also view a graph based on the block vs.
             cases by clicking the graph button """

        sg.popup_ok_cancel(string2, title="About...", grab_anywhere=True)
    elif event == "Help":
        layout3 = [
            [
                sg.Text("What can I help you with?"),
                sg.InputOptionMenu(
                    values=["Formats", "Graphs", "Inputting Data"],
                    k="helpoption",
                ),
            ],
            [sg.Button("Submit", k="help")],
            [sg.Text(text="", size=(70, 8), k="L@bel")],
        ]
        window3 = sg.Window(title="Help", layout=layout3)
        while True:
            event1, value1 = window3.read()
            if event1 == sg.WINDOW_CLOSED:
                break
            elif event1 == "help":
                if value1["helpoption"] == "Formats":
                    window3.find_element("L@bel").Update(
                        """The date has to be in YYYY-MM-DD format.Example:2020-09-12\n
                    The Address should start with Flat no/Plot no. Example:D-128 """
                    )

                elif value1["helpoption"] == "Graphs":
                    window3.find_element("L@bel").Update(
                        "The Graph takes data from the Address and no. of cases(hence the block should be the first alphabet)"
                        "It can be edited using the options provided in the matplotlib library"
                    )
                elif value1["helpoption"] == "Inputting Data":
                    window3.find_element("L@bel").Update(
                        "The code handles duplicate data for you so no need to worry about that."
                        "You need to enter data manually for each entry as there is not automation available."
                        "The data should follow the formats specified and remember to wait after clicking submit"
                    )
        ## helps user to use the application smoothly
        # noinspection PyUnboundLocalVariable
        window3.close()
window2.close()
