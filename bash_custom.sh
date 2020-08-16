#!/bin/bash
# .bash_profile custom command template
# paste this into your .bash_profile to run IBWebAPI shortcuts with the 'broker' command
# calling 'broker' gets the account summary, and runs the server login process if not logged in
# calling 'broker _____' runs any other functions in functions.py

function broker() {
    FILEPATH="~/path/to/your/IBWebAPI"
    cd $FILEPATH
    if [ -z $1 ]; then
        echo "Getting account summary..."
        status=$(python3 functions.py checkstatus)
        echo $status
        if [ "$status" = "No response" ]; then
            echo "Server not initiated."
            ./startserver.sh
            sleep 1
            echo "Server started"
        elif [ "$status" = "Not logged in" ]; then
            python3 functions.py login
        else
            python3 functions.py summary
        fi
    else
        python3 functions.py $1
    fi
    cd
}
