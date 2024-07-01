### Text messages and file management menu buttons.

## The title message.
fsnode =
    <b><i>{ $type ->
        [dir] Folder
        *[file] File
    }</i> { $symbol }: { $name }</b>

    <i>{ $path }</i>
    ---
    🔸 <u><i>Owner:</i></u> { $user }
    🔸 <u><i>In favorites:</i></u> { $favorite }
    🔸 <u><i>Size:</i></u> { $size }
    🔸 <u><i>Recent changes:</i></u> { $last_modified }

## Deleting a file.
fsnode-delete = 
    Are you sure you want to delete the file <b>{ $name }</b>? 💣

    <b>This action cannot be undone.</b>
fsnode-delete-alert = The file "{ $name }" was successfully deleted. 💀

## Create a folder.
fsnode-mkdir-start = Enter the name of the folder you want to create. 📂
fsnode-mkdir-success = Folder <b>{ $name }</b> successfully created. 👍
fsnode-mkdir-incorrectly = The folder cannot be named that way. 🫷

## Upload files.
fsnode-upload-start = 
    Send the files as a document to download them. 📄

    Or click "{stop-button}" to finish the download.
fsnode-upload-error = An error occurred while trying to upload files. 😵‍💫
fsnode-upload-success =
    Your file <b>"{$name }"</b> has been successfully uploaded to Nextcloud. 
    
    <i>You can continue working with other files or complete the download process.</i>
fsnode-upload-incorrectly = The file must be in the form of a document. 🙅‍♂️

## Download file.
fsnode-url =
The weight of this file <b>{ $size}</b> exceeds the allowed <i>{ $size_limit }</i>. 🏋️‍♂️

    You can follow the link and download this file yourself.

    <i><u>File link</u></i>: { $url }

## File management menu buttons.
fsnode-delete-button = ❌ Delete
fsnode-download-button = ⬇️ Download
fsnode-upload-button = ⬆️ Upload
fsnode-mkdir-button = 🆕 Create folder
fsnode-pag-back-button = ⬅️
fsnode-pag-next-button = ➡️