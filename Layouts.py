import PySimpleGUI as sg

Login_Layout = [
    [sg.Text(text="Enter Mysql Login Credentials")],
    ## Layout for window
    [sg.Text(text="Username"), sg.In(default_text="root", key="username")],
    [sg.Text(text="Password"), sg.In(password_char="*", key="password")],
    [
        sg.Button(button_text="Login", key="login"),
        sg.Button(button_text="Cancel", key="Cancel"),
    ],
    [
        sg.Text(text="Save Password?"),
        sg.Radio("Yes", "radio1", key="--SAVE--"),
        sg.Radio("No", "radio1"),
    ],
    [sg.Text(key="label", text="", size=(60, 1))],
]

RightColumn = [
    [
        sg.Text(
            text="Create Users Here",
        )
    ],
    [
        sg.Text(text="Enter Name"),
        sg.In(default_text="ABCD", text_color="black", key="name"),
    ],
    [
        sg.Text(text="Enter Phone"),
        sg.In(default_text="1234567890", text_color="black", key="phone"),
    ],
    [
        sg.Text(text="Enter Address"),
        sg.In(default_text="H-1892", text_color="black", key="address"),
    ],
    [
        sg.Text(text="Covid Status"),
        sg.Radio(text="+ve", key="+ve", group_id="radio1"),
        sg.Radio(text="-ve", key="-ve", group_id="radio1", default=True),
    ],
    [sg.Button(button_text="Submit", key="submit", pad=(70, 0))],
    [sg.Button(button_text="Update", key="Update", pad=(70, 10))],
    [sg.Text(text="", size=(40, 1), key="UserError")],
]

## Layout of row 1 column 2 for creating new users
menulayout = [
    ["Options", ["Clear Database", "Delete Saved Password"]],
    ["Help", ["About...", "Help"]],
]
leftColumn = [
    [sg.Text(text="Find Users Here")],
    [
        sg.Text(text="Search User By"),
        sg.InputOptionMenu(
            values=["UserID", "Name", "Address", "Phone", "CovidStatus"], key="option"
        ),
    ],
    [
        sg.Text(text="Enter the query"),
        sg.In(key="squery"),
        sg.Button(button_text="Search", key="search"),
    ],
    [
        sg.Table(
            headings=["UserID", "Name", "Phone", "Address", "CovidStatus"],
            values=[
                ("UID", " SAMPLE ", "1234567890", "VWXYZ", "-ve"),
            ],
            enable_events=True,
            key="list",
            size=(300, 10),
            pad=(70, 10),
        )
    ],
]

## Layout of row 1 column 1 for searching existing users

DisabledLeftColumn = [
    [
        sg.Text(text="Update"),
        sg.InputOptionMenu(
            values=["---", "Name", "Phone", "Address", "CovidStatus"],
            key="l3option",
            default_value="---",
        ),
    ],
    [sg.Text("Enter UserID"), sg.In(key="UQuery")],
    [sg.Text("Enter New Value"), sg.In(key="NValue")],
    [
        sg.Button("Update", key="update"),
        sg.Button(button_text="Back to Create Users", key="return", visible=False),
    ],
]

## Layout of row 1 column 2 (not visible untill update button is pressed) for updating info of existing users

LeftColumn1 = [
    [sg.Text(text="Log Meetings Here", pad=(10, 0))],
    [
        sg.Text(text="Enter UserIDs"),
        sg.In(default_text="1,2,4", text_color="black", key="UIs"),
    ],
    [
        sg.Text(text="Enter Date    "),
        sg.In(default_text="yyyy-mm-dd", text_color="black", key="Date"),
    ],
    [
        sg.Text(text="Enter Purpose"),
        sg.InputOptionMenu(
            values=["Friend/Family", "Business", "Service and Repair", "Other"],
            key="purpose",
        ),
    ],
    [sg.Button(button_text="Submit", key="Submit")],
    [sg.Text(text="", key="MeetError", size=(40, 1))],
]

## Layout of row 2 column 1 for logging meetings of users

RightColumn1 = [
    [sg.Button("COVID test centre near me", k="hospitallist", pad=(20, 10))],
    [sg.Button("View Graphs", k="graph", pad=(20, 10))],
]

layout2 = [
    [sg.Menu(menulayout)],
    [
        sg.Column(leftColumn),
        sg.VSeperator(color="lightblue", pad=(0, 0)),
        sg.Column(RightColumn, key="CreateUser"),
        sg.Column(DisabledLeftColumn, visible=False, key="UpdateUser"),
    ],
    [sg.HorizontalSeparator(color="lightblue", pad=(0, 10))],
    [
        sg.Column(LeftColumn1),
        sg.VSeperator(color="lightblue", pad=(0, 0)),
        sg.Column(RightColumn1),
    ],
]
