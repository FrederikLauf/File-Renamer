*** Settings ***
Library    FileRenamerGuiTestLibrary.py

Test Setup    Open File Renamer App


*** Test Cases ***
Original File List Sorting Options
    Select Test Image Folder
    Original List Should Be Ordered By    Name
    Select Sort By    Date
    Original List Should Be Ordered By    Date
    Select Sort By    Homonymity And Date
    Original List Should Be Ordered By    Homonymity And Date
    
Behaviour Of Digits Spinbox
    Select Test Image Folder
    Digits Spinbox Should Have Value    2
    Enter Start Number    990
    Digits Spinbox Should Have Value    3
    Select Strictly Increase
    Digits Spinbox Should Have Value    4
    
Preview Of Renamed Files
    Select Test Image Folder
    Preview List Numbers Should Start From    1
    Enter Start Number    99
    Preview List Numbers Should Start From    99
    Enter Prefix    MyPrefix
    Preview List Prefixes Should Equal    MyPrefix