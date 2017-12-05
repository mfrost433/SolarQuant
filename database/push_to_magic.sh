#turn off remote apache but start mysql
ssh -t jwgorman@192.168.1.89 "sudo systemctl stop apache2";
ssh -t jwgorman@192.168.1.89 "sudo systemctl start mysql";

#back up the database here
mysqldump  --add-drop-table -u solarquant -psolarquant solarquant > /var/www/html/solarquant/database/solarquant1.sql

# delete anything in /tmp
#ssh -t jwgorman@192.168.1.89 "sudo rm /var/www/html/solarquant/* -R;";

# rsync everything over to host
rsync -a /var/www/html/solarquant jwgorman@192.168.1.89:/var/www/html

#open up emergent directory
ssh -t jwgorman@192.168.1.89 "sudo chown jwgorman:www-data /var/www/html/solarquant/* -R";
ssh -t jwgorman@192.168.1.89 "sudo chmod 777 /var/www/html/solarquant/emergent/* -R";

# delete anything in /tmp
#ssh -t jwgorman@192.168.1.89 "sudo rm /tmp/*.sh;sudo rm /tmp/*.txt;";

# drop all the tables in solarquant

# restore the database
ssh -t jwgorman@192.168.1.89 "mysql -u solarquant --password=solarquant solarquant < /var/www/html/solarquant/database/solarquant1.sql";

#start remote apache
ssh -t jwgorman@192.168.1.89 "sudo systemctl start apache2";
