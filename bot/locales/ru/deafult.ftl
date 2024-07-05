### Текстовые сообщения базовых команд бота и надписей для кнопок основных клавиатур.

## Основные команды.
start =
    Привет! 👋
    Я @{ $bot_name }, который поможет тебе управлять и работать с Nextcloud ☁️.

    Введите /auth, чтобы начать авторизацию.
help =
    Это Telegram бот для работы с Nextcloud.

    Представляет собой удобный инструмент для управления файлами и папками в облачном хранилище. Благодаря боту пользователи могут легко и быстро удалять, скачивать, загружать файлы, создавать новые папки, управлять корзиной и искать файлы по их названию.

    <b>Прежде, чем начать работу с ботом, вам необходимо пройти авторизацию, для этого введите /auth.</b> Сайт откроется внутри телеграмма, если протокол защищенный, в ином случае вам нужно вручную скопировать ссылку и открыть ее в браузере, чтобы пройти авторизацию. Время на авторизацию ограничено, о чем будет сказано в сообщении авторизации.

    <b>Безопасность</b>

    Вы можете использовать бота в различных чатах, но учитывайте, что остальные пользователи чата увидят содержимое ваших папок и различную информацию о файлах, которая может быть конфиденциальной. Но нажимать на кнопки меню может только тот пользователь, который вызвал сообщение с этим меню.

    ---

    После прохождения авторизации у вас появится главное меню с разными возможностями:

    ---

    <b>{ fsnode-menu-button } - Меню управления файлами, где можно перемещаться по файловой иерархии и управлять файлами и папками.</b>

    <u><i>👆 Имя файла:</i></u> Сообщение изменится на описание выбранного файла, также изменятся возможные действия и доступные файлы, если это директория.

    <u>{ fsnode-delete-button }:</u> Вызовет дополнительное меню, где вам необходимо подтвердить удаление файла, в случае подтверждения файл будет удален, а в случае отказа вы вернетесь к меню управления файлом.

    <u>{ fsnode-download-button }:</u> После нажатия, бот вам отправит сообщение с прикрепленным файлов в виде документа. Если размер файла превышает заданный лимит в настройках бота (20Мб по умолчанию), то отправиться ссылка на файл, которая будет действительная в течение 8 часов. Скачать можно только файлы, но не директории.

    <u>{ fsnode-upload-button }:</u> После нажатия бот переходит в режим ожидания файлов, которые вы хотите загрузить. Отправьте файлы, но учитываете, что будут загружены только файлы, отправленные в формате документа. Когда вы закончили отправлять файлы или передумали, нажмите кнопку "{ stop-button }", чтобы вернуться в режим меню управления файлом. После, вам придет новое меню с обновленным списком файлов внутри директории.

    <u>{ fsnode-mkdir-button }:</u> Бот перейдет в режим ожидания названия папки. После отправки вами названия папки, папка будет создана и вам придет новое меню управления файлом с обновленным списком файлов внутри директории, где и появится новая папка. Если вы передумали создавать папку, то нажмите кнопку "{ cancel-button }".

    <u>{ back-button }:</u> Меню управления файлом обновится и покажет меню предыдущей директории.

    ---

    <b>{ search-button } - Система поиска по тексту по вашим файлам Nextcloud.</b>

    После нажатия кнопки, бот начнет ожидать название файла, который вы хотите найти. Когда вы отправили запрос, то выведется сообщение с результатом поиска. Не обязательно вводить название целиком, вы можете отправить только часть названия, бот найдет все подходящие по названию файлы.

    <u><i>👆 Имя файла:</i></u> По нажатию на кнопку с названием файла, откроется меню управления этим файлом.

    ---

    <b>{ trashbin-button } - Управление корзиной c удаленными файлами Nextcloud.</b>

    После нажатия, вам придет меню корзины, где будут перечислены удаленные файлы и кнопка очистки корзины.

    <u><i>👆 Имя файла:</i></u> Откроется меню действий с файлом из корзины, где его можно будет восстановить, для этого нажмите "{ trashbin-restore-button }" или удалить, для этого нажмите "{ trashbin-delete-button }", если никаких действия вы предпринимать не хотите, то нажмите "{ cancel-button }" и вы вернетесь к меню корзины.

    <u>{ trashbin-cleanup-button  }:</u> Кнопка очистки корзины, когда вы ее нажмете, запросится подтверждение, в случае согласия корзина будет очищена и файлы из нее будут удалены безвозвратно, в случае отказа, сообщение вернется к меню корзины.

    ---

    <b>Общее</b>

    { fsnode-pag-back-button } { fsnode-pag-next-button }: Любое меню со списком файлов вмещает по умолчанию только 8 файлов. В случае, если в списке содержится больше 8 файлов, то можно нажимая на стрелки просматривать список файлов.

    ---

    <b>Open Source</b>

    Этот бот является проектом с открыт исходным кодом. Вы можете поучаствовать в разработке.

    <i><a href="https://github.com/blvdek/nc_tg_bot">Исходный код</a></i>

## Кнопки главного меню.
fsnode-menu-button = 🗃️ Файлы
search-button = 🔍 Поиск
trashbin-button = 🗑️ Корзина

## Кнопки действий.
confirm-button = ✅ Да
deny-button = ❌ Нет
cancel-button = 🚫 Отменить
stop-button = ⛔ Стоп
back-button = ⏮️ Вернуться
