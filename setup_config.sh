#!/bin/bash

echo "Configuration Setup Script"

# Demande le choix entre Chrome et Firefox pour le premier dictionnaire
while true; do
    read -p "Choose Browser for the first account (Chrome/Firefox): " FIRST_BROWSER
    FIRST_BROWSER=$(echo "$FIRST_BROWSER")  # Convert to lowercase
    # Valide le choix du navigateur
    if [ "$FIRST_BROWSER" != "Chrome" ] && [ "$FIRST_BROWSER" != "Firefox" ]; then
        echo "Invalid browser choice. Please choose Chrome or Firefox."
        continue
    fi
    break
done
# Dictionnaire de configuration de base avec le choix du navigateur
BASE_CONFIG='[
    {
        "COMMENT": "Chrome, Firefox",
        "BROWSER": "'$FIRST_BROWSER'"
    }
]'
# Initialiser la configuration avec le dictionnaire de base
CONFIG=$BASE_CONFIG

# Loop for multiple accounts
while true; do
    # Prompt for account details
    read -p "Enter Comment: " COMMENT
    read -p "Enter Calendar ID: " IDCALENDAR
    read -p "Enter Project ID: " IDPROJECT
    read -p "Enter Epitech Email: " EMAIL
    read -p "Enter Popup Minutes (integer): " POPUP_MIN
    read -p "Enter Base Color (integer): " COLOR_BASE
    read -p "Enter Exam Color (integer): " COLOR_EXAM
    read -p "Enter Before Exam Color (integer): " COLOR_BEFORE_EXAM
    read -p "Enter Project Color (integer): " COLOR_PROJECT
    read -p "BTTF (YES/NO): " BTTF
    read -s -p "Enter Password: " PASSWORD

    # Add account details to configuration
    NEW_ACCOUNT='{"COMMENT": "'$COMMENT'", "IDCALENDAR": "'$IDCALENDAR'", "IDPROJECT": "'$IDPROJECT'", "EMAIL": "'$EMAIL'", "POPUP_MIN": '$POPUP_MIN', "COLOR_BASE": '$COLOR_BASE', "COLOR_EXAM": '$COLOR_EXAM', "COLOR_BEFORE_EXAM": '$COLOR_BEFORE_EXAM', "COLOR_PROJECT": '$COLOR_PROJECT', "BTTF": "'$BTTF'", "A2F": "'YES'", "PASSWORD*": "'$PASSWORD'"}'
    CONFIG=$(jq '. += ['"$NEW_ACCOUNT"'] | unique' <<< "$CONFIG")
    echo ""
    # Ask if another account needs to be added
    read -p "Do you want to add another account? (yes/no): " ADD_ANOTHER
    ADD_ANOTHER=$(echo "$ADD_ANOTHER" | tr '[:upper:]' '[:lower:]')  # Convert to lowercase

    if [ "$ADD_ANOTHER" != "yes" ]; then
        break
    fi
done

# Display the final configuration
echo "Final Configuration:"
echo "$CONFIG" | jq .

# Save the configuration to a file (you can change the filename if needed)
echo "$CONFIG" > config.json

echo "Configuration saved to config.json"
echo "The password will be encrypted during the first execution of sync_IntrAgenda.py."
