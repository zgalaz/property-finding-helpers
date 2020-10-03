# Property Finding Helpers
This package provides an easy way of parsing property offers (with user-specific settings) from the property finding 
portal "nehnutelnosti.sk" in Slovakia and sending them via e-mail. 

This package is developed by [Zoltan Galaz](http://zoltan.galaz.eu/) who created it while searching for the best 
property for him, his wife and the kids (in the future) to buy. For more information, please contact the author 
at <zoltan@galaz.eu>.

* * * * * * * * *

## Installation
```
git clone git@github.com:zgalaz/property-finding-helpers.git
cd property-find-helpers
python3 -m virtualenv .venv
source .venv/bin/activate
pip install .
```

## Structure
```
+---helpers
|   +---parsers
|   |   +---portals
|   |   |       base.py
|   |   |       nehnutelnosti.py
|   |   |       
|   |   \---websites
|   |           parser.py
|   |           
|   +---senders
|   |       data_formatter.py
|   |       email_builder.py
|   |       email_sender.py
|   |       
|   +---utils
|   |       common.py
|   |       logger.py
|   |       
|   \---watchdog
|       |   dog.py
|       |   __init__.py
|       |   
|       +---database
|       \---settings
|               watchdog.json
|               
+---settings
|       email.json
```

## Use
The package supports only the watchdog function so far (If needed, the functionality of the helper can be updated/extended). To be able to run the watchdog, please follow these steps:

1. in `settings/email.json` update the following field(s): *email_address*, *email_password*, *server*, and *port*
2. in `helpers/watchdog/settings/watchdog.json` update the following field(s): *url* 
3. run the watchdog: `python run.py --email <receiver@email.com>`
4. or create a bash script, that can be run periodically via the system's task scheduler, with the following content: `"<local_path>\property-finding-helpers\venv\Scripts\python.exe" <local_path>\property-finding-helpers\run.py --email <receiver@email.com>`


## Note
The package is created for non-commercial use only. It is meant exclusively for personal use with the intention to help anybody to catch the good property offers as soon as possible to be able to find the property he/she dreams of.


# License
This project is licensed under the terms of the MIT license. For more details, see the **LICENSE** file.