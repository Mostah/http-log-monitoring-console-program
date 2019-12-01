#
# Makefile of the project
#

.ONESHELL:

init:
	( \
		python3 -m pip install virtualenv; \
		virtualenv env; \
		source env/bin/activate; \
		pip3 install -r requirements.txt; \
		make prepare-server; \
	)

prepare-server:
	( \
		cd back; \
		rm -r migrations; \
		cd app; \
		rm -r app.db; \
		cd ../; \
		flask db init; \
		flask db migrate; \
		flask db upgrade; \
		cd ../; \
	)
		
run-test:
	( \
		source env/bin/activate; \
		pytest; \
	)

run-server:
	( \
		source env/bin/activate; \
		cd back; \
		flask run; \
	)

run-app:
	( \
		source env/bin/activate; \
		python3 monitoring.py; \
	)

