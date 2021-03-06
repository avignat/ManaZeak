#!/bin/bash

vmzk="0.1.2"
mzkdir=$(dirname $0)

createNecessaryFiles() {
    echo -en "Setting up necessary files ... "
    if [ ! -d "log" ]; then
      mkdir log
    fi
    if [ ! -f "log/debug.log" ]; then
      touch log/debug.log
    fi
    echo -e "OK\n"
}

if [ $# -eq 0 ]; then
    echo -e "\e[31mERROR\e[39m No arguments supplied"
    echo -e "Script usage: ./mzk.sh --help"

elif [ $1 = "init" ]; then
    echo -e "\nWelcome to the init wizard for ManaZeak. This will help you setup your ManaZeak environment."
    createNecessaryFiles
    read -p "Please enter a path for your music library: " musicpath

    if [ -z $musicpath ]; then
	    musicpath="$HOME/Music"
    elif [ ${musicpath:0:1} != "/" -a ${musicpath:0:1} != "~" -a ${musicpath:0:2} != "./" -a ${musicpath:0:3} != "../" -a ! -d $musicpath ]; then
	    musicpath="$HOME/$musicpath"
    fi

    echo -en "Setting music library path to $musicpath ... "
    dockerconf=$(sed "s/\/PATH\/TO\/MUSIC/$(echo $musicpath | sed 's / \\/ g')/g" $mzkdir/docker-compose.yml.example)
    echo -e "Done"
    read -p "Please enter the path under which to store your ManaZeak database: " dbpath

    if [ -z $dbpath ]; then
	    dbpath="$mzkdir/dbdata"
    elif [ ${dbpath:0:1} != "/" -a ${dbpath:0:1} != "~" -a ${dbpath:0:2} != "./" -a ${dbpath:0:3} != "../" ]; then
        dbpath="$mzkdir/$dbpath"
    fi

    echo -en "Setting database data folder to $dbpath ... "
    dockerconf=$(echo "$dockerconf" | sed "s/\/PATH\/TO\/DB_DATA/$(echo $dbpath | sed 's / \\/ g')"/g)
    echo -e "Done"
    echo "$dockerconf" > $mzkdir/docker-compose.yml
    echo -e "\nManaZeak wizard setup complete ! You can now run the next mzk.sh commands to build your containers.\n"

elif [ $1 = "build" ]; then
    createNecessaryFiles
    eval "docker-compose build"
    eval "npm install"

elif [ $1 = "dev" ]; then
    eval "docker-compose up -d"
    eval "npm run dev"

elif [ $1 = "debug" ]; then
    eval "docker-compose up -d"
    eval "npm run debug"

elif [ $1 = "prod" ]; then
    eval "docker-compose up -d"
    eval "npm run prod"

elif [ $1 = "stop" ]; then
    eval "docker-compose stop"
    eval "docker ps"

elif [ $1 = "clean" ]; then
    eval "docker-compose rm -sf"
    echo -e "\e[93mWARNING\e[39m Images haven't been removed"
    printf "Use docker rmi \$(docker images -q) to remove every image on the system\n"

elif [ $1 = "repy" ]; then
    eval "docker kill manazeak_app 2>/dev/null"
    eval "docker start -i manazeak_app"

elif [ $1 = "test" ]; then
    eval "npm run test"

elif [ $1 = "doc" ]; then
    eval "npm run doc"

elif [ $1 = "sonar-scanner" ]; then
    if [ -z "$2" ]; then
        echo -e "\e[31mERROR\e[39m Your argument is invalid"
        echo -e "You need to give an API key as a second argument. Usage ./mzk.sh sonar-scanner APIKEY"
    else
        eval "node_modules/sonar-scanner/bin/sonar-scanner -D sonar.login=$2"
    fi

elif [ $1 = "--help" ] || [ $1 = "-h" ]; then
    printf -- "#  ManaZeak-cli v$vmzk, available commands:\n#\n"
    printf -- "#  ./mzk.sh init : Run the initialisation wizard\n"
    printf -- "#  ./mzk.sh build : Build ManaZeak\n#\n"
    printf -- "#  ./mzk.sh dev : Run a dev environment\n"
    printf -- "#  ./mzk.sh debug : Run a dev environment with frontend debug info\n"
    printf -- "#  ./mzk.sh prod : Run a production environment\n#\n"
    printf -- "#  ./mzk.sh stop : Stop ManaZeak application\n"
    printf -- "#  ./mzk.sh clean : Remove ManaZeak containers\n"
    printf -- "#  ./mzk.sh repy : Run the manazeak container in interactive mode\n#\n"
    printf -- "#  ./mzk.sh doc : Generates both the Python and JavaScript documentations\n"
    printf -- "#  ./mzk.sh test : Run all unit tests\n"
    printf -- "#  ./mzk.sh sonar-scanner xxx: Perform a sonare-scanner on the folder. Require an API key (xxx) as second parameter\n#\n"
    printf -- "#  ./mzk.sh --help : Display the script usage  (or -h)\n"
    printf -- "#  ./mzk.sh --version : Display the version number (or -v)\n"

elif [ $1 = "--version" ] || [ $1 = "-v" ]; then
    printf "ManaZeak $vmzk\n"

else
    echo -e "\e[31mERROR\e[39m Your argument is invalid"
    echo -e "Script usage: ./mzk.sh --help"
fi
