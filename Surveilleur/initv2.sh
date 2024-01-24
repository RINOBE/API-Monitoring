#!/bin/bash

# Répertoire contenant les scripts Python
script_directory="$(dirname "$(readlink -f "$0")")"

# Créer un service systemd pour un script
create_systemd_service() {
    script_name=$(basename "$1")
    service_name="${script_name%.py}.service"

    cat > "/etc/systemd/system/${service_name}" <<EOF
[Unit]
Description=Script to send ${script_name} data

[Service]
ExecStart=/usr/bin/python3 "${script_directory}/${script_name}"

[Install]
WantedBy=multi-user.target
EOF
}

# Activer et démarrer le service
enable_and_start_service() {
    script_name=$(basename "$1")
    service_name="${script_name%.py}.service"
    systemctl enable "${service_name}"
    systemctl start "${service_name}"
}

# Ajouter la ligne PROMPT_COMMAND dans le .bashrc et sourcer le fichier
add_prompt_command() {
    user="$1"
    bashrc_file="/home/$user/.bashrc"
    
    # Si l'utilisateur est root, ajuster le chemin du .bashrc
    if [ "$user" = "root" ]; then
        bashrc_file="/root/.bashrc"
    fi

    # Vérifier si le fichier .bashrc existe pour l'utilisateur
    if [ -f "$bashrc_file" ]; then
        # Vérifier si la ligne PROMPT_COMMAND n'existe pas déjà
        if ! grep -q 'PROMPT_COMMAND=' "$bashrc_file"; then
            echo 'PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND$'\n'}history -a; source $bashrc_file;"' >> "$bashrc_file"
            source "$bashrc_file"  # Sourcing the .bashrc to apply changes
            echo "Added PROMPT_COMMAND to $bashrc_file for user $user"
        else
            echo "PROMPT_COMMAND already exists in $bashrc_file for user $user"
        fi
    fi
}

# Obtenir la liste des utilisateurs du système
user_list=$(getent passwd | cut -d: -f1)

# Créer et activer les services pour chaque script
for script in "${script_directory}"/*.py; do
    create_systemd_service "$script"
    enable_and_start_service "$script"
done

# Ajouter la ligne PROMPT_COMMAND dans le .bashrc de tous les utilisateurs
for user in $user_list; do
    add_prompt_command "$user"
done
