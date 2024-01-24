#!/bin/bash
rm -f /var/log/user_histories/*
# Active l'enregistrement de l'historique
set -o history

# Met à jour l'historique actuel
history -a

# Définit le répertoire pour stocker les fichiers d'historique
histories_dir="/var/log/user_histories"

# Crée le répertoire s'il n'existe pas
mkdir -p "$histories_dir"

# Parcourt tous les répertoires d'utilisateurs dans /home
for user_dir in /home/*; do
    # Obtient le nom de l'utilisateur à partir du chemin du répertoire
    user=$(basename "$user_dir")
    
    # Définit le fichier d'historique pour l'utilisateur actuel
    user_history_file="$histories_dir/$user.history"
    
    # Copie le fichier d'historique de l'utilisateur
    if [ -f "$user_dir/.bash_history" ];then
        cp "$user_dir/.bash_history" "$user_history_file"
        # Ajoute le nom d'utilisateur à chaque ligne de l'historique
        sed -i "s/^/$user /" "$user_history_file"
        cat "$user_history_file"
    fi

done

# Traite l'historique de l'utilisateur root
root_history_file="$histories_dir/root.history"
if [ -f "/root/.bash_history" ];then
    cp /root/.bash_history "$root_history_file"
    sed -i "s/^/root /" "$root_history_file"
    cat "$root_history_file"
    rm -f /root/.bash_history
fi
# Parcourt tous les répertoires d'utilisateurs dans /home
for user_dir in /home/*; do
    # Obtient le nom de l'utilisateur à partir du chemin du répertoire
    user=$(basename "$user_dir")

    # Définit le fichier d'historique pour l'utilisateur actuel
    user_history_file="$histories_dir/$user.history"

    # Copie le fichier d'historique de l'utilisateur
    rm -f "$user_dir/.bash_history" 

done
rm -f /var/log/user_stories/*
