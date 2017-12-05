#turn off remote apache but start mysql
ssh -t solarquant@192.168.1.88 "sudo systemctl stop apache2";
wait;
ssh -t solarquant@192.168.1.88 "sudo systemctl start mysql";
wait;

#back up the database here
mysqldump  --add-drop-table -u solarquant -psolarquant solarquant > /var/www/html/solarquant/database/solarquant1.sql

# delete anything in /tmp
#ssh -t solarquant@192.168.1.88 "sudo rm /var/www/html/solarquant/* -R;";


#only for new installs
ssh -t solarquant@192.168.1.88 "sudo mkdir /var/www/html/solarquant";

#open up emergent directory
ssh -t solarquant@192.168.1.88 "sudo chown solarquant:www-data /var/www/html/solarquant/* -R";
ssh -t solarquant@192.168.1.88 "sudo chmod 777 /var/www/html/solarquant/ -R";


# rsync everything over to host
rsync -a /var/www/html/solarquant solarquant@192.168.1.88:/var/www/html

ssh -t solarquant@192.168.1.88 "sudo chmod 777 /var/www/html/solarquant/emergent/* -R";

# delete anything in /tmp
#ssh -t solarquant@192.168.1.88 "sudo rm /tmp/*.sh;sudo rm /tmp/*.txt;";

# drop all the tables in solarquant

# restore the database
ssh -t solarquant@192.168.1.88 "mysql -u solarquant --password=solarquant solarquant < /var/www/html/solarquant/database/solarquant1.sql";

#start remote apache
ssh -t solarquant@192.168.1.88 "sudo systemctl start apache2";
