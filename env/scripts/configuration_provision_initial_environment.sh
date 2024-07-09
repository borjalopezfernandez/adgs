
########
# Configuration
########
# USERS
declare -A users
declare -A user_uids
users["ADGS_USER"]="adgs"
user_uids["ADGS_USER"]="2020"

# FOLDERS
declare -A folders
declare -A folders_ownership
declare -a folders_order
FOLDER="ADGS"
folders_order+=( "$FOLDER" )
folders[$FOLDER]="/data/adgs"
folders_ownership[$FOLDER]=${users["ADGS_USER"]}

FOLDER="ADGS_DDBB"
folders_order+=( "$FOLDER" )
folders[$FOLDER]="${folders['ADGS']}/adgs_db"
folders_ownership[$FOLDER]=${users["ADGS_USER"]}

FOLDER="ADGS_MINARC"
folders_order+=( "$FOLDER" )
folders[$FOLDER]="${folders['ADGS']}/arc"
folders_ownership[$FOLDER]=${users["ADGS_USER"]}

FOLDER="ADGS_MINARC_LOG"
folders_order+=( "$FOLDER" )
folders[$FOLDER]="${folders['ADGS']}/arc/log"
folders_ownership[$FOLDER]=${users["ADGS_USER"]}

FOLDER="ADGS_DEC"
folders_order+=( "$FOLDER" )
folders[$FOLDER]="${folders['ADGS']}/dec"
folders_ownership[$FOLDER]=${users["ADGS_USER"]}

FOLDER="ADGS_DEC_LOG"
folders_order+=( "$FOLDER" )
folders[$FOLDER]="${folders['ADGS']}/dec/log"
folders_ownership[$FOLDER]=${users["ADGS_USER"]}

FOLDER="ADGS_MONITORING"
folders_order+=( "$FOLDER" )
folders[$FOLDER]="${folders['ADGS']}/adgs_monitoring"
folders_ownership[$FOLDER]=${users["ADGS_USER"]}

FOLDER="BOA_DDBB"
folders_order+=( "$FOLDER" )
folders[$FOLDER]="${folders['ADGS_MONITORING']}/boa_ddbb"
folders_ownership[$FOLDER]=${users["ADGS_USER"]}

FOLDER="BOA_LOG"
folders_order+=( "$FOLDER" )
folders[$FOLDER]="${folders['ADGS_MONITORING']}/log"
folders_ownership[$FOLDER]=${users["ADGS_USER"]}

FOLDER="BOA_INTRAY"
folders_order+=( "$FOLDER" )
folders[$FOLDER]="${folders['ADGS_MONITORING']}/intray_boa"
folders_ownership[$FOLDER]=${users["ADGS_USER"]}

FOLDER="CERTIFICATES"
folders_order+=( "$FOLDER" )
folders[$FOLDER]="${folders['ADGS']}/adgs_certificates_and_secret_key"
folders_ownership[$FOLDER]=${users["ADGS_USER"]}

FOLDER="RBOA_ARCHIVE"
folders_order+=( "$FOLDER" )
folders[$FOLDER]="${folders['ADGS_MONITORING']}/rboa_archive"
folders_ownership[$FOLDER]=${users["ADGS_USER"]}

FOLDER="MONITORING_MINARC_ARCHIVE"
folders_order+=( "$FOLDER" )
folders[$FOLDER]="${folders['ADGS_MONITORING']}/minarc_archive"
folders_ownership[$FOLDER]=${users["ADGS_USER"]}

FOLDER="ORC_DDBB"
folders_order+=( "$FOLDER" )
folders[$FOLDER]="${folders['ADGS_MONITORING']}/orc_ddbb"
folders_ownership[$FOLDER]=${users["ADGS_USER"]}

FOLDER="PROMETHEUS_DDBB"
folders_order+=( "$FOLDER" )
folders[$FOLDER]="${folders['ADGS_MONITORING']}/prometheus_ddbb"
folders_ownership[$FOLDER]=${users["ADGS_USER"]}
