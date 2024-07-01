#### Basic command texts for the bot and button labels for the main keyboards.

## Basic commands.
start = 
    Hello! 👋 
    I am @{ $bot_name }, which will help you manage and work with Nextcloud ☁️.

    Enter /auth to start authentication.
help = 
    This is a Telegram bot for working with Nextcloud.

    It represents a convenient tool for managing files and folders in cloud storage. Thanks to the bot, users can easily and quickly delete, download, upload files, create new folders, manage the trash, and search for files by their name.

    <b>Before starting to work with the bot, you need to go through authentication, enter /auth.</b> The site will open inside Telegram if the protocol is secure, otherwise, you will need to manually copy the link and open it in a browser to go through authentication. The time for authentication is limited, about which will be said in the authentication message.

    <b>Safety</b>

    You can use the bot in various chats, but keep in mind that other chat users will see the contents of your folders and various file information that may be confidential. But only the user who called the menu message can press the menu buttons.

    ---

    After going through authentication, you will get the main menu with various possibilities:

    ---

    <b>{ fsnode-menu-button } - File management menu, where you can navigate through the file hierarchy and manage files and folders.</b>

    <u><i>👆 File name:</i></u> The message will change to describe the selected file, also the possible actions and available files will change if it's a directory.

    <u>{ fsnode-delete-button }:</u> Will call an additional menu where you need to confirm the deletion of the file, in case of confirmation the file will be deleted, in case of refusal you will return to the file management menu.

    <u>{ fsnode-download-button }:</u> After pressing, the bot will send you a message with the attached file as a document. If the file size exceeds the set limit in the bot settings (20MB by default), then a link to the file will be sent, which will be valid for 8 hours. Only files, but not directories, can be downloaded.

    <u>{ fsnode-upload-button }:</u> After pressing, the bot switches to waiting mode for the files you want to upload. Send the files, but keep in mind that only documents will be uploaded. When you finish sending files or change your mind, press the "{ stop-button }" button to return to the file management menu. Then, you will receive a new menu with an updated list of files inside the directory, where the new folder will appear. If you decide not to create a folder, press the "{ cancel-button }".

    <u>{ fsnode-mkdir-button }:</u> Бот перейдет в режим ожидания названия папки. После отправки вами названия папки, папка будет создана и вам придет новое меню управления файлом с обновленным списком файлов внутри директории, где и появится новая папка. Если вы передумали создавать папку, то нажмите кнопку "{ cancel-button }".

    <u>{ back-button }:</u> The file management menu will update and show the menu of the previous directory.

    ---

    <b>{ search-button } - Text search system for your Nextcloud files.</b>

    After pressing the button, the bot will start waiting for the name of the file you want to find. When you send the request, a message with the search result will be displayed. It's not necessary to enter the full name, you can send just part of the name, the bot will find all matching files by name.

    <u><i>👆 File name:</i></u> By clicking on the button with the file name, the file management menu for this file will open.

    ---

    <b>{ trashbin-button } - Trash bin management with deleted Nextcloud files.</b>

    After pressing, you will receive a trash bin menu, where deleted files will be listed and a trash bin cleanup button.

    <u><i>👆 File name:</i></u> Opens the action menu for the file from the trash bin, where it can be restored by pressing "{ trashbin-restore-button }" or deleted by pressing "{ trashbin-delete-button }", if you don't want to take any action, press "{ cancel-button }" and you will return to the trash bin menu.

    <u>{ trashbin-cleanup-button }:</u> Trash bin cleanup button, when you press it, confirmation will be requested, in case of agreement the trash bin will be cleaned and the files from it will be permanently deleted, in case of refusal, the message will return to the trash bin menu.

    ---

    <b>General</b>

    { fsnode-pag-back-button } { fsnode-pag-next-button }: Any file list menu contains by default only 8 files. In case there are more than 8 files in the list, you can scroll through the file list by pressing the arrows.

    ---

    <b>Open Source</b>

    This bot is an open-source project. You can participate in development.

    <i><a href="https://github.com/blvdek/nc_tg_bot">Source code</a></i>

## Main menu buttons.
fsnode-menu-button = 🗃️ Files
search-button = 🔍 Search
trashbin-button = 🗑️ Trash bin

## Action buttons.
confirm-button = ✅ Yes
deny-button = ❌ No
cancel-button = 🚫 Cancel
stop-button = ⛔ Stop
back-button = ⏮️ Back