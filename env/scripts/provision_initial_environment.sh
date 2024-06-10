#!/bin/bash
#################################################################
#
# Provision of the initial environment for the ADGS
#
# module adgs
#################################################################

USAGE="Usage: `basename $0`"

PROVISIONING_DIRECTORY="$(dirname "$(realpath "$0")")"

source $PROVISIONING_DIRECTORY/configuration_provision_initial_environment.sh

if [ `whoami` != 'root' ]; then
    echo "ERROR: The provision of the initial environment for the ADGS needs to be performed with root privileges."
fi

WELCOME_MESSAGE="\n
Welcome to the provision of the initial environment for the ADGS :-)\n
These are the configuration options that will be applied to provision the initial environment:\n"
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
    read -p "Do you wish to proceed with the provision of the initial environment for the ADGS?" answer
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
echo "INFO: Creating users"

# Create relevant users
for user in ${!users[@]}; do
    # Check that the user name is not already available
    id ${users[${user}]} &> /dev/null
    status=$?
    if [ $status -eq 0 ]
    then
        echo "ERROR: The user ${users[${user}]} already exists. Initial provision must have been performed already"
        exit -1
    fi
    # Check that the user id is not already available
    getent passwd ${user_uids[${user}]} &> /dev/null
    status=$?
    if [ $status -eq 0 ]
    then
        echo "ERROR: The user UID ${user_uids[${user}]} already exists. Initial provision must have been performed already"
        exit -1
    fi
    user_name=${users[${user}]}
    user_uid=${user_uids[${user}]}
    echo "INFO: Creating the user with name $user_name and UID $user_uid. The user will have a directory in the home folder..."
    useradd -m -r -u $user_uid $user_name
    echo "INFO: User with name $user_name and UID $user_uid has been created"
done

echo ""
echo "INFO: Creating folders"

for folder_order_id in ${!folders_order[@]}; do
    folder=${folders_order[$folder_order_id]}
    path=${folders[${folder}]}

    # Check that the folder is not already available
    if [ -d $path ];
    then
        echo "ERROR: The directory $path already exists ($folder). Initial provision must have been performed already"
        exit -1
    fi
    echo "INFO: Creating the folder ($folder) with path $path..."
    mkdir -p $path
    echo "INFO: Folder ($folder) with path $path has been created"

    if [ ${folders_ownership[$folder]} ]
    then
        user_name=${folders_ownership[$folder]}
        # Check that the user name is available
        id $user_name &> /dev/null
        status=$?
        if [ $status -ne 0 ]
        then
            echo "ERROR: The user ${user_name} does not exist. There must be an error in the configuration of the provision"
        else
            echo "INFO: Changing the ownership of the folder ($folder) with path $path to the user $user_name..."
            chown $user_name $path
            echo "INFO: Folder ($folder) with path $path has been assigned to the user $user_name"
        fi
    fi
done
