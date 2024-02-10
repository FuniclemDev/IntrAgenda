import json
import requests
import os
import time
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import subprocess
from selenium.common.exceptions import NoSuchElementException

# Configuration de l'accès à l'API Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json')
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
service = build('calendar', 'v3', credentials=creds)

# Créer une instance du service Google Calendar
debut = datetime.now()
fin = debut + timedelta(days=365)
debut = debut.strftime("%Y-%m-%d")
fin = fin.strftime("%Y-%m-%d")

def clear_calendar(id):
    events_result = service.events().list(
    calendarId= id,
    timeMin= debut + 'T00:00:00Z',
    timeMax= fin + 'T23:59:59Z',
    singleEvents=True,
    orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    # Supprimer chaque événement individuellement
    for event in events:
        event_id_to_delete = event['id']
        event_summary = event.get('summary', 'Unknown Event')
        service.events().delete(
            calendarId=id,
            eventId=event_id_to_delete
        ).execute()
        print(f'Event deleted: {event_summary}')

def start_and_end_time(event_data, service):
    start_time = ""
    end_time = ""
    room = "N/A"
    event = {}
    event_color_id = event_color_id_base
    if (not event_data.get('rdv_group_registered') and not event_data.get('rdv_indiv_registered')):
        print("rdv_event")
        start_time = datetime.strptime(event_data.get('start', ''), '%Y-%m-%d %H:%M:%S').isoformat()
        end_time = datetime.strptime(event_data.get('end', ''), '%Y-%m-%d %H:%M:%S').isoformat()
        print(event_data.get('start', ''), event_data.get('end', ''))
    elif (not event_data.get('rdv_indiv_registered')):
        print("rdv_group")
        start_time = ""
        end_time = ""
        i = 0
        for carac in event_data.get('rdv_group_registered', ''):
            if (carac == '|'):
                i = 1
                continue
            if (i == 0):
                start_time += carac
            if (i == 1):
                end_time += carac
        print(start_time, end_time)
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S').isoformat()
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S').isoformat()
    else:
        print("rdv_indiv")
        start_time = ""
        end_time = ""
        i = 0
        for carac in event_data.get('rdv_indiv_registered', ''):
            if (carac == '|'):
                i = 1
                continue
            if (i == 0):
                start_time += carac
            if (i == 1):
                end_time += carac
        print(start_time, end_time)
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S').isoformat()
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S').isoformat()

    if (event_data.get('room') and event_data.get('room', '').get('code', '')):
        brut = event_data.get('room', '').get('code', '')
        room = ""
        for carac in range(len(brut) - 1, -1, -1):
            if (brut[carac] == '/' or brut[carac] == '-'):
                break
            room += brut[carac]
        room = room[::-1]
        if (room == ("gauche")):
            room = 'Amphi-G.'
        if (room == ("droite")):
            room = 'Amphi-D.'
    if (event_data.get('type_code') == 'exam'):
        event_color_id = event_color_id_base_exam
        event = {
        'summary': f'({room}) EXAM',
        'description': event_data.get('titlemodule', '--None--') + '\n--EPITECH--\n' + 'UPDATE: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
        'start': {
            'dateTime': (datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S') - timedelta(minutes=30)).isoformat(),
            'timeZone': 'Europe/Paris',
        },
        'end': {
            'dateTime': start_time,
            'timeZone': 'Europe/Paris',
        },
        'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'popup', 'minutes': popup_min},
        ],
        },
        'colorId': event_color_id_base_exam_before,
        }
        # Envoyer la requête pour créer l'événement avant l'examen
        service.events().insert(calendarId=IDCALENDAR, body=event).execute()
        event_name = f'({room}) {event_data.get("acti_title", "Unknown Event")}'
        print(f'Alerte exam created: {event_name}')
    
    event = {
        'summary': f'({room}) {event_data.get("acti_title", "Unknown Event")}',
        'description': event_data.get('titlemodule', '--None--') + '\n--EPITECH--\n' + 'UPDATE: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
        'start': {
            'dateTime': start_time,
            'timeZone': 'Europe/Paris',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Europe/Paris',
        },
        'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'popup', 'minutes': popup_min},
        ],
        },
    'colorId': event_color_id,
    }

    # Envoyer la requête pour créer l'événement
    service.events().insert(calendarId=IDCALENDAR, body=event).execute()
    event_name = f'({room}) {event_data.get("acti_title", "Unknown Event")}'
    print(f'Event created: {event_name}')
    print("")

def send_to_google_calendar(events_data_list, debut, fin):

    # Itérer sur la liste des événements et créer chaque événement
    for event_data in events_data_list:
        # Si une séance présente
        if (event_data.get('module_registered') and event_data.get('event_registered') != (False)):
            start_and_end_time(event_data, service)



def auto_login(i_globat):
    login_url = 'https://sts.epitech.eu/adfs/ls/?client-request-id=80f6f3f6-f763-4593-9df1-4a94fb15317b&wa=wsignin1.0&wtrealm=urn%3afederation%3aMicrosoftOnline&wctx=LoginOptions%3D3%26estsredirect%3d2%26estsrequest%3drQQIARAA02I21DO0Ukk1ME0xMTSx1DU0MzLRNTEzMtdNNE1K1DU3MTdKNLZMNTFOTCoS4hL49vlbQ_L3ya5zP3pN-S1qWL2KUT2jpKSg2EpfPzOvpChRL7UgsyQ1OUMvtVQ_sbQkQz8_LS0zOdXYzHQHI-MFRsYXjIy3mPj9HYFSRiAivyizKnUWM6P-Jma25Pzc3Py8G8yMj5glknNSc1PzSvRS8ovSUx0Qhl5gYXzFwmTA8YOFcREr0D3PPVVC8vd_8J4kxVF9Uk2I4RSrfkZmVkmSc46rdl56YViqoblfgEmlhY9lvrdJYkZ4RZZncXZxlWNYoVliarGthZXhBDbGD2yMHewMuziJ9coBXoYffKdeND49e-3HW49X_DpVEaHFUYXePpVu-l5pvmnB7mHlFelFOcYmFV5B-YauyV7hVQW57r4RYW6-thsEGAA1&cbcxt=&mkt=&lc='
    driver.get(login_url)
    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.ID, 'userNameInput')))
    driver.find_element(By.ID, 'userNameInput').send_keys(username)
    password_input = driver.find_element(By.ID, 'passwordInput')
    wait = WebDriverWait(driver, 0.1)
    password_input.send_keys(password)
    try:
        wait.until(EC.visibility_of_element_located((By.ID, 'submitButton')))
        driver.find_element(By.ID, 'submitButton').click()
    except:
        i_globat = i_globat
    if a2f:
        wait = WebDriverWait(driver, 200)
        #A2F verification
        try:
            wait.until(EC.visibility_of_element_located((By.ID, 'idSIButton9')))
        except:
            print("\n===============\nA2F Button not found: TIMEOUT\n===============\n")
        driver.find_element(By.ID, 'idSIButton9').click()

def reformat(string):
    result = ""
    li = []
    for a in string:
        if a == '/':
            li.append(result)
            result = ''
            continue
        if a == ',':
            li.append(result)
            break
        result += a
    result = li[2] + '-' + li[1] + '-' + li[0]
    return result

def get_projects():
    if not a2f:
        wait = WebDriverWait(driver, 200)
        try:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'activite')))
        except:
            print("\n===============\nHome's Intranet not found: TIMEOUT\n===============\n")
    driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", driver.find_elements(By.CLASS_NAME, 'activite')[0])
    driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", driver.find_elements(By.CLASS_NAME, 'note')[0])
    driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", driver.find_elements(By.CLASS_NAME, 'susie')[0])
    project_list = driver.find_element(By.CLASS_NAME, 'projet').find_elements(By.TAG_NAME, 'article')
    i = 180
    try:
        driver.find_element(By.CLASS_NAME, 'projet').find_element(By.CLASS_NAME, 'view_more').click()
    except:
        i = 180
    for article in project_list:
        try:
            article.find_element(By.TAG_NAME, 'p')
            continue
        except:
            h3_text = "It's ok you pass"
        # Exemple d'extraction de texte de l'élément h3 dans chaque article
        h3_text = article.find_element(By.TAG_NAME, 'h3').text
        if h3_text[:18] == "Back To The Future" and not bttf:
            continue
        # Exemple d'extraction de texte de l'élément de date dans chaque article
        date_text = reformat(article.find_elements(By.CLASS_NAME, 'date')[0].text)
        date_text2 = reformat(article.find_elements(By.CLASS_NAME, 'date')[1].text)
        i -= 10
        driver.execute_script(f"arguments[0].style.backgroundColor = 'rgb({i}, {i}, {i})'", article)
        # Afficher les informations extraites
        print(f"Titre: {h3_text}")
        print(f"Date: {date_text} à {date_text2}")
        event = {
            'summary': f'{h3_text}',
            'description': '--EPITECH--\n' + 'UPDATE: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            'start': {
                'date': date_text,
                'timeZone': 'Europe/Paris',
            },
            'end': {
                'date': date_text2,
                'timeZone': 'Europe/Paris',
            },
            'reminders': {
            'useDefault': False,
            },
        'colorId': event_color_id_project,
        }

        # Envoyer la requête pour créer l'événement
        service.events().insert(calendarId=IDPROJECT, body=event).execute()
        print(f'Project created: {h3_text}')
        print("")

def execute_test(debut, fin, i_glob):
    wait = WebDriverWait(driver, 100)
    if not is_already_login():
        auto_login(i_glob)
        test = True
    else:
        test = wait.until(lambda driver: driver.find_element(By.ID, 'toggle-sidebar') and driver.current_url.startswith('https://intra.epitech.eu'))
    print("login access OK")

    # Effectuer une requête HTTP pour récupérer le contenu JSON et les projets
    if test:
        get_projects()
        driver.get("https://intra.epitech.eu/planning/load?format=json&start=" + debut + "&end=" + fin)
        wait = WebDriverWait(driver, 200)
        json_data = ""
        if i_glob == 1:
            json_data = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body'))).text
        else:
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
            wait = WebDriverWait(driver, 1)
            while i_glob < 20 and test == True:
                try:
                    test = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "pre"))).text
                except:
                    i_glob += 1
                list_fire = driver.find_elements(By.TAG_NAME, 'li')
                try:
                    list_fire[1].click()
                except:
                    i_glob = i_glob
            try:
                json_data = driver.find_element(By.TAG_NAME, "pre").text
            except:
                print("\n===============\nJSON Data not found\n===============\n")
                time.sleep(2)
                exit(84)
    # Fermer le navigateur
    driver.quit()
    send_to_google_calendar(json.loads(json_data), debut, fin)


# Fonction pour vérifier si la page de connexion est présente
def is_login_page_present():
    try:
        wait.until(EC.visibility_of_element_located((By.ID, "auth-input-login")))
        print("Connection success")
        return True
    except:
        print("Connection to the page failed")
        return False

def is_already_login():
    try:
        wait.until(lambda driver: EC.visibility_of_element_located(By.ID, 'toggle-sidebar') and driver.current_url.startswith('https://intra.epitech.eu'))
        return True
    except:
        return False

def crypt(password):
    try:
        # Exécutez l'exécutable compilé et capturez la sortie
        resultat = subprocess.check_output(["build/exe.linux-x86_64-3.11/addon", "go_crypted", password])
        return  resultat.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution : {e}")

def uncrypt(password):
    try:
        # Exécutez l'exécutable compilé et capturez la sortie
        resultat = subprocess.check_output(["build/exe.linux-x86_64-3.11/addon", "go_uncrypted", password])
        return  resultat.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution : {e}")

# URL de la page web contenant le JSON
url = 'file://' + os.getcwd() + "/waiting.html"
chemin_fichier_json = os.getcwd() + '/config.json'
with open(chemin_fichier_json, 'r') as fichier:
    donnees_json = json.load(fichier)
i_globa = 0

for the_browser in donnees_json:
    try:
        if i_globa == 0:
            if the_browser['BROWSER'] == "Chrome":
                i_globa = 1
            elif the_browser['BROWSER'] == "Firefox":
                i_globa = 2
            else:
                print("\n===============\nWrong browser\n===============\n")
                time.sleep(2)
                exit(84)
            continue
    except:
        test = False

for profil in donnees_json:
    try:
        test = profil["BROWSER"]
        continue
    except:
        test = False
    if i_globa == 1:
        driver = webdriver.Chrome()
        print("===============\nNext User\n===============\n")
    if i_globa == 2:
        driver = webdriver.Firefox()
        print("===============\nNext User\n===============\n")
    # Utiliser Selenium pour effectuer la connexion
    driver.get(url)
    driver.maximize_window()
    test = False
    wait = WebDriverWait(driver, 20)
    IDCALENDAR = profil['IDCALENDAR']
    IDPROJECT = profil['IDPROJECT']
    username = profil['EMAIL']
    try:
        password = profil['PASSWORD']
        password = uncrypt(password)
        if password[0] == '\n':
            print("\n===============\nWrong Key PASSWORD, Please retype your password in Config.json")
    except:
        password = profil['PASSWORD*']
        profil['PASSWORD'] = profil.pop('PASSWORD*')
        profil['PASSWORD'] = crypt(password)
    popup_min = str(profil['POPUP_MIN'])
    event_color_id_base = str(profil['COLOR_BASE'])
    event_color_id_base_exam = str(profil['COLOR_EXAM'])
    event_color_id_base_exam_before = str(profil['COLOR_BEFORE_EXAM'])
    event_color_id_project = str(profil['COLOR_PROJECT'])
    if profil['A2F'] == 'YES':
        a2f = True
    else:
        a2f = False
    if profil['BTTF'] == "YES":
        bttf = True
    else:
        bttf = False
    with open(chemin_fichier_json, 'w') as fichier:
        json.dump(donnees_json, fichier, indent=4)
    try:
        clear_calendar(IDCALENDAR)
        clear_calendar(IDPROJECT)
        print("\n")
        driver.get('https://intra.epitech.eu')
        if is_login_page_present():
            execute_test(debut, fin, i_globa)
            print("\n===============\nProgram result : SUCCESS\n===============\n")
            time.sleep(1)
    except:
        print("\n===============\nProgram result : CRASH\n===============\n")
        time.sleep(2)
        exit(84)
exit(0)
