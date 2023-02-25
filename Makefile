init:
	test -n "$(name)"
	rm -rf ./.git
	find ./ -type f -exec perl -pi -e 's/pl4n3t/$(name)/g' *.* {} \;
	mv ./pl4n3t ./$(name)

npm-install:
	docker exec -it pl4n3t npm install

webpack-dev:
	docker exec -it pl4n3t npm run dev

webpack-dev-server:
	docker exec -it pl4n3t npm run dev-server

webpack-build:
	docker exec -it pl4n3t npm run build

superuser:
	docker exec -it pl4n3t ./manage.py createsuperuser

shell:
	docker exec -it pl4n3t ./manage.py shell

makemigrations:
	docker exec -it pl4n3t ./manage.py makemigrations

migrate:
	docker exec -it pl4n3t ./manage.py migrate

initialfixture:
	docker exec -it pl4n3t ./manage.py loaddata initial

testfixture:
	docker exec -it pl4n3t ./manage.py loaddata test

test:
	docker exec -it pl4n3t ./manage.py test

statics:
	docker exec -it pl4n3t ./manage.py collectstatic --noinput

makemessages:
	docker exec -it pl4n3t django-admin makemessages

compilemessages:
	docker exec -it pl4n3t django-admin compilemessages
