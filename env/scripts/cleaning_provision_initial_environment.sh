#!/bin/bash
#################################################################
#
# Cleaning of the provision of the initial environment for the ADGS
#
# module adgs
#################################################################

USAGE="Usage: `basename $0`"

PROVISIONING_DIRECTORY="$(dirname "$(realpath "$0")")"

source $PROVISIONING_DIRECTORY/configuration_provision_initial_environment.sh

if [ `whoami` != 'root' ]; then
    echo "ERROR: The cleaning of the provision of the initial environment for the ADGS needs to be performed with root privileges."
    exit -1
fi

WELCOME_MESSAGE="\n
Welcome to the cleaning of the provision of the initial environment for the ADGS :-)\n
These are the configuration options that will be cleaned:\n"
for folder_order_id in ${!folders_order[@]}; do
    folder=${folders_order[$folder_order_id]}
    path=${folders[${folder}]}
    WELCOME_MESSAGE=$WELCOME_MESSAGE"\n- ${folder}: ${path}"
done
for user in ${!users[@]}; do
    WELCOME_MESSAGE=$WELCOME_MESSAGE"\n- ${user}: NAME=${users[${user}]} / UID=${user_uids[${user}]}"
done

echo -e $WELCOME_MESSAGE"\n"

while true; do
    read -p "Do you wish to proceed with the cleaning of the provision of the initial environment for the ADGS?" answer
    case $answer in
        [Yy]* )
            break;;
        [Nn]* )
            echo "No worries, the initializer will not continue";
            exit;;
        * ) echo "Please answer Y or y for yes or N or n for no. Answered: $answer";;
    esac
done

echo ""
echo "INFO: Deleting folders"

for folder_order_id in ${!folders_order[@]}; do
    folder=${folders_order[$folder_order_id]}
    path=${folders[${folder}]}

    # Check that the folder is available
    if [ -d $path ];
    then
        echo "INFO: Deleting the folder ($folder) with path $path..."
        rm -ri $path
        echo "INFO: Folder ($folder) with path $path has been deleted"
    else
        echo "WARNING: Folder ($folder) with path $path was not available to be cleaned"
    fi
done

echo ""
echo "INFO: Deleting users"

# Delete relevant users
for user in ${!users[@]}; do
    # Check that the user name is available
    id ${users[${user}]} &> /dev/null
    status=$?
    if [ $status -eq 0 ]
    then
        user_name=${users[${user}]}
        user_uid=${user_uids[${user}]}
        echo "INFO: Deleting the user with name $user_name and UID $user_uid..."
        userdel -r $user_name
        echo "INFO: User with name $user_name and UID $user_uid has been deleted"
    else
        echo "WARNING: The user ${users[${user}]} was not available to be cleaned"
    fi
done
