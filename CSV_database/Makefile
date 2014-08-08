# Download location database

target = allCountries.zip
source = allCountries.txt

target:
	rm -f ${target} ${source}
	wget http://download.geonames.org/export/zip/allCountries.zip
	unzip allCountries.zip

