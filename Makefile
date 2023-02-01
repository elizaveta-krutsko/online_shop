run_db:
	docker run -e POSTGRES_PASSWORD=root -p 5432:5432 -v online_shop_volume:/var/lib/postgresql/data -d --rm postgres:14

stop_db:
	docker stop $(shell docker ps -a --filter volume=online_shop_volume | grep postgres:14 | cut -c -12)